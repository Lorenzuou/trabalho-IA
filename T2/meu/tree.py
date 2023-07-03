import random
import pygame
from pygame.locals import *
from math import floor

PARAMETERS_QTD = 16
SMALL_CACTUS = 0
LARGE_CACTUS = 1

BIRD = 2


# Decision tree model parameters
parameters = {
    'height_bird': 100,
    'distance_bird': 50,
    'distance_small_cactus': 300,
    'distance_large_cactus': 250,
    'distance_bird_then_small_cactus': 300,
    'distance_bird_then_large_cactus': 250,
    'distance_bird_then_bird': 300,
    'distance_small_cactus_then_bird': 300,
    'distance_small_cactus_then_small_cactus': 300,
    'distance_small_cactus_then_large_cactus': 250,
    'distance_large_cactus_then_large_cactus': 250,
    'distance_large_cactus_then_bird': 250, 
    'distance_large_cactus_then_small_cactus': 300, 
    'height_bird_after_bird': 75,
    'height_bird_after_small_cactus': 75,
    'height_bird_after_large_cactus': 75,
    
}

# {
#     'height_bird': 0,
#     'distance_bird': 1,
#     'distance_small_cactus': 2,
#     'distance_large_cactus': 3,
#     'distance_bird_then_small_cactus': 4,
#     'distance_bird_then_large_cactus': 5,
#     'distance_bird_then_bird': 6,
#     'distance_small_cactus_then_bird': 7,
#     'distance_small_cactus_then_small_cactus': 8,
#     'distance_small_cactus_then_large_cactus': 9,
#     'distance_large_cactus_then_large_cactus': 10,
#     'distance_large_cactus_then_bird': 11,
#     'distance_large_cactus_then_small_cactus': 12
#     'height_bird_after_bird': 13,
#     'height_bird_after_small_cactus': 14,
#     'height_bird_after_large_cactus': 15,
# }



class Particle:
    # PSO parameters
    swarm_size = 20
    max_iterations = 100
    c1 = 2.05  # Cognitive component weight
    c2 = 2.05  # Social component weight
    w = 0.5  # Inertia weight
    # max_velocity = 2

    def randomize(self, position):
        # Soma valores pequenos entre 1 e 10 para cada parâmetro da position, para evitar que a velocidade seja sempre 0
        for i in range(PARAMETERS_QTD):
            position[i] = position[i] + random.uniform(-50, 50)
        return position
    def __init__(self,seed= None, state = None ):
        if seed:
            random.seed(seed)
        if state: 
            self.position = state
        else: 
            s = list(parameters.values())
            self.position = self.randomize(s)
        
       
        self.velocity = [0] * PARAMETERS_QTD
        self.best_position = self.position[:]
        self.best_fitness = 0
        self.fitness = 0


    def update_position(self,global_best):
        for i in range(PARAMETERS_QTD):
    
            self.velocity[i] = self.w * self.velocity[i] + self.c1 * random.random() * (self.best_position[i] - self.position[i]) + self.c2 * random.random() * (global_best[i] - self.position[i])
            
            self.position[i] += self.velocity[i]

        # print(global_best == particle.best_position)



# Árvore de decisão
def make_decision(state, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
    # Primeira, checa se é um pássaro
    if obType == BIRD:
       if nextObType == BIRD: 
            if distance > state.position[6]: 
                return 'K_DOWN'
            else:
                if obHeight > state.position[13]:
                        return 'K_DOWN'
                else: 
                        return 'K_UP'
       else:
              if nextObType == SMALL_CACTUS:
                if distance > state.position[4]: 
                     return 'K_DOWN'
                else:
                     return 'K_UP'
              else:
                if nextObType == LARGE_CACTUS:
                     if distance > state.position[5]: 
                          return 'K_DOWN'
                     else:
                          return 'K_UP'
    else: 
        # Checa se é um cacto pequeno
        if obType == SMALL_CACTUS:
            if nextObType ==BIRD: 
                if distance > state.position[7]:
                    return 'K_DOWN'
                else: 
                    if obHeight > state.position[14]:
                        return 'K_DOWN'
                    else: 
                        return 'K_UP'
            else:
                if nextObType == SMALL_CACTUS:
                    if distance > state.position[8]: 
                        return 'K_DOWN'
                    else:
                        return 'K_UP'
                else:
                    if nextObType == LARGE_CACTUS:
                        if distance > state.position[9]: 
                            return 'K_DOWN'
                        else:
                            return 'K_UP'
        else: 
            if nextObType ==BIRD: 
                if distance > state.position[11]:
                    return 'K_DOWN'
                else: 
                    if obHeight > state.position[15]:
                        return 'K_DOWN'
                    else: 
                        return 'K_UP'
            else:
                if nextObType == LARGE_CACTUS:
                    if distance > state.position[10]: 
                        return 'K_DOWN'
                    else:
                        return 'K_UP'
                else:
                    if nextObType == SMALL_CACTUS:
                        if distance > state.position[12]: 
                            return 'K_DOWN'
                        else:
                            return 'K_UP'
                        
    

class KeyTreeClassifier:
    def __init__(self, parameters):
        if isinstance(parameters, list):
            self.parameters = Particle(state=parameters)
        else: 

            self.parameters = parameters

        

    def keySelector(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):

        decision = make_decision(self.parameters, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType)
        return decision
        

    def updateState(self, state):
        self.state = state

