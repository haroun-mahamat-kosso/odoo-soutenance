from odoo import models, fields, api 

class FacturePersonnalise(models.Model):
    _name = 'facture.personnalise'
    _description = 'Facture Personnalisée'

    name = fields.Char(string="Numéro de facture", required=True)
    customer_id = fields.Many2one('res.partner', string="Client", required=True)
    date = fields.Date(string="Date de la facture", default=fields.Date.today)
    amount_total = fields.Float(string="Montant total")
    state = fields.Selection([('draft', 'Brouillon'), ('sent', 'Envoyé'), ('paid', 'Payé')], string="État", default='draft')
    invoice_lines = fields.One2many('facture.personnalise.line', 'invoice_id', string="Lignes de facture")

    @api.depends('invoice_lines')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(line.amount for line in record.invoice_lines)

    # Méthode d'impression de la facture
    def print_facture(self):
        return self.env.ref('formation__sup.facture_personnalise_report').report_action(self)

class FacturePersonnaliseLine(models.Model):
    _name = 'facture.personnalise.line'
    _description = 'Ligne de facture personnalisée'

    invoice_id = fields.Many2one('facture.personnalise', string="Facture")
    product_id = fields.Many2one('product.product', string="Produit")
    quantity = fields.Float(string="Quantité", default=1)
    price_unit = fields.Float(string="Prix unitaire")
    amount = fields.Float(string="Montant", compute="_compute_amount", store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.price_unit
