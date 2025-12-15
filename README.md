# GoInsight

[![Partner Tenuki](https://img.shields.io/badge/Partner-Tenuki-orange)](https://tenuki-brest.jeudego.org)
[![Partner IMT Atlantique](https://img.shields.io/badge/Partner-IMT_Atlantique-blue)](https://www.imt-atlantique.fr/en)
[![Website KataGo](https://img.shields.io/badge/Website-KataGo-green)](https://katagotraining.org)
[![GitHub KataGo](https://img.shields.io/badge/Github-KataGo-black)](https://github.com/lightvector/KataGo)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/license/MIT)

<table>
  <tr>
    <td width="150">
      <img src="assets/GoInsight_logo.png" alt="Logo" width="250"/>
    </td>
    <td>
      <p>GoInsight is a tool to help Go player analyse their games. It uses a fine-tuned version of <b>KataGo</b>, alongside various pre and post-processings steps to provide a user-friendly feedbacks on Go games. This project is the result of the collaboration between <b>Tenuki</b> and <b>IMT Atlantique</b>.</p>
    </td>
  </tr>
</table>

## Installation

This project requires Python `3.7` or higher. Please ensure Python `3.7+` is installed and available on your `PATH` before running the setup.

### Unix (Linux/MacOS)

First, open a terminal in the directory you'd like to clone the project in.

```bash
# Clone the repo
git clone https://github.com/leobeaumont/GoInsight.git
cd GoInsight
```
```bash
# Setup the environement
make setup
```
```bash
# Activate the virtual environment
source .venv/bin/activate
```
```bash
# Download KataGo model
make get-model
```

You're all setup !

### Windows

First, open PowerShell in the directory where you'd like to clone the project.

```powershell
# Clone the repo
git clone https://github.com/leobeaumont/GoInsight.git
cd ./GoInsight/
```
```powershell
# Allow PowerShell scripts to run (first time only)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
```powershell
# Setup the environment
.\make.ps1 setup
```
```powershell
# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```
```Powershell
# Download KataGo model
.\make.ps1 get-model
```

## Commands

### Run KataGo in terminal

This start an instance of KataGo, type gtp commands to interact with it.
- Use `quit` command to close the instance
- Use `list_commands` to get a list of all the commands

#### Unix (Linux/MacOs)

```bash
make run-model
```
#### Windows

```Powershell
.\make.ps1 run-model
```

### Optimise KataGo for your device (optional)

Start a batch of tests to find the best parameters (This will take a few minutes)

#### Unix (Linux/MacOS)

```bash
make opt-model
```
#### Windows

```Powershell
.\make.ps1 opt-model
```

### Tests

This will run all tests declared in the tests directory

#### Unix (Linux/MacOS)

```bash
make tests
```

#### Windows

```powershell
.\make.ps1 tests
```

### Documentation

This will open the project's documentation on your default web browser

#### Unix (Linux/MacOS)

```bash
make docs
```

#### Windows

```powershell
.\make.ps1 docs
```

### Clean project

Remove setup files and the virtual environment from the project

#### Unix (Linux/MacOS)

```bash
make clean
```

#### Windows

```powershell
.\make.ps1 clean
```

## Contributing

Contributions are not welcome yet, as this project is part of students cursus a `IMT Atltantique`. The project will be opened to contributors after the course ended.

## Acknowledgements

### Structures

- `Tenuki` Brest Go association.
- `IMT Atlantique` engineering school.
- `KataGo` open ource Go engine.

### Supervisors and clients

- Coppin Gilles
- Le Hir Mathieu
- Peillard Étienne

### Project members

- Beaumont Léo (leo.beaumont@imt-atlantique.net)
- Chambriard Léopold (leopold.chambriard@imt-atlantique.net)
- Chouki Mouad (mouad.chouki@imt-atlantique.net)
- Disdier Jordan (jordan.disdier@imt-atlantique.net)
- Garrana Simon (simon.garrana@imt-atlantique.net)
- Miranda-Gonzales Marcelo (marcelo.miranda-gonzales@imt-atlantique.net)
- Roubertou Amaury (amaury.roubertou@imt-atlantique.net)

## Contacts

For any questions or supports, please contact leo.beaumont@imt-atlantique.net.

## Features

### SGFTree

L’objet SgfTree est une représentation complète et structurée d’un fichier SGF (Smart Game Format), format standard utilisé pour décrire des parties de jeux de plateau comme le Go. Il sert d’interface centrale pour lire, manipuler, comparer, convertir et écrire des parties SGF, tout en conservant la structure en arbre propre à ce format.

#### Représentation interne d’une partie SGF

Un SgfTree représente un noeud de l’arbre SGF.
Chaque noeud contient :

- un dictionnaire de propriétés SGF (properties), où chaque clé est un identifiant SGF (par exemple B, W, SZ, etc.) associé à une liste de valeurs,

- une liste de nœuds enfants (children), permettant de représenter les variantes de jeu.

Cette structure permet de modéliser fidèlement :

- la ligne principale d’une partie,

- les variantes et sous-variantes,

- l’ordre exact des coups et des métadonnées.

#### Création d’un SgfTree
Un SgfTree peut être créé de plusieurs manières :
- Depuis un fichier SGF
La méthode from_sgf(path) lit un fichier SGF sur le disque, vérifie son existence, puis le parse pour construire l’arbre correspondant.


- Depuis un objet Game
La méthode from_game(game) permet de convertir un objet Game (logique interne du moteur) en arbre SGF, assurant ainsi une interopérabilité totale entre la représentation logique du jeu et le format SGF.


- Par parsing direct d’une chaîne SGF
La fonction parse(input) transforme une chaîne SGF brute en un SgfTree, en validant rigoureusement la syntaxe (parenthèses, propriétés, majuscules, délimiteurs, etc.).


#### Conversion vers d’autres formats
Le SgfTree joue un rôle de pont entre différents formats :
- Vers un objet Game
La méthode to_game() reconstruit un objet Game à partir de l’arbre SGF, permettant ensuite de simuler la partie, l’analyser ou la modifier.

- Vers une chaîne ou un fichier SGF
La méthode to_sgf(path=None) sérialise l’arbre en une chaîne SGF valide.
Si un chemin est fourni, le SGF est également écrit dans un fichier.


La sérialisation respecte les règles du SGF :
- échappement des caractères spéciaux,

- gestion correcte des variantes,

- génération d’un SGF syntaxiquement valide.


#### Accès à la séquence de coups
La méthode move_sequence() permet d’extraire la suite des coups joués, dans l’ordre, à partir de l’arbre :
- les coups sont convertis du format SGF vers le format GTP,

- la taille du plateau est automatiquement détectée si nécessaire,

- les coups peuvent être retournés soit sous forme de chaînes ("B A19"), soit sous forme de tuples (("B", "A19")).

Cette méthode est particulièrement utile pour :
- rejouer une partie,

- interfacer avec un moteur de Go,

- analyser ou afficher une partie coup par coup.

#### Gestion de la taille du plateau
La méthode get_board_size() extrait la taille du plateau à partir de la propriété SZ du nœud racine :
- elle supporte les formats carrés et rectangulaires,

- elle valide les tailles par rapport à une constante maximale,

- elle garantit que la taille retournée est cohérente et exploitable.

#### Parsing SGF robuste
Le module inclut un parseur SGF complet qui :
- valide la structure des arbres,

- interdit les propriétés en minuscules,

- gère correctement les caractères échappés,

- détecte les erreurs de syntaxe (arbres vides, délimiteurs incorrects, format invalide).

Cela garantit que tout SgfTree créé à partir d’un SGF est structurellement valide.

### Classe Move
L’objet Move représente un coup individuel dans une partie de Go. Il encapsule toutes les informations nécessaires pour décrire, interpréter, valider et convertir un coup entre différents formats standards (interne, SGF et GTP).
Rôle général

#### Un Move relie :
- une partie (Game),

- une couleur (noir ou blanc),

- une position sur le plateau ou un pass,

- un numéro de tour dans la partie.

Il constitue ainsi l’unité de base permettant de rejouer une partie, de l’exporter ou de l’analyser.

#### Création et validation d’un coup

Lors de l’instanciation :

- la couleur peut être fournie explicitement (B / W), sinon elle est déduite automatiquement à partir de l’état de la partie,

- la position est validée à l’aide du plateau associé au jeu,

- un coup sans position correspond à un pass.
Toute tentative de jouer sur une position invalide provoque une erreur, garantissant la cohérence de la partie.

#### Conversion entre formats de coordonnées

La classe Move fournit plusieurs méthodes de conversion essentielles :

- SGF -> coordonnées internes
 sgf_to_coord() traduit une position SGF ("dd") en coordonnées (x, y) utilisables par le moteur.

- SGF -> GTP
 sgf_to_gtp() convertit une coordonnée SGF en notation GTP (A19, Q4, etc.), en tenant compte de la taille du plateau et du cas particulier du pass.

- GTP -> Move
 from_gtp() permet de créer directement un objet Move à partir d’une instruction GTP standard ("w A19"), en validant la syntaxe et les coordonnées.

Ces conversions assurent l’interopérabilité avec :
- les moteurs de Go,

- les interfaces graphiques,

- les fichiers SGF.

#### Export du coup
Un Move peut être exporté sous différents formats :

- Vers GTP
to_gtp() retourne une commande GTP valide représentant le coup.


- Vers SGF
to_sgf() génère la propriété SGF correspondante ({"B": ["dd"]}), directement exploitable dans un arbre SGF.

### Classe Board
L’objet Board représente l’état du plateau de Go à un instant donné, construit à partir d’une séquence de coups. Il est responsable de toute la logique spatiale : placement des pierres, groupes, libertés et captures.
#### Rôle général
Un Board :
- maintient une représentation matricielle du plateau,

- applique les règles fondamentales du Go (libertés, captures),

- permet des opérations locales et globales sur l’état du jeu.

Il constitue le socle de la logique de jeu.
#### Initialisation du plateau
Lors de sa création :
- le plateau est dimensionné (par défaut 19×19),

- la liste des coups est utilisée pour reconstruire l’état du jeu,

- chaque coup est joué dans l’ordre avec mise à jour automatique des captures.

Toute incohérence dans la séquence de coups est détectée immédiatement.
#### Validation des positions
La méthode is_valid_pos() vérifie :
- que la position est dans les limites du plateau,

- qu’elle n’est pas déjà occupée.

Elle est utilisée aussi bien pour jouer que pour retirer des coups, garantissant l’intégrité du plateau.
#### Manipulation des coups
Le plateau peut être modifié dynamiquement :
- Ajout d’un coup
add_move() place une pierre et déclenche la détection des captures.

- Suppression d’un coup
remove_move() enlève une pierre, soit par référence directe, soit par coordonnées.

Ces opérations permettent par exemple :
- le retour en arrière,

- l’édition d’une partie,

- l’analyse de positions intermédiaires.

#### Analyse locale du plateau

Le plateau fournit des outils d’analyse essentiels :
- Voisinage orthogonal
_neighbors() retourne les intersections adjacentes selon la connectivité du Go.

- Groupes et libertés
group_and_liberties() identifie :

- un groupe de pierres connectées,

- l’ensemble de ses libertés.


Cette méthode est au cœur de la logique de capture.
#### Gestion des captures
La méthode update_board() :
- examine les groupes affectés par un coup,

- détecte ceux qui n’ont plus de libertés,

- retire automatiquement les pierres capturées.

Cette implémentation est volontairement agnostique des règles avancées (ko, suicide interdit, etc.), ce qui la rend robuste et facilement extensible.
#### Sélection de zones
La méthode area_selection_positions() permet d’extraire toutes les intersections d’une zone rectangulaire du plateau, en notation GTP.
Elle est particulièrement utile pour :

- l’analyse locale,

- l’intégration avec des moteurs,

- des outils de visualisation ou de statistiques.


### Classe Analizer
L’objet Analizer est responsable de l’analyse automatique d’une partie de Go à l’aide du moteur KataGo.
Il constitue la couche centrale reliant :
- la représentation interne du jeu (Game, SgfTree),

- le moteur d’IA externe,

- les données nécessaires à l’interface utilisateur.


#### Rôle général
Un Analizer permet :
- d’analyser toute la partie coup par coup (analyse globale),

- d’effectuer une analyse approfondie d’un coup précis,

- d’extraire des indicateurs quantitatifs (winrate, score lead),

- de normaliser les résultats du point de vue d’un joueur donné (Noir ou Blanc).

#### Initialisation

Lors de sa création :
- le fichier SGF est chargé et converti en SgfTree,

- le joueur analysé (B ou W) est fixé,

- les structures de stockage des résultats sont initialisées.

Toute valeur invalide pour le joueur est immédiatement rejetée.

#### Analyse globale de la partie
La méthode shalow_game_analysis() :
- sélectionne automatiquement le binaire KataGo selon le système d’exploitation,

- reconstruit la partie à partir de l’arbre SGF,

- génère l’entrée JSON attendue par KataGo,

- lance une analyse pour chaque tour de la partie,

- collecte et trie les résultats.


Le résultat est stocké dans game_analysis et contient, pour chaque coup :
- winrate,

- score lead,

- joueur courant,

- coups recommandés par l’IA.

Cette analyse constitue la base de toutes les autres fonctionnalités.

#### Analyse approfondie d’un coup

La méthode deep_turn_analysis() permet d’analyser un tour spécifique en profondeur :
- avec éventuellement une restriction spatiale (zone autorisée ou interdite),

- avec une profondeur de recherche plus importante,

- en extrayant les meilleures variantes possibles.

Les résultats sont stockés dans turn_analysis, indexés par numéro de tour.

#### Extraction d’indicateurs globaux
game_score_lead() retourne l’évolution du score tout au long de la partie,

les données sont prêtes à être utilisées pour des graphiques ou statistiques.

#### Données de base pour l’interface
La méthode turn_basic_data() fournit les informations essentielles à afficher pour un tour donné :
- winrate du joueur analysé,

- score lead du joueur analysé,

- meilleur coup proposé par KataGo,

- score attendu après ce coup,

- joueur devant jouer le coup suivant.

Toutes les valeurs sont normalisées du point de vue du joueur sélectionné, ce qui simplifie fortement l’affichage.
#### Données avancées pour l’interface
La méthode turn_advanced_data() retourne :

- une liste ordonnée des meilleurs coups,

- leur score attendu,

- une variation principale tronquée.


Ces données sont destinées à un affichage détaillé ou interactif.

### Classe Evaluator
L’objet Evaluator est chargé de qualifier la qualité des coups joués à partir des résultats fournis par l’Analizer.

#### Rôle général

Un Evaluator :
- transforme des données numériques (winrate) en jugements qualitatifs,

- fournit une lecture humaine et pédagogique de la partie,

- applique une grille de classification standard.

#### Classification d’un coup
La méthode classify_move() :
- compare le winrate avant et après un coup,

- calcule la perte (ou le gain) de winrate,

- corrige le signe selon le joueur qui a joué,

- classe le coup dans une catégorie :

BEST
EXCELLENT
GOOD
INACCURACY
MISTAKE
BLUNDER

Les seuils de classification sont définis dans MOVE_CLASSIFICATION_BOUNDS.

#### Classification de toute la partie

La méthode classify_game() applique cette logique à tous les coups de la partie et retourne une liste alignée avec les tours du jeu.
Cette classe permet donc de produire :
- des annotations automatiques,

- des commentaires pédagogiques,

- des statistiques de performance.

### Classe API
La classe API constitue la couche d’interface externe du projet.
Elle expose une API simple, orientée consommation par une interface graphique ou un client web.
#### Rôle général
L’API :

- orchestre Analizer et Evaluator,

- masque la complexité de KataGo et des structures internes,

- retourne uniquement des données JSON prêtes à l’emploi.


#### Analyse complète au chargement
La méthode all_moves_analysis() :

- lance l’analyse globale de la partie,

- classe tous les coups,

- regroupe toutes les données dans un seul objet JSON.

Les données retournées incluent :

- les informations détaillées par tour,

- la classification qualitative de chaque coup,

- l’évolution du score sur toute la partie.

Cette méthode est conçue pour être appelée au chargement initial d’une analyse.

#### Analyse approfondie avec filtre spatial
La méthode deep_turn_area_analysis() :

- lance une analyse approfondie d’un coup donné,

- permet de limiter ou d’exclure une zone du plateau,

- retourne uniquement les meilleurs coups et variantes.

Cette fonctionnalité est idéale pour :

- l’exploration interactive,

- l’analyse locale,

- l’enseignement et le commentaire de parties.


#### Format de sortie
Toutes les méthodes de l’API retournent :
- des chaînes JSON bien formatées,

- directement exploitables par un frontend,

- sans dépendance aux objets internes du moteur.