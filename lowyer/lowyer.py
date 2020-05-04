from odoo import fields,api,models, _
from odoo.exceptions import ValidationError
from datetime import datetime



class inherit_user(models.Model):
    _inherit = 'res.partner'
    company_type = fields.Selection(selection_add=[('ob', 'odoo ob'), ('ox', 'odoo ox')])

class pay_customer_amount(models.Model):
    _name = 'lowyer.payamount'
    idtrans=fields.Integer('Transaction')
    date=fields.Datetime('Date')
    amount=fields.Float('Amount',required=True)
    notes=fields.Char('Notes')
    idpaycust=fields.Many2one('lowyer.paycust',string='Transaction Link')


class pay_customer(models.Model):
    _name = 'lowyer.paycust'

    @api.onchange('idtrans')
    def _onchange_idtrans(self):
        lines=[]
        val = {
            'idtrans': self.idtrans.id,
            'amount': 5,
            'date': datetime.today()
        }
        lines.append((0, 0, val))
        self.idpayamount = lines




        # for rec in self:
        #     # lines = [(6, 0, 0)]
        #     lines = []
        #     for line in self.idtrans:
        #         print('type', type(line))
        #         print('type_id', type(line.id))
        #         val = {
        #             'idtrans': line.id,
        #             'amount': 5,
        #             'date': datetime.today()
        #         }
        #         lines.append((0, 0, val))
        #         print('lines_nex:', lines)
        #     rec.idpayamount = lines

    @api.onchange('idcust')
    def onchange_idcust_id(self):
        for rec in self:
            rec.idtrans = ""
            return {'domain': {'idtrans': [('idCust', '=', rec.idcust.id)]}}

    idcust=fields.Many2one('lowyer.customer',required=True,string='Customer')
    idtrans=fields.Many2one('lowyer.trans',required=True, string='Transaction')

    idpayamount=fields.One2many('lowyer.payamount','idpaycust', string='Amount')

class ahkam(models.Model):
    _name = 'lowyer.ahkam'
    _sql_constraints = [
        ('idtrns_uniq', 'unique (idtrns)', 'Transaction must be unique!'),
    ]

    @api.onchange('dt_session','oppos_date','appeal_date','appeal_appos_date')
    def fun_degree_change(self):
        for rec in self:
            if rec.dt_session:
                rec.deg=25
            if rec.dt_session and rec.oppos_date:
                rec.deg=50
            if rec.dt_session and rec.oppos_date and rec.appeal_date:
                rec.deg = 75
            if rec.dt_session and rec.oppos_date and rec.appeal_date and rec.appeal_appos_date:
                rec.deg=100



    @api.depends('dt_session','oppos_date','appeal_date','appeal_appos_date')
    def fun_degree(self):
        for rec in self:
            if rec.dt_session:
                rec.deg=25
            if rec.dt_session and rec.oppos_date:
                rec.deg=50
            if rec.dt_session and rec.oppos_date and rec.appeal_date:
                rec.deg = 75
            if rec.dt_session and rec.oppos_date and rec.appeal_date and rec.appeal_appos_date:
                rec.deg=100


    idtrns = fields.Many2one('lowyer.trans', string='transaction name')
    opp_name = fields.Char('opponent name')
    opp_address = fields.Char('opponent address')
    court = fields.Char('court')
    cust_name = fields.Char('Customer name')
    dt_session = fields.Date('Date session')
    judgment = fields.Char('Judgment')
    inv_num = fields.Char('Inventory number')
    oppos_date = fields.Date('Opposition Date')
    inv_num2 = fields.Char('Inventory number')
    appeal_date = fields.Date('Appeal date')
    inv_num3 = fields.Char('Inventory number')
    appeal_appos_date = fields.Date('Appellate Opposition Date')
    final = fields.Char('What was done in the final lawsuit')
    sv = fields.Boolean('Save', default=False)
    tot = fields.Integer('Total',default=100)
    deg = fields.Float('Degree',compute='fun_degree',store=True)

    @api.onchange('idtrns')
    def onchange_idtrns(self):
        self.opp_address=self.idtrns.address
        self.court = self.idtrns.court
        self.opp_name = self.idtrns.khsm
        self.cust_name = self.idtrns.idCust.name

    @api.model
    def create(self, vals):
        ad = self.env['lowyer.trans'].browse(vals['idtrns'])
        vals['opp_address'] = ad.address
        vals['court'] = ad.court
        vals['opp_name'] = ad.khsm
        vals['cust_name'] = ad.idCust.name
        result = super(ahkam, self).create(vals)
        return result

    @api.multi
    def write(self, vals):
        ad = self.env['lowyer.trans'].browse(self.idtrns.id)
        vals['opp_address'] = ad.address
        vals['court'] = ad.court
        vals['opp_name'] = ad.khsm
        vals['cust_name'] = ad.idCust.name
        return super(ahkam, self).write(vals)



