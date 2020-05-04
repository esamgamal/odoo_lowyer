from odoo import fields, api, models, _
from odoo.exceptions import ValidationError


class lowyertransient(models.TransientModel):
    _name = 'lowyer.lowyer.transient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name_2 = fields.Char('Name')
    Grad_2 = fields.Date('GraduationDate')
    phone_2 = fields.Char('Phone')
    def create_lowyer_trs(self):
        vals = {
            'name': self.name_2,
            'GraduationDate': self.Grad_2,
            'phone': self.phone_2
        }
        self.env['lowyer.lowyeres'].create(vals)

class lowyertwkeltransient(models.TransientModel):
    _name = 'lowyer.twkel.transient'
    idCst = fields.Many2one('lowyer.customer')
    twkNo = fields.Char('twkNo', required=True)
    harf = fields.Char('harf', required=True)
    year = fields.Char('year', required=True, default='2020')
    karyMonth = fields.Char('karyMonth', required=True)

    def create_twkel_trs(self):
        vals = {
            'idCst': self.idCst.id,
            'twkNo': self.twkNo,
            'harf': self.harf,
            'year': self.year,
            'karyMonth': self.karyMonth,
            'authid' : self.twkNo + '/' + self.harf + ' Year ' + self.year + ' ' + self.karyMonth
        }
        self.idCst.message_post(body='Create authentication Success Esam Gamal', subject='Create authentication')
        self.env['lowyer.twkel'].create(vals)

    def get_twkel_trs(self):


        """
       idtwkel = self.env['lowyer.twkel'].search([('idCst', '=', docids[0])])
        count = self.env['lowyer.trans'].search_count([('idLowyer', '=', self.id)]) 
        """
        a=self.env['lowyer.twkel'].search([('idCst', '=', self.idCst.id)])

        cnt = self.env['lowyer.twkel'].search_count([])
        print('testtt', cnt)
        for rec in a:
            print(rec.twkNo, rec.harf)







