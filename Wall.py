import numpy as np
import Line
from scipy.constants import c, mu_0, epsilon_0

Eps_Air = epsilon_0
Sigma_Air = 0  # conductivity
Antenna_Freq = 27e9
BETA = 2 * np.pi * Antenna_Freq / c


class Wall(Line.Line):
    def __init__(self,color, Width, epsilon, sigma, StartVec, EndVec):
        self._width = Width/6 # notee l dans le sylla
        self.color= color
        self._Eps_Complexe = epsilon * epsilon_0  # s'assurer qu'on entre bien epsr*eps0 alors
        self._Sigma = sigma
        super(Wall, self).__init__(StartVec, EndVec)


    def Compute_Coeff_Perp (self, Theta_I, Eps_Complexe_Air, Eps_Complexe_Wall):
        """
        Is a method of class "Wall" wish is call
        when we have a ray wish have a reflexion/transmision with a wall with
        a incidence angle Theta_I
        Returns the reflection coefficient for a perpendicular polarization
        """
        Z_Air = np.sqrt(mu_0 / Eps_Complexe_Air)
        Z_Wall = np.sqrt(mu_0 / Eps_Complexe_Wall)
        Theta_T = np.arcsin(np.sqrt(np.real(Eps_Complexe_Air) / np.real(Eps_Complexe_Wall)) * np.sin(Theta_I))
        Coeff_Perp = (Z_Wall * np.cos(Theta_I) - Z_Air * np.cos(Theta_T)) / (Z_Wall * np.cos(Theta_I) + Z_Air * np.cos(Theta_T))

        return Coeff_Perp

    def Compute_Reflex_Coeff(self, Theta_I):
        """
        Is a method of class "Wall" wish is call
        when we have a ray wish have a reflexion with a wall with
        a incidence angle Theta_I
        return : reflexion coefficient
        """
        Eps_Complexe_Wall = self._Eps_Complexe - 1j * self._Sigma / (2 * np.pi * Antenna_Freq)
        Eps_Complexe_Air = Eps_Air - 1j * Sigma_Air / (2 * np.pi * Antenna_Freq)
        Theta_T = np.arcsin(np.sqrt(np.real(Eps_Complexe_Air) / np.real(Eps_Complexe_Wall)) * np.sin(Theta_I))
        Coeff_Perp = self.Compute_Coeff_Perp(Theta_I, Eps_Complexe_Air, Eps_Complexe_Wall)
        Gamma_m = 1j * 2 * np.pi * Antenna_Freq * np.sqrt(mu_0 * Eps_Complexe_Wall)
        s = self._width / np.cos(Theta_T)  #Distance traveled into the wall
        Exp_Part = np.exp(-2 * Gamma_m * s + 1j * BETA * 2 * s * np.sin(Theta_T) * np.sin(Theta_I))
        Coeff_Reflex_Tot = Coeff_Perp - (1 - (Coeff_Perp*Coeff_Perp)) * Coeff_Perp * Exp_Part /\
                           (1 - (Coeff_Perp * Coeff_Perp) * Exp_Part)
        return Coeff_Reflex_Tot

    def Compute_Transmission_Coeff(self, Theta_I):

        """
        Is a method of class "Wall" wish is call
        when we have a ray wish passed through a wall with
        a incidence angle Theta_I
        return : transmission coefficient
        """
        Eps_Complexe_1 = Eps_Air - 1j * Sigma_Air / (2 * np.pi * Antenna_Freq)
        Eps_Complexe_2 = self._Eps_Complexe - 1j * self._Sigma / (2 * np.pi * Antenna_Freq)
        Theta_T = np.arcsin(np.sqrt(np.real(Eps_Complexe_1) / np.real(Eps_Complexe_2)) * np.sin(Theta_I))
        Coeff_Perp = self.Compute_Coeff_Perp(Theta_I, Eps_Complexe_1, Eps_Complexe_2)
        Gamma_m = 1j * 2 * np.pi * Antenna_Freq * np.sqrt(mu_0 * Eps_Complexe_2)
        s = self._width / np.cos(Theta_T)
        Coeff_Transmission_Tot = ((1-(Coeff_Perp*Coeff_Perp)) * np.exp(-Gamma_m*s) /
                                  (1 - Coeff_Perp * Coeff_Perp * np.exp(-2*Gamma_m*s)
                                   * np.exp(1j * BETA * 2 * s * np.sin(Theta_T) * np.sin(Theta_I))))

        return Coeff_Transmission_Tot
