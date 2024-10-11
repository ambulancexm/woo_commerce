#!/bin/bash

# Vérifier si le script est exécuté avec les droits sudo
if [ "$EUID" -ne 0 ]; then
    echo "Veuillez exécuter ce script avec sudo."
    exit 1
fi

# Installer python3-venv si ce n'est pas déjà fait
if ! dpkg -s python3-venv &> /dev/null; then
    echo "Installation de python3-venv..."
    sudo apt-get update
    sudo apt-get install python3-venv -y
fi

# Définir le chemin vers le dossier de ton projet
PROJECT_DIR="/path/to/your/project"  # Remplace par le chemin de ton projet

# Changer de répertoire vers le projet
cd "$PROJECT_DIR" || { echo "Le dossier $PROJECT_DIR n'existe pas."; exit 1; }

# Installer Git si ce n'est pas déjà fait
if ! command -v git &> /dev/null; then
    echo "Installation de Git..."
    sudo apt-get install git -y
fi

# Cloner le projet (remplace l'URL par celle de ton projet)
REPO_URL="https://github.com/your/repository.git"  # Remplace par l'URL de ton dépôt
if [ ! -d ".git" ]; then
    echo "Clonage du dépôt Git..."
    git clone "$REPO_URL" .
else
    echo "Le dépôt Git existe déjà."
fi

# Créer un environnement virtuel s'il n'existe pas déjà
if [ ! -d "venv" ]; then
    echo "Création d'un nouvel environnement virtuel..."
    python3 -m venv venv
else
    echo "Environnement virtuel existant trouvé."
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances à partir de requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installation des dépendances à partir de requirements.txt..."
    pip install --upgrade pip  # Met à jour pip
    pip install -r requirements.txt
else
    echo "Le fichier requirements.txt n'existe pas."
fi

# Désactiver l'environnement virtuel
deactivate

echo "Configuration terminée ! Tu peux maintenant travailler sur ton projet."
