from odoo import models, fields

class TrainingEvaluation(models.Model): # Modèle d'évaluation des formations
    _name = 'training.evaluation'
    _description = 'Evaluation de la formation' # Description du modèle
    
    course_id = fields.Many2one('training.course', string="Formation", required=True) # La formation concernée par l'évaluation
    student_id = fields.Many2one( string="Apprenant", domain=[('is_student', '=', True)], required=True) # L'apprenant qui a passé l'évaluation
    score = fields.Float(string='Score', help="Le score final de l'évaluation") # Score de l'apprenant à l'évaluation
    evaluation_date = fields.Date(string="Date d'évaluation", default=fields.Date.today) # Date de l'évaluation