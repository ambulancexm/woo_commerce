#!/bin/bash

# Définir le chemin vers le dossier de ton projet
PROJECT_DIR="/path/to/your/project"  # Remplace par le chemin de ton projet

# Changer de répertoire vers le projet
cd "$PROJECT_DIR" || { echo "Le dossier $PROJECT_DIR n'existe pas."; exit 1; }

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "L'environnement virtuel n'existe pas. Veuillez d'abord exécuter setup_project.sh."
    exit 1
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Exécuter le fichier principal du projet
if [ -f "main.py" ]; then  # Remplace "main.py" par le nom de ton fichier principal
    echo "Lancement de l'application..."
    python main.py
else
    echo "Le fichier principal main.py n'existe pas dans le projet."
fi

# Désactiver l'environnement virtuel
deactivate
