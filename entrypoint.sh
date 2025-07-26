    #!/bin/bash
    set -ex # Ajout de -ex pour le débogage détaillé

    # Ce script est un point d'entrée personnalisé pour le conteneur Odoo sur Render.
    # Il s'assure que la base de données est initialisée si elle est vide,
    # et que le service Odoo reste actif pour les vérifications de santé de Render.

    # Fonction pour vérifier si la base de données est initialisée
    # Odoo crée la table 'ir_module_module' quand la DB est initialisée.
    # Nous utilisons 'psql' pour vérifier l'existence de cette table.
    db_is_initialized() {
        PGPASSWORD="$PGPASSWORD" psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB_NAME" -tAc "SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'ir_module_module';"
    }

    echo "Starting Odoo entrypoint script..."

    # Boucle d'attente pour la base de données
    echo "Waiting for PostgreSQL database to be ready..."
    until PGPASSWORD="$PGPASSWORD" psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB_NAME" -c '\q'; do
      >&2 echo "Postgres is unavailable - sleeping"
      sleep 1
    done
    echo "PostgreSQL is ready!"

    # Vérifie si la base de données Odoo est initialisée
    if [ "$(db_is_initialized)" != "1" ]; then
        echo "Odoo database '$DB_NAME' is not initialized. Initializing 'base' module..."
        # Initialise la base de données avec le module 'base'
        # --stop-after-init : Odoo s'arrêtera après l'initialisation
        # --addons-path : s'assure que les modules sont trouvés
        # --no-http : ne démarre pas le serveur HTTP pendant l'initialisation
        # --load=base : charge uniquement le module base
        /usr/bin/python3 /usr/bin/odoo -d "$DB_NAME" \
            --init base \
            --stop-after-init \
            --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/var/lib/odoo/addons/16.0,/mnt/extra-addons \
            --db_host="$HOST" \
            --db_port="$PORT" \
            --db_user="$USER" \
            --db_password="$PASSWORD" \
            --master-passwd="$ODOO_MASTER_PASSWORD" \
            --no-http

        echo "Odoo database initialization complete."
    else
        echo "Odoo database '$DB_NAME' is already initialized."
    fi

    # Démarre le serveur Odoo en mode normal
    echo "Starting Odoo server..."
    # Exécute la commande Odoo principale, en passant tous les arguments reçus par le script
    exec /usr/bin/python3 /usr/bin/odoo \
        --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/var/lib/odoo/addons/16.0,/mnt/extra-addons \
        --db_host="$HOST" \
        --db_port="$PORT" \
        --db_user="$USER" \
        --db_password="$PASSWORD" \
        --master-passwd="$ODOO_MASTER_PASSWORD" \
        "$@" # Passe les arguments du CMD (ici "odoo" seul)
    