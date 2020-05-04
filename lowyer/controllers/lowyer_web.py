
from odoo import http
from odoo.http import request


class check_trans(http.Controller):

    @http.route('/update_customer', type='json', auth='public')
    def update_customer(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                customer = request.env['lowyer.customer'].sudo().search([('id', '=', rec['id'])])
                if customer:
                    customer.sudo().write(rec)
                args = {'success': True, 'message': 'Success'}
        return args

    @http.route('/get_transaction', type='json', auth='public')
    def get_transaction(self):
        trans_rec = request.env['lowyer.trans'].search([])
        trans = []
        for rec in trans_rec:
            vals = {
                'id': rec.kadId,
                'name': rec.year,
            }
            trans.append(vals)
        print('web service')
        data = {'status': 200, 'response': trans, 'message': 'Success Esam Gamal'}
        return data

    @http.route('/create_customer', type='json', auth='public')
    def create_customer(self, **rec):
        if request.jsonrequest:
            print('test', rec)
            if rec['p_name']:
                vals = {'name': rec['p_name'],
                        'jop': rec['p_jop'],
                        'email': rec['p_email']
                        }
            new_customer = request.env['lowyer.customer'].sudo().create(vals)
            args = {'success': True, 'message': 'Success Esam Gamal', 'ID': new_customer.id}
        return args
