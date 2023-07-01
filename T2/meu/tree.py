import random
import pygame
from pygame.locals import *

PARAMETERS_QTD = 15 
SMALL_CACTUS = 0
LARGE_CACTUS = 1

BIRD = 2


# Decision tree model parameters
parameters = {
    'height_bird': 100,
    'distance_bird': 50,
    'distance_small_cactus': 300,
    'distance_large_cactus': 300,
    'distance_bird_then_small_cactus': 300,
    'distance_bird_then_large_cactus': 300,
    'distance_bird_then_bird': 300,
    'distance_small_cactus_then_bird': 300,
    'distance_small_cactus_then_small_cactus': 300,
    'distance_small_cactus_then_large_cactus': 300,
    'distance_large_cactus_then_large_cactus': 300,
    'distance_large_cactus_then_bird': 300, 
    'distance_large_cactus_then_small_cactus': 300, 
    'height_bird_after_bird': 50,
    'height_bird_after_small_cactus': 50,
    'height_bird_after_large_cactus': 50,
    
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
    max_velocity = 2

    def randomize(self):
        # Soma valores pequenos entre 1 e 10 para cada parâmetro da position, para evitar que a velocidade seja sempre 0
        for i in range(PARAMETERS_QTD):
            self.position[i] = self.position[i] + random.uniform(-10, 10)


    def __init__(self,s = list(parameters.values()) ):
        self.position = s
        self.randomize()
        self.velocity = [0] * PARAMETERS_QTD
        self.best_position = self.position[:]
        self.best_fitness = 0
        self.fitness = 0
from math import floor


def update_position(particle,global_best):
    for i in range(PARAMETERS_QTD):
        print("------------------")
        print(Particle.w*particle.velocity[i])
        print(Particle.c1*random.uniform(0,1)*(abs(particle.best_position[i]- particle.position[i])))
        print(Particle.c2*random.uniform(0,1)*(abs(global_best.position[i] - particle.position[i])))
        print("------------------")
        particle.velocity[i] = floor(Particle.w*particle.velocity[i] + Particle.c1*random.uniform(0,1)*(abs(particle.position[i] - particle.position[i])) + 
                                Particle.c2*random.uniform(0,1)*(abs(particle.best_position[i] - particle.position[i])))
        particle.position[i] += particle.velocity[i]
    # print(particle.velocity)
    # print(particle.position)






def make_decision(state, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
    # Primeira, checa se é um pássaro
    if obType == BIRD:
       if nextObType == BIRD: 
           if distance > state.position[6]: 
                if obHeight > state.position[13]:
                   return 'K_UP'
                else: 
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
                    if obHeight > state.position[14]:
                        return 'K_DOWN'
                    else: 
                        return 'K_UP'
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
        if obType == LARGE_CACTUS:
            if nextObType ==BIRD: 
                if distance > state.position[11]:
                      if obHeight > state.position[15]:
                            return 'K_DOWN'
                      else: 
                            return 'K_UP'
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

