    FROM odoo:16
    LABEL MAINTAINER="Haroun Kosso <haroun.kosoo@afreetech.com>"
    RUN pip3 install xlsxwriter \
        && pip3 install xlrd \
        && pip3 install openpyxl
COPY ./modules /mnt/extra-addons/

# Copie le script d'entrée personnalisé et lui donne les permissions d'exécution directement
# La commande RUN chmod +x n'est plus nécessaire car les permissions sont définies ici
COPY --chmod=+x ./entrypoint.sh /usr/local/bin/entrypoint.sh

# Définit le script d'entrée comme point de démarrage du conteneur
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# La commande par défaut passée au script d'entrée
CMD ["odoo"]
    