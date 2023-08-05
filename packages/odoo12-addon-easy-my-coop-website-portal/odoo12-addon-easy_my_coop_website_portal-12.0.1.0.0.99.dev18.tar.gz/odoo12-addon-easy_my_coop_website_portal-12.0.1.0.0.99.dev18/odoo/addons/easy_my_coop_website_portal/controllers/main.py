# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017-2018 Rémy Taymans <remy@coopiteasy.be>
# Copyright 2019 Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _
from odoo.exceptions import AccessError, MissingError
from odoo.fields import Date
from odoo.http import request, route

from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.portal import (
    CustomerPortal,
    pager as portal_pager,
)


class CooperatorPortalAccount(CustomerPortal):
    CustomerPortal.MANDATORY_BILLING_FIELDS.extend(
        ["iban", "birthdate_date", "gender"]
    )

    def _prepare_portal_layout_values(self):
        values = super(
            CooperatorPortalAccount, self
        )._prepare_portal_layout_values()
        # We assume that commercial_partner_id always point to the
        # partner itself or to the linked partner. So there is no
        # need to check if the partner is a "contact" or not.
        partner = request.env.user.partner_id
        coop = partner.commercial_partner_id
        partner_obj = request.env["res.partner"]
        coop_bank = (
            request.env["res.partner.bank"]
            .sudo()
            .search([("partner_id", "in", [coop.id])], limit=1)
        )
        invoice_mgr = request.env["account.invoice"]
        capital_request_count = invoice_mgr.search_count(
            [
                ("state", "in", ["open", "paid", "cancelled"]),
                # Get only the release capital request
                ("release_capital_request", "=", True),
            ]
        )

        invoice_count = invoice_mgr.search_count(
            [("release_capital_request", "=", False)]
        )
        iban = ""
        if partner.bank_ids:
            iban = partner.bank_ids[0].acc_number

        fields_desc = partner_obj.sudo().fields_get(["gender"])

        values.update(
            {
                "coop": coop,
                "coop_bank": coop_bank,
                "capital_request_count": capital_request_count,
                "invoice_count": invoice_count,
                "iban": iban,
                "genders": fields_desc["gender"]["selection"],
            }
        )
        return values

    def details_form_validate(self, data):
        error, error_message = super(
            CooperatorPortalAccount, self
        ).details_form_validate(data)
        sub_req_obj = request.env["subscription.request"]
        iban = data.get("iban")
        valid = sub_req_obj.check_iban(iban)

        if not valid:
            error["iban"] = "error"
            error_message.append(_("You iban account number is not valid"))
        return error, error_message

    @route(["/my/account"], type="http", auth="user", website=True)
    def account(self, redirect=None, **post):
        res = super(CooperatorPortalAccount, self).account(redirect, **post)
        if not res.qcontext.get("error"):
            partner = request.env.user.partner_id
            partner_bank = request.env["res.partner.bank"]
            iban = post.get("iban")
            if iban:
                if partner.bank_ids:
                    bank_account = partner.bank_ids[0]
                    bank_account.acc_number = iban
                else:
                    partner_bank.sudo().create(
                        {"partner_id": partner.id, "acc_number": iban}
                    )
        return res

    @route(
        ["/my/invoices", "/my/invoices/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_invoices(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        res = super(CooperatorPortalAccount, self).portal_my_invoices(
            page, date_begin, date_end, sortby, **kw
        )
        invoice_obj = request.env["account.invoice"]
        qcontext = res.qcontext
        if qcontext:
            invoices = invoice_obj.search(
                [("release_capital_request", "=", False)]
            )
            invoice_count = len(invoices)
            qcontext["invoices"] = invoices
            qcontext["pager"]["invoice_count"] = invoice_count
        return res

    @route(
        [
            "/my/release_capital_request",
            "/my/release_capital_request/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_release_capital_request(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        """Render a page with the list of release capital request.
        A release capital request is an invoice with a flag that tell
        if it's a capital request or not.
        """
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        invoice_mgr = request.env["account.invoice"]

        domain = [
            ("partner_id", "in", [partner.commercial_partner_id.id]),
            ("state", "in", ["open", "paid", "cancelled"]),
            # Get only the release capital request
            ("release_capital_request", "=", True),
        ]
        archive_groups = self._get_archive_groups_sudo(
            "account.invoice", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">=", date_begin),
                ("create_date", "<", date_end),
            ]

        # count for pager
        capital_request_count = invoice_mgr.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/release_capital_request",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
            },
            total=capital_request_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager and archive selected
        invoices = invoice_mgr.sudo().search(
            domain, limit=self._items_per_page, offset=pager["offset"]
        )
        values.update(
            {
                "date": date_begin,
                "capital_requests": invoices,
                "page_name": "Release request",
                "pager": pager,
                "archive_groups": archive_groups,
                "default_url": "/my/release_capital_request",
            }
        )
        return request.render(
            "easy_my_coop_website_portal.portal_my_capital_releases", values
        )

    @route(
        ["/my/invoices/<int:invoice_id>"],
        type="http",
        auth="public",
        website=True,
    )
    # fmt: off
    def portal_my_invoice_detail(
        self,
        invoice_id,
        access_token=None,
        report_type=None,
        download=False,
        **kw
    ):
        # fmt: on
        # override in order to not retrieve release capital request as invoices
        try:
            invoice_sudo = self._document_check_access(
                "account.invoice", invoice_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        if invoice_sudo.release_capital_request:
            report_ref = "easy_my_coop.action_cooperator_invoices"
        else:
            report_ref = "account.account_invoices"
        if report_type in ("html", "pdf", "text"):
            return self._show_report(
                model=invoice_sudo,
                report_type=report_type,
                report_ref=report_ref,
                download=download,
            )

        values = self._invoice_get_page_view_values(
            invoice_sudo, access_token, **kw
        )
        PaymentProcessing.remove_payment_transaction(
            invoice_sudo.transaction_ids
        )
        return request.render("account.portal_invoice_page", values)

    @route(
        ["/my/cooperator_certificate/pdf"],
        type="http",
        auth="user",
        website=True,
    )
    def get_cooperator_certificat(self, **kw):
        """Render the cooperator certificate pdf of the current user"""
        partner = request.env.user.partner_id

        return self._show_report(
            model=partner,
            report_type="pdf",
            report_ref="easy_my_coop.action_cooperator_report_certificat",
            download=True,
        )

    def _render_pdf(self, pdf, filename):
        """Render a http response for a pdf"""
        pdfhttpheaders = [
            ("Content-Disposition", 'inline; filename="%s.pdf"' % filename),
            ("Content-Type", "application/pdf"),
            ("Content-Length", len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)

    def _get_archive_groups_sudo(
        self,
        model,
        domain=None,
        fields=None,
        groupby="create_date",
        order="create_date desc",
    ):
        """Same as the one from website_portal_v10 except that it runs
        in root.
        """
        if not model:
            return []
        if domain is None:
            domain = []
        if fields is None:
            fields = ["name", "create_date"]
        groups = []
        for group in (
            request.env[model]
            .sudo()
            .read_group(domain, fields=fields, groupby=groupby, orderby=order)
        ):
            label = group[groupby]
            date_begin = date_end = None
            for leaf in group["__domain"]:
                if leaf[0] == groupby:
                    if leaf[1] == ">=":
                        date_begin = leaf[2]
                    elif leaf[1] == "<":
                        date_end = leaf[2]
            groups.append(
                {
                    "date_begin": Date.to_string(Date.from_string(date_begin)),
                    "date_end": Date.to_string(Date.from_string(date_end)),
                    "name": label,
                    "item_count": group[groupby + "_count"],
                }
            )
        return groups
