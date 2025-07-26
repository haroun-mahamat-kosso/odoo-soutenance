FROM odoo:16
LABEL MAINTAINER="Haroun Kosso <haroun.kosoo@afreetech.com>"
RUN pip3 install xlsxwriter \
    && pip3 install xlrd \
    && pip3 install openpyxl
COPY ./modules /mnt/extra-addons/

# Copie le script d'entrée personnalisé
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Définit le script d'entrée comme point de démarrage du conteneur
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# La commande par défaut passée au script d'entrée (ici, juste 'odoo')
CMD ["odoo"]
