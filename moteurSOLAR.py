import pygame, sys, random
import pygame_menu
from pygame.locals import *
from math import *
import json

class vec2():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __add__(self,other):
        return vec2(self.x + other.x, self.y + other.y)
    def __sub__(self,other):
        return vec2(self.x - other.x, self.y - other.y)
    def __rmul__(self,other):
        if type(other) == int or type(other) == float:
            return vec2(self.x * other, self.y * other)
        else:    
            return vec2(self.x * other.x, self.y * other.y)
    def __truediv__(self,other):
        return vec2(self.x / other, self.y / other)
    def __mod__(self,other):
        return vec2(self.x % other, self.y % other)
    def norme(self):
        return sqrt(abs(self.x)**2 + abs(self.y)**2)
    def tup(self):
        return (self.x, self.y)

    def inbound(self):
        self.x = self.x % SPACE_X
        self.y = self.y % SPACE_Y
        return self


class Planet():
    def __init__(self, mass, pos, speed, color = (255,255,255), diameter = 20):
        self.mass = mass
        self.pos = pos
        self.speed = speed
        self.diameter = diameter
        self.color = color
        self.acc = vec2(0,0)

    def display(self,SCREEN, WINDOW_X,WINDOW_Y,SPACE_X,SPACE_Y):
        d = self.diameter * (WINDOW_Y/SPACE_Y)
        pygame.draw.circle(SCREEN, self.color, RtoS(self.pos, WINDOW_X,WINDOW_Y,SPACE_X,SPACE_Y).tup(), d)

    def resultante(self, planets,G):
        acc = vec2(0,0)
        for planet in planets:
            if planet != self:
                F = (G * planet.mass) / (((self.pos - planet.pos).norme())**2)
                directionVector = (self.pos - planet.pos) / (self.pos - planet.pos).norme()
                acc += - F*directionVector
                self.acc = acc
    
    def updAgent(self,TIME_SCALE,FPS,INBOUND=False):
        self.speed += self.acc
        self.pos = self.pos + (TIME_SCALE/FPS)*self.speed
        if INBOUND: self.pos = self.pos.inbound()

def generateRandomPlanets(N):
    planets = []
    for i in range(N):
        max_mass = 100
        mass = random.uniform(0,max_mass)
        diameter = random.uniform(SPACE_X/200,SPACE_X/50)
        pos = vec2(random.uniform(SPACE_X/4,3*SPACE_X/4),random.uniform(SPACE_Y/4,3*SPACE_Y/4))
        speed = vec2(random.uniform(-10,10), random.uniform(-10,10))
        color = (50,50,random.randint(150,255))
        p = Planet(mass, pos, speed, color = color, diameter = diameter)
        planets.append(p)

    return planets

def generateRandomPlanet(pos):
    mass = random.uniform(0,100)
    diameter = mass
    speed = vec2(random.uniform(0,2), random.uniform(0,2))
    color = (random.randint(150,255),0,0)
    p = Planet(mass, pos, speed, color = color, diameter = diameter)
    return p

def fileToJson(path):
    jsonD = '{'
    with open(path,"r") as f:
        for line in f.readlines():
            line = line.strip().split("=")
            jsonD += '"'+line[0]+'":'+line[1]+","
    jsonD = jsonD[:-1]+"}"
    return json.loads(jsonD)

def simulationReader(displayFile,simFile):

    simData = fileToJson(simFile)
    print("B:",simData)

    displayData = fileToJson(displayFile)
    print("A:",displayData)

    WINDOW_X = displayData["WINDOW_X"]
    WINDOW_Y = displayData["WINDOW_Y"]
    TIME_SCALE = displayData["TIME_SCALE"]
    
    planets = []
    for p in simData["PLANETS"]:
        pos = vec2(p["pos"][0],p["pos"][1])
        speed = vec2(p["speed"][0],p["speed"][1])
        planets.append(Planet(p["mass"],pos,speed,color=p["color"],diameter=p["diameter"]))
    print(planets)
                       

    main(displayData["BACKGROUND"],displayData["FPS"],displayData["TIME_SCALE"],displayData["WINDOW_X"],displayData["WINDOW_Y"],simData["SPACE_X"],simData["SPACE_Y"],simData["G"],simData["INBOUND"],planets)
    

### AFFICHAGE

def RtoS(vecteur, WINDOW_X,WINDOW_Y,SPACE_X,SPACE_Y):
    X = vecteur.x * (WINDOW_X / SPACE_X)
    Y = vecteur.y * (WINDOW_Y / SPACE_Y)
    return vec2(X,Y)

def StoR(vecteur, WINDOW_X,WINDOW_Y,SPACE_X,SPACE_Y):
    X = vecteur.x * (SPACE_X / WINDOW_X )
    Y = vecteur.y * (SPACE_Y / WINDOW_Y )
    return vec2(X,Y)


def main(BACKGROUND,FPS,TIME_SCALE,WINDOW_X,WINDOW_Y,SPACE_X,SPACE_Y,G,INBOUND,planets) :
    
    pygame.init()
    fpsClock = pygame.time.Clock()

    WINDOW = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
    pygame.display.set_caption('SOLAR')

    
    global PAUSE
    looping = True
    WINDOW.fill(BACKGROUND)
    
    while looping :
        WINDOW.fill(BACKGROUND)

        #Boucle d'évènements
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                #planets.append(generateRandomPlanet(StoR(vec2(pos[0],pos[1]))))
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == 109: #PRESS M
                    print("pause")
                    PAUSE = (PAUSE + 1) % 2                  

        if not PAUSE:
            #Mise à jour
            for planet in planets:
                planet.resultante(planets,G)
                

            for planet in planets:
                planet.updAgent(TIME_SCALE,FPS,INBOUND)
                planet.display(WINDOW, WINDOW_X,WINDOW_Y,SPACE_X,SPACE_Y)
            pygame.display.update()
            fpsClock.tick(FPS)

### PARAMETRES ###
"""
# -> AFFICHAGE <- #
BACKGROUND = (0, 0, 0)
FPS = 60
TIME_SCALE = 2
WINDOW_X = 600
WINDOW_Y = 600

# -> PHYSIQUE <- #
SPACE_X = 1000
SPACE_Y = 1000
G = 6.67
INBOUND = False
"""
##################

#INIT
global PAUSE
PAUSE = False

if __name__ == "__main__":
    simulationReader("defaultParam.txt","sim1.txt")

    """    
    # -> AFFICHAGE <- #
    BACKGROUND = (0, 0, 0)
    FPS = 60
    TIME_SCALE = 2
    WINDOW_X = 600
    WINDOW_Y = 600

    # -> PHYSIQUE <- #
    SPACE_X = 1000
    SPACE_Y = 1000
    G = 6.67
    INBOUND = True
    
    planets = generateRandomPlanets(100)
    main(BACKGROUND,FPS,TIME_SCALE,WINDOW_X,WINDOW_Y,SPACE_X,SPACE_Y,G,INBOUND,planets)
    """


