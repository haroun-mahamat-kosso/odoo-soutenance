from odoo import models, fields

class TrainingEnrollement(models.Model): # Modèle d'inscription à une formation
    _name = 'training.enrollment' # Nom technique du modèle
    _description = 'Inscription à une formation' # Description du modèle
    
    # student_id = fields.Many2one('res.partner', string="Apprenant", domain=[('is_student', '=', True)]) # L'apprenant, relation avec le modèle res.partner
    cours_id = fields.Many2one('Training.course', string="Formation", required=True) # La formation, relation avec le modèle TrainingCourse
    enrollment_date = fields.Date(string="Date d'inscription", default=fields.Date.today) # Date d'inscription (par défaut, la date du jour)
    progress = fields.Float(string="Progrès", default=0.0) # Progrès de l'apprenant dans la formation (en pourcentage)
    state = fields.Selection([
        ('ongoing', 'En cours'),
        ('completed', 'Terminée'),
        ('dropped', 'Abandonnée')
    ], default='ongoing', string="Statut") # Valeur par défaut : 'en cours'