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
![Menu Principal](screenshots/menu_principal.png)
Le menu principal vous permet d'accéder aux différentes fonctionnalités de l'application :
- Gestion des clients
- Gestion des contrats
- Gestion des événements
- Gestion des utilisateurs

#### Gestion des Clients
![Liste des Clients](screenshots/liste_clients.png)
La vue liste des clients affiche un tableau avec les informations principales :
- Nom de l'entreprise
- Contact principal
- Email
- Téléphone
- Date de création

![Fiche Client](screenshots/fiche_client.png)
La fiche client détaillée permet de :
- Voir toutes les informations du client
- Modifier les informations
- Voir l'historique des contrats
- Ajouter des notes

#### Gestion des Contrats
![Liste des Contrats](screenshots/liste_contrats.png)
Le tableau des contrats affiche :
- Référence du contrat
- Client associé
- Montant total
- Montant restant à payer
- Statut du contrat

![Fiche Contrat](screenshots/fiche_contrat.png)
La fiche contrat détaillée permet de :
- Voir tous les détails du contrat
- Gérer les paiements
- Voir les événements associés
- Modifier le statut

### Fonctionnalités Principales

#### Création d'un nouveau client
1. Accédez au menu "Clients"
2. Cliquez sur "Nouveau Client"
3. Remplissez le formulaire
4. Validez la création

#### Création d'un nouveau contrat
1. Accédez à la fiche client
2. Cliquez sur "Nouveau Contrat"
3. Remplissez les informations du contrat
4. Validez la création

#### Suivi des paiements
1. Accédez à la fiche contrat
2. Cliquez sur "Ajouter un paiement"
3. Remplissez le montant et la date
4. Validez l'enregistrement

### Conseils d'utilisation
- Utilisez les filtres pour trouver rapidement une information
- Les champs obligatoires sont marqués d'un astérisque (*)
- Vous pouvez exporter les données en format CSV
- Les modifications sont sauvegardées automatiquement

