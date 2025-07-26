    #!/bin/bash
    set -ex # Active le mode débogage (affiche chaque commande exécutée) et quitte en cas d'erreur

    echo "--- Démarrage du script d'entrée personnalisé Odoo ---"

    # Construit l'URL de la base de données à partir des variables d'environnement
    # Cette syntaxe est plus robuste pour psql
    DATABASE_URL="postgresql://${USER}:${PGPASSWORD}@${HOST}:${PORT}/${DB_NAME}"

    # Fonction pour vérifier si la base de données est initialisée
    db_is_initialized() {
        echo "Vérification de l'initialisation de la base de données..."
        # Utilise la chaîne de connexion complète pour psql
        # -tAc : (t) pas de headers, (A) sortie non alignée, (c) commande SQL
        psql "${DATABASE_URL}" -tAc "SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'ir_module_module';"
        local result=$? # Capture le code de retour de la commande psql
        echo "Résultat de db_is_initialized (code de retour psql): $result"
        return $result # Retourne le code de retour
    }

    echo "Attente que la base de données PostgreSQL soit prête à ${HOST}:${PORT}..."
    # Boucle d'attente pour la base de données
    until psql "${DATABASE_URL}" -c '\q'; do
      >&2 echo "Postgres est indisponible - mise en veille..."
      sleep 1
    done
    echo "PostgreSQL est prêt !"

    # Vérifie si la base de données Odoo a besoin d'être initialisée
    # La fonction db_is_initialized retourne 0 si la table existe (DB initialisée), 1 sinon.
    # On veut initialiser si la table n'existe PAS (donc si db_is_initialized retourne 1)
    if [ "$(db_is_initialized)" != "1" ]; then
        echo "La base de données Odoo '$DB_NAME' est déjà initialisée."
    else
        echo "La base de données Odoo '$DB_NAME' n'est PAS initialisée. Tentative d'initialisation du module 'base'..."
        # Initialise la base de données avec le module 'base'
        # --stop-after-init : Odoo s'arrêtera après l'initialisation
        # --addons-path : assure que les modules sont trouvés
        # --no-http : empêche le démarrage du serveur HTTP pendant l'initialisation
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

        # Vérifie si la commande d'initialisation a réussi
        if [ $? -eq 0 ]; then
            echo "Commande d'initialisation de la base de données Odoo exécutée avec succès."
        else
            echo "ERREUR : La commande d'initialisation de la base de données Odoo a échoué avec le code de sortie $?."
            exit 1 # Quitte le script si l'initialisation échoue
        fi
    fi

    echo "Démarrage du serveur Odoo en mode normal..."
    # Exécute la commande Odoo principale, en passant tous les arguments reçus par le script
    exec /usr/bin/python3 /usr/bin/odoo \
        --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/var/lib/odoo/addons/16.0,/mnt/extra-addons \
        --db_host="$HOST" \
        --db_port="$PORT" \
        --db_user="$USER" \
        --db_password="$PASSWORD" \
        --master-passwd="$ODOO_MASTER_PASSWORD" \
        "$@" # Passe les arguments du CMD (ici "odoo" seul)
    