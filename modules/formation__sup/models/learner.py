from odoo import models, fields

class LearnerPerson(models.Model):
    _name = 'learner.person'
    _description = 'Apprenant'
    
    name = fields.Char(string="Noms et Prénoms", required=True)
    dateNaiss = fields.Date(string="Date de naissance", required=True)
    phone = fields.Char(string="Numéro Téléphone")    