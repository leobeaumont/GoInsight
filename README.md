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

The SgfTree object is a complete and structured representation of an SGF (Smart Game Format) file, a standard format used to describe games of board games like Go. It serves as a central interface for reading, manipulating, comparing, converting, and writing SGF games, while preserving the tree structure inherent to this format.

#### Internal Representation of an SGF Game

An SgfTree represents a node of the SGF tree.
Each node contains:

- a dictionary of SGF properties, where each key is an SGF identifier (e.g., B, W, SZ, etc.) associated with a list of values,

- a list of child nodes, allowing the representation of game variants.

This structure allows for the accurate modeling of:

- the main line of a game,

- variants and sub-variants,

- the exact order of moves and metadata.

#### Creating an SGF Tree
An SGF tree can be created in several ways:

- From an SGF file
The `from_sgf(path)` method reads an SGF file from disk, checks for its existence, and then parses it to construct the corresponding tree.

- From a Game object
The `from_game(game)` method converts a Game object (internal engine logic) into an SGF tree, thus ensuring complete interoperability between the game's logical representation and the SGF format.

- By directly parsing an SGF string
The `parse(input)` function transforms a raw SGF string into an SGF tree, rigorously validating the syntax (parentheses, properties, capitalization, delimiters, etc.).

#### Conversion to Other Formats
The SgfTree acts as a bridge between different formats:

- To a Game object
The `to_game()` method reconstructs a Game object from the SGF tree, allowing you to then simulate, analyze, or modify the game.

- To an SGF string or file
The `to_sgf(path=None)` method serializes the tree into a valid SGF string.

If a path is provided, the SGF is also written to a file.

The serialization adheres to SGF rules:

- escaping of special characters,

- correct handling of variants,

- generation of a syntactically valid SGF.

#### Accessing the Move Sequence
The `move_sequence()` method extracts the sequence of moves played, in order, from the tree:

- Moves are converted from SGF format to GTP format,

- The board size is automatically detected if necessary,

- Moves can be returned either as strings ("B A19") or as tuples ("B", "A19").

This method is particularly useful for:

- Replaying a game,

- Interfacing with a Go engine,

- Analyzing or displaying a game move by move.

#### Managing the Board Size
The `get_board_size()` method extracts the board size from the `SZ` property of the root node:

- It supports square and rectangular formats,

- It validates sizes against a maximum constant,

- It guarantees that the returned size is consistent and usable.

#### Robust SGF Parsing
The module includes a complete SGF parser that:

- validates tree structure,

- prohibits lowercase properties,

- correctly handles escaped characters,

- detects syntax errors (empty trees, incorrect delimiters, invalid format).

This ensures that any SgfTree created from an SGF is structurally valid.

### Move Class
The Move object represents an individual move in a game of Go. It encapsulates all the information necessary to describe, interpret, validate, and convert a move between different standard formats (internal, SGF, and GTP).

General Role

#### A Move links:

- a game,

- a color (black or white),

- a position on the board or a pass,

- a turn number in the game.

It thus constitutes the basic unit for replaying, exporting, or analyzing a game.

#### Creating and Validating a Move

During instantiation:

- The color can be explicitly provided (B/W), otherwise it is automatically deduced from the game state,

- The position is validated using the game board,

- A move without a position corresponds to a pass.
Any attempt to play on an invalid position results in an error, ensuring the game's consistency.

#### Conversion Between Coordinate Formats

The Move class provides several essential conversion methods:

- SGF -> Internal Coordinates

sgf_to_coord() translates an SGF position ("dd") into coordinates (x, y) usable by the engine.

- SGF -> GTP
sgf_to_gtp() converts an SGF coordinate into GTP notation (A19, Q4, etc.), taking into account the board size and the specific case of a pass.

- GTP -> Move
`from_gtp()` allows you to directly create a Move object from a standard GTP instruction ("w A19"), validating the syntax and coordinates.

These conversions ensure interoperability with:

- Go engines,

- Graphical interfaces,

- SGF files.

#### Exporting a Move
A move can be exported in different formats:

- To GTP
`to_gtp()` returns a valid GTP command representing the move.

- To SGF
`to_sgf()` generates the corresponding SGF property (`{"B": ["dd"]}`), which can be directly used in an SGF tree.

### Board Class
The Board object represents the state of the Go board at a given moment, constructed from a sequence of moves. It is responsible for all the spatial logic: stone placement, groups, liberties, and captures.

#### General Role
A Board:

- maintains a matrix representation of the board,

- applies the fundamental rules of Go (liberties, captures),

- allows local and global operations on the game state.

It forms the basis of the game logic.
#### Board Initialization
Upon creation:

- the board is sized (19×19 by default),

- the move list is used to reconstruct the game state,

- each move is played in order with automatic updating of the captures.

Any inconsistency in the move sequence is detected immediately.

#### Position Validation
The `is_valid_pos()` method checks:

- that the position is within the board boundaries,

- that it is not already occupied.

It is used both to play and to remove moves, guaranteeing the integrity of the board.

#### Move Manipulation
The board can be modified dynamically:

- Adding a move
`add_move()` places a stone and triggers capture detection.

- Removing a move
`remove_move()` removes a stone, either by direct reference or by coordinates.

These operations allow, for example:

- going back,

- editing a game,

- analyzing intermediate positions.

#### Local Board Analysis

The board provides essential analysis tools:

- Orthogonal Neighborhood
`_neighbors()` returns adjacent intersections according to Go connectivity.

- Groups and Freedoms
`group_and_liberties()` identifies:

- a group of connected stones,

- the set of its freedoms.

This method is at the heart of the capture logic.

#### Capture Management
The update_board() method:

- examines the groups affected by a move,

- detects those that have run out of liberties,

- automatically removes captured stones.

This implementation is intentionally agnostic to advanced rules (KO, suicide forbidden, etc.), making it robust and easily extensible.

#### Area Selection
The area_selection_positions() method extracts all intersections of a rectangular area of ​​the board, using GTP notation.

It is particularly useful for:

- local analysis,

- integration with engines,

- visualization or statistical tools.

### Analyzer Class
The Analyzer object is responsible for the automatic analysis of a Go game using the KataGo engine.

It forms the central layer connecting:

- the internal game representation (Game, SgfTree),

- the external AI engine,

- the data required for the user interface.

#### General Role
An Analyzer allows you to:

- analyze the entire game move by move (global analysis),

- perform an in-depth analysis of a specific move,

- extract quantitative indicators (win rate, score lead),

- normalize the results from the perspective of a given player (Black or White).

#### Initialization

During its creation:

- the SGF file is loaded and converted into an SgfTree,

- the analyzed player (Black or White) is set,

- the result storage structures are initialized.

Any invalid value for the player is immediately rejected.

#### Overall Game Analysis
The shalow_game_analysis() method:

- automatically selects the KataGo binary based on the operating system,

- reconstructs the game from the SGF tree,

- generates the JSON input expected by KataGo,

- runs an analysis for each turn of the game,

- collects and sorts the results.

The result is stored in game_analysis and contains, for each move:

- win rate,

- score lead,

- current player,

- moves recommended by the AI.

This analysis forms the basis of all other features.

#### In-Depth Move Analysis

The deep_turn_analysis() method allows for in-depth analysis of a specific turn:

- optionally with a spatial restriction (allowed or forbidden zone),

- with a greater search depth,

- by extracting the best possible variations.

The results are stored in `turn_analysis`, indexed by turn number.

#### Extracting Global Indicators
`game_score_lead()` returns the score evolution throughout the game.

The data is ready to be used for graphs or statistics.

#### Basic Data for the Interface
The `turn_basic_data()` method provides the essential information to display for a given turn:

- win rate of the analyzed player,

- Lead score of the analyzed player,

- Best move suggested by KataGo,

- Expected score after this move,

- Player who should play the next move.

All values ​​are normalized from the perspective of the selected player, which greatly simplifies the display.

#### Advanced Data for the Interface
The turn_advanced_data() method returns:

- An ordered list of the best moves,

- Their expected score,

- A truncated main variation.

This data is intended for detailed or interactive display.

### Evaluator Class
The Evaluator object is responsible for assessing the quality of the moves played based on the results provided by the Analyzer.

#### General Role

An Evaluator:
- Transforms numerical data (win rate) into qualitative judgments,

- Provides a human and educational interpretation of the game,

- Applies a standard classification grid.

#### Move Classification
The classify_move() method:

- compares the win rate before and after a move,

- calculates the win rate loss (or gain),

- corrects the sign according to the player who played,

- classifies the move into a category:

BEST
EXCELLENT
GOOD
INACCURACY
MISTAKE
BLUNDER

Classification thresholds are defined in MOVE_CLASSIFICATION_BOUNDS.

#### Entire Game Classification

The classify_game() method applies this logic to all moves in the game and returns a list aligned with the game's turns.
This class therefore allows for the production of:

- automatic annotations,

- performance statistics.

### API Class
The API class constitutes the external interface layer of the project.

It exposes a simple API, designed for consumption through a graphical interface or a web client.

#### General Role
The API:

- orchestrates the Analyzer and Evaluator,

- hides the complexity of GoInsight and its internal structures,

- returns only ready-to-use JSON data.

#### Full Analysis on Load
The all_moves_analysis() method:

- launches the overall analysis of the game,

- classifies all moves,

- groups all data into a single JSON object.

The returned data includes:

- detailed information per turn,

- the qualitative classification of each move,

- the score evolution over the entire game.

This method is designed to be called upon the initial load of an analysis.

#### In-Depth Analysis with Spatial Filtering
The deep_turn_area_analysis() method:

- launches an in-depth analysis of a given move,

- allows limiting or excluding an area of ​​the board,

- returns only the best moves and variations.

This feature is ideal for:

- interactive exploration,

- analyze a specific area of the game,

- local analysis,

- teaching and commenting on games.

#### Output Format
All API methods return:

- well-formatted JSON strings,

- directly usable by a frontend,

- without any dependency on internal engine objects.