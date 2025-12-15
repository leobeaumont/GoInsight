# GoInsight — Design Decisions Summary

## Overall Orientation
- **Built on KataGo**: the project relies on KataGo for all evaluations and variations, which shaped the internal API toward JSON structures compatible with the engine’s `analysis` mode.
- **Analysis / evaluation separation**: responsibilities are split between an analysis layer (collecting KataGo outputs) and an evaluation layer (qualifying moves), making it possible to refine each aspect independently.
- **Unified vocabulary**: terminology from Go (SGF, GTP, winrate) is preserved in code and documentation to avoid ambiguity between the user interface and the implementation.

## Software Architecture
- **Data layer**: the `Game`, `SgfTree`, and `Move` structures encapsulate SGF parsing and board reconstruction, isolating domain logic from format-specific details.
- **Feature layer**: the `analysis` and `evaluation` modules expose clear services (`Analyzer`, `Evaluator`) that can be composed or tested independently while sharing common constants.
- **API entry points**: a dedicated module simplifies programmatic usage and acts as a façade for future integrations (web interface or CLI tools) without exposing internal complexity.
- **Readability principle**: public signatures favor explicit parameters (player color, move number to analyze, GTP selection) to limit side effects and make calls from other languages easier.

## Analysis Workflow
- **Two-level analysis**: a “broad” pass over the entire game to establish context, followed by “deep” analyses per move to zoom in on key decisions, optimizing computation time without sacrificing precision on important sequences.
- **Board area selection**: targeted analysis accepts lists of allowed or forbidden moves; explicit allow/avoid inversion provides fine-grained control to focus on local fights without external noise.
- **Explicit limits**: the number of variations and sequence length are capped to ensure results remain usable for human players and to avoid combinatorial explosion on the engine side.
- **Player perspective**: all metrics are re-centered on the analyzed color, ensuring consistent interpretation of winrate and score regardless of the protagonist.

## User Experience Choices
- **Error typology**: the classes BEST / EXCELLENT / GOOD / INACCURACY / MISTAKE / BLUNDER represent winrate loss thresholds designed to speak to players, distinguishing between minor inaccuracies and major blunders while aligning with pedagogical expectations.
- **Visual highlights**: the notion of an “important square” and the option to ignore a zone are built in from the start to guide attention rather than overwhelm users with variations.
- **Game narrative**: quick access to score lead per move helps contextualize swings and connect KataGo annotations to a simple story (where the game turns, who gains the advantage, when it is lost).

## Configuration and Constants
- **Centralized paths**: model directories, neural network weights, and configuration files are defined in a constants module, avoiding duplication and simplifying KataGo or model version migrations.
- **Documented thresholds**: move classification boundaries are grouped in a single table, making pedagogical calibration easier without diving back into algorithms.
- **Dedicated configurations**: separate files drive fast whole-game analysis and deep per-move analysis, allowing independent tuning of compute budgets depending on use case (full review vs. local study).
- **Cross-platform compatibility**: KataGo binary resolution is OS-dependent to avoid divergent scripts between macOS, Linux, and Windows, reducing user support overhead.

## Reliability and Maintainability
- **Input validation**: systematic checks (valid color, move within game range, prior analysis performed) prevent silent errors and ensure predictable behavior when integrated into other tools.
- **Effect isolation**: the distinction between immutable global analysis and per-move stored local analyses avoids unnecessary recomputation and reduces the risk of result corruption.
- **Transparent workflows**: exchanges with KataGo use readable, sorted JSON, facilitating debugging (line-by-line inspection) and reproducibility of analysis sessions.

## Scalability
- **Mode extensibility**: the current structure allows new modes (e.g., live auto-review or real-time suggestions) to be added by reusing the targeted analysis pipeline and existing constants.
- **Model replacement**: decoupling the binary, configuration, and network weights allows model changes without touching application code, opening the door to specialized versions (handicap, blitz, 9×9).
- **Future integrations**: by keeping APIs simple and formats standard (SGF / GTP / JSON), the project is ready for graphical interfaces, web services, or tournament connectors without major refactoring.

## Deployment and Operations
- **Unified scripts**: the use of `Makefile` and `make.ps1` provides symmetric commands across Unix and Windows for setup, testing, or model optimization, reducing manual steps.
- **Model download**: KataGo weight retrieval is externalized into scripts to keep the repository lightweight and minimize version-related file errors.
- **Optional optimization**: hardware profiling (`opt-model`) is offered but not required, respecting student machine constraints while enabling performance gains on powerful systems.

## Data and Formats
- **SGF fidelity**: SGF parsing preserves rules, komi, and initial stones so that analysis exactly reflects the original game conditions.
- **GTP for selections**: choosing the GTP format to target or exclude moves aligns with KataGo communication and advanced player habits, avoiding an extra conversion layer.
- **Sorting and indexing**: analysis results are sorted by move number so that subsequent calls (statistics, visualizations) can rely on simple indices without reprocessing.

## Quality and Pedagogy
- **Feedback hierarchy**: combining global scores (winrate, score lead) with annotated variations serves both beginners (synthetic indicators) and advanced players (detailed lines).
- **Result predictability**: by consistently reapplying the same configuration for a given analysis, identical sessions produce identical outputs—crucial for pedagogy and published examples.
- **Living documentation**: this summary is designed as an orientation map to quickly onboard new contributors or partners without multiplying technical guides.
