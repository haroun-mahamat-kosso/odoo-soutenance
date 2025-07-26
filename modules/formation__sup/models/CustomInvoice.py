from odoo import models, fields, api
from odoo.exceptions import UserError

class CustomInvoice(models.Model):
    _name = 'custom.invoice'
    _description = 'Facture Personnalisée'

    # Déclaration des champs
    name = fields.Char(string='Référence', required=True, copy=False, default='Nouveau')
    student_id = fields.Many2one('student', string='Étudiant', required=True)
    date_invoice = fields.Date(string='Date de Facture', default=fields.Date.context_today)
    total_amount = fields.Float(string='Montant Total', compute='_compute_total_amount')
    line_ids = fields.One2many('custom.invoice.line', 'invoice_id', string='Lignes de Facture')

    @api.depends('line_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.amount for line in record.line_ids)

    def action_download_invoice(self):
        """Générer et télécharger le PDF de la facture personnalisée"""
        report = self.env.ref('formation__sup.custom_invoice_report')  # Référence au rapport de la facture personnalisée
        if not report:
            raise UserError('Le rapport de la facture n\'a pas été trouvé.')
        
        # Utilisation de report_action pour générer le rapport PDF
        return report.report_action(self)

    def get_report_values(self, docids, data=None):
        """Retourne les données nécessaires pour le rendu du rapport"""
        docs = self.browse(docids)  # Récupère les factures basées sur les identifiants
        return {
            'doc': docs,  # Assure que 'doc' contient les informations nécessaires
            'docids': docids,
        }

class CustomInvoiceLine(models.Model):
    _name = 'custom.invoice.line'
    _description = 'Ligne de Facture Personnalisée'

    # Déclaration des champs
    product_id = fields.Many2one('product.product', string='Produit', required=True)
    quantity = fields.Float(string='Quantité', default=1.0)
    price_unit = fields.Float(string='Prix Unitaire')
    amount = fields.Float(string='Montant', compute='_compute_amount')

    invoice_id = fields.Many2one('custom.invoice', string='Facture')

    @api.depends('quantity', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.price_unit
