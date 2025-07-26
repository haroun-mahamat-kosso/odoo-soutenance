FROM odoo:16
LABEL MAINTAINER="Haroun Kosso <haroun.kosoo@afreetech.com>"
RUN pip3 install xlsxwriter \
    && pip3 install xlrd \
    && pip3 install openpyxl
COPY ./modules /mnt/extra-addons/


