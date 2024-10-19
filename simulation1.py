from moteurSOLAR import *

### GUIDE UTILISATEUR ###

### PARAMETRES ###

# -> AFFICHAGE <- #
BACKGROUND = (0, 0, 0) #Couleur de l'arrière plan (RGB)
FPS = 60 #Image par seconde
TIME_SCALE = 1
WINDOW_X = 600 #Taille horizontale de la fenetre
WINDOW_Y = 600 #Taille verticale de la fenetre

# -> PHYSIQUE <- #
SPACE_X = 100 #Taille (en m) horizontale de l'espace simulé
SPACE_Y = 100 #Taille (en m) horizontale de l'espace simulé
G = 6.67 #Constante gravitationelle
INBOUND = False #True: Quand un corps arrive sur un bord, il conserve sa vitesse et repart du bord opposé
                #False: Il continue sa course en dehors de l'écran

##################

#Objet Planet: (Mass, Position, Vitesse, Couleur = (255,255,255), Diametre (en m))

A = Planet(10,vec2(SPACE_X/2, SPACE_Y/2), vec2(0,0), color = (0,0,255), diameter = 1)
B = Planet(1,vec2(SPACE_X/4, SPACE_Y/2), vec2(0,5), color = (255,0,0), diameter = 1)
C = Planet(1,vec2(3*SPACE_X/4, SPACE_Y/2), vec2(0,-5), color = (0,255,0), diameter = 1)

planets=[A,B,C]


WINDOW = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
main(planets)
