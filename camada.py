import numpy as np
import ezdxf as ez
from solo import Solo
from superficie_terreno import Superficie_Terreno

class Camada:
    
    def __init__(self, solo: Solo, superficie_terreno: Superficie_Terreno, caminho_arquivo=None ):
        self.superficie_terreno = superficie_terreno   
        self.solo = solo
        if caminho_arquivo==None:
            return
        self.caminho_arquivo = caminho_arquivo
        coordenadas = self.pega_pontos(self.caminho_arquivo)
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
    
    def pega_pontos(self, caminho_arquivo: str):
        doc = ez.readfile(caminho_arquivo)
        msp = doc.modelspace()
        pontos_aux = []
        for entidade in msp:
            dtype = entidade.dxftype()
            if dtype == "POLYLINE":
                pontos_aux.append(list(entidade.points()))
            elif dtype == "LWPOLYLINE":
                pontos_aux.append(list(entidade.get_points()))
            elif dtype == "LINE":
                aux = (list(entidade.dxf.start), list(entidade.dxf.end))
                pontos_aux.append(aux)
        pontos = [[0 for i in range(0, 2)] for j in range(0, len(pontos_aux[0]))]
        for i in range(0, len(pontos_aux[0])):
            pontos[i][0] = pontos_aux[0][i][0]
            pontos[i][1] = pontos_aux[0][i][1]
        if pontos[0][0] >  pontos[-1][0]:
            return pontos[::-1]    
        else:
            return pontos