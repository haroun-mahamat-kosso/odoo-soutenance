    FROM odoo:16
    LABEL MAINTAINER="Haroun Kosso <haroun.kosoo@afreetech.com>"
    RUN pip3 install xlsxwriter \
        && pip3 install xlrd \
        && pip3 install openpyxl
    COPY ./modules /mnt/extra-addons/

    # Correction : Retrait de --no-http-cli car l'option n'est pas reconnue
    # --init base : initialise la base de données avec les modules de base d'Odoo
    CMD ["odoo", "--init", "base"]
    