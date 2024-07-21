# Checker Game AI

## Overview

This project is an implementation of an AI for a checker game. The AI is designed to play checkers with various levels of difficulty, utilizing different algorithms and strategies to make moves. The project includes both a command-line interface and potentially a graphical user interface for interacting with the game.

Key features include:

- Multiple game modes
- Configurable board sizes
- Various AI difficulty levels

### To run the program under different modes, please use the following instructions:
k = who runs first
## Running the Program in Manual Mode

python3 main.py {row} {col} {k} m {order} <br>
  e.g. "python3 main.py 7 7 2 m 0" <br>
  
## Running the Program in AI v.s. AI Mode

python3 main.py {row} {col} {k} {AI_path 1} {AI_path 2} <br>
  e.g. "python3 main.py 7 7 2 l {AI_path 1} {AI_path 2}" <br>

## Running the Program in Human v.s. AI Mode

python3 main.py {row} {col} {k} {AI_path} <br>
  e.g. "python3 main.py 7 7 2 n {AI_path}" <br>
