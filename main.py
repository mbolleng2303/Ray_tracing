# --- CUSTOMIZABLE VARIABLES ---
import pygame as pygame
import numpy as np

from Wall import Wall
from Button import Button
from Antenna import Antenna
from Simulation1 import Simulation1
import time

#musée
w1=[(10,10),(10,45)]
w2=[(10,45),(0,45)]
w3=[(0,45),(0,110)]
w4=[(0,110),(35,110)]
w5=[(35,110),(35,100)]
w6 =[(35,100),(95,100)]
w7 =[(105,100),(165,100)]
w8 =[(165,100),(165,110)]
w9 =[(165,110),(200,110)]
w10 =[(200,110),(200,45)]
w11 =[(200,45),(190,45)]
w12 =[(190,45),(190,10)]
w13 =[(190,10),(165,10)]
w14 =[(165,10),(165,20)]
w15 =[(165,20),(110,20)]
w16 =[(110,20),(110,15)]
w17 =[(110,15),(115,15)]
w18 =[(115,15),(115,0)]
w19 =[(115,0),(85,0)]
w20 =[(85,0),(85,15)]
w21 =[(85,15),(90,15)]
w22 =[(90,15),(90,20)]
w23 =[(90,20),(35,20)]
w24 =[(35,20),(35,10)]
w25 =[(35,10),(10,10)]
lswallsbéton = [w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13,w14,w15,w16,w17,w18,w19,w20,w21,w22,w23,w24,w25]


w1=[(10,35),(13,35)]
w2=[(15,35),(35,35)]
w3=[(35,35),(35,20)]
w4=[(10,45),(13,45)]
w5=[(15,45),(35,45)]
w6=[(35,45),(35,80)]
w7=[(35,60),(85,60)]
w8=[(0,80),(5,80)]
w9=[(10,80),(35,80)]
w10=[(30,80),(30,95)]
w11=[(37,80),(68,80)]
w12=[(70,80),(95,80)]
w13=[(75,80),(75,85)]
w14=[(85,60),(85,70)]
w15=[(75,100),(75,95)]
w16=[(95,80),(95,60)]
w17=[(95,60),(90,60)]
w18=[(90,60),(90,45)]
w19=[(90,40),(90,30)]
w20=[(90,30),(110,30)]
w21=[(110,30),(110,40)]
w22=[(110,40),(140,40)]
w23=[(140,40),(140,20)]
w24=[(165,20),(165,30)]
w25=[(165,40),(165,45)]
w26=[(165,45),(185,45)]
w27=[(190,45),(187,45)]
w28=[(175,45),(175,80)]
w29=[(175,80),(125,80)]
w30=[(125,80),(125,85)]
w31=[(120,80),(105,80)]
w32=[(125,100),(125,95)]
w33=[(105,80),(105,60)]
w34=[(105,60),(140,60)]
w35=[(110,60),(110,54)]
w36=[(110,52),(110,45)]
w37=[(110,45),(140,45)]
w38=[(140,45),(140,50)]
w39=[(140,50),(150,50)]
w40=[(152,50),(160,50)]
w41=[(160,50),(160,70)]
w42=[(160,70),(140,70)]
w43=[(140,70),(140,60)]

lswallsbriques=[w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13,w14,w15,w16,w17,w18,w19,w20,w21,w22,w23,w24,w25,w26,w27,w28,w29,w30,w31,w32,w33,w34,w35,w36,w37,w38,w39,w40,w41,w42,w43]



museum=[lswallsbéton,lswallsbriques]






from Entire_Ray import Entire_Ray








pas = 5
raytrace = False
number_of_rays = 45  # Max 360
wall_thicknes = 0.5*6
boundarySpacing = 100
antenna_img_scale = 0.3
antenna_img_angle = 0
nbr_reflex = 4

# WINDOW
pygame.init()
size = (1400, 860)
menuSize = (100, 860)
surface = pygame.display.set_mode(size, pygame.DOUBLEBUF)
menuSurface = pygame.Surface(menuSize)
pygame.display.set_caption("Raytracing")
font = pygame.font.SysFont("monospace", 20)

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
GRAY = (128,128,128)
bleu = (255,213,0)
cyan = (255,159,0)
vert_pale = (255,129,2)
vert = (255,92,0)
jaune = (255,64,35)
orange = (255,43,0)
rouge = (216,31,42)
rouge_fonce = (202,0,42)
rouge_fonce_1 = (161,40,48)
rouge_fonce_2 = (94,10,11)
rouge_fonce_3 = (0,0,0)
# OBJECT LIST AND VARIABLE

Cloison = ('Cloison', RED, 2.25, 0.04)
Brique = ('Brique', YELLOW, 4.6, 0.02)
Béton = ('Béton', GREEN, 5, 0.014)
wall_material_init = Brique
wall_material = wall_material_init

"""-----image init-----"""
img = pygame.image.load('antenna.png')
img.convert()
img = pygame.transform.rotozoom(img, antenna_img_angle, antenna_img_scale)
antenna_img = img.get_rect()

walls = []
rays = []
antennas = []
grid = []
TX=[]
RX=[]
"""-----Events management variable-----"""
drawing = False  # indicate that the controller drawing walls
wall_starting_pos = (0, 0)
place_instance = False  # indicate that the controller place antenna
program_run = True  # main loop
first_antenna = True  # in order to delete first tower
place_end = True  # in order to keep the tower after "place end" button
clear = False
clock = pygame.time.Clock()
# --- INITIAL SETUP ---

# BUTTON
resetButton = Button(10, size[1] - menuSize[1] + 10, 70, 25, 'Reset', RED)
playButton = Button(10, resetButton.y + 10 + resetButton.height, 70, 25, 'Play', GREEN)
CloisonButton = Button(10, playButton.y + 10 + playButton.height, 70, 25, 'cloison', Cloison[1])
BriqueButton = Button(10, CloisonButton.y + 10 + CloisonButton.height, 70, 25, 'brique', Brique[1])
BétonButton = Button(10, BriqueButton.y + 10 + BriqueButton.height, 70, 25, 'béton', Béton[1])
SimuButton = Button(10, BétonButton.y + 10 + BétonButton.height, 70, 25, 'Run_Simu', vert_pale)


# Boundaries

def addBoundaries():
    walls.append(Wall(wall_material_init[1],wall_thicknes,wall_material_init[2], wall_material_init[3],np.array([boundarySpacing, boundarySpacing]), np.array([size[0] - boundarySpacing, boundarySpacing])))
    walls.append(
        Wall(wall_material_init[1],wall_thicknes, wall_material_init[2], wall_material_init[3], np.array([boundarySpacing, boundarySpacing]),
             np.array([boundarySpacing, size[1] - boundarySpacing])))
    walls.append(
        Wall(wall_material_init[1],wall_thicknes, wall_material_init[2], wall_material_init[3], np.array([boundarySpacing, size[1] - boundarySpacing]),
             np.array([size[0] - boundarySpacing, size[1] - boundarySpacing])))
    walls.append(
        Wall(wall_material_init[1],wall_thicknes, wall_material_init[2], wall_material_init[3], np.array([size[0] - boundarySpacing, size[1] - boundarySpacing]),
             np.array([size[0] - boundarySpacing, boundarySpacing])))

def arrangemuseum():
    murbeton = museum[0]
    murbriques = museum[1]
    lswallsbriques=[]

    lswallbeton = []
    for i in range(len(murbeton)):
        wll = murbeton[i]  # [(10,10),(10,45)]
        startreel = wll[0]  # (10,10)
        endreel = wll[1]  # (10,45)

        startarranged = np.array([boundarySpacing +startreel[0]*6,boundarySpacing +startreel[1]*6])
        endarranged = np.array([boundarySpacing +endreel[0]*6,boundarySpacing +endreel[1]*6])
        nwwallbet = [startarranged,endarranged]
        lswallbeton.append(nwwallbet)
        walls.append(
            Wall(Béton[1], wall_thicknes, Béton[2], Béton[3],
                 startarranged,
                 endarranged))



    for i in range(len(murbriques)):
        wll = murbriques[i]  # [(10,10),(10,45)]
        startreel = wll[0]  # (10,10)
        endreel = wll[1]  # (10,45)

        startarranged = np.array([boundarySpacing +startreel[0]*6,boundarySpacing +startreel[1]*6])
        endarranged = np.array([boundarySpacing +endreel[0]*6,boundarySpacing +endreel[1]*6])
        nwwallbet = [startarranged,endarranged]
        lswallsbriques.append(nwwallbet)

        walls.append(
            Wall(Brique[1], wall_thicknes, Brique[2], Brique[3],
                 startarranged,
                 endarranged))