class check_type(models.Model):
    _name = 'check.type.cases'
    name = fields.Char('Name', required=True)

class trans(models.Model):
    _name = 'lowyer.trans'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Transaction"
    _rec_name = 'kadId'

    @api.depends('idtransDate')
    def max_date_trans(self):
        for rec in self:
            x = self.env['lowyer.trans.date'].search_count([('idtrans', '=', rec.id)])
            print('xxxx',x)
            if x>0 :
                xx=self.env['lowyer.trans.date'].search([('idtrans','=',rec.id)], order='id desc')[0].id
                xx2=self.env['lowyer.trans.date'].search([('idtrans','=',rec.id) , ('id','=',xx)])
                rec.datemax = xx2.toDate

    @api.depends('idtransDate')
    def min_date_trans(self):
        for rec in self:
            x = self.env['lowyer.trans.date'].search_count([('idtrans', '=', rec.id)])
            print('xxxxMIN',x)
            if x > 0:
                xx = self.env['lowyer.trans.date'].search([('idtrans', '=', rec.id)], order='id')[0].id
                xx2 = self.env['lowyer.trans.date'].search([('idtrans', '=', rec.id), ('id', '=', xx)])
                rec.datemin = xx2.transDate



    idahkm = fields.One2many('lowyer.ahkam', 'idtrns')
    idCust = fields.Many2one('lowyer.customer', required=True)
    name_eng=fields.Char('Name English')
    name_eng_upper = fields.Char('Name English Upper', compute='_action_upper_customer', inverse='_action_lower_customer')
    # payment_cust=fields.One2many('idtrans',string='Customer Payment')
    sfth=fields.Char('sfth')
    amount=fields.Float('amount',required=True,default=0)
    nokd = fields.Char('nokd', required=True)
    year = fields.Char('year', required=True)
    court = fields.Char('court', required=True)
    idType = fields.Many2one('lowyer.type', required=True)
    crc = fields.Char('crc')
    idLowyer = fields.Many2one('lowyer.lowyeres')
    khsm = fields.Char('Opponent')
    sfth_khsm = fields.Char('Opponent Adjective')
    address = fields.Text('address')
    subject = fields.Text('subject')
    kadId = fields.Char('kadId')
    datetest=fields.Date('Date Test')

    datemin = fields.Date('Date Min', compute='min_date_trans', store=True)

    datemax = fields.Date('Date Max', compute='max_date_trans',store=True)

    email = fields.Char(string='email', related='idCust.email')
    seq_id = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                         index=True, default=lambda self: _('New'))
    idtransDate = fields.One2many('lowyer.trans.date', 'idtrans', string='Transaction Date')
    idtransImage = fields.One2many('lowyer.trans.image', 'idtranss', string='Transaction Image')
    state = fields.Selection([('first', 'Progress'),('save', 'Saved'),('reject', 'Reject')] , default = "first")

    @api.depends('name_eng')
    def _action_upper_customer(self):
        for rec in self:
            rec.name_eng_upper = self.name_eng.upper() if rec.name_eng else False


    def _action_lower_customer(self):
        for rec in self:
            rec.name_eng = self.name_eng_upper.lower() if rec.name_eng_upper else False

    def action_send_mail_trans(self):
        template_id = self.env.ref('lowyer.email_template_lowyers').id
        print('template_id',template_id)
        self.idLowyer.message_post(body='Create Lowyer Success', subject='Create Lawyer')
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    @api.multi
    def pass_action(self):
        self.state = 'save'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'esam gamal',
                'type': 'rainbow_man',
            }
        }
        # return True


    @api.multi
    def pass_action_r(self):
        self.state = 'reject'

    @api.multi
    def pass_action_s(self):
        self.state = 'first'


    @api.model
    def create(self, vals):

        # print('self.id.create1:', vals.get('id')
        # print('self.id.create2:', self.id)
        #

        # xx = self.env['lowyer.trans.date'].search([('idtrans', '=', self.id)], order='id desc')[0].id
        # xx2 = self.env['lowyer.trans.date'].search([('idtrans', '=', self.id), ('id', '=', xx)])
        # vals['datemax']=xx2.transDate


        idTyp = self.env['lowyer.type'].browse(vals['idType'])
        vals['kadId'] = vals.get('nokd') + ' ' + vals.get('year') + ' ' + str(idTyp.name) + ' ' + vals.get('court')
        if vals.get('seq_id', ('New')) == ('New'):
            vals['seq_id'] = self.env['ir.sequence'].next_by_code('lowyer.trans.sequence') or _('New')

        # print('create id', vals.get('id'))
        result = super(trans, self).create(vals)

        return result

    # @api.multi
    # def write(self, vals):
    #     print('4',self.id)
    #     x = self.env['lowyer.trans.date'].search_count([('idtrans', '=', self.id)])
    #     if x>0 :
    #         print('grate')
    #         xx = self.env['lowyer.trans.date'].search([('idtrans', '=', self.id)], order='id desc')[0].id
    #         xx2 = self.env['lowyer.trans.date'].search([('idtrans', '=', self.id), ('id', '=', xx)])
    #         vals['datemax']=xx2.transDate
    #         return super(trans, self).write(vals)



class customer(models.Model):
    _name = 'lowyer.customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.multi
    def delAuthentication(self):
        for rec in self:
            print('rec',rec)
            rec.idTwks = [(5, 0, 0)]

    @api.multi
    def delAuthentication2(self):
        for rec in self:
            print('rec2', rec)
            rec.idTwks.unlink()

    @api.multi
    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s %s' % (field.name, field.address)))
        return res


    name=fields.Char('Name',required=True,default='Customer Name')
    jop=fields.Char('Jop',default='Jop')
    email=fields.Char('email')
    address=fields.Char('Address',default='Address')
    trans_ids = fields.One2many('lowyer.trans', 'idCust')
    idTwks = fields.One2many('lowyer.twkel', 'idCst', string='Twkel Id')
    seq_id = fields.Char(string='Order Reference', required=True, copy=False,readonly=True,
                       index=True, default=lambda self: _('New'))


    @api.multi
    def print_report(self):
        # data = {
        #     'model': 'lowyer.customer',
        #     'form': self.read()[0]
        # }
        # print('data',data)
        # return self.env.ref('lowyer.action_lowyer_customer').with_context(landscape=True).report_action(self, data=data)

        return self.env.ref('lowyer.action_lowyer_customer').report_action(self)


    @api.model
    def create(self, vals):
        if vals.get('seq_id', ('New')) == ('New'):
            vals['seq_id'] = self.env['ir.sequence'].next_by_code('lowyer.customer.sequence') or _('New')
        result = super(customer, self).create(vals)
        return result

    @api.multi
    def show_total_collection(self):
        raise ValidationError(('Customer Name is :' + self.name))
        # raise ValidationError(_("Recursion found for tax '%s'.") % (self.name,))

    @api.multi
    def cr_lowyer_customer(self):
        print('cron test')





class lowyeres(models.Model):
    _name = 'lowyer.lowyeres'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.depends('salary')
    def lowyer_degree(self):
        for rec in self:
            if rec.salary<=1500 :
                rec.degree='junior'
            else:
                rec.degree='senior'


    @api.model
    def default_get(self, fields_list):
        print('test------ defualt value')
        res=super(lowyeres, self).default_get(fields_list)
        res['salary']=1500
        res['GraduationDate'] = datetime.today()
        res['name']='Please enter the lawyer’s name'
        return res


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            rec.order_id=""
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}


    @api.model
    def get_trans_court_cnt(self):
        count = self.env['lowyer.trans'].search_count([('idLowyer', '=', self.id)])
        self.count = count

    name=fields.Char('Name',required=True,default='Lowyer Name')
    idTrans = fields.One2many('lowyer.trans', 'idLowyer', string='Trans Id')
    Nickname=fields.Char('Nickname')
    GraduationDate=fields.Datetime('GraduationDate')
    College = fields.Char('College')
    University = fields.Char('University')
    address = fields.Char('Address')
    phone = fields.Char('phone')
    experience = fields.Float(string='Experience')
    phone2 = fields.Char('phone2')
    Academic_qualifications = fields.Text('Academic Qualifications')
    prior_experiences = fields.Text('Prior Experiences')
    salary = fields.Float('Salary', default=0, required=True)
    degree = fields.Selection(selection=[
        ('senior', 'Senior'), ('junior', 'Junior')], string="Degree", compute=lowyer_degree, store=True)

    image = fields.Binary()
    active = fields.Boolean('Active', default=True)
    _sql_constraints = [
        ('name_lowyers_uniq', 'unique (name)', 'Name must be unique!'),
    ]
    seq_id = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                         index=True, default=lambda self: _('New'))
    count = fields.Integer(string='Transaction', compute=get_trans_court_cnt)

    partner_id = fields.Many2one("res.partner", string="Customer")
    order_id = fields.Many2one("sale.order", string="Sale order")

    # @api.depends('active')
    # @api.onchange('active')
    # def action_active(self):
    #     print('active',self.active)
    #     if self.active:
    #         return {
    #             'effect': {
    #                 'fadeout': 'slow',
    #                 'message': 'esam gamal',
    #                 'type': 'rainbow_man',
    #             }
    #         }

    def action_open_trans(self):
        return {
            'name': _('Customer'),
            'domain': [('idLowyer', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'lowyer.trans',
            'view_id': False,
            'views': False,
            'type': 'ir.actions.act_window',
        }


    @api.model
    def create(self, vals):
        if vals.get('seq_id', ('New')) == ('New'):
            vals['seq_id'] = self.env['ir.sequence'].next_by_code('lowyer.lowyer.sequence') or _('New')
        print('esam3',self.seq_id)
        result = super(lowyeres, self).create(vals)
        return result

class typekd(models.Model):

    _name = 'lowyer.type'
    name=fields.Char('name')
    idtrans = fields.One2many('lowyer.trans', 'idType',string='Trans Id')


class twkel(models.Model):
    _name = 'lowyer.twkel'
    _rec_name = 'twkNo'

    @api.depends('twkNo','harf','year','karyMonth')
    @api.model
    def calc_authid(self):
        print('pre insert2')
        self.authid = str(self.twkNo) + str('/') + str(self.harf) + ' Year ' + str(self.year) + ' ' + str(self.karyMonth)


    twkNo = fields.Char('twkNo', required=True)
    idCst = fields.Many2one('lowyer.customer')
    harf = fields.Char('harf', required=True)
    year = fields.Char('year',required=True,default='2020')
    _sql_constraints = [
        ('name_uniqx', 'unique ("twkNo","harf","year","karyMonth")', 'No Doublicate Twkel !'),
    ]

    karyMonth = fields.Char('karyMonth', required=True)
    authid=fields.Char('authentication', compute=calc_authid, store=True,readonly=True)

    @api.model
    def create(self, vals):
        vals['authid'] = vals['twkNo'] + '/' + vals['harf'] + ' Year ' + vals['year'] + ' ' + vals['karyMonth']
        print('idCst',self.idCst)


        result = super(twkel, self).create(vals)
        return result


class transDate(models.Model):
    _name = 'lowyer.trans.date'
    transDate=fields.Date('Tranacation Date',required=True)
    note=fields.Char('Notes')
    toDate=fields.Date('To Date',required=True)
    idtrans = fields.Many2one('lowyer.trans')
    # sequence = fields.Integer(string="Sequence")
    sgn = fields.Binary(string="Signature")


class transImage(models.Model):
    _name = 'lowyer.trans.image'
    _rec_name = 'note'
    image = fields.Binary()
    note = fields.Char('Note',required=True)
    idtranss = fields.Many2one('lowyer.trans')
    sequence = fields.Integer(string="Sequence")


class managwork(models.Model):
    _name = 'lowyer.manag.work'
    _rec_name = 'transDate'
    _order = 'transDate'
    transDate=fields.Date('Tranacation Date',required=True)
    notes=fields.Char('Notes',required=True)
    idlower=fields.Many2one('lowyer.lowyeres',string='Lowey Name', required=True)
    complete = fields.Boolean('Complete', default=False)

class inhiret_action_sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self,vals):
        print('test_inhiret')
        res=super(inhiret_action_sale_order, self).action_confirm()
        return res












