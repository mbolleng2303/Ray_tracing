import Antenna
import Wall
from typing import List
import time

class Simulation1:
    def __init__(self, Walls: List[Wall.Wall], Tx: List[Antenna.Antenna], Rx: List[Antenna.Antenna]):

        self.Array_Wall = Walls
        self.Tx = Tx
        self.Rx = Rx


    def CreateImageFor_AllWalls(self, transmitter: Antenna.Antenna):
        Images = []

        for w in self.Array_Wall:
            if transmitter.Sym_Wall != w:
                Images.append(transmitter.CreateImage(w))
        return Images

    def Generate_Img_Antenna(self, Transmitters: List[Antenna.Antenna]):
        Images = []
        for t in Transmitters:
            Images.extend(self.CreateImageFor_AllWalls(t))

        return Images

    def Run_Simulation(self, Nbr_Reflex):
        """
        Is a method of class "Simulation" wish is call
        when we want to run the image method for all Tx (imaged or not)
        for 0,1,2,3,..,Nbr_Reflex-1  number of reflexion.
        return : None
        """
        print("Start Simulation")
        Array_Tx = self.Tx
        for i in range(Nbr_Reflex):
            for tx in Array_Tx:
                for rx in self.Rx:
                    New_Ray = tx.Img_Method(rx._Get_Pos, self.Array_Wall)
                    if New_Ray is not None:
                        rx.rays.append(New_Ray)
            if i != Nbr_Reflex-1 :
                Array_Tx = self.Generate_Img_Antenna(Array_Tx)
