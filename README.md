# Pacman MDP Agent Solver
Markovian Decision Process Solver Agent for classic Pacman game shows the implementation of an AI agent capable of winning the arcade game of Pac-Man using an MDP solver that follows a policy based on Value Iteration.

The game itself is also modelled as a stochastic variation of the Pac-Man game, meaning that some transitions are probabilistic. In the context of the Pac-Man game, the agent has an 80% probability of going in the direction specified by the policy, and a 10% change of going to either direction perpendicular to that. If the agent hits a wall, it will not move.

The sole file here is meant to be used with [Berkley's Pac-Man Projects](http://ai.berkeley.edu/project_overview.html). It therefore only contains the logic associated with a MDP agent trying to win the Pac-Man game.
