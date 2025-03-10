# Bot d'Équilibrage d'Équipes pour Age of Empires 2

Un bot Discord pour créer des équipes équilibrées pour les parties multijoueurs d'Age of Empires 2, en tenant compte des classements ELO des joueurs, de leurs préférences de position, et en suggérant des civilisations optimales.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.3.0%2B-blue)](https://discordpy.readthedocs.io/en/stable/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Vue d'ensemble

Ce bot aide les communautés Age of Empires 2 à créer des équipes justes et équilibrées pour les matchs multijoueurs. Il est particulièrement utile pour les communautés avec des joueurs de différents niveaux de compétence (classements ELO allant de 1100 à 2400).

### Fonctionnalités principales

- **Enregistrement des joueurs** : Enregistrez les joueurs avec leurs pseudos Steam et récupérez automatiquement leurs classements ELO
- **Équilibrage d'équipes** : Générez des compositions d'équipes équilibrées basées sur l'ELO des joueurs et leurs préférences
- **Optimisation des positions** : Suggérez des positions optimales (flanc/poche) pour les joueurs en fonction de leur historique de performances
- **Suggestions de civilisations** : Recommandez des civilisations en fonction de la position, de la carte et de la composition de l'équipe
- **Historique des matchs** : Suivez les résultats des parties et maintenez des statistiques pour les joueurs
- **Résilience API** : Mécanismes de secours pour gérer l'indisponibilité des API

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Un token de bot Discord du [Portail Développeur Discord](https://discord.com/developers/applications)
- Accès au serveur Discord où vous souhaitez ajouter le bot
- Git (optionnel, pour cloner le dépôt)

### Guide d'installation

1. **Obtenir le code** :

   ```bash
   # Cloner le dépôt
   git clone https://github.com/yourusername/AGE-Team-Balancing.git
   cd AGE-Team-Balancing

   # Alternativement, téléchargez et extrayez le fichier ZIP depuis GitHub
   ```

2. **Configurer un environnement virtuel** :

   ```bash
   # Créer un environnement virtuel
   python -m venv venv

   # Activer l'environnement virtuel
   # Sur Windows :
   venv\Scripts\activate
   # Sur macOS/Linux :
   source venv/bin/activate
   ```

3. **Installer les dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer le bot** :

   ```bash
   # Créer un fichier de configuration
   cp .env.example .env
   ```

   Puis modifiez le fichier `.env` avec vos paramètres. Au minimum, vous devez définir :

   - `DISCORD_TOKEN` : Votre token de bot Discord du Portail Développeur Discord

5. **Exécuter le bot** :

   ```bash
   python main.py
   ```

### Configuration du Bot Discord

1. Allez sur le [Portail Développeur Discord](https://discord.com/developers/applications)
2. Cliquez sur "New Application" et donnez-lui un nom
3. Naviguez vers l'onglet "Bot" et cliquez sur "Add Bot"
4. Sous "Privileged Gateway Intents", activez :
   - Server Members Intent
   - Message Content Intent
5. Sous "Token", cliquez sur "Copy" pour copier votre token de bot (à placer dans votre fichier `.env`)
6. Pour ajouter le bot à votre serveur, allez dans l'onglet "OAuth2" > "URL Generator"
7. Sélectionnez les scopes "bot" et "applications.commands"
8. Sélectionnez les permissions suivantes pour le bot :
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Use Slash Commands
9. Copiez l'URL générée et ouvrez-la dans votre navigateur pour ajouter le bot à votre serveur

## Configuration

Le bot est configuré via des variables d'environnement dans le fichier `.env`. Voici ce que signifie chaque paramètre :

### Configuration du Bot Discord

- `DISCORD_TOKEN` : Votre token de bot Discord
- `COMMAND_PREFIX` : Préfixe pour les commandes du bot (par défaut : `!`)
- `BOT_STATUS` : Message de statut affiché pour le bot

### Configuration de l'API

- `AOE2_GG_API_BASE_URL` : URL de base pour l'API aoe2.gg
- `AOE_NEXUS_API_BASE_URL` : URL de base pour l'API AOE Nexus
- `AOCREC_API_BASE_URL` : URL de base pour l'API AOCREC
- `API_TIMEOUT` : Délai d'attente en secondes pour les requêtes API
- `API_CACHE_TTL` : Durée de vie en secondes pour les réponses API mises en cache

### Configuration de la base de données

- `DATABASE_URL` : Chaîne de connexion à la base de données (utilise SQLite par défaut)

### Configuration de l'équilibrage d'équipes

- `ELO_1V1_WEIGHT` : Poids donné aux classements ELO 1v1 (0-1)
- `ELO_TEAM_WEIGHT` : Poids donné aux classements ELO d'équipe (0-1)
- `POSITION_FACTOR_MIN` : Facteur d'ajustement minimum pour les préférences de position
- `POSITION_FACTOR_MAX` : Facteur d'ajustement maximum pour les préférences de position
- `ACCEPTABLE_TEAM_DIFF_PERCENT` : Différence en pourcentage maximale acceptable entre les équipes

### Paramètres supplémentaires

- `LOG_LEVEL` : Niveau de journalisation (INFO, DEBUG, etc.)
- `LOG_FORMAT` : Format de journalisation (console ou json)
- `DEV_MODE` : Activer les fonctionnalités du mode développement
- `ENABLE_ML_BALANCER` : Activer l'équilibreur d'apprentissage automatique (si implémenté)

## Utilisation

### Commandes de base

- `/register [pseudo_steam]` - Enregistrez-vous avec votre pseudo Steam
- `/profile [utilisateur?]` - Consultez votre profil ou celui d'un autre utilisateur
- `/queue [preference_position?]` - Rejoignez la file d'attente pour une partie
- `/leave` - Quittez la file d'attente
- `/status` - Vérifiez l'état actuel de la file d'attente
- `/balance [2v2|3v3|4v4]` - Générez des compositions d'équipes équilibrées

### Commandes avancées

- `/preferences [flanc|poche] [civilisations?]` - Définissez vos préférences de position et de civilisation
- `/civ_suggest [position] [carte?]` - Obtenez des suggestions de civilisations
- `/report_result [victoire|défaite]` - Signalez le résultat d'une partie
- `/stats [joueur?]` - Consultez les statistiques des joueurs
- `/history` - Consultez les compositions d'équipes précédentes

### Commandes d'administration

- `/admin_update_elo [utilisateur]` - Forcez la mise à jour des classements ELO d'un joueur
- `/admin_force [utilisateur] [équipe]` - Forcez un joueur dans une équipe spécifique
- `/admin_config [paramètre] [valeur?]` - Consultez ou modifiez la configuration du bot
- `/admin_status` - Consultez l'état du bot
- `/clear_queue` - Videz la file d'attente

## Dépannage

### Problèmes courants

1. **Le bot ne répond pas aux commandes** :

   - Vérifiez si le bot est en ligne sur Discord
   - Vérifiez que vous avez activé les intents correctes dans le Portail Développeur Discord
   - Assurez-vous que le bot dispose des permissions appropriées sur votre serveur

2. **Erreurs API lors de la récupération des classements ELO** :

   - Vérifiez votre connexion Internet
   - Vérifiez les URL de base des API dans votre fichier `.env`
   - Les API peuvent être temporairement indisponibles ; le bot dispose de mécanismes de secours

3. **Le bot plante au démarrage** :
   - Vérifiez votre token Discord
   - Assurez-vous que toutes les dépendances sont correctement installées
   - Consultez les journaux d'erreurs pour des problèmes spécifiques

### Obtenir de l'aide

Si vous rencontrez des problèmes non couverts ici, veuillez :

1. Vérifier les journaux pour les messages d'erreur
2. Ouvrir une issue sur GitHub avec des détails sur votre problème
3. Inclure les messages d'erreur pertinents et votre configuration (supprimez les informations sensibles)

## Développement

### Structure du projet

```tree
/AGE-Team-Balancing
  /src
    /api           - Clients API pour récupérer les données des joueurs
    /balancer      - Algorithmes d'équilibrage d'équipes
    /models        - Modèles de données
    /data          - Données statiques (civilisations, cartes)
    /bot           - Implémentation du bot Discord
    /utils         - Fonctions utilitaires
    /services      - Services supplémentaires
  /tests           - Suite de tests
  main.py          - Point d'entrée
  config.py        - Configuration
  requirements.txt - Dépendances
```

### Exécution des tests

```bash
pytest
```

### Style de code

Ce projet suit les directives de style PEP 8. Vous pouvez vérifier votre style de code avec :

```bash
flake8 .
```

Et formater votre code avec :

```bash
black .
```

## Développement futur

Notre feuille de route comprend :

1. **Intégration de base de données** : Remplacer le stockage en mémoire par une base de données persistante
2. **Métriques avancées** : Implémenter un suivi plus sophistiqué des performances des joueurs
3. **Équilibreur d'apprentissage automatique** : Utiliser le ML pour prédire les résultats des parties et créer des équipes équilibrées
4. **Interface Web** : Développer une application web complémentaire pour une interaction plus facile
5. **Internationalisation** : Ajouter la prise en charge de plusieurs langues
6. **Gestion des canaux vocaux** : Déplacer automatiquement les joueurs vers les canaux vocaux d'équipe

Consultez le fichier `project-plan.md` pour plus de détails sur le développement futur.

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à soumettre une Pull Request.

1. Forkez le dépôt
2. Créez votre branche de fonctionnalité (`git checkout -b fonctionnalite/super-fonctionnalite`)
3. Committez vos modifications (`git commit -m 'Ajouter une super fonctionnalité'`)
4. Poussez vers la branche (`git push origin fonctionnalite/super-fonctionnalite`)
5. Ouvrez une Pull Request

Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour des informations plus détaillées.

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## Remerciements

- [discord.py](https://github.com/Rapptz/discord.py) pour le wrapper de l'API Discord
- [AoE2.net](https://aoe2.net/) pour l'API Age of Empires 2
- La communauté Age of Empires 2 pour l'inspiration et le soutien
