import pygame
import os
import random
import time
from sys import exit
from neural import DinoClassifier

pygame.init()

# Valid values: HUMAN_MODE or AI_MODE
GAME_MODE = "HUMAN_MODE"
RENDER_GAME = True

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
if RENDER_GAME:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus4.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 90
    Y_POS = 330
    Y_POS_DUCK = 355
    JUMP_VEL = 17
    JUMP_GRAV = 1.1

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = 0
        self.jump_grav = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck and not self.dino_jump:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 20:
            self.step_index = 0

        if userInput == "K_UP" and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput == "K_DOWN" and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif userInput == "K_DOWN":
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = True
        elif not (self.dino_jump or userInput == "K_DOWN"):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_duck:
            self.jump_grav = self.JUMP_GRAV * 4
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel
            self.jump_vel -= self.jump_grav
        if self.dino_rect.y > self.Y_POS + 10:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.jump_grav = self.JUMP_GRAV
            self.dino_rect.y = self.Y_POS

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def getXY(self):
        return (self.dino_rect.x, self.dino_rect.y)


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle():
    def __init__(self, image, type):
        super().__init__()
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()

        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

    def getXY(self):
        return (self.rect.x, self.rect.y)

    def getHeight(self):
        return y_pos_bg - self.rect.y

    def getType(self):
        return (self.type)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 345


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)

        # High, middle or ground
        if random.randint(0, 3) == 0:
            self.rect.y = 345
        elif random.randint(0, 2) == 0:
            self.rect.y = 260
        else:
            self.rect.y = 300
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 19:
            self.index = 0
        SCREEN.blit(self.image[self.index // 10], self.rect)
        self.index += 1


class KeyClassifier:
    def __init__(self, state):
        pass

    def keySelector(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
        pass

    def updateState(self, state):
        pass


def first(x):
    return x[0]


class KeySimplestClassifier(KeyClassifier):
    def __init__(self, state):
        self.state = state

    def keySelector(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight,nextObType):
        self.state = sorted(self.state, key=first)
        for s, d in self.state:
            if speed < s:
                limDist = d
                break
        if distance <= limDist:
            if isinstance(obType, Bird) and obHeight > 50:
                return "K_DOWN"
            else:
                return "K_UP"
        return "K_NO"

    def updateState(self, state):
        self.state = state


def playerKeySelector():
    userInputArray = pygame.key.get_pressed()

    if userInputArray[pygame.K_UP]:
        return "K_UP"
    elif userInputArray[pygame.K_DOWN]:
        return "K_DOWN"
    else:
        return "K_NO"


def playGame():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    logs = []
    clock = pygame.time.Clock()
    cloud = Cloud()
    font = pygame.font.Font('freesansbold.ttf', 20)

    player = Dinosaur()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 383
    points = 0

    obstacles = []
    death_count = 0
    spawn_dist = 0

    def score():
        global points, game_speed
        points += 0.25
        if points % 100 == 0:
            game_speed += 1

        if RENDER_GAME:
            text = font.render("Points: " + str(int(points)), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SCREEN.blit(text, textRect)


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

        if RENDER_GAME:
            SCREEN.fill((255, 255, 255))

        distance = 1500
        nextObDistance = 2000
        obHeight = 0
        nextObHeight = 0
        obType = 2
        nextObType = 2
        if len(obstacles) != 0:
            xy = obstacles[0].getXY()
            distance = xy[0]
            obHeight = obstacles[0].getHeight()
            obType = obstacles[0]

        if len(obstacles) == 2:
            nextxy = obstacles[1].getXY()
            nextObDistance = nextxy[0]
            nextObHeight = obstacles[1].getHeight()
            nextObType = obstacles[1]

        if GAME_MODE == "HUMAN_MODE":
            userInput = playerKeySelector()
            # FAZ LOG, PARA CRIAR DATASET
            if userInput != "K_NO":
                logs.append((userInput, distance, obHeight, game_speed, obType, nextObDistance, nextObHeight, nextObType))
            

        else:
            userInput = aiPlayer.keySelector(distance, obHeight, game_speed, obType, nextObDistance, nextObHeight,
                                             nextObType)
        

        if len(obstacles) == 0 or obstacles[-1].getXY()[0] < spawn_dist:
            spawn_dist = random.randint(0, 670)
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 5) == 5:
                obstacles.append(Bird(BIRD))

        player.update(userInput)

        if RENDER_GAME:
            player.draw(SCREEN)

        for obstacle in list(obstacles):
            obstacle.update()
            if RENDER_GAME:
                obstacle.draw(SCREEN)


        if RENDER_GAME:
            background()
            cloud.draw(SCREEN)

        cloud.update()

        score()

        if RENDER_GAME:
            clock.tick(60)
            pygame.display.update()

        for obstacle in obstacles:
            if player.dino_rect.colliderect(obstacle.rect):
                if RENDER_GAME:
                    #write logs to file, append
                    with open('logs.csv', 'a') as f:
                        for log in logs:
                            print(log)
                            #turn tuple into string, separated by comma
                            log = ','.join(str(x) for x in log)
                            f.write(log)
                            f.write('\n')
                    pygame.time.delay(2000)
                death_count += 1
                return points


# Change State Operator
def change_state(state, position, vs, vd):
    aux = state.copy()
    s, d = state[position]
    ns = s + vs
    nd = d + vd
    if ns < 15 or nd > 1000:
        return []
    return aux[:position] + [(ns, nd)] + aux[position + 1:]


# Neighborhood
def generate_neighborhood(state):
    neighborhood = []
    state_size = len(state)
    for i in range(state_size):
        ds = random.randint(1, 10)
        dd = random.randint(1, 100)
        new_states = [change_state(state, i, ds, 0), change_state(state, i, (-ds), 0), change_state(state, i, 0, dd),
                      change_state(state, i, 0, (-dd))]
        for s in new_states:
            if s != []:
                neighborhood.append(s)
    return neighborhood




from scipy import stats
import numpy as np


def manyPlaysResults(rounds):
    results = []
    for round in range(rounds):
        results += [playGame()]
    npResults = np.asarray(results)
    return (results, npResults.mean() - npResults.std())

# crossover that generates two children, using random crossover point
def crossover(dino1, dino2):
    child1 = []
    child2 = []

    weight1 = dino1.get_weights()
    weight2 = dino2.get_weights()
    crossover_point = random.randint(0, len(weight1))
    for i in range(len(weight1)):
        child1.append([])
        child2.append([])
        for j in range(len(weight1[i])):
            if i < crossover_point:
                child1[i].append(weight1[i][j])
                child2[i].append(weight2[i][j])
            else:
                child1[i].append(weight2[i][j])
                child2[i].append(weight1[i][j])
    return child1, child2
# mutation that changes a random gene to a random value
def mutation(weight,mutation_rate):
    for i in range(len(weight)):
        for j in range(len(weight[i])):
            if random.random() < mutation_rate:
                weight[i][j] = weight[i][j] * random.uniform(0.5, 1.5)

    return weight

# select k individuals from the population that have the best fitness
def selection(population, scores, k=5):
    selection_ids = [ ]
    for i in range(k):
        selection_ids.append(np.argmax(scores))
        scores[np.argmax(scores)] = -99999999999

    new_population = []
    for i in selection_ids:
        new_population.append(population[i])
    return new_population



def dino_train(n_rounds, n_players):
    global aiPlayer
    global top_score
    global dinos

    if(len(dinos) == 0):
        # primeiro round, vmaos treinar todos os dinossauros com valores de pesos aleatorios
        # SUBSTITUIR ISSO POR DADOS DE ALGUEM JOGANDO, daí treinar primeiro com eles para inicializar as coisas
        for p in range(n_players):
            aiPlayer = DinoClassifier()
            dinos.append(aiPlayer)          
            res, value = manyPlaysResults(n_rounds)
            best_player = aiPlayer       
            if value > top_score:
                top_score = value
                best_player = aiPlayer

        # treinar todos os dinossauros com os pesos do melhor jogador
        for dino in dinos: 
            dino.fit(best_player.inputs,best_player.outputs,epochs=10,lr=0.01)

    new_players = []
    # Aplicar aqui a heuristica de genetico
    for p in range(n_players):
        # escolher dois pais aleatoriamente
        parent1 = random.choice(dinos)
        parent2 = random.choice(dinos)
        # fazer crossover
        child1, child2 = crossover(parent1, parent2)
        # fazer mutacao
        child1 = mutation(child1,0.1)
        child2 = mutation(child2,0.1)
        # criar dois novos jogadores com os pesos dos filhos
        new_players.append(DinoClassifier(child1))
        new_players.append(DinoClassifier(child2))
    

    
    best_player = new_players[0]
    scores = []
    for i in range(len(new_players)):
        aiPlayer = new_players[i]
        value, res = manyPlaysResults(n_rounds) 
        mean_value = np.mean(value)
        scores.append(mean_value)
        
        print("player ", i, " score: ", mean_value)
        if mean_value > top_score:
            top_score = mean_value
            best_player = new_players[i]

    # Seleciona os K melhores jogadores
    dinos = selection(new_players, scores, k=5)

    # Treina so os melhores jogadores
    for dino in dinos:
        dino.fit(best_player.inputs,best_player.outputs,epochs=10,lr=0.01)
    print("top score: ", top_score)

    if top_score > 1000:
       # Faz algo com o melhor jogador
        print("top score: ", top_score)
        return

    # Chama recursivamente, coloca aqui um criterio de parada 
    dino_train(n_rounds, n_players)



    
    
        
def main():
    global aiPlayer
    global dinos
    global top_score

    dinos = []
    top_score = 0
    dino_train(5, 5)


    # initial_state = [(15, 250), (18, 350), (20, 450), (1000, 550)]
    # aiPlayer = KeySimplestClassifier(initial_state)
    # best_state, best_value = gradient_ascent(initial_state, 5000)
    # aiPlayer = KeySimplestClassifier(best_state)
    # res, value = manyPlaysResults(30)
    # npRes = np.asarray(res)
    # print(res, npRes.mean(), npRes.std(), value)


main()
