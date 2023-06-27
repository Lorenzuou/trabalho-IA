import random
import pygame
from pygame.locals import *

# Decision tree model parameters
parameters = {
    'distance_threshold': 300,
    'obHeight_threshold': 50,
    'speed_threshold': 10,
    'obType_threshold': 0.5,
    'nextObDistance_threshold': 150,
    'nextObHeight_threshold': 100,
    'nextObType_threshold': 0.5
}

# PSO parameters
swarm_size = 20
max_iterations = 100
c1 = 2.0  # Cognitive component weight
c2 = 2.0  # Social component weight
w = 0.7  # Inertia weight
max_velocity = 2.0

class Particle:
    def __init__(self,s = [300, 50, 10, 150, 100] ):
        self.position = s
        self.velocity = [random.uniform(-max_velocity, max_velocity) for _ in range(5)]
        self.best_position = self.position[:]
        self.best_fitness = 0



def update_position(particle,global_best):
    for i in range(5):
        particle.velocity[i] = w * particle.velocity[i] + \
                               c1 * random.random() * (particle.best_position[i] - particle.position[i]) + \
                               c2 * random.random() * (global_best[i] - particle.position[i])
        particle.velocity[i] = max(-max_velocity, min(max_velocity, particle.velocity[i]))
        particle.position[i] += particle.velocity[i]
        particle.position[i] = max(0, min(1, particle.position[i]))


def make_decision(distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
    if distance > parameters['distance_threshold']:
        if obHeight < parameters['obHeight_threshold']:
            if speed < parameters['speed_threshold']:
                # Checking if it is a bird
                if obType == 2 and obHeight > parameters['nextObHeight_threshold']:
                    return 'K_DOWN'
                else:
                    return 'K_UP'
            else:
                if nextObDistance < parameters['nextObDistance_threshold']:
                    return 'K_UP'
                else:
                    return 'K_DOWN'
        else:
            if nextObHeight < parameters['nextObHeight_threshold']:
                return 'K_DOWN'
            else:
                if nextObType < parameters['nextObType_threshold']:
                    return 'K_DOWN'
                else:
                    return 'K_UP'
    else:
        return 'K_UP'

class KeyTreeClassifier:
    def __init__(self, state):
        self.state = state

        

    def keySelector(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
        # for s, d in self.state:
        #     if speed < s:
        #         limDist = d
        #         break



        decision = make_decision(distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType)
        return decision
        

    def updateState(self, state):
        self.state = state

