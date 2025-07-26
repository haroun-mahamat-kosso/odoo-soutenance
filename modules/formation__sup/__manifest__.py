# -*- coding: utf-8 -*-
{
    'name': "formation_Sup",
    'sequence': -100,

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,

    'depends': ['base', 'sale'],

    'data': [
        # Sécurité
        'security/ir.model.access.csv',

        # Vues
        'views/TrainingCourse.xml',
        'views/menu.xml',
        'views/student.xml',
        'views/trainer.xml',
        # 'views/custom_invoice.xml',
        # 'views/report_invoice.xml',
        # 'views/report_actions.xml',
        'views/assets.xml',  # Inclure le fichier assets.xml pour charger les styles CSS
        # 'views/facture_personnalise.xml',
        # 'views/facture_personnalise_report.xml',
        # 'reports/facture_personnalise_report.xml',
        # 'views/menu_lateral.xml',  # Assurez-vous que ce fichier est bien référencé ici
    ],
    # icone
    'icon': '/formation__sup/static/src/img/FormationSup.png',  # Lien vers l'icône
    
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'formation__sup/static/src/css/custom_styles.css',  # Chemin vers votre CSS
        ],
    },

}