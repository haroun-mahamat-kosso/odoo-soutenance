FROM odoo:16
LABEL MAINTAINER="Haroun Kosso <haroun.kosoo@afreetech.com>"
RUN pip3 install xlsxwriter \
    && pip3 install xlrd \
    && pip3 install openpyxl
COPY ./modules /mnt/extra-addons/

# Ajout de la commande de démarrage pour Odoo
# --init base : initialise la base de données avec les modules de base d'Odoo
# --no-http-cli : désactive le client HTTP en ligne de commande, ce qui est préférable pour les déploiements sur des plateformes comme Render
CMD ["odoo", "--init", "base", "--no-http-cli"]
