2D Map Generator
================
A simplistic world map generator written in python.


## Background
This project was meant to be a way to generate world maps for 2D top-down games
based on a random seed.


## How it works
1. Generate a random binary matrix.
2. Smooth matrix by blurring neighboring cells and rounding back to binary.
3. Find spawns
	1. Pick 2 random playable cells
	2. Run modified k-means to move spawns into logical areas on map.
	3. If position is outside map area, move to closest cell.
4. Run A* type search to ensure spawns are reachable.
	1. Start at first spawn and search for the other.
	2. Return when other spawn is found.
	3. If spawn not found there must be an 'island' that all searched cells
	   are a part of.
	4. Set new map area to searched cells.
	5. Goto step 3 and find new spawns.
5. Generate visual version of map.
