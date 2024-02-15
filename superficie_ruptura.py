from math import isnan
import numpy as np
from perfil_logitudinal import Perfil_Longitudinal

class Superficie_Ruptura:
    
    def __init__(self, perfil_longitudinal: Perfil_Longitudinal, x0: float, y0: float, raio: float):
        self.x0 = x0
        self.y0 = y0
        self.raio = raio
        self.perfil_longitudinal = perfil_longitudinal
        self.dominio = self.perfil_longitudinal.superficie_terreno.dominio
        self.imagem = self.funcao(self.dominio)
        self.limites = self.encontra_limites()
        self.imagem_raio_esquerda = self.funcao_raio_esquerda(self.dominio)
        self.imagem_raio_direita = self.funcao_raio_direira(self.dominio)

        # print(self.x0, self.y0, self.raio)
        # print(len(self.imagem), len(self.dominio))
        # print("----------------")

    def funcao(self, x):
        if type(x) == np.float64:
            x = [x]
        y = [0 for i in range(0, len(x))]
        for i in range(0, len(x)):
            #print(self.perfil_longitudinal.superficie_terreno.funcao(x[i]), - (self.raio ** 2 - (x[i] - self.x0) ** 2) ** 0.5 + self.y0)
            if x[i] < (self.x0 - self.raio):
                y[i] = np.nan
            elif x[i] > (self.x0 + self.raio):
                y[i] = np.nan
            elif self.perfil_longitudinal.superficie_terreno.funcao(x[i]) < - (self.raio ** 2 - (x[i] - self.x0) ** 2) ** 0.5 + self.y0:
                y[i] = np.nan
            else:
                y[i] = - (self.raio ** 2 - (x[i] - self.x0) ** 2) ** 0.5 + self.y0
        return y

    def encontra_limites(self):
        lista_lim_esquerdo = []
        lista_lim_direito = []
        tamanho_superficies = []
        limite_esquerdo = np.nan
        limite_direito = np.nan
        for i in range(0, len(self.dominio)):
            if i == 0 and not np.isnan(self.imagem[i]):
                lista_lim_esquerdo.append(self.dominio[i])
            elif np.isnan(self.imagem[i - 1]) and not np.isnan(self.imagem[i]):
                lista_lim_esquerdo.append(self.dominio[i])

        for i in range(0, len(self.dominio)):
            if i == len(self.dominio) - 1 and not np.isnan(self.imagem[i]):
                lista_lim_direito.append(self.dominio[i])
            elif np.isnan(self.imagem[i]) and not np.isnan(self.imagem[i - 1]):
                lista_lim_direito.append(self.dominio[i - 1])


        if len(lista_lim_esquerdo) == 1:
            # print("Só foi encontrado uma superfície")
            limite_esquerdo = lista_lim_esquerdo[0]
            limite_direito = lista_lim_direito[0]
            return (limite_esquerdo, limite_direito)
        
    
        elif len(lista_lim_esquerdo) == 0:
            # print("Superfície de ruptura não cruza superfície do terreno")
            return (limite_esquerdo, limite_direito)
        
        else:
            for i in range(0, len(lista_lim_esquerdo)):
                tamanho_superficies.append(lista_lim_direito[i] - lista_lim_esquerdo[i])
            # print("tamanho dassuperfícies: ",tamanho_superficies)
            for i in range(0, len(tamanho_superficies)):
                if tamanho_superficies[i] == np.amax(tamanho_superficies):
                    limite_esquerdo = lista_lim_esquerdo[i]
                    limite_direito = lista_lim_direito[i]
                    return (limite_esquerdo, limite_direito)

    def funcao_raio_esquerda(self, x):
        yi = self.funcao([self.limites[0]])
        if self.limites[0] < self.x0:
            return np.interp(x, [self.limites[0], self.x0], [yi[0], self.y0], left = np.nan, right = np.nan)
        else:
            return np.interp(x, [self.x0, self.limites[0]], [self.y0, yi[0]], left = np.nan, right = np.nan)

    def funcao_raio_direira(self, x):
        yf = self.funcao([self.limites[1]])     
        return np.interp(x, [self.x0, self.limites[1]], [self.y0, yf[0]], left = np.nan, right = np.nan)
    
    def funcao_mp(self,x, mi, nu):
        return np.sin(np.pi * ((x - self.limites[0])/(self.limites[1] - self.limites[0]))** nu) ** mi
    
    def funcao_sp(self,x):
        return 1