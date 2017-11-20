# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    id_card = fields.Char(string='身分證字號')
    line_id = fields.Char(string='LINE ID')
    fb_id = fields.Char(string='FB 名稱')
    emergency_contact = fields.Char(string='緊急聯絡人')
    emergency_relation = fields.Char(string='關係')
    emergency_mobile = fields.Char(string='緊急聯絡人電話')

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|',('name', operator, name), '|', ('mobile', operator, name), ('ref',operator, name)]

        banks = self.search(domain + args, limit=limit)
        return banks.name_get()



class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    copy_user_id = fields.Many2one(related='user_id',string='業務員')
    copy_company_id = fields.Many2one(related='company_id',string='銷售的健身房')
    class_len = fields.Integer(compute='_compute_take_count')
    contract_sdate = fields.Date(string="合約生效日", required=False, )
    contract_edate = fields.Date(string="合約到期日", required=False, )
    Identity_type = fields.Selection(string="身份別", selection=[(u'新生', u'新生'), (u'續約生', u'續約生'), ], required=False, )
    Introducer = fields.Char(string="介紹人", required=False, )
    contract_memo = fields.Char(string="備註", required=False, )

    # 計算有幾堂課
    def _compute_take_count(self):
        for partner in self:
            list = self.env['service.class'].search([('class_order_id.order_id', '=', partner.id)])
            partner.class_len = len(list)

    # 當改變自訂欄位的業務員或者公司，會同時改變其他資訊下的資料

    @api.onchange('copy_user_id','copy_company_id')
    def auto_set(self):
        self.user_id = self.copy_user_id
        self.company_id = self.copy_company_id

    # 查看從銷售訂單新增到課程清單有那些課程
    def open_class_list(self):
        action = self.env.ref('gym_service_checkin.service_class_view_action').read()[0]
        action['domain'] = [('class_order_id.order_id', '=', self.id)]
        return action

    # 取消銷售訂單時刪除課程清單，待做
    @api.multi
    def action_cancel(self):
        res = super(InheritSaleOrder, self).action_cancel()
        return res

    # 確認訂單後，將銷售訂單的明細寫入課程清單
    @api.multi
    def action_confirm(self):
        res = super(InheritSaleOrder, self).action_confirm()
        for line in self.order_line:
            if line.product_id.check_in_ok is True:
                class_id = self.env['service.class'].create({
                    'name': line.order_partner_id.id,
                    'class_order_id': line.id,
                    'class_product_id': line.product_id.id,
                    'class_amount': line.product_uom_qty,
                    'class_company_name': line.company_id.name,
                    'class_product_price': line.price_reduce_taxexcl
                })
        return res


# class inheritSaleReport(models.Model):
#     _inherit = 'sale.order.line'

    # checkin_list = fields.One2many(comodel_name='service.checkin.line', inverse_name='checkin_order2')
    # checkin_rest = fields.Float(string='剩餘簽到次數', compute='comput_times', store=True)
    # checkin_times = fields.Integer(string='簽到次數', compute='comput_times', store=True)
    # order_partner_mobile = fields.Char(related='order_partner_id.mobile')


    # @api.multi
    # def name_get(self, context=None):
    #     result = []
    #     for record in self:
    #         name = "[%s](%s) %s in %s" % (record.order_partner_id.name, record.order_partner_mobile, record.name,
    #                                     record.company_id.name)
    #         result.append((record.id, name))
    #     return result

    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     args = args or []
    #     domain = []
    #     partners = self.env['res.partner'].search([('name', operator, name)], limit=limit)
    #     if name:
    #         domain = ['|', ('name', operator, name), ('order_partner_mobile', operator, name)]
    #         if partners:
    #             domain = ['|'] + domain + [('order_partner_id', 'in', partners.ids)]
    #     else:
    #         if partners:
    #             domain = [('order_partner_id', 'in', partners.ids)]
    #
    #     banks = self.search(domain + args, limit=limit)
    #     return banks.name_get()

    # @api.depends('checkin_list.checkin_amount')
    # def comput_times(self):
    #     for line in self.search([]):
    #         line.checkin_times = 0
    #         for list in line.checkin_list:
    #             line.checkin_times += list.checkin_amount
    #         line.checkin_rest = line.product_uom_qty - line.checkin_times


class product_template(models.Model):
    _inherit = ['product.template']

    check_in_ok = fields.Boolean(string='可簽到')


class ServiceClass(models.Model):
    _name = 'service.class'
    _rec_name = 'class_product_id'
    _description = u'課程明細檔'

    name = fields.Many2one(comodel_name='res.partner', string='客戶', ondelete='cascade')
    class_order_id = fields.Many2one(comodel_name='sale.order.line', string='關聯的訂單', ondelete='cascade')
    class_product_id = fields.Many2one(comodel_name='product.product', string='簽到產品', ondelete='cascade')
    class_amount = fields.Integer(string='購買堂數')
    class_checkin_times = fields.Integer(string='已簽到次數', compute='comput_times', store=True)
    class_checkin_rest = fields.Integer(string='剩餘簽到次數', compute='comput_times', store=True)
    class_checkin_list = fields.One2many(comodel_name='service.checkin.line', inverse_name='checkin_order2', string='已簽到列表')
    class_sale_user_id = fields.Many2one(related='class_order_id.salesman_id',string='業務員', store=True)
    class_company_name = fields.Char(string='公司名稱')

    class_checkin_price = fields.Float(string='已簽到金額', compute='comput_times', store=True)
    class_amount_price = fields.Float(string='總金額', compute='compute_price', store=True)
    class_checkin_rest_prcie = fields.Float(string='剩餘金額', compute='comput_times', store=True)
    class_product_price = fields.Float(string='單價', readonly=True)
    # class_member = fields.Many2many(related='class_checkin_list.checkin_member', string='執行員工', store=True)
    # order_partner_mobile = fields.Char(related='name.mobile')
    # order_compamy_id = fields.Many2one(related='class_order_id.company_id')

    @api.depends('class_amount','class_product_price')
    def compute_price(self):
        for line in self:
            line.class_amount_price = line.class_product_price * line.class_amount

    # 檢查簽到次數用
    @api.constrains('class_checkin_rest')
    def check_amount(self):
        if self.class_checkin_rest < 0:
            raise ValidationError(u'客戶：%s的 %s 剩餘訂購次數大於簽到次數' % (self.name.name, self.class_product_id.name))

    # @api.multi
    # def name_get(self, context=None):
    #     result = []
    #     for record in self:
    #         name = "%s in %s" % (record.class_product_id.name, record.order_compamy_id.name)
    #         result.append((record.id, name))
    #     return result

    @api.depends('class_checkin_list.checkin_amount','class_checkin_list.parent','class_product_price')
    def comput_times(self):
        for line in self:
            line.checkin_times = 0
            for list in line.class_checkin_list:
                line.class_checkin_times += list.checkin_amount
            line.class_checkin_rest = line.class_amount - line.class_checkin_times
            line.class_checkin_rest_prcie = line.class_product_price * line.class_checkin_rest
            line.class_checkin_price = line.class_product_price * line.class_checkin_times

    def update_product_price(self):

        for line in self.search([]):
            line.class_product_price = line.class_order_id.price_reduce_taxexcl


class ServiceCheckin(models.Model):
    _name = 'service.checkin'
    _description = u'簽到主檔'

    name = fields.Char(string='簽到ID')
    checkin_date = fields.Datetime(string='建表時間', default=lambda self: fields.Datetime.now(), readonly=True)
    checkin_member = fields.Many2one(comodel_name='res.users', string='執行員工', default=lambda self: self.env.user.id)
    # checkin_pack = fields.Many2one(comodel_name='product.product',string='簽到產品', domain=[('check_in_ok','=',True)])
    checkin_list = fields.One2many(comodel_name='service.checkin.line',inverse_name='parent',string='簽到明細')
    checkin_account = fields.Many2one(comodel_name='account.move', string='會計憑證')
    checkin_account_list = fields.One2many(comodel_name='account.move' ,inverse_name='class_service_id',string='會計憑證列表')
    checkin_account_len = fields.Integer(compute='_compute_account_count')
    state = fields.Selection([(1, '未產生會計傳票'), (2, '已產生')],
                             string='Status', default=1, index=True)

    # 計算產生的會計憑證有幾張
    def _compute_account_count(self):
        for partner in self:
            partner.checkin_account_len = len(partner.checkin_account_list)

    # 查看會計憑證用
    def open_account_list(self):
        action = self.env.ref('account.action_move_journal_line').read()[0]
        action['domain'] = [('class_service_id', '=', self.id)]
        return action

    # def _compute_take_count(self):
    #     for partner in self:
    #         list = self.env['service.class'].search([('class_order_id.order_id', '=', partner.id)])
    #         partner.class_len = len(list)

    @api.model
    def create(self, vals):
        now_code = fields.datetime.now().strftime("%Y%m%d")
        res_id = super(ServiceCheckin, self).create(vals)
        res_id.write({
            'name': self.env.user.company_id.name + str(now_code) + str(res_id.id)
        })
        return res_id

    # 產生會計憑證用：尋找同樣會計科目的名字中，屬於某個的科目
    def compute_account_id(self,account,company):
         account_list= self.env['account.account'].search([('code','=',account.code),('company_id','=',company.id)])
         return account_list.id

    # 產生會計憑證用：尋找是其他分錄的名字中，屬於某個公司的分錄
    def compute_journal(self,company):
        jounal_list = self.env['account.journal'].search([('company_id','=',company.id),('type','=','general'),('code','=','MISC')])
        return jounal_list.id

    # 產生會計憑證
    def checkuin_access(self):

        if self.state != 1:
            raise ValidationError(u'錯誤，會計憑證已產生')
        if self.env.user.company_id.name != u'母公司':
            raise ValidationError(u'錯誤，只有在母公司才能產生會計憑證')
        account = self.env['account.move']
        # 先找出簽到明細有哪幾家公司
        company = self.env['res.company']
        for line in self.checkin_list:
            now_company = line.checkin_order2.class_order_id.company_id
            exist = False
            for company_line in company:
                if company_line == now_company:
                    exist = True

            if exist is False:
                company += now_company
        # 再將同一公司的明細通通放到res，最後在一次寫入
        for line in company:
            res = []
            account_id = None

            for list in self.checkin_list:
                list_company = list.checkin_order2.class_order_id.company_id
                if line == list_company:
                    # 檢查該公司的產品的會計科目有沒有設好
                    # if list.checkin_order2.class_order_id.product_id.get_in_account_id:
                    #     raise ValidationError(u'產品%s未設定好會計科目，在%s' % (list.checkin_order2.class_order_id.product_id.name,list_company.name))
                    # if list.checkin_order2.class_order_id.product_id.property_account_income_id:
                    #     raise ValidationError(u'產品%s未設定好會計科目，在%s' % (list.checkin_order2.class_order_id.product_id.name,list_company.name))

                    checkin_amount = list.checkin_amount
                    credit_account = list.checkin_order2.class_order_id.product_id.categ_id.get_in_account_id
                    credit = {
                        'account_id': self.compute_account_id(credit_account, line),
                        'credit': list.checkin_order2.class_order_id.price_reduce_taxexcl * checkin_amount,
                        'name': list.checkin_order2.class_product_id.name,
                        'partner_id': list.checkin_order2.name.id
                    }
                    debit_account = list.checkin_order2.class_order_id.product_id.categ_id.property_account_income_categ_id
                    debit = {
                            'account_id': self.compute_account_id(debit_account, line),
                            'debit': list.checkin_order2.class_order_id.price_reduce_taxexcl * checkin_amount,
                            'name': list.checkin_order2.class_product_id.name,
                            'partner_id': list.checkin_order2.name.id
                             }
                    res.append([0, 0, credit])
                    res.append([0, 0, debit])

            account_id = account.create({
                'journal_id': self.compute_journal(line),
                'class_service_id': self.id
            })
            account_id.write({
                'line_ids': res,
            })
        self.state = 2




