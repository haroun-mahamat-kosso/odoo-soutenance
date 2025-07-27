    #!/bin/bash
    set -ex # Active le mode débogage (affiche chaque commande exécutée) et quitte en cas d'erreur

    echo "--- Démarrage du script d'entrée personnalisé Odoo ---"

    # Construit l'URL de la base de données à partir des variables d'environnement
    # Cette syntaxe est plus robuste pour psql
    DATABASE_URL="postgresql://${USER}:${PGPASSWORD}@${HOST}:${PORT}/${DB_NAME}"

    # Fonction pour vérifier si la base de données est initialisée
    # Retourne 0 si la table 'ir_module_module' existe (DB initialisée), 1 sinon.
    db_is_initialized() {
        echo "Vérification de l'initialisation de la base de données..."
        # Utilise la chaîne de connexion complète pour psql
        # -tAc : (t) pas de headers, (A) sortie non alignée, (c) commande SQL
        # Si la table existe, psql retourne 0 (succès). Sinon, il retourne 1 (échec).
        psql "${DATABASE_URL}" -tAc "SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'ir_module_module';"
    }

    echo "Attente que la base de données PostgreSQL soit prête à ${HOST}:${PORT}..."
    # Boucle d'attente pour la base de données
    until psql "${DATABASE_URL}" -c '\q'; do
      >&2 echo "Postgres est indisponible - mise en veille..."
      sleep 1
    done
    echo "PostgreSQL est prêt !"

    # Toujours tenter d'initialiser/mettre à jour la base de données avec le module 'base'
    # Cela garantit que la DB est toujours à jour et bien initialisée.
    echo "Tentative d'initialisation/mise à jour du module 'base' pour la base de données Odoo '$DB_NAME'..."
    /usr/bin/python3 /usr/bin/odoo -c /etc/odoo/odoo.conf -d "$DB_NAME" \
        --init base \
        --stop-after-init \
        --db_host="$HOST" \
        --db_port="$PORT" \
        --db_user="$USER" \
        --db_password="$PASSWORD" \
        --no-http # Suppression de --master-passwd

    # Vérifie si la commande d'initialisation a réussi
    if [ $? -eq 0 ]; then
        echo "Commande d'initialisation de la base de données Odoo exécutée avec succès."
    else
        echo "ERREUR : La commande d'initialisation de la base de données Odoo a échoué avec le code de sortie $?."
        exit 1 # Quitte le script si l'initialisation échoue
    fi

    echo "Démarrage du serveur Odoo en mode normal..."
    # Exécute la commande Odoo principale pour un fonctionnement normal
    # Le --master-passwd n'est PAS nécessaire ici car la DB est déjà initialisée
    # IMPORTANT : --addons-path est maintenant géré par la variable d'environnement ODOO_ADDONS_PATH
    exec /usr/bin/odoo -c /etc/odoo/odoo.conf \
        --db_host="$HOST" \
        --db_port="$PORT" \
        --db_user="$USER" \
        --db_password="$PASSWORD" \
        "$@" # Passe les arguments du CMD (ici "odoo" seul)
    