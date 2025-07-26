    FROM odoo:16
    LABEL MAINTAINER="Haroun Kosso <haroun.kosoo@afreetech.com>"
    RUN pip3 install xlsxwriter \
        && pip3 install xlrd \
        && pip3 install openpyxl
COPY ./modules /mnt/extra-addons/

# Copie le script d'entrée personnalisé et lui donne les permissions d'exécution directement
COPY --chmod=+x ./entrypoint.sh /usr/local/bin/entrypoint.sh

# Copie le fichier de configuration Odoo
COPY ./odoo_dev_conf/odoo.conf /etc/odoo/odoo.conf

# Définit le script d'entrée comme point de démarrage du conteneur, en l'exécutant avec bash
# C'est crucial pour s'assurer que le script est interprété correctement et que set -ex fonctionne
ENTRYPOINT ["bash", "/usr/local/bin/entrypoint.sh"]
# La commande par défaut passée au script d'entrée
CMD ["odoo"]
    