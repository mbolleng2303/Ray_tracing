import Line
from typing import List
import pygame
from scipy.constants import c
import numpy as np
#everything below to remove and place it in the antenna
#Gtx = 4*np.pi*0.13
Gtx = 32/(6*np.pi)
Ptx = 0.1
FREQ = 27e9
Beta = 2 * np.pi * (FREQ) / c
H_EQ = -c / (FREQ * np.pi)
R_A = 720*np.pi/32

class Short_Ray(Line.Line):


    def __init__(self, StartVec, EndVec, Gains: list):
        super(Short_Ray, self).__init__(StartVec, EndVec)
        self.gains = Gains

    def __add__(self, otherRay: "Short_Ray"):
        return Entire_Ray([self, otherRay])


class Entire_Ray:
    def __init__(self, beams):

        # beams : a list containing all the rays along one trajectory

        self.Distance_Traveled = 0
        self.Coordinates = []
        self.Coefficients = []
        for b in beams:
            self.add(b)

    def add(self, beam: "Short_Ray"):
        self.Distance_Traveled += beam.Distance / 6
        #print("distance", beam.Distance/6)
        self.Coordinates.append([beam.Vec1, beam.Vec2])
        self.Coefficients.extend(beam.gains)

    def Compute_E(self, Gtx, Ptx, Beta):
        """
        Is a method of class "Ray" wish is call
        when we want to compute  the complex
        electric field for a direct path d
        """
        d = self.Distance_Traveled
        E = np.sqrt(60*Gtx*Ptx) * np.exp(-1j * Beta * d) / d
        return E

    def averagePower(self, eField):
        """
        Returns the average power for a given electric field
        """
        power = 1/(8*R_A) * (np.linalg.norm(H_EQ * eField))**2
        return power

    def Compute_power(self):
        """
        Returns the power received by Rx
        """
        coeff = np.prod(self.Coefficients)
        #Compute Elec field
        d = self.Distance_Traveled
        E = coeff * np.sqrt(60 * Gtx * Ptx) * np.exp(-1j * Beta * d) / d
        #average power
        power = 1/(8*R_A) * (np.linalg.norm(H_EQ * E))**2

        return power