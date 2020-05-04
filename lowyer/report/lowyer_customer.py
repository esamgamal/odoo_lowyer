from odoo import api, models,_


class CustomerReport(models.AbstractModel):
    _name = 'report.lowyer.lowyer_customer'
    _description = 'Customer Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['lowyer.customer'].browse([docids[0]])

        idtwkel = self.env['lowyer.twkel'].search([('idCst', '=', docids[0])])
        twkel_list=[]
        for a in idtwkel:
            vals={
                'twkNo':a.twkNo,
                'harf':a.harf,
                'year':a.year,
                'karyMonth':a.karyMonth,
            }
            twkel_list.append(vals)
        print('twkel_list',twkel_list)
        return  {
            'docs': docs,
            'doc_model': 'lowyer.customer',
            'data': data,
            'twkel_list_tmp':twkel_list,
        }

