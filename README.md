# 🎮 Puissance 4 - Projet Python

![Puissance 4](https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Puissance4_01.svg/1200px-Puissance4_01.svg.png)

## 📝 Description

Ce projet est une implémentation du jeu classique Puissance 4 en Python, utilisant la bibliothèque Tkinter pour l'interface graphique. Le jeu propose des fonctionnalités avancées comme :
- Un affichage réaliste des jetons avec effets 3D
- Un mode joueur contre IA
- Un système de sauvegarde/chargement des parties
- Des animations pour les victoires

## 👥 Équipe

Ce projet a été réalisé par :
- **Sheyma ABBES ()**
- **Bilel BENHAMIDA (22407740)** *(Responsable de la publication du code)*
- **Wafaa CHAKEUR (22406506)** *(Responsable de la révision du code et documentation avec Docstring)*
- **Idris ERNADOTE (22401987)**

## 🛠️ Fonctionnalités techniques

### 🔧 Bibliothèques utilisées
- **Tkinter** : Pour l'interface graphique
- **JSON** : Pour la sauvegarde/chargement des parties
- **Random** : Pour l'IA et le choix aléatoire du premier joueur
- **Math** : Pour les calculs d'interpolation des couleurs

### 🎨 Fonctionnalités graphiques
- Jetons avec dégradés de couleur réalistes
- Animation des jetons gagnants (clignotement)
- Barre de victoire animée
- Plateau avec effet de profondeur

### ⚙️ Fonctionnalités du jeu
- Système de manches avec score
- IA basique avec stratégie centrale
- Annulation du dernier coup
- Paramètres personnalisables (taille du plateau, alignements nécessaires, etc.)

## 📚 Comment ça marche ?

### 🎯 Règles du jeu
Le Puissance 4 se joue à deux joueurs sur une grille verticale de 6 lignes et 7 colonnes. Chaque joueur dispose de jetons d'une couleur (rouge ou jaune). Tour à tour, ils insèrent un jeton dans une colonne, qui tombe au point le plus bas disponible. Le premier joueur à aligner 4 jetons horizontalement, verticalement ou diagonalement gagne la manche.

### 💻 Architecture du code
Le code est structuré autour de plusieurs composants principaux :

1. **Gestion du plateau** :
   - Représentation matricielle du plateau
   - Logique de placement des jetons
   - Vérification des victoires et matchs nuls

2. **Interface graphique** :
   - Dessin du plateau et des jetons
   - Gestion des événements souris
   - Affichage des scores et informations

3. **Système de jeu** :
   - Gestion des tours des joueurs
   - Mécanisme de manches
   - Sauvegarde/chargement des parties

4. **Intelligence Artificielle** :
   - Algorithme de choix des colonnes
   - Priorisation des colonnes centrales

### 🧠 L'IA
L'IA utilise une stratégie simple :
1. Elle choisit d'abord parmi les colonnes valides (non pleines)
2. Elle privilégie les colonnes centrales pour maximiser ses chances
3. Elle sélectionne aléatoirement parmi les meilleures options disponibles

## 🚀 Comment lancer le jeu

1. Assurez-vous d'avoir Python 3 installé
2. Clonez ce dépôt :
   ```bash
   git clone https://github.com/BilelBenhamida/puissance4.git Projet