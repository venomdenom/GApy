# Genetic algorithm implementation
A simple genetic algorithm implementation based on handwritten game.

## About
Recently, I visited Digital Maraphon finals from Sber. The final task was to write an algorithm that solves Game 21. Here, I made a poor copy of it and tried to solve it with genetic algorithm method.

## How to use
1. Clone the repo
```sh
git clone https://github.com/venomdenom/GApy.git
```
2. Run
```sh
pip install -r requirements.txt
cd src
```
3. If you want to play the game:
    * Edit assets/level.txt, where 0 - simple path, 1 - wall, 2 - acid, $ - starting position, # - finish
    * Open game.py and add 
```python 
Robot_game().init_game()
```
    * Run 
```sh 
python3.12 game.py
```

4. Otherwise run 
```sh 
python3.12 model.py
```
