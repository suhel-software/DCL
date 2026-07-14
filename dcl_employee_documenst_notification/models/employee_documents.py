# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DclHrEmployeeDocument(models.Model):
    _name = 'dcl.hr.employee.document'
    _description = 'HR Employee Documents Custom'

    name = fields.Char(string='Document Name', required=True, copy=False,
                       help='You can give your Document name.')
    description = fields.Text(string='Description', copy=False, help="Description")
    expiry_date = fields.Date(string='Expiry Date', copy=False, help="Date of expiry")
    employee_ref = fields.Many2one('hr.employee', invisible=1, copy=False)
    doc_attachment_id = fields.Many2many('ir.attachment', 'dcl_doc_attach_rel',
                                         'doc_id', 'attach_id3',
                                         string="Attachment",
                                         help='You can attach the copy of your document',
                                         copy=False)
    issue_date = fields.Date(string='Issue Date', default=fields.datetime.now(),
                             help="Date of issue", copy=False)
    document_type = fields.Many2one('dcl.document.type', string="Document Type",
                                    help="Document type")
    before_days = fields.Integer(string="Days",
                                 help="How many number of days before to get the notification email")
    notification_type = fields.Selection([
        ('single', 'Notification on expiry date'),
        ('multi', 'Notification before few days'),
        ('everyday', 'Everyday till expiry date'),
        ('everyday_after', 'Notification on and after expiry')
    ], string='Notification Type',
        help="""
        Notification on expiry date: You will get notification only on expiry date.
        Notification before few days: You will get notification in 2 days.On expiry date and number of days before date.
        Everyday till expiry date: You will get notification from number of days till the expiry date of the document.
        Notification on and after expiry: You will get notification on the expiry date and continues upto Days.
        If you did't select any then you will get notification before 7 days of document expiry.""")

    # Custom fields
    amount = fields.Float(string="Amount", help="Amount for Increment, Promotion, or Permanent")
    document_type_name = fields.Char(related='document_type.name', string='Document Type Name')
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount', store=True)
    last_increment = fields.Date(string="Last Increment Date", compute='_compute_last_values', readonly=False, store=True)
    last_promotion = fields.Date(string="Last Promotion Date", compute='_compute_last_values', readonly=False, store=True)

    @api.depends('employee_ref.contract_id.wage', 'amount')
    def _compute_total_amount(self):
        for record in self:
            wage = record.employee_ref.contract_id.wage or 0.0
            record.total_amount = wage + record.amount

    @api.depends('employee_ref', 'document_type')
    def _compute_last_values(self):
        for record in self:
            last_inc = False
            last_prom = False
            if record.employee_ref:
                docs = self.env['dcl.hr.employee.document'].search([
                    ('employee_ref', '=', record.employee_ref.id),
                    ('expiry_date', '!=', False)
                ], order='expiry_date desc')
                for d in docs:
                    if d.document_type.name == 'Increment' and not last_inc:
                        last_inc = d.expiry_date
                    elif d.document_type.name == 'Promotion' and not last_prom:
                        last_prom = d.expiry_date
                    if last_inc and last_prom:
                        break
            record.last_increment = last_inc
            record.last_promotion = last_prom

    def mail_reminder(self):
        """Sending document expiry notification to employees and global recipients."""
        date_now = fields.Date.today()
        match = self.search([])

        # Load global recipients from settings
        params = self.env['ir.config_parameter'].sudo()
        recipient_ids_str = params.get_param('dcl_employee_documenst_notification.global_document_expiry_recipient_ids', '')
        global_recipients = self.env['hr.employee']
        if recipient_ids_str:
            recipient_ids = [int(x) for x in recipient_ids_str.split(',') if x.isdigit()]
            global_recipients = self.env['hr.employee'].browse(recipient_ids)

        for i in match:
            if i.expiry_date:
                # Collect all recipient emails
                emails = []
                for recipient in global_recipients:
                    if recipient.work_email and recipient.work_email not in emails:
                        emails.append(recipient.work_email)
                
                if not emails:
                    continue
                email_to = ','.join(emails)
                job_title = " (%s)" % i.employee_ref.job_id.name if i.employee_ref.job_id.name else ""

                if i.notification_type == 'single':
                    if date_now == i.expiry_date:
                        mail_content = "Dear HR Team,<br><br>I hope you are doing well.<br><br>" \
                                       "This is a gentle reminder that it may be time to conduct the performance evaluation for Mr. " + str(i.employee_ref.name or '') + job_title + \
                                       ". Kindly review the evaluation process as per the company's policy and schedule.<br><br>" \
                                       "Thank you for your attention."
                        main_content = {
                            'subject': 'Reminder: Annual Performance Review – %s' % (i.employee_ref.name),
                            'author_id': self.env.user.partner_id.id,
                            'body_html': mail_content,
                            'email_to': email_to,
                        }
                        self.env['mail.mail'].create(main_content).send()
                elif i.notification_type == 'multi':
                    exp_date = fields.Date.from_string(
                        i.expiry_date) - timedelta(days=i.before_days)
                    if date_now == exp_date or date_now == i.expiry_date:
                        mail_content = "Dear HR Team,<br><br>I hope you are doing well.<br><br>" \
                                       "This is a gentle reminder that it may be time to conduct the performance evaluation for Mr. " + str(i.employee_ref.name or '') + job_title + \
                                       ". Kindly review the evaluation process as per the company's policy and schedule.<br><br>" \
                                       "Thank you for your attention."
                        main_content = {
                            'subject': 'Reminder: Annual Performance Review – %s' % (i.employee_ref.name),
                            'author_id': self.env.user.partner_id.id,
                            'body_html': mail_content,
                            'email_to': email_to,
                        }
                        self.env['mail.mail'].create(main_content).send()
                elif i.notification_type == 'everyday':
                    exp_date = fields.Date.from_string(
                        i.expiry_date) - timedelta(days=i.before_days)
                    if date_now >= exp_date and date_now <= i.expiry_date:
                        mail_content = "Dear HR Team,<br><br>I hope you are doing well.<br><br>" \
                                       "This is a gentle reminder that it may be time to conduct the performance evaluation for Mr. " + str(i.employee_ref.name or '') + job_title + \
                                       ". Kindly review the evaluation process as per the company's policy and schedule.<br><br>" \
                                       "Thank you for your attention."
                        main_content = {
                            'subject': 'Reminder: Annual Performance Review – %s' % (i.employee_ref.name),
                            'author_id': self.env.user.partner_id.id,
                            'body_html': mail_content,
                            'email_to': email_to,
                        }
                        self.env['mail.mail'].create(main_content).send()
                elif i.notification_type == 'everyday_after':
                    exp_date = fields.Date.from_string(
                        i.expiry_date) + timedelta(days=i.before_days)
                    if i.expiry_date <= date_now <= exp_date:
                        mail_content = "Dear HR Team,<br><br>I hope you are doing well.<br><br>" \
                                       "This is a gentle reminder that it may be time to conduct the performance evaluation for Mr. " + str(i.employee_ref.name or '') + job_title + \
                                       ". Kindly review the evaluation process as per the company's policy and schedule.<br><br>" \
                                       "Thank you for your attention."
                        main_content = {
                            'subject': 'Reminder: Annual Performance Review – %s' % (i.employee_ref.name),
                            'author_id': self.env.user.partner_id.id,
                            'body_html': mail_content,
                            'email_to': email_to,
                        }
                        self.env['mail.mail'].create(main_content).send()
                else:
                    exp_date = fields.Date.from_string(
                        i.expiry_date) - timedelta(days=7)
                    if date_now == exp_date:
                        mail_content = "Dear HR Team,<br><br>I hope you are doing well.<br><br>" \
                                       "This is a gentle reminder that it may be time to conduct the performance evaluation for Mr. " + str(i.employee_ref.name or '') + job_title + \
                                       ". Kindly review the evaluation process as per the company's policy and schedule.<br><br>" \
                                       "Thank you for your attention."
                        main_content = {
                            'subject': 'Reminder: Annual Performance Review – %s' % (i.employee_ref.name),
                            'author_id': self.env.user.partner_id.id,
                            'body_html': mail_content,
                            'email_to': email_to,
                        }
                        self.env['mail.mail'].create(main_content).send()

    @api.constrains('expiry_date')
    def check_expr_date(self):
        for each in self:
            if each.expiry_date:
                exp_date = fields.Date.from_string(each.expiry_date)
                if exp_date < date.today():
                    raise ValidationError('Your Document Is Expired.')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _dcl_document_count(self):
        for each in self:
            document_ids = self.env['dcl.hr.employee.document'].sudo().search(
                [('employee_ref', '=', each.id)])
            each.dcl_document_count = len(document_ids)

    def dcl_document_view(self):
        self.ensure_one()
        domain = [
            ('employee_ref', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'dcl.hr.employee.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            'context': "{'default_employee_ref': %s}" % self.id
        }

    dcl_document_count = fields.Integer(compute='_dcl_document_count',
                                    string='# Documents')


class DclEmployeeAttachment(models.Model):
    _inherit = 'ir.attachment'

    dcl_doc_attach_rel = fields.Many2many('dcl.hr.employee.document',
                                          'dcl_doc_attach_rel', 'attach_id3',
                                          'doc_id',
                                          string="Attachment", invisible=1)
    dcl_attach_rel = fields.Many2many('dcl.hr.document', 'dcl_attach_rel', 'attachment_id3',
                                      'document_id',
                                      string="Attachment", invisible=1)
