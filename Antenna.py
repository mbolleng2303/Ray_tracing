import numpy as np

from Wall import Wall
from Entire_Ray import Entire_Ray, Short_Ray
from Line import Line
from typing import Callable, Any, List
import colorsys as cl
import pygame

pas = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
GRAY = (128, 128, 128)
bleu = (255, 213, 0)
cyan = (255, 159, 0)
vert_pale = (255, 129, 2)
vert = (255, 92, 0)
jaune = (255, 64, 35)
orange = (255, 43, 0)
rouge = (216, 31, 42)
rouge_fonce = (202, 0, 42)
rouge_fonce_1 = (161, 40, 48)
rouge_fonce_2 = (94, 10, 11)
rouge_fonce_3 = (0, 0, 0)


class Antenna:
    def __init__(self, PosVec, EmittedPower, Gains, ImagedSource = None, Sym_Wall = None):
        self._Get_Pos = PosVec
        self._emittedPower = EmittedPower
        self.gains = Gains
        self.Antenna_From = ImagedSource
        self.Sym_Wall = Sym_Wall
        self.rays = []

    def CreateImage(self, symWall: "Wall.wall") -> "Antenna":
        # compute antenna img
        pos = []
        if (np.shape(symWall.Direction)[0] == 3):
            ax1 = np.dot(symWall.Direction[:, 0], self._Get_Pos - symWall.Vec2) * symWall.Direction[:, 0] + symWall.Vec2
            ax2 = np.dot(symWall.Direction[:, 1], self._Get_Pos - symWall.Vec2) * symWall.Direction[:, 1] + symWall.Vec2
            pos = ax1 + ax2
        else:
            pos = np.dot(symWall.Direction, self._Get_Pos - symWall.Vec2) * symWall.Direction + symWall.Vec2
        pos += (pos - self._Get_Pos)

        return Antenna(pos, None, None, self, symWall)

    def Img_Method(self, Rx_pos, Array_Wall, Entire_Ray=None, Prev_Wall=None):
        """
        Is a method of class "Antenna" wish is call
        when we want to compute the ray tracing.
        it take a rx antenna, a list of all wall
        on the map for the first iteration. This method
        is call for all Tx antenna (virtual or original).
        In the recursive case (with n reflexion) it takes
        in argument an object of class Entire_ray whish contains
        all ray that are linked in the same way ( and their attributes
        coeff,distance, etc...)
        and the wall object Prev_wall use to allow to have multiple reflexion
        with some transmission between themself.
        It returns : None if we have no valid situation
                   : Entire_Ray if we found a way with n reflexions
        """
        Array_Gain = []
        Point = self._Get_Pos
        Reflex = False
        #trace a line from Tx (img or original)
        # to Rx or reflexion point
        Tracing = Line(Rx_pos, self._Get_Pos)
        for wall in Array_Wall:
            Intersected, Intersect_Point = Tracing.Intersect(wall)
            if Intersected:
                Theta_I = Tracing.Compute_Theta_I(wall)
                if wall == self.Sym_Wall:
                    #reflexion
                    Array_Gain.append(wall.Compute_Reflex_Coeff(Theta_I))
                    Reflex = True
                    Point = Intersect_Point
                elif (wall != Prev_Wall):
                    #transmission
                    Array_Gain.append(wall.Compute_Transmission_Coeff(Theta_I))
                    pass

        if (Entire_Ray is not None):
            #for the recursivity (add to the other previous ray)
            Entire_Ray.add(Short_Ray(Rx_pos, Point, Array_Gain))
        else:
            #or for the first step create a new entire ray
            Entire_Ray = Entire_Ray([Short_Ray(Rx_pos, Point, Array_Gain)])

        if (Reflex):
            #recursivity to go from the end to the begining
            Entire_Ray = self.Antenna_From.Img_Method(Point, Array_Wall, Entire_Ray, self.Sym_Wall)

            return Entire_Ray
        else:
            #stop the recursivity because we found the last ray
            if self.Antenna_From == None :
                return Entire_Ray
            else:
                # No valid Situation
                return None

    def getPower(self):
        if len(self.rays) != 0:
            powers = [ray.Compute_power() for ray in self.rays]
            powerTot = np.sum(powers)
            powerTot = 10 * np.log10(powerTot / 0.001)
            return powerTot
        else:
            return 0

    def dBmToBinary(self):
        if len(self.rays) != 0:
            powers = [ray.Compute_power() for ray in self.rays]
            powerTot = np.sum(powers)
            powerTot = 10 * np.log10(powerTot / 0.001)
            Mbs = (379 / 31) * powerTot + (54 + (82 * 379 / 31))
            Mbstest = 40 +(320-40)*(powerTot+82)/(-73+82)
            return Mbstest
        else:
            return 0

    def draw(self, surface, tx=None, ray= None):

        if not tx:
            dbm = self.dBmToBinary()
            power = self.getPower()
            res = dbm

            if res >= 320:
                res = 320
                hsv = ((100 - (res / 3.20)) / 100, 1, 1)

            elif res <= 20:
                res = 39
                hsv = ((100 - (res / 3.50)) / 100, 0, 0)



            else:
                res = dbm
                hsv = ((100 - (res / 3.20)) / 100, 1, 1)


            #hsv = (((res / 3.20)) / 100, (100 - (res / 3.20)) / 100, ((res / 3.20)) / 100)

            c = cl.hsv_to_rgb(hsv[0], hsv[1], hsv[2])

            pygame.draw.rect(surface, (int(np.round(c[0] * 255)), int(np.round(c[1] * 255)), int(np.round(c[2] * 255))),
                             (self._Get_Pos[0] - pas / 2, self._Get_Pos[1] - pas / 2, 6 * pas, 6 * pas))

            if ray :
                for ray in self.rays:
                    for i in range(len(ray.Coordinates)):
                        if len(ray.Coordinates) == 1:
                            c = rouge_fonce_1
                        elif len(ray.Coordinates) == 2:
                            c = YELLOW
                        elif len(ray.Coordinates) == 3:
                            c = cyan
                        else:
                            c = GREEN

                        pygame.draw.line(surface, c, ray.Coordinates[i][0], ray.Coordinates[i][1], 2)


        else:
            pygame.draw.circle(surface, cyan, (self._Get_Pos[0], self._Get_Pos[1]), pas)
    def colorbar (self, surface, tx=None, ray= None):
        nmb = 20

        if  tx:

            for dbm in range(40,320+nmb,nmb) :

                res = dbm
                #print (dbm,dbm+nmb)
                hsv = ((100- (res / 3.20)) / 100, 1,1)
                c = cl.hsv_to_rgb(hsv[0], hsv[1], hsv[2])

                pygame.draw.rect(surface,
                                 (int(np.round(c[0] * 255)), int(np.round(c[1] * 255)), int(np.round(c[2] * 255))),
                                 (1350, 50+(dbm-40)*30/20, 27 * pas, 27*pas * pas))



            """
            if dbm <= 60 :
                c = (17, 0, 255)
            elif dbm <= 120 and dbm >60:
                c = (0, 162, 255)
            elif dbm <= 200 and dbm >120:
                c = (0,255, 137)
            elif dbm <= 250 and dbm >200:
                c = (0, 162, 255)
            elif dbm <= 300 and dbm >250:
                c = (247, 255, 0)
            else :
                c = (255,0,0)
            """
