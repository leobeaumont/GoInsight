# GoInsight

[![Python v3.12.3](https://img.shields.io/badge/Python-v3.12.3-red)](https://www.python.org/downloads/release/python-3123)
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

## Features

- `Better move highlights`.
- `Blunder and mistake highlights`.
- `Important square highlight` to help the player understand the engine choice.
- `Ignorable area` to be able to study a specific area of the game.

## Installation

This project is coded and tested under python version `3.12.3`. We cannot garantee the code to work on other python versions.

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
# Open environment
source .venv/bin/activate
```
You're all setup !

## Commands

### Documentation
```bash
# This will open code's documentation on your default web browser
make docs
```
### Clean project
```bash
# Remove setup files from the project
make clean
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