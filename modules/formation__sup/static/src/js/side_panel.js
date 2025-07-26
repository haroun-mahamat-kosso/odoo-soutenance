odoo.define('formation_Sup.side_panel', function (require) {
    "use strict";
    
    var SidePanel = require('web.SidePanel');
    var client = require('web.client');
    
    // Définir la classe de notre menu latéral personnalisé
    var MySidePanel = SidePanel.extend({
        // Personnaliser le contenu du menu ici
        init: function (parent, options) {
            this._super.apply(this, arguments);
        },
        
        // Ici, tu peux ajouter des méthodes pour contrôler l'affichage du contenu
        start: function() {
            this._super.apply(this, arguments);
            this.$el.addClass('o_sidebar');  // Ajouter la classe de menu latéral
        }
    });
    
    // Ajouter l'option de menu latéral personnalisé à l'application
    client.addAction('side_panel', MySidePanel);
});
