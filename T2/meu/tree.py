import random
import pygame
from pygame.locals import *

# Decision tree model parameters
parameters = {
    'height_bird': 100,
    'distance_bird': 50,
    'distance_small_cactus': 300,
    'distance_large_cactus': 300,
}

# PSO parameters
swarm_size = 20
max_iterations = 100
c1 = 2.05  # Cognitive component weight
c2 = 2.05  # Social component weight
w = 0.5  # Inertia weight
max_velocity = 2



class Particle:
    def __init__(self,s = list(parameters.values()) ):
        self.position = s
        self.velocity = [random.uniform(-max_velocity, max_velocity) for _ in range(4)]
        self.best_position = self.position[:]
        self.best_fitness = 0


def update_position(particle,global_best):
    for i in range(4):
        particle.velocity[i] = w * particle.velocity[i] + c1 * random.random() * (particle.best_position[i] - particle.position[i]) + c2 * random.random() * (global_best.position[i] - particle.position[i])
        particle.velocity[i] = max(-max_velocity, min(max_velocity, particle.velocity[i]))
        particle.position[i] += particle.velocity[i]

def make_decision(state, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
    if obType == 2:
        if obHeight > state.position[0]: 
            return 'K_DOWN'
        else:
            if distance > state.position[1]: 
                return 'K_DOWN'
            else:
                return 'K_UP'
    else: 
        if obType == 1:
            if distance > state.position[2]: 
                return 'K_DOWN'
            else:
                return 'K_UP'
        else:
            if obType == 0:
                if distance > state.position[3]: 
                    return 'K_DOWN'
                else:
                    return 'K_UP'
            else:
                return 'K_NO'
    

class KeyTreeClassifier:
    def __init__(self, parameters):
        self.parameters = parameters

        

    def keySelector(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
        # for s, d in self.state:
        #     if speed < s:
        #         limDist = d
        #         break
        # print(self.parameters)


        decision = make_decision(self.parameters, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType)
        return decision
        

    def updateState(self, state):
        self.state = state

