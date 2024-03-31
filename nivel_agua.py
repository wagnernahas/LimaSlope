import numpy as np
from superficie_terreno import Superficie_Terreno
import lerarquivo

class Nivel_Agua:
    
    def __init__(self, superficie_terreno: Superficie_Terreno, caminho_arquivo=None):  
        self.superficie_terreno = superficie_terreno      
        if caminho_arquivo==None:
            return
        self.superficie_terreno = superficie_terreno
        coordenadas = lerarquivo.pega_pontos(caminho_arquivo)
        self.atribuicaodecoordenadas(coordenadas)

    def __repr__(self):
        return "Nivel Dagua"
    
    def atribuicaodecoordenadas(self,coordenadas):
        self.coordenadas_x = [0 for i in range(0, len(coordenadas))]
        self.coordenadas_y = [0 for i in range(0, len(coordenadas))]
        for i in range(0, len(coordenadas)):
            self.coordenadas_x[i] = coordenadas[i][0]
            self.coordenadas_y[i] = coordenadas[i][1]
        self.dominio = self.superficie_terreno.dominio
        self.imagem = self.funcao(self.dominio)
    
    def atribuicaodecoordenadaslidas(self,cx,cy):
        self.coordenadas_x = cx
        self.coordenadas_y = cy
        self.dominio = self.superficie_terreno.dominio
        self.imagem = self.funcao(self.dominio)
 
    def funcao(self, x):
        return np.interp(x, self.coordenadas_x, self.coordenadas_y, left = np.nan, right = np.nan)
