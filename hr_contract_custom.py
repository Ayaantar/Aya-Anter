from odoo import models, fields, api
from datetime import timedelta


class HrSalary(models.Model):
    _name = 'hr.contract'
    _inherit = ['hr.contract', 'mail.thread', 'mail.activity.mixin']

    gross_salary = fields.Float(string='Gross Salary')
    wage_per_day = fields.Float(string='Wage Per Day', compute='_compute_wage_per_day', store=True, readonly=False)
    wage_per_hour = fields.Float(string='Wage Per Hour', compute='_compute_wage_per_hour', store=True, readonly=False)


    insurance_salary = fields.Float(string='Insurance Salary')
    insurance_start_date = fields.Date(string='Insurance Start Date')
    medical_insurance_date = fields.Date(string='Medical Insurance Date')
    insurance_id = fields.Char(string='Insurance ID')
    last_years = fields.Float(string='إعفاء من سنوات سابقة')
    job_position_insurance = fields.Char(string='Ins. Job Position')
    exemption = fields.Float(string= 'حد الاعفاء')
    income = fields.Float(string='الوعاء الخاضع الضريبة', compute='_calculate_exemption')
    salary_type = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank')], string='Salary Type')
    certificate = fields.Selection([
        ('graduate', 'Graduate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ], string='Certificate Level',related='employee_id.certificate')

    housing = fields.Float(string="Housing Allowance")
    transportation = fields.Float(string="Transportation Allowance")
    other = fields.Float(string="Other Allowances")
    retirement_date = fields.Date(string='Retirement Date')
    retired = fields.Boolean(string='Retired')
    retirement_alert_sent = fields.Boolean(string='Retirement Alert Sent', default=False)

    # def check_retirement_alerts(self):
    #     print('check_retirement_alerts')
    #     today = fields.Date.today()
    #     alert_date = today + timedelta(days=30)
    #     contracts = self.search([
    #         ('retirement_date', '=', alert_date),
    #         # ('retirement_alert_sent', '=', False)
    #     ])
    #     print(contracts)
    #     for contract in contracts:
    #         # إرسال التنبيه
    #         template_id = self.env.ref('hr_salary_edit.retirement_alert_email_templatee').id
    #         print(template_id)
    #         self.env['mail.template'].browse(template_id).send_mail(contract.id, force_send=True)
    #         # تحديث حالة التنبيه
    #         contract.retirement_alert_sent = True


    # def action_submit(self):
    #     self.state = 'submitted'
    #     users = self.env.ref('hr_payroll.group_hr_payroll_manager').users
    #     for user in users:
    #         self.activity_schedule('openacademy.mail_act_course_approval', user_id=user.id,
    #                                note=f'Please Approve course {self.name}')
    def check_retirement_alerts(self):
        print('check_retirement_alerts')
        today = fields.Date.today()
        alert_date = today + timedelta(days=30)
        contracts = self.search([
            ('retirement_date', '=', alert_date),
            # ('retirement_alert_sent', '=', False)
        ])
        print('contracts', contracts)
        print('contracts', self.env.uid)
        user_id = self.env.uid
        for contract in contracts:
            contract.activity_schedule('hr_egyptian_localizationn.mail_activity_retirement_date', user_id=user_id,
                                           note=f'Please cheek contract {self.name}')
            # إرسال التنبيه
            # template_id = self.env.ref('hr_egyptian_localizationn.retirement_alert_email_templateee').id
            # email_template = self.env['mail.template'].browse(template_id)
            # email_template.send_mail(contract.id, force_send=True)
            #
            # # تسجيل الرسالة في Chatter
            # contract.message_post(
            #     body=f"Retirement alert sent to {contract.employee_id.name} for retirement date {contract.retirement_date}")
            #
            # # تحديث حالة التنبيه
            # contract.retirement_alert_sent = True

    @api.depends('gross_salary')
    def _compute_wage_per_day(self):
        for contract in self:
            contract.wage_per_day = contract.gross_salary / 30

    @api.depends('wage_per_day')
    def _compute_wage_per_hour(self):
        for contract in self:
            contract.wage_per_hour = contract.wage_per_day / 8


    @api.depends('gross_salary', 'insurance_salary', 'exemption', 'last_years')
    def _calculate_exemption(self):
        for rec in self:
            rec.income = (rec.gross_salary * 12) - (((rec.insurance_salary * 12 ) * 0.11) + rec.exemption + rec.last_years)



