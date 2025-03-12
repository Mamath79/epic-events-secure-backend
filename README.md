# Epic Events CRM

## Description
Epic Events CRM est une application de gestion de la relation client (CRM) développée en Python. Cette application permet de gérer les clients, les contrats et les événements pour une entreprise d'événementiel.

## Prérequis
- Python 3.8 ou supérieur
- MySQL
- Un environnement virtuel Python

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/Mamath79/OC_P12_D-veloppez-une-architecture-back-end-securisee-avec-Python-et-SQL.git
cd epic_events
```

2. Créez et activez un environnement virtuel :
```bash
python -m venv env
source env/bin/activate  # Sur Unix/macOS
# ou
.\env\Scripts\activate  # Sur Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configuration de l'environnement :
Créez un fichier `.env` à la racine du projet avec les variables suivantes :
```env
DB_USER=votre_utilisateur
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nom_de_votre_base
```

## Structure du Projet
```
epic_events/
├── crm/
│   ├── controllers/    # Logique de contrôle
│   ├── models/        # Modèles de données
│   ├── views/         # Interface utilisateur
│   ├── services/      # Services métier
│   ├── repositories/  # Accès aux données
│   ├── database/      # Configuration de la base de données
│   └── utils/         # Utilitaires
├── test/              # Tests unitaires et d'intégration
├── main.py           # Point d'entrée de l'application
├── config.py         # Configuration globale
└── requirements.txt   # Dépendances du projet
```

## Utilisation

Pour lancer l'application :
```bash
python main.py
```

## Tests

Pour exécuter les tests :
```bash
pytest
```

Pour générer un rapport de couverture :
```bash
coverage run -m pytest
coverage report
```

## Qualité du Code

Le projet utilise :
- Flake8 pour le linting
- Black pour le formatage
- Coverage.py pour la couverture des tests

Pour vérifier la qualité du code :
```bash
flake8
```

## Sécurité
- Authentification sécurisée avec JWT
- Hachage des mots de passe avec Argon2
- Protection contre les injections SQL avec SQLAlchemy
- Variables d'environnement pour les données sensibles

## Base de données
Le projet utilise MySQL comme système de gestion de base de données. Un schéma de la base de données est disponible dans le fichier `epic_events_databse.png`.

## Manuel Utilisateur

### Navigation dans l'application

#### Menu Principal
Le menu principal vous permet d'accéder aux différentes fonctionnalités de l'application :

- **Gestion des clients**
- **Gestion des contrats**
- **Gestion des événements**
- **Gestion des utilisateurs**
- **Filtrage avancé**

#### Gestion des Clients
La vue liste des clients affiche un tableau avec les informations principales :
- **Nom de l'entreprise**
- **Contact principal**
- **Email**
- **Téléphone**
- **Date de création**
- **Contrats associés**

#####  **Filtrage dynamique**
Possibilité de **filtrer** la liste des clients selon plusieurs critères :
- Nom
- Prénom
- Email
- ID de l'entreprise

#### Gestion des Contrats
Le tableau des contrats affiche :
- **Référence du contrat**
- **Client associé**
- **Montant total**
- **Montant restant à payer**
- **Statut du contrat**
- **Commercial responsable**

#####  **Filtrage avancé**
- Statut du contrat (signé, en attente, annulé)
- ID du client
- ID du commercial
- Montant minimum/maximum

#### Gestion des Événements
Chaque événement est lié à :
- Un client
- Un contrat
- Un support manager (si assigné)

#####  **Filtrage dynamique**
- Date de début / fin
- ID du client
- ID du contrat
- **Filtrage des événements sans support affecté**

#### Gestion des Utilisateurs
Les utilisateurs sont affichés avec :
- **Nom et prénom**
- **Email**
- **Nom d’utilisateur**
- **Département**

#####  **Filtrage par rôles**
- Nom
- Prénom
- Email
- ID du département

### Fonctionnalités Principales

####  **Création d'un nouveau client**
1. Accédez au menu "Clients"
2. Sélectionnez **"Créer un client"**
3. Remplissez le formulaire (nom, prénom, entreprise, etc.)
4. Confirmez l’ajout

#### **Création d'un contrat**
1. Accédez à la fiche client
2. Sélectionnez **"Créer un contrat"**
3. Saisissez le montant total, montant payé, statut et commercial
4. Confirmez l’ajout

#### **Gestion des événements**
1. Accédez au menu "Événements"
2. Sélectionnez **"Créer un événement"**
3. Assignez un support manager si nécessaire
4. Confirmez l’ajout

####  **Filtrage avancé**
Chaque menu possède une option pour appliquer des **filtres dynamiques**, permettant de :
- Voir uniquement les éléments pertinents
- Afficher uniquement les contrats en attente
- Lister les événements sans support assigné