import random
import pygame
from pygame.locals import *
from math import floor

PARAMETERS_QTD = 25

# Obstacles
SMALL_CACTUS = 0
LARGE_CACTUS = 1
BIRD = 2


# # Decision tree model parameters
# parameters = {
#     'height_bird': 100,
#     'distance_bird': 50,
#     'distance_small_cactus': 300,
#     'distance_large_cactus': 250,
#     'distance_bird_then_small_cactus': 300,
#     'distance_bird_then_large_cactus': 250,
#     'distance_bird_then_bird': 300,
#     'distance_small_cactus_then_bird': 300,
#     'distance_small_cactus_then_small_cactus': 300,
#     'distance_small_cactus_then_large_cactus': 250,
#     'distance_large_cactus_then_large_cactus': 250,
#     'distance_large_cactus_then_bird': 250, 
#     'distance_large_cactus_then_small_cactus': 300, 
#     'height_bird_after_bird': 75,
#     'height_bird_after_small_cactus': 75,
#     'height_bird_after_large_cactus': 75,
    
# }


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


parameters = { 
    'distance_bird_then_small_cactus': 300,
    'distance_bird_then_large_cactus': 250,
    'distance_bird_then_bird': 300,
    'distance_small_cactus_then_bird': 300,
    'distance_small_cactus_then_small_cactus': 300,
    'distance_small_cactus_then_large_cactus': 300,
    'distance_large_cactus_then_large_cactus': 300,
    'distance_large_cactus_then_bird': 300,
    'distance_large_cactus_then_small_cactus': 300,
    'height_bird_after_bird': 75,
    'height_bird_after_small_cactus': 75,
    'height_bird_after_large_cactus': 75,
    'distance_bird_then_small_cactus_v2': 300,
    'distance_bird_then_large_cactus_v2': 250,
    'distance_bird_then_bird_v2': 300,
    'distance_small_cactus_then_bird_v2': 300,
    'distance_small_cactus_then_small_cactus_v2': 300,
    'distance_small_cactus_then_large_cactus_v2': 300,
    'distance_large_cactus_then_large_cactus_v2': 300,
    'distance_large_cactus_then_bird_v2': 300,
    'distance_large_cactus_then_small_cactus_v2': 300,
    'height_bird_after_bird_v2': 75,
    'height_bird_after_small_cactus_v2': 75,
    'height_bird_after_large_cactus_v2': 75,
    'distance_change':500
}

# {
#   'distance_bird_then_small_cactus': 0,
#   'distance_bird_then_large_cactus': 1,
#   'distance_bird_then_bird': 2,
#   'distance_small_cactus_then_bird': 3,
#   'distance_small_cactus_then_small_cactus': 4,
#   'distance_small_cactus_then_large_cactus': 5,
#   'distance_large_cactus_then_large_cactus': 6,
#   'distance_large_cactus_then_bird': 7,
#   'distance_large_cactus_then_small_cactus': 8,
#   'height_bird_after_bird': 9,
#   'height_bird_after_small_cactus': 10,
#   'height_bird_after_large_cactus': 11,
    # 'distance_bird_then_small_cactus_v2': 12,
    # 'distance_bird_then_large_cactus_v2': 13,
    # 'distance_bird_then_bird_v2': 14,
    # 'distance_small_cactus_then_bird_v2': 15,
    # 'distance_small_cactus_then_small_cactus_v2': 16,
    # 'distance_small_cactus_then_large_cactus_v2': 17,
    # 'distance_large_cactus_then_large_cactus_v2': 18,
    # 'distance_large_cactus_then_bird_v2': 19,
    # 'distance_large_cactus_then_small_cactus_v2': 20,
    # 'height_bird_after_bird_v2': 21,
    # 'height_bird_after_small_cactus_v2': 22,
    # 'height_bird_after_large_cactus_v2': 23,
    # 'distance_change':24
# }









class Particle:
    # PSO parameters
    swarm_size = 20
    max_iterations = 100
    c1 = 2.05  # Cognitive component weight
    c2 = 2.15  # Social component weight
    w = 0.5 # Inertia weight
    # max_velocity = 2

    def randomize(self, position):
        # Soma valores pequenos entre 1 e 10 para cada parâmetro da position, para evitar que a velocidade seja sempre 0
        for i in range(PARAMETERS_QTD):
            # variate 25 % +- of the parameter
            position[i] = position[i] + random.randint(-int(position[i] * 0.25), int(position[i] * 0.25))
            
            
        return position
    def __init__(self,seed= None, state = None ):
        self.distance_travelled = 0
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

    def setDistance_travelled(self, distance_travelled):
        self.distance_travelled = distance_travelled


    def update_position(self,global_best):
        for i in range(PARAMETERS_QTD):
    
            self.velocity[i] = self.w * self.velocity[i] + self.c1 * random.random() * (self.best_position[i] - self.position[i]) + self.c2 * random.random() * (global_best[i] - self.position[i])
            
            self.position[i] += self.velocity[i]



    # Árvore de decisão
    def make_decision(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
        if distance < self.position[24]:
            # Primeira, checa se é um pássaro
            if obType == BIRD:
                if nextObType == BIRD: 
                        if distance > self.position[2]: 
                            return 'K_DOWN'
                        else:
                            if obHeight > self.position[9]:
                                    return 'K_DOWN'
                            else: 
                                    return 'K_UP'
                else:
                        if nextObType == SMALL_CACTUS:
                            if distance > self.position[0]: 
                                return 'K_DOWN'
                            else:
                                return 'K_UP'
                        else:
                            if distance > self.position[1]: 
                                return 'K_DOWN'
                            else:
                                return 'K_UP'
            else: 
                    # Checa se é um cacto pequeno
                    if obType == SMALL_CACTUS:
                        if nextObType ==BIRD: 
                            if distance > self.position[3]:
                                return 'K_DOWN'
                            else: 
                                if obHeight > self.position[10]:
                                    return 'K_DOWN'
                                else: 
                                    return 'K_UP'
                        else:
                            if nextObType == SMALL_CACTUS:
                                if distance > self.position[4]: 
                                    return 'K_DOWN'
                                else:
                                    return 'K_UP'
                            else:
                                if nextObType == LARGE_CACTUS:
                                    if distance > self.position[5]: 
                                        return 'K_DOWN'
                                    else:
                                        return 'K_UP'
                    else: 
                        if nextObType ==BIRD: 
                            if distance > self.position[7]:
                                return 'K_DOWN'
                            else: 
                                if obHeight > self.position[11]:
                                    return 'K_DOWN'
                                else: 
                                    return 'K_UP'
                        else:
                            if nextObType == LARGE_CACTUS:
                                if distance > self.position[6]: 
                                    return 'K_DOWN'
                                else:
                                    return 'K_UP'
                            else:
                                if nextObType == SMALL_CACTUS:
                                    if distance > self.position[8]: 
                                        return 'K_DOWN'
                                    else:
                                        return 'K_UP'
                                    
        else:
            if obType == BIRD:
                if nextObType == BIRD: 
                        if distance > self.position[14]: 
                            return 'K_DOWN'
                        else:
                            if obHeight > self.position[21]:
                                    return 'K_DOWN'
                            else: 
                                    return 'K_UP'
                else:
                        if nextObType == SMALL_CACTUS:
                            if distance > self.position[12]: 
                                return 'K_DOWN'
                            else:
                                return 'K_UP'
                        else:
                            if distance > self.position[13]: 
                                return 'K_DOWN'
                            else:
                                return 'K_UP'
            else: 
                # Checa se é um cacto pequeno
                if obType == SMALL_CACTUS:
                    if nextObType ==BIRD: 
                        if distance > self.position[15]:
                            return 'K_DOWN'
                        else: 
                            if obHeight > self.position[22]:
                                return 'K_DOWN'
                            else: 
                                return 'K_UP'
                    else:
                        if nextObType == SMALL_CACTUS:
                            if distance > self.position[16]: 
                                return 'K_DOWN'
                            else:
                                return 'K_UP'
                        else:
                            if nextObType == LARGE_CACTUS:
                                if distance > self.position[17]: 
                                    return 'K_DOWN'
                                else:
                                    return 'K_UP'
                else: 
                    if nextObType ==BIRD: 
                        if distance > self.position[19]:
                            return 'K_DOWN'
                        else: 
                            if obHeight > self.position[23]:
                                return 'K_DOWN'
                            else: 
                                return 'K_UP'
                    else:
                        if nextObType == LARGE_CACTUS:
                            if distance > self.position[18]: 
                                return 'K_DOWN'
                            else:
                                return 'K_UP'
                        else:
                            if nextObType == SMALL_CACTUS:
                                if distance > self.position[20]: 
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

        decision = self.parameters.make_decision(distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType)
        return decision
        

    def updateState(self, state):
        self.state = state





