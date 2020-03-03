# CHESS AI

In this project, I implemented the game of Chess from scratch in Python. Everything from input processing to game logic was controlled by the central Chess.py class which encoded the position and type of pieces in a 2D python list (I learned about bitboards after I was already done creating the game logic).

Game.py handled input events use the Python Tkinter GUI library.

ai.py ran the minimax algorithm with alpha beta pruning to create and efficiently prune thousands of decision trees.