#addBoundaries()

def test():



    walls.append(
        Wall(wall_material_init[1], wall_thicknes, wall_material_init[2], wall_material_init[3],
            np.array([boundarySpacing +160*6,100]),
            np.array([boundarySpacing +160*6,760])))
arrangemuseum()
def optimisation() :
    init_x = 200
    end_x = 1100
    init_y = 200
    end_y = 660
    couv_opti =[0,0,0,0]
    pos_opti_x=  (0,0)
    pos_opti_y = (0,0)
    for i in range (init_x,end_x,6*pas) :
        for j in range (i,end_x,6*pas) :
            for k in range (init_y, end_y,6*pas) :
                for l in range (k, end_y, 6*pas) :
                    if (i!=j and k!=l) :
                        tx_antenna = Antenna(np.array([i+0.01, k+0.01]), 0.1, [])
                        tx_antenna2 = Antenna(np.array([j+0.01, l+0.01]), 0.1, [])
                        print("p-a pute")
                        RX = []

                        TX.append(tx_antenna)
                        TX.append(tx_antenna2)
                        simulation()
                        sim = Simulation1(walls, TX, RX)
                        sim.Run_Simulation(1)
                        dbm_tot = 0
                        oui = 0
                        non = 0
                        res =0
                        for rx in RX:
                            dbm = rx.dBmToBinary()
                            #print(dbm)
                            if dbm <= 40 :
                                non += 1
                                res += 40
                            else :
                                oui+=1
                                if dbm >=320:
                                    res += 320
                                else :
                                    res +=dbm
                            rx.draw(surface, False, False)

                        ratio = oui/(oui+non)
                        res = res/(oui+non)
                        for wall in walls:
                            pygame.draw.line(surface, wall.color, wall.Vec1, wall.Vec2, 2)
                        for tx_antenna in TX:
                            tx_antenna.draw(surface, True)
                        pygame.display.flip()
                        if ratio == couv_opti[0] :
                            if res >= couv_opti[1] :
                                couv_opti = [ratio, res, tx_antenna2._Get_Pos, tx_antenna._Get_Pos]
                                print(couv_opti)
                        elif ratio > couv_opti[0] :
                            couv_opti = [ratio, res, tx_antenna2._Get_Pos, tx_antenna._Get_Pos]
                            print(couv_opti)
                        else :
                            pass
def add_rx():
    #rx_antenna = Antenna(np.array([boundarySpacing+100.5*6, boundarySpacing+75.5*6]), 0, [])
    tx_antenna = Antenna(np.array([boundarySpacing+6*100.01,boundarySpacing+65.01*6]),0.1,[])

    #X.append(rx_antenna)
    rx_antenna = Antenna(np.array([boundarySpacing + 145 * 6, boundarySpacing + 65 * 6]), 0, [])
    RX.append(rx_antenna)
    TX.append(tx_antenna)



#add_rx()

def drawMenu():
    # Set color and transparency of the menu box
    menuSurface.fill(WHITE)
    menuSurface.set_alpha(126)

    # Draw menu box
    surface.blit(menuSurface, (0, size[1] - menuSize[1]))

    # Draw buttons
    resetButton.draw(surface)
    playButton.draw(surface)
    BriqueButton.draw(surface)
    BétonButton.draw(surface)
    CloisonButton.draw(surface)
    SimuButton.draw(surface)

def simulation ():
    for i in range (boundarySpacing,size[0]-boundarySpacing,int(6*pas)) :
        for j in range (boundarySpacing,size[1]-boundarySpacing,int(6*pas)) :
            RX.append(Antenna(np.array([i-6, j-6]), 0, []))
def drawGrid():
    for i in range(boundarySpacing, size[0]-boundarySpacing,int (6*pas)):

        for j in range(boundarySpacing, size[1]-boundarySpacing, int(6*pas)):
            a = (i, j, pas*6-1, pas*6-1)
            pygame.draw.rect(surface, GRAY, a)
            # rectLis.append()
while program_run:

    # --- MAIN EVENT LOOP ---
    for event in pygame.event.get():
        # If user wants to leave
        if event.type == pygame.QUIT:
            program_run = False

            # User has changed the size of a window


        # User has clicked mouse button
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #start_antenna_pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                # Check if user clicked on one of the buttons
                if resetButton.clicked(pos):
                    walls = []
                    #addBoundaries()
                    antennas = []
                    rays = []

                    clear = True

                elif playButton.clicked(pos):
                    clear = False
                    # Change status of play button
                    if place_instance:
                        #raytrace=True
                        playButton.color = GREEN
                        playButton.text = 'Place TX'
                        #  antennas = []
                        first_antenna = not first_antenna
                        place_end = True
                        start = time.time()
                        sim = Simulation1(walls, TX, RX)
                        sim.Run_Simulation(4)
                        end = time.time()
                        print(
                            f"Finished Predict, Total time of the run : {int((end - start) / 60)}:{(end - start) % 60}")


                    else:


                        playButton.color = RED
                        playButton.text = 'Place End'





                    drawing = False
                    place_instance = not place_instance
                elif place_instance:
                    if not first_antenna and not place_end:
                        #start_antenna_pos = pygame.mouse.get_pos()
                        #print('tic')
                        pass


                    else:
                        #  antennas = []
                        first_antenna = not first_antenna




                elif CloisonButton.clicked(pos):
                    wall_material = Cloison


                elif BétonButton.clicked(pos):
                    wall_material = Béton

                elif BriqueButton.clicked(pos):
                    wall_material = Brique

                elif SimuButton.clicked(pos):
                    """RX = []
                    simulation()
                    start=time.time()
                    sim = Simulation1(walls, TX, RX)
                    sim.Predict(3)
                    end = time.time()
                    print(
                        f"Finished Predict, Total time of the run : {int((end - start) / 60)}:{(end - start) % 60}")
                    print("simu finish")"""
                    optimisation()


                elif not place_instance:  # Drawing a wall

                    # Check if user is already drawing a wall
                    if drawing:
                        # Finish drawing and add a new wall
                        drawing = False
                        walls.append(Wall(wall_material[1],wall_thicknes,wall_material[2],wall_material[3],np.array([wall_starting_pos[0],wall_starting_pos[1]]),np.array ([pos[0],pos[1]])))
                    else:
                        # Start drawing
                        drawing = True
                        wall_starting_pos = pos

            elif event.button == 3:  # Right Click
                drawing = False



    # --- GAME LOGIC ---
        #if not first_antenna and not clear and place_end:
            #tx_antenna = Antenna(np.array([start_antenna_pos[0], start_antenna_pos[1]]), 0.1, [])

            #TX.append(tx_antenna)

            #sim = Simulation1(walls, TX, RX)
            #sim.Predict(4)




    # --- DRAWING ---
    surface.fill(BLACK)
    drawGrid()

    # Draw currently constructing wall
    if drawing:
        pygame.draw.line(surface, WHITE, wall_starting_pos, pygame.mouse.get_pos(), 2)



    # Draw antenna and rays
    drawMenu()
    if (place_instance or place_end) and not clear:

        for tx_antenna in TX:

            tx_antenna.draw(surface, True)
            tx_antenna.colorbar(surface, True)
            #pygame.draw.rect(surface, RED,(tx_antenna._pos[0],tx_antenna._pos[1],20,20) , 2)
            #surface.blit(img, tx_antenna.img_antenna)
            #pygame.draw.rect(surface, RED, tx_antenna.img_antenna, 1)
            # antenna.center = pygame.mouse.get_pos()
            #tx_antenna.img_antenna.center = tx_antenna.position
            ''' dessinne les rays 
            for ray in tx_antenna.rays:
                pygame.draw.line(surface, RED, ray.start_pos, ray.end_point, 1)
            '''

        for rx_antenna in RX :
            rx_antenna.draw(surface, False, raytrace)
        # Draw existing walls
        for wall in walls:
            pygame.draw.line(surface, wall.color, wall.Vec1, wall.Vec2, 2)
    # Draw menu and all buttons



    # --- UPDATE THE SCREEN ---
    pygame.display.flip()

    clock.tick(60)

pygame.quit()