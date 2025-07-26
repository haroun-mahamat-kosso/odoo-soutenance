from odoo import models, fields

class TrainerFormateur(models.Model): # Modification du modèle 'res.partner' pour ajouter des attributs aux partenaires
    _inherit = 'learner.person' # On hérite du modèle 'learner.person' (modèle de base pour les partenaires)
    _name = 'trainer.formateur'
    _description = 'Formateur'
    
    is_trainer = fields.Boolean(string="Formation") # Champ pour identifier un formateur (true ou false)
    specialite = fields.Char(string="Spécialité", required=True)
    qualification = fields.Char(string="Qualification", required=True)
    anneeExperience = fields.Integer(string="Année d'expérience", required=True)