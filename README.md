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
### SGFTree

`SgfTree` is a complete, structured representation of an SGF (Smart Game Format) file, the standard format used to describe board game records such as Go. It acts as the central interface to read, manipulate, compare, convert and write SGF trees while preserving the tree structure of the format.

#### Internal representation of an SGF game

A `SgfTree` represents a node of the SGF tree. Each node contains:

- a dictionary of SGF properties (`properties`) where each key (for example `B`, `W`, `SZ`, etc.) maps to a list of values;
- a list of child nodes (`children`) used to represent variations.

This structure models the mainline of a game, all variations and the exact order of moves and metadata.

#### Constructing a `SgfTree`

A `SgfTree` can be created in several ways:
- from an SGF file: `from_sgf(path)` reads and parses a file to build the tree;
- from a `Game` object: `from_game(game)` converts internal game objects into an SGF tree;
- by parsing an SGF string: `parse(input)` validates and parses an SGF string.

#### Conversion and serialization

`SgfTree` acts as a bridge:
- to a `Game` object via `to_game()`;
- to an SGF string or file via `to_sgf(path=None)` (writes to disk if `path` is provided).

Serialization handles escaping, variations and produces a syntactically valid SGF.

#### Accessing the move sequence

`move_sequence()` extracts the ordered sequence of moves:
- converts SGF moves to GTP notation;
- auto-detects board size when needed;
- returns moves as strings ("B A19") or tuples (("B", "A19")).

This is useful to replay a game, interface with a Go engine, or display moves step-by-step.

#### Board size handling

`get_board_size()` reads the `SZ` property from the root node and:
- supports square and rectangular boards;
- validates the size against a maximum limit;
- returns a size usable by the engine.

#### Robust SGF parsing

The module includes a parser that:
- validates the tree structure;
- forbids lowercase property identifiers;
- correctly handles escaped characters;
- detects syntax errors (empty trees, incorrect delimiters, invalid format).

This guarantees that any `SgfTree` produced from an SGF is structurally valid.

### Move

The `Move` object represents a single move in a Go game. It encapsulates all information required to describe, validate and convert a move between internal, SGF and GTP formats.

#### Structure and role

A `Move` links:
- a game (`Game`),
- a color (black or white),
- a board coordinate or a pass,
- a move number.

It is the basic unit to replay, export or analyze a game.

#### Creation and validation

- color can be provided (B/W) or inferred from the game state;
- coordinates are validated against the associated `Board`;
- a move without coordinates represents a pass.

An attempt to play on an invalid coordinate raises an error.

#### Coordinate conversions

`Move` provides several conversion helpers:
- `sgf_to_coord()` converts an SGF coordinate ("dd") to internal `(x, y)`;
- `sgf_to_gtp()` converts SGF coordinates to GTP notation (A19, Q4, etc.) taking board size into account;
- `from_gtp()` constructs a `Move` from a GTP command (e.g. "w A19").

These conversions ensure interoperability with engines, GUIs and SGF files.

#### Export

- `to_gtp()` returns a valid GTP command for the move;
- `to_sgf()` generates the corresponding SGF property (e.g. `{"B": ["dd"]}`).

### Board

`Board` represents the state of the Go board at a given time, built from a sequence of moves. It is responsible for spatial logic: stone placement, groups, liberties and captures.

#### Responsibilities

A `Board`:
- maintains a matrix representation of the board;
- enforces basic rules (liberties, captures);
- supports local and global operations on the game state.

#### Initialization

- sizes the board (default 19×19);
- reconstructs the state from a move list;
- applies each move in order and updates captures.

Any inconsistency in the move sequence is detected immediately.

#### Position validation

`is_valid_pos()` checks that a coordinate is within bounds and not already occupied.

#### Move manipulation

- `add_move()` places a stone and triggers capture detection;
- `remove_move()` removes a stone (by reference or coordinates).

These operations enable undo, editing and intermediate-state analysis.

#### Local analysis utilities

- `_neighbors()` returns orthogonally adjacent intersections;
- `group_and_liberties()` identifies a connected group and its liberties.

These methods are central to capture logic.

#### Capture handling

`update_board()`:
- examines groups affected by a move;
- detects groups with no liberties;
- removes captured stones automatically.

The implementation intentionally ignores advanced rule variations (ko, suicide rules, etc.) to remain robust and extensible.

#### Area selection

`area_selection_positions()` returns all intersections in a rectangular area (GTP notation). Useful for local analysis, engine integration and visualization.

### Analizer

`Analizer` is responsible for automatic analysis of a Go game using the KataGo engine. It is the central layer connecting the internal game representation (`Game`, `SgfTree`), the AI engine and the UI data.

#### Role

`Analizer` provides:
- full-game analysis move-by-move;
- deep analysis of a specific move;
- extraction of quantitative indicators (winrate, score lead);
- normalization of results from a given player's perspective (Black or White).

#### Initialization

On creation:
- the SGF file is loaded and converted into an `SgfTree`;
- the analyzed player (B/W) is fixed;
- result storage structures are initialized.

Invalid player values are rejected.

#### Full-game analysis

`shalow_game_analysis()`:
- selects the KataGo binary for the current OS;
- reconstructs the game from the SGF tree;
- generates the JSON input expected by KataGo;
- runs an analysis for each move;
- collects and sorts the results.

Results are stored in `game_analysis` and include, for each move: winrate, score lead, current player and recommended moves.

#### Deep analysis of a move

`deep_turn_analysis()` performs a deep search for a specific turn:
- can restrict or exclude a spatial area;
- increases search depth;
- extracts best variations.

Results are stored in `turn_analysis` indexed by move number.

#### Global indicators

`game_score_lead()` returns the score lead evolution through the game, ready for plotting and statistics.

#### Basic data for UI

`turn_basic_data()` provides the essential fields for a turn: winrate for the analyzed player, score lead, best suggested move and expected post-move score.

### Evaluator

`Evaluator` is responsible for grading moves using results from the `Analizer`.

#### Role

An `Evaluator`:
- transforms numeric data (winrate) into qualitative judgments;
- provides pedagogical, human-readable feedback;
- applies a standard classification grid.

#### Move classification

`classify_move()`:
- compares winrate before and after a move;
- computes winrate loss (or gain);
- adjusts sign based on the player who moved;
- classifies the move into categories:

BEST
EXCELLENT
GOOD
INACCURACY
MISTAKE
BLUNDER

Thresholds are defined in `MOVE_CLASSIFICATION_BOUNDS`.

#### Full-game classification

`classify_game()` applies the above logic to all moves and returns an aligned list of classifications for the whole game. This enables automatic annotations, pedagogical comments and performance statistics.

### API

`API` provides the external interface layer of the project. It exposes a simple JSON-oriented API designed to be consumed by a GUI or web client.

#### Responsibilities

- orchestrates `Analizer` and `Evaluator`;
- hides KataGo and internal object complexity;
- returns JSON-ready payloads.

#### Full analysis on load

`all_moves_analysis()`:
- runs the full-game analysis;
- classifies all moves;
- aggregates data into a single JSON object.

Returned data includes per-move details, qualitative classifications and score evolution for the whole game.

#### Deep analysis with spatial filter

`deep_turn_area_analysis()`:
- runs a deep analysis for a given move with spatial filters;
- returns only the best moves and variations;

This is useful for interactive exploration, local analysis and teaching.

#### Output format

All API methods return well-formed JSON strings, directly consumable by a frontend and independent from internal engine objects.

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