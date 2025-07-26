from odoo import models, fields, api

class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'Formation'
    
    name = fields.Char(string="Titre de la formation", required=True)
    description = fields.Text(string="Description")
    start_date = fields.Date(string="Date de début")
    end_date = fields.Date(string="Date de fin")
    duration = fields.Integer(string="Durée estimée (en heures)")
    prixFormation = fields.Integer(string="Prix", required=True)
    trainer = fields.Many2many('res.partner', string="Formateur")
    state = fields.Selection([
         ('open', 'Ouverte'),
         ('ongoing', 'En cours'),
         ('closed', 'Terminée')
     ], default='open', string='Statut')
    
    # Champ pour lier chaque formation à un produit de type 'Service'
    product_id = fields.Many2one('product.product', string="Produit associé", required=True, help="Produit associé à la formation pour la vente", domain="[('type', '=', 'service')]")
    
    # Prix de la formation calculé en fonction du produit associé
    price = fields.Float(string="Prix de la formation", compute='_compute_price', store=True)
    
    # Calcul du prix basé sur le produit associé
    @api.depends('product_id')
    def _compute_price(self):
        for record in self:
            if record.product_id:
                record.price = record.product_id.lst_price  # Prix basé sur le produit associé

    # Relier la formation aux commandes de vente
    sale_order_ids = fields.One2many('sale.order.line', 'product_id', string='Commandes de Vente')
    
    # Relier la formation aux étudiants
    student_ids = fields.Many2many('student', string="Étudiants inscrits")
