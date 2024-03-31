import numpy as np
import ezdxf as ez

import config
import lerarquivo


class Superficie_Terreno:
    
    def __init__(self, caminho_arquivo=None):
        if caminho_arquivo==None:
            return
        coordenadas = lerarquivo.pega_pontos(caminho_arquivo)
        self.atribuicaodecoordenadas(coordenadas)

    def __repr__(self):
        return "Superfície do terreno"
    
    def atribuicaodecoordenadas(self,coordenadas):
        self.coordenadas_x = [0 for i in range(0, len(coordenadas))]
        self.coordenadas_y = [0 for i in range(0, len(coordenadas))]
        for i in range(0, len(coordenadas)):
            self.coordenadas_x[i] = coordenadas[i][0]
            self.coordenadas_y[i] = coordenadas[i][1]
        self.dominio = np.arange(self.coordenadas_x[0], self.coordenadas_x[len(self.coordenadas_x) - 1], config.INC)
        self.imagem = self.funcao(self.dominio)
    
    def atribuicaodecoordenadaslidas(self,cx,cy):
        self.coordenadas_x = cx
        self.coordenadas_y = cy
        self.dominio = np.arange(self.coordenadas_x[0], self.coordenadas_x[len(self.coordenadas_x) - 1], config.INC)
        self.imagem = self.funcao(self.dominio)
                           
    def funcao(self, x: list[float]):
        return np.interp(x, self.coordenadas_x, self.coordenadas_y, left = np.nan, right = np.nan)
    
