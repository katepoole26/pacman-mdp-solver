# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random

""" 
AIN Pacman Coursework
Katherine Poole 
1/12/2023
k23074532

I'm sorry my pacman doesn't win a lot consistently. I think he's at least having fun eating food and making ghost friends. 
I am a newer python programmer and I spent a lot of time on this coursework -- I tried my best :)  
Learned a lot while doing it though!
"""

# Set reward values and constants
food_reward = 12 #20 
capsule_reward = 25 
empty_coordinate_reward = 0 
bellman_constant = -1 
ghost_reward = -25 #-60 
scared_ghost_reward = 25 #40 
ghosts_radius_award = -15 #-20 
ghosts_radius_scared_award = 8#20
wall_value = '$'
pacman_value = 0
# discount factor for Bellmans equation 
gamma = 0.9
# error tolerance delta - used for convergence in value iteration 
error_tol = .001


## Build Markovian agent
class MDPAgent(Agent):
    
    """ 
    This is an MDP Agent that uses value iteration and Bellman's equation to calculate the highest utility path for 
    Pacman to navigate the grid environment. Pacman is designed to eat food and capsules while avoiding ghosts. This 
    allows him to solve the grid and win games (sometimes:()
    """

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        name = 'Pacman'

        # initialize previous move to track pacmans movement to break oscillations 
        self.previous_move = None


    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)
        
        # Test printing for 
        print "Corner locations:"
        print api.corners(state)
        print "Wall Locations:"
        print api.walls(state)
          
    
    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"


    # Function to populate coordinate 'map' array with appropriate reward values (MEDIUM CLASSIC)
    def get_value_map(self, state, food, capsules, ghosts, walls):

        # Grab needed coordinates from api
        food = api.food(state)
        capsules = api.capsules(state)
        walls = api.walls(state)
        corners = api.corners(state)
        width = corners[1][0] +1  # grab second coordinate pair, X value for width  # +1 accounts for starting at 0
        height = corners[2][1] +1 # grab third coordinate pair, Y value for height
        pacman = api.whereAmI(state)
        ghosts = api.ghosts(state)
        ghost_state = api.ghostStates(state)
        ghost_state_time = api.ghostStatesWithTimes(state)  # scared for 30 seconds 

        # Create empty value map dictionary to store value map
        value_map = dict()
        
        # add food values to map 
        for f in food: 
            value_map[f] = food_reward  # change food locations to the food reward
        # add capsule values to value map 
        for c in capsules:
            value_map[c] = capsule_reward
        # add ghost rewards to value map 
        for g in ghosts:
            value_map[g] = ghost_reward
        # check if ghosts are scared    
        for state, time in zip(ghost_state, ghost_state_time):
            if time[1] >= 7 and state[1] == 1:      # scared time grtr than 7 seconds left, ghost is scared [1]
                value_map[state[0]] = scared_ghost_reward
        # add walls to value map 
        for w in walls:
            value_map[w] = wall_value
        # mark pacman's current location
        if pacman in value_map:
                value_map[pacman] = pacman_value

        # set all x, y coordinates not represented in the dictionary by values to 0 for utility updating
        for x in range(width):
            for y in range(height):
                if (x,y) not in value_map.keys():
                    value_map[(x,y)] = 0

        # seek to bottom left corner first to prevent oscillation down there, then update reward to negative value to keep pacman away 
        if value_map[(1,1)] == food_reward:
            value_map.update({(1,1): 100})
        else: 
            value_map.update({(1,1): -50})

        return value_map
    

    # Function to populate coordinate 'map' array with appropriate reward values (MEDIUM CLASSIC)
    def get_value_map_small(self, state, food, capsules, ghosts, walls):

        # Grab needed coordinates from api
        food = api.food(state)
        capsules = api.capsules(state)
        walls = api.walls(state)
        corners = api.corners(state)
        width = corners[1][0] +1  # grab second coordinate pair, X value for width  # +1 accounts for starting at 0
        height = corners[2][1] +1 # grab third coordinate pair, Y value for height
        pacman = api.whereAmI(state)
        ghosts = api.ghosts(state)
        ghost_state = api.ghostStates(state)
        ghost_state_time = api.ghostStatesWithTimes(state)  # scared for 30 seconds 
        
        # Create empty value map dictionary to store value map
        value_map = dict()
        
        # add food values to map 
        for f in food: 
            value_map[f] = food_reward  # change food locations to the food reward
        # add capsule values to value map 
        for c in capsules:
            value_map[c] = capsule_reward
        # add ghost rewards to value map 
        for g in ghosts: #ghosts:
            if g not in walls:
                value_map[g] = ghost_reward
        # check if ghosts are scared    
        for state, time in zip(ghost_state, ghost_state_time):
            if time[1] >= 7 and state[1] == 1:      # scared time grtr than 7 seconds left, ghost is scared [1]
                value_map[state[0]] = scared_ghost_reward
        # add walls to value map 
        for w in walls:
            value_map[w] = wall_value
        # mark pacman's current location
        if pacman in value_map:
                value_map[pacman] = pacman_value

        # set all x, y coordinates not represented in the dictionary by values to 0 for utility updating
        for x in range(width):
            for y in range(height):
                if (x,y) not in value_map.keys():
                    value_map[(x,y)] = 0

        return value_map


    # Calculate transition utilities for moving from a current state to possible NSEW states
    def get_max_utility(self, value_map, pacman_current):
    
        # dict to store possible NSEW moves
        adjacent_coordinates = {
            "north": (pacman_current[0], pacman_current[1] + 1),
            "south": (pacman_current[0], pacman_current[1] - 1),
            "east": (pacman_current[0] + 1, pacman_current[1]),
            "west": (pacman_current[0] - 1, pacman_current[1])
        }
        # list to store possible utilities from a coordinate
        utilities = []
        
        # Utility calculations for Bellman's equation:   
        # Check that N, E, W are not walls. If not walls, use the true reward values for their relative coordinate. 
        # If they are walls, then adjust reward values to be the value of the current coordinate
        # Sum up all probability*reward values

        # for NSEW, coordinates in directions dictionary
        for direction, coord in adjacent_coordinates.items():
            util = 0.0   # set all utilities to 0 to start

            # start with forward facing direction, valid move no wall 
            if value_map[coord] != wall_value:
                util += (0.8 * value_map[coord])    # stochastic environment means 80% change of intended direction move
            else:   
                # take current coordinate utility if there is a wall 
                util += (0.8 * value_map[pacman_current])

            # Utilities of remaining perpendicular directions
            for adj_direction, adj_coord in adjacent_coordinates.items():
                if adj_direction != direction:
                    if value_map[adj_coord] != wall_value:
                        util += (0.1 * value_map[adj_coord]) # 10% chance perpendicular to intended move 
                    else:
                        util += (0.1 * value_map[pacman_current])

            # add calculated utilities to
            utilities.append(util)

        return max(utilities)
    

    # Implement value iteration to constantly update the map. Medium version has ghost radius
    """ Value iteration logic and code references https://towardsdatascience.com/implement-value-iteration-in-python-a-minimal-working-example-f638907f3437 """
    def value_iteration(self, state, value_map):

        # define variables
        ghosts = api.ghosts(state)
        food = api.food(state)
        capsule = api.capsules(state)
        walls = api.walls(state)
        corners = api.corners(state)
        width = corners[1][0] +1  # grab second coordinate pair, X value for width  # +1 accounts for starting at 0
        height = corners[2][1] +1 # grab third coordinate pair, Y value for height

        # Initialize value map
        value_map = self.get_value_map(state, food, ghosts, capsule, walls)

        while True: # iterate until convergence 
            
            map_copy = value_map.copy() # create copy of map prior to iterating for value comparison
            delta = 0

            for x in range(width):
                for y in range(height):
                    # only calculate iterative utilities where there is no game reward
                    if (x,y) not in walls and (x,y) not in food and (x,y) not in capsule and (x,y) not in ghosts and (x,y) != (1,1):   

                        # Calculate updated coordinate value using max utility method in Bellman's equation
                        """ Bellman = constant reward r + discount gamma * max utility of available states """
                        new_value = bellman_constant + (gamma * self.get_max_utility(map_copy, (x,y)))
                        map_copy[(x,y)] = new_value

                        # store difference in old and new utility calculations to use for convergence break
                        delta = max(delta, abs(value_map[(x,y)] - map_copy[(x,y)]))

            # break if difference in utilities converges with error tolerance delta 
            if delta < error_tol:
                break

            return map_copy
        

    # Implement value iteration to constantly update the map. Small version has no ghost radius -- too small
    """ Value iteration logic and code references https://towardsdatascience.com/implement-value-iteration-in-python-a-minimal-working-example-f638907f3437 """
    def value_iteration_small(self, state, value_map):

        # define variables
        ghosts = api.ghosts(state)
        food = api.food(state)
        capsule = api.capsules(state)
        walls = api.walls(state)
        corners = api.corners(state)
        width = corners[1][0] +1  # grab second coordinate pair, X value for width  # +1 accounts for starting at 0
        height = corners[2][1] +1 # grab third coordinate pair, Y value for height

        # Initialize value map
        value_map = self.get_value_map_small(state, food, ghosts, capsule, walls)

        while True: # iterate until convergence 
            
            map_copy = value_map.copy() # create copy of map prior to iterating for value comparison
            delta = 0

            for x in range(width):
                for y in range(height):
                    # only calculate iterative utilities where there is no game reward
                    if (x,y) not in walls and (x,y) not in food and (x,y) not in capsule and (x,y) not in ghosts:   

                        # Calculate updated coordinate value using max utility method in Bellman's equation
                        """ Bellman = constant reward r + discount gamma * max utility of available states """
                        new_value = bellman_constant + (gamma * self.get_max_utility(map_copy, (x,y)))
                        map_copy[(x,y)] = new_value

                        # store difference in old and new utility calculations to use for convergence break
                        delta = max(delta, abs(value_map[(x,y)] - map_copy[(x,y)]))

            # break if difference in utilities converges with error tolerance delta 
            if delta < error_tol:
                break

            return map_copy


    # Build policy selection function to pass the optimal action to getAction function below 
    def get_policy(self, state, value_map_iterated, pacman_current):
        
        # Location pacman 
        pacman_current = api.whereAmI(state)

        # get values for adjacent cells from pacman, store in dictionary 
        adjacent_dict = {}
        # north
        move_n = (pacman_current[0], pacman_current[1] + 1)
        # south 
        move_s = (pacman_current[0], pacman_current[1] - 1)
        # east
        move_e = (pacman_current[0] + 1, pacman_current[1])
        # west
        move_w = (pacman_current[0] - 1, pacman_current[1])

        # add keys to dictionary with appropriate values
        adjacent_dict[move_n] = value_map_iterated[move_n]
        adjacent_dict[move_s] = value_map_iterated[move_s]
        adjacent_dict[move_e] = value_map_iterated[move_e]
        adjacent_dict[move_w] = value_map_iterated[move_w]

        # filter dictionary to retain only numeric values e.g. get rid of walls that threw off max
        numeric_values = {k: v for k, v in adjacent_dict.items() if isinstance(v, (int, float))}
        # lambda method to return highest numeric only value from move dictionary referenced from chatGPT

        # Return the best policy based on adjacent utilities (NUMERIC ONLY) to use in getAction method
        if max(numeric_values, key = lambda k: numeric_values[k]) == move_n:    
            # lambda method to return highest numeric only value from move dictionary referenced from chatGPT
            return Directions.NORTH
        if max(numeric_values, key = lambda k: numeric_values[k]) == move_s:
            return Directions.SOUTH
        if max(numeric_values, key = lambda k: numeric_values[k]) == move_e:
            return Directions.EAST
        if max(numeric_values, key = lambda k: numeric_values[k]) == move_w:
            return Directions.WEST


    def getAction(self, state):
        
        # Initiate needed locations
        food = api.food(state)
        ghosts = api.ghosts(state)
        capsule = api.capsules(state)
        walls = api.walls(state)
        corners = api.corners(state)
        width = corners[1][0] +1  # grab second coordinate pair, X value for width  # +1 accounts for starting at 0
        height = corners[2][1] +1 # grab third coordinate pair, Y value for height
        legal = api.legalActions(state)
        pacman_current = api.whereAmI(state)

        # value iteration & policy selection - medium map
        if width >= 12:
            # Grabs a new value map dictionary after every action pacman makes 
            value_map = self.get_value_map(state, food, ghosts, capsule, walls)
            iterated_map = self.value_iteration(state, value_map)

        else: 
            value_map = self.get_value_map_small(state, food, ghosts, capsule, walls)
            iterated_map = self.value_iteration_small(state, value_map)
        
        # use get policy method to select best policy, pass to the makeMove method
        policy = self.get_policy(state, iterated_map, pacman_current)

        # Prevent Pacman from repeating its previous move
        if policy == Directions.NORTH and self.previous_move == Directions.SOUTH:
            policy = random.choice([Directions.EAST, Directions.WEST])
        elif policy == Directions.SOUTH and self.previous_move == Directions.NORTH:
            policy = random.choice([Directions.EAST, Directions.WEST])
        elif policy == Directions.EAST and self.previous_move == Directions.WEST:
            policy = random.choice([Directions.NORTH, Directions.SOUTH])
        elif policy == Directions.WEST and self.previous_move == Directions.EAST:
            policy = random.choice([Directions.NORTH, Directions.SOUTH])

        self.previous_move = policy  # Update the previous move

        return api.makeMove(policy, legal)

