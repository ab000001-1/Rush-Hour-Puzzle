## Rush Hour Puzzle Solver

## Overview
This project implements a program to solve the "Rush Hour" puzzle, a game played on a 6x6 grid with vehicles (cars and trucks) that move horizontally or vertically. 
The goal is to move the red car (X) to the exit on the right side of the third row from the top. The program reads the initial board configuration from standard input and outputs 
a sequence of moves to achieve the goal.

## Game Description

#### Board: 6x6 grid with vehicles (cars: 2 squares, trucks: 3 squares).

#### Vehicles: 

#### Cars: Red (X), Light Green (A), Orange (B), Blue (C), Pink (D), Purple (E), Green (F), Dark Grey (G), Beige (H), Yellow (I), Brown (J), Dark Green (K).

#### Trucks: Orange (O), Pink (P), Blue (Q), Green (R).

#### Movement: Vehicles move forward or backward in their orientation (H: horizontal, V: vertical).

#### Objective: Move the red car (X) to the exit (right side, row 3).

## Input/Output

#### Input: Standard input with one vehicle per line, each containing:

#### Vehicle ID (e.g., X for red car, A for light green car).

#### Coordinates (x, y) of the vehicle’s top-left square (0,0: top-left; 5,5: bottom-right).

#### Orientation (H: horizontal, V: vertical).

#### Example: A1OH (car A at x=1, y=0, horizontal).


#### Output: Standard output with one move per line, each as a two-letter code:

#### First letter: Vehicle ID.

#### Second letter: Direction (L: left, R: right, U: up, D: down).

#### Example: AL (move car A one space left).



## Implementation
#### The program implements three approaches to find a minimum-depth solution:

#### Brute-Force Breadth-First Search: Explores all possible moves level by level.

#### Best-First Search with Heuristic 1: Uses an admissible heuristic to prioritize moves.

#### Best-First Search with Heuristic 2: Uses a second admissible heuristic, designed to provide higher or equal estimates compared to the first.

## Features

#### Validates input and ensures correct output format.

#### Compares search space exploration (nodes visited) across the three approaches.

#### Includes tables, figures, and graphs to visualize performance.

#### Provides arguments for heuristic admissibility and comparative effectiveness.

## Notes

#### The program avoids references to unrelated elements (e.g., Jackie Chan, Chris Tucker).
#### Focuses on clear presentation, including proper grammar, spelling, and formatting.

