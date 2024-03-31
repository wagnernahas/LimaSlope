import numpy as np
import ezdxf as ez
from solo import Solo
from superficie_terreno import Superficie_Terreno
import lerarquivo

class Camada:
    
    def __init__(self, solo: Solo, superficie_terreno: Superficie_Terreno, caminho_arquivo=None ):
        self.superficie_terreno = superficie_terreno   
        self.solo = solo
        if caminho_arquivo==None:
            return
        coordenadas = lerarquivo.pega_pontos(caminho_arquivo)
        self.atribuicaodecoordenadas(coordenadas)
    
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
        
    def __repr__(self):
        return self.solo.nomeclatura

    def funcao(self, x):
        if type(x) == np.float64:
            x = [x]
        y = [0 for i in range(0, len(x))]
        for i in range(0, len(x)):
            if self.superficie_terreno.funcao(x[i]) < np.interp(x[i], self.coordenadas_x, self.coordenadas_y, left = np.nan, right = np.nan):
                y[i] = np.nan
            else:
                y[i] = np.interp(x[i], self.coordenadas_x, self.coordenadas_y, left = np.nan, right = np.nan)
        return y
