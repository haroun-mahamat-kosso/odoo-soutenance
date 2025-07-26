from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Student(models.Model):
    _inherit = 'learner.person'
    _name = 'student'
    _description = 'Etudiant'
    
    # Champs de l'étudiant
    is_student = fields.Boolean(string="Apprenant")
    courses = fields.Many2many('training.course', string="Formation")
    
    sale_order_id = fields.Many2one('sale.order', string='Commande de Vente')

    @api.model
    def creation_bonCommande_facture(self, records):
        # Si records est passé sous forme d'IDs, récupérez les objets correspondants
        records = self.browse(records)  # Récupérer les enregistrements complets
        for record in records:
            if record.courses:  # Vérifier qu'il y a au moins une formation
                # Créer un partenaire temporaire basé sur le nom de l'étudiant
                temporary_partner = self.env['res.partner'].create({
                    'name': record.name,  # Utiliser le nom de l'étudiant comme nom du partenaire
                    'is_company': False,  # Le partenaire n'est pas une entreprise
                    'company_id': self.env.user.company_id.id,  # Associer l'entreprise de l'utilisateur connecté
                })
                _logger.info('Création d\'un partenaire temporaire pour l\'étudiant : %s', temporary_partner.name)

                # Assurez-vous que le partenaire a une liste de prix valide
                if not temporary_partner.property_product_pricelist:
                    raise ValueError("Le partenaire temporaire n'a pas de liste de prix définie.")
                
                # Liste des lignes de commande à créer
                sale_order_lines = []
                for course in record.courses:
                    if course.product_id:
                        # Inclure la description de la formation dans la ligne de commande
                        line_description = f"{course.name}\n{course.description}"  # Description complète de la formation
                        
                        sale_order_lines.append((0, 0, {
                            'product_id': course.product_id.id,  # Produit lié à la formation
                            'product_uom': course.product_id.uom_id.id,  # Unité de mesure
                            'product_uom_qty': 1,  # Quantité de produits
                            'price_unit': course.product_id.lst_price,  # Prix de la formation
                            'name': line_description,  # Description avec le nom et la description de la formation
                        }))
                
                if sale_order_lines:
                    # Création de la commande de vente avec toutes les lignes
                    sale_order = self.env['sale.order'].create({
                        'partner_id': temporary_partner.id,  # Utiliser le partenaire temporaire
                        'pricelist_id': temporary_partner.property_product_pricelist.id,  # Liste de prix
                        'date_order': fields.Datetime.now(),  # Date de la commande
                        'company_id': temporary_partner.company_id.id,  # Entreprise (via partenaire)
                        'partner_invoice_id': temporary_partner.id,  # Adresse de facturation
                        'partner_shipping_id': temporary_partner.id,  # Adresse de livraison
                        'order_line': sale_order_lines,  # Ajouter toutes les lignes de commande
                    })

                    # Vérifiez si la commande a bien été créée avant de continuer
                    if sale_order:
                        # Lier la commande de vente à l'étudiant
                        record.sale_order_id = sale_order.id

                        # Confirmer la commande de vente
                        sale_order.action_confirm()

                        # Créer la facture si la méthode est disponible
                        if sale_order.invoice_status == 'to invoice':
                            sale_order._create_invoices()  # Création de la facture pour la commande

                        _logger.info(f"Commande de vente {sale_order.id} créée et confirmée.")
                        return sale_order  # Retourner la commande de vente après traitement
                    else:
                        raise ValueError("La commande de vente n'a pas pu être créée.")
                else:
                    raise ValueError("Aucune ligne de commande valide n'a été ajoutée.")
            else:
                _logger.warning(f"Aucune formation trouvée pour l'étudiant {record.name}.")
    def open_invoice_window(self):
        """ Ouvre une fenêtre modale pour éditer la facture """
        if not self.sale_order_id:
            raise UserError("Aucune commande de vente liée à cet étudiant.")

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',  # Facture de sortie
            'partner_id': self.sale_order_id.partner_id.id,  # Partenaire de la commande
            'invoice_line_ids': [(0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
            }) for line in self.sale_order_id.order_line],
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
            'context': {
                'default_move_type': 'out_invoice',
            },
        }
    def create_custom_invoice(self):
        # Créer une facture personnalisée liée à l'étudiant
        invoice_vals = {
            'name': self.name + ' - Facture',  # Vous pouvez ajouter une logique pour générer une référence unique
            'student_id': self.id,
            'date_invoice': fields.Date.context_today(self),
        }
        invoice = self.env['custom.invoice'].create(invoice_vals)

        # Ajoutez des lignes à la facture personnalisée
        for course in self.courses:
            self.env['custom.invoice.line'].create({
                'invoice_id': invoice.id,
                'product_id': course.product_id.id,  # Assurez-vous que chaque cours est associé à un produit
                'quantity': 1,  # Vous pouvez ajuster selon le cas
                'price_unit': course.product_id.lst_price,  # Utilisation du prix du produit
            })

        # Retourner l'action pour ouvrir la facture personnalisée
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture Personnalisée',
            'res_model': 'custom.invoice',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }
