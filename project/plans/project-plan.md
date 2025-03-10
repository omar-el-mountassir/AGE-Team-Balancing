# Plan de Projet de Balancement d'Équipes pour Age of Empires 2

Version 1.1

## Résumé Exécutif

Ce document présente le plan détaillé pour le développement d'un bot Discord destiné à la communauté Age of Empires 2. Le bot automatisera la création d'équipes équilibrées pour les parties multijoueurs, en tenant compte des ELO des joueurs, de leurs positions préférées, et suggérera des civilisations adaptées selon le contexte de jeu.

Le projet sera réalisé en deux phases principales:

1. Un MVP fonctionnel couvrant les besoins essentiels (6 semaines) - **COMPLÉTÉ**
2. Une phase d'enrichissement avec intelligence artificielle et fonctionnalités avancées

Cette solution répondra directement au défi de créer des parties équitables entre joueurs de niveaux très variés (ELO 1v1 de 1100 à 2400), tout en enrichissant l'expérience de jeu avec des recommandations stratégiques.

## Contexte du Projet

Notre communauté de joueurs d'Age of Empires 2 interagit principalement via Discord. Nous organisons régulièrement des parties d'équipe personnalisées et non classées entre nous. Le défi principal est que les niveaux de compétence (ELO) de nos joueurs varient considérablement :

- ELO 1v1 : de 1100 à 2400.
- ELO de partie d'équipe : de 1200 à 2000.

Nous souhaitons créer un système capable de suggérer trois compositions d'équipe différentes et équilibrées, compte tenu des ELO variables des joueurs impliqués.

## État Actuel du Projet

Nous avons complété la première phase du projet qui consistait à développer un MVP fonctionnel. Les fonctionnalités suivantes ont été implémentées:

- Système d'enregistrement des joueurs avec leur pseudo Steam
- Récupération automatique des ELO depuis les API d'Age of Empires 2
- Algorithme de balancement d'équipes basé sur les ELO et les préférences de position
- Système de file d'attente pour les parties
- Suggestion de civilisations adaptées à la position, carte et composition d'équipe
- Suivi des résultats de parties et statistiques de joueurs
- Commandes d'administration pour la gestion du bot

Le système est fonctionnel et peut être utilisé par la communauté. Une documentation complète a été créée pour faciliter l'installation, la configuration, et l'utilisation du bot.

## Objectifs et Portée

Le projet vise à créer un bot Discord qui:

1. Enregistre les joueurs avec leurs ELO (récupérés automatiquement ou saisis manuellement)
2. Propose plusieurs compositions d'équipes équilibrées basées sur les ELO et les préférences de position
3. Suggère des civilisations optimales selon la position et la carte
4. Suit l'historique des parties et calcule des statistiques de performance

### Critères de Succès

- Le déséquilibre entre les équipes suggérées ne dépasse pas 3% en moyenne
- L'écart de temps de fin de partie entre équipes est réduit d'au moins 20% par rapport aux parties sans balancement
- 80% des utilisateurs trouvent le système facile à utiliser et utile
- Les suggestions de civilisations sont pertinentes dans au moins 75% des cas

## Architecture Technique

### Vue d'Ensemble

Le bot est développé en Python, utilisant:

- Discord.py pour l'interface Discord
- SQLite pour le stockage des données (prévu pour une future migration vers PostgreSQL)
- Clients API pour récupérer les données de joueurs depuis AoE2.GG et autres sources
- Algorithmes personnalisés de balancement d'équipes et de suggestion de civilisations

### Structure du Projet

```
/AGE-Team-Balancing
  /src
    /api           - Clients API pour les données de joueurs
    /balancer      - Algorithmes de balancement d'équipes
    /models        - Modèles de données
    /data          - Données statiques (civilisations, cartes)
    /bot           - Implémentation du bot Discord
    /utils         - Fonctions utilitaires
    /services      - Services supplémentaires
  /tests           - Tests unitaires et d'intégration
  main.py          - Point d'entrée
  config.py        - Gestion de la configuration
```

### Composants Principaux

1. **Modèles de Données** (`src/models/`)

   - `Player`: Joueur avec ses informations Discord, Steam et ELO
   - `Team`: Équipe de joueurs avec leurs positions et civilisations
   - `Civilization`: Données de civilisation avec forces et évaluations
   - `GameResult`: Résultat de partie pour les statistiques

2. **Clients API** (`src/api/`)

   - Interface commune pour tous les clients API
   - Client AoE2.GG implémenté
   - Système de fallback en cas d'indisponibilité d'API

3. **Algorithmes de Balancement** (`src/balancer/`)

   - Algorithme de génération de compositions d'équipes équilibrées
   - Analyseur de positions optimales pour les joueurs
   - Système de suggestion de civilisations

4. **Bot Discord** (`src/bot/`)
   - Commandes pour l'enregistrement, la file d'attente, et le balancement
   - Interface utilisateur avec embeds et boutons
   - Système de gestion des permissions

## Plan d'Implémentation

### Phase 1: MVP Fonctionnel (Complétée)

- ✅ Développement des modèles de données
- ✅ Implémentation de la récupération des ELO via API
- ✅ Création de l'algorithme de balancement d'équipes de base
- ✅ Développement des commandes Discord essentielles
- ✅ Système de suggestion de civilisations basique
- ✅ Tests et déploiement initial

### Phase 2: Enrichissement et Intelligence Artificielle (En Cours de Planification)

- 🔲 Migration vers une base de données persistante (PostgreSQL)
- 🔲 Intégration de modèles ML pour prédire les résultats des matchs
- 🔲 Amélioration des suggestions de civilisations basée sur les données historiques
- 🔲 Ajout d'une interface web pour la visualisation des statistiques
- 🔲 Internationalisation pour supporter plusieurs langues
- 🔲 Gestion automatique des canaux vocaux pour les équipes

## Calendrier de Développement

| Phase | Composant                    | Durée Estimée | Statut   |
| ----- | ---------------------------- | ------------- | -------- |
| 1     | Modèles de données           | 1 semaine     | Complété |
| 1     | Clients API                  | 1 semaine     | Complété |
| 1     | Algorithme de balancement    | 2 semaines    | Complété |
| 1     | Commandes Discord            | 1 semaine     | Complété |
| 1     | Suggestions de civilisations | 1 semaine     | Complété |
| 2     | Migration base de données    | 2 semaines    | Planifié |
| 2     | Modèles ML                   | 4 semaines    | Planifié |
| 2     | Interface web                | 3 semaines    | Planifié |
| 2     | Internationalisation         | 1 semaine     | Planifié |
| 2     | Gestion des canaux vocaux    | 1 semaine     | Planifié |

## Dépendances et Risques

### Dépendances

- Disponibilité des API externes (AoE2.GG, etc.)
- Stabilité de l'API Discord
- Qualité des données d'ELO disponibles

### Risques et Mitigations

| Risque                                            | Impact | Probabilité | Mitigation                                                          |
| ------------------------------------------------- | ------ | ----------- | ------------------------------------------------------------------- |
| Indisponibilité des API                           | Élevé  | Moyen       | Système de fallback entre plusieurs API, cache local ✅             |
| Changements dans l'API Discord                    | Élevé  | Faible      | Suivi des annonces Discord, tests réguliers                         |
| Données d'ELO incomplètes                         | Moyen  | Élevé       | Option de saisie manuelle, estimation basée sur les performances ✅ |
| Complexité algorithmique pour les grandes équipes | Moyen  | Moyen       | Optimisations et limites de taille d'équipe configurables ✅        |

## Plan de Test et Validation

- Tests unitaires pour les algorithmes de balancement
- Tests d'intégration pour les interactions entre composants
- Tests utilisateurs avec la communauté
- Métriques de performance pour évaluer la qualité des équipes générées

## Plan de Déploiement et Maintenance

### Déploiement

1. Déploiement sur un serveur VPS ou service cloud
2. Monitoring et alertes en cas de problème
3. Sauvegarde automatique des données

### Maintenance

- Mises à jour régulières basées sur les retours utilisateurs
- Ajustements des algorithmes selon les performances observées
- Maintenance des dépendances et mises à jour de sécurité

## Conclusion et Prochaines Étapes

La phase MVP du projet a été complétée avec succès. Le bot est fonctionnel et peut être utilisé par la communauté.

Les prochaines étapes sont:

1. Déployer le bot en production et le faire utiliser par la communauté
2. Recueillir les retours des utilisateurs pour identifier les opportunités d'amélioration
3. Commencer la planification détaillée de la Phase 2 avec le développement de la persistence des données et l'intelligence artificielle

Le bot représente une solution solide au problème de déséquilibre dans les parties d'équipe et contribuera à améliorer l'expérience de jeu de notre communauté.

---

_Document préparé par l'équipe AGE-Team-Balancing_
_Dernière mise à jour: 10 Mars 2025_