class InheritAccountMoove(models.Model):
    _inherit = 'account.move'

    class_service_id = fields.Many2one(comodel_name='service.checkin', string='關聯的簽到主檔', ondelete='cascade')


class ServiceCheckinLine(models.Model):
    _name = 'service.checkin.line'
    _description = u'簽到明細檔'
    _rec_name = 'checkin_partner'

    name = fields.Char()
    parent = fields.Many2one(comodel_name='service.checkin', ondelete='cascade')
    checkin_partner = fields.Many2one(comodel_name='res.partner',string='簽到客戶', required=True)
    checkin_order2 = fields.Many2one(comodel_name='service.class', string='銷售訂單', required=True,
                                     domain="[('name','=', checkin_partner),('class_checkin_rest','>',0)]", ondelete='cascade')  # demo用

    # checkin_class = fields.Many2one(comodel_name='service.class',compute='compute_set_class',store=True)
    # checkin_limit_member = fields.Many2one(related='checkin_order.partner_id', string='測試')
    # checkin_pack = fields.Many2one(comodel_name='product.product', string='簽到產品',domain=[('check_in_ok','=',True)])
    checkin_rest_amount = fields.Integer(string='剩餘次數', related='checkin_order2.class_checkin_rest')
    checkin_amount = fields.Integer(string='簽到次數', default=1)
    checkin_member = fields.Many2one(comodel_name='res.users', string='執行員工', compute='compute_set_class', store=True)
    checkin_couch = fields.Many2one(comodel_name='res.users', string='教練', required=True)
    checkin_sale_user_id = fields.Many2one(related='checkin_order2.class_order_id.salesman_id', string='業務員', store=True)
    checkin_parent_date = fields.Datetime(default=lambda self: fields.Datetime.now(), string='簽到時間(明細)')

    checin_class_product = fields.Many2one(related='checkin_order2.class_product_id', store=True, string='簽到產品')

    # 將簽到明細寫入執行員工
    @api.depends('parent.checkin_member')
    def compute_set_class(self):
        for line in self:
            line.checkin_member = line.parent.checkin_member


    # 塞選顯示的客戶為有購買課程的客戶列表
    @api.onchange('checkin_partner')
    def domain_partner(self):
        partner_list = self.env['service.class'].search([])
        res = self.env['res.partner']
        for line in partner_list:
            exist = False
            for list in res:
                if list == line.name:
                    exist = True
            if exist is False and line.class_checkin_rest > 0:
                res += line.name
        return {
            'domain': {
                'checkin_partner': [('id', 'in', res.ids)],
            }}





