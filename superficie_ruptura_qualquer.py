import numpy as np
import ezdxf as ez
from perfil_logitudinal import Perfil_Longitudinal
from superficie_terreno import Superficie_Terreno




class Superficie_Ruptura_Qualquer:
    
    def __init__(self, superficie_terreno, caminho_arquivo = None):
        self.superficie_terreno = superficie_terreno   
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
        self.x0 = np.nan
        self.y0 = np.nan
        self.raio = np.nan
        self.limites = self.encontra_limites()
        self.imagem_raio_esquerda = np.nan
        self.imagem_raio_direita = np.nan
        
    def atribuicaodecoordenadaslidas(self,cx,cy):
        self.coordenadas_x = cx
        self.coordenadas_y = cy
        self.dominio = self.superficie_terreno.dominio
        self.imagem = self.funcao(self.dominio)
        self.x0 = np.nan
        self.y0 = np.nan
        self.raio = np.nan
        self.limites = self.encontra_limites()
        self.imagem_raio_esquerda = np.nan
        self.imagem_raio_direita = np.nan
                
    def __repr__(self):
        return "Superfície de Ruptura"

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
        
    def encontra_limites(self):
        lista_lim_esquerdo = []
        lista_lim_direito = []
        tamanho_superficies = []
        limite_esquerdo = np.nan
        limite_direito = np.nan
        for i in range(0, len(self.dominio)):
            if i == 0 and not np.isnan(self.imagem[i]):
                lista_lim_esquerdo.append(self.dominio[i])
            elif np.isnan(self.imagem[i - 1]) and not np.isnan(self.imagem[i]) :
                lista_lim_esquerdo.append(self.dominio[i])

        for i in range(0, len(self.dominio)):
            if i == len(self.dominio) and self.imagem[i] is not np.nan:
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
            # print("foram encontradas mais de uma superfície") 
            for i in range(0, len(lista_lim_esquerdo)):
                tamanho_superficies.append(lista_lim_direito[i] - lista_lim_esquerdo[i])
            # print("tamanho dassuperfícies: ",tamanho_superficies)
            for i in range(0, len(tamanho_superficies)):
                if tamanho_superficies[i] == np.amax(tamanho_superficies):
                    limite_esquerdo = lista_lim_esquerdo[i]
                    limite_direito = lista_lim_direito[i]
                    return (limite_esquerdo, limite_direito)
        
    def funcao_mp(self,x, mi, nu):
        return np.sin(np.pi * ((x - self.limites[0])/(self.limites[1] - self.limites[0]))** nu) ** mi
    
    def funcao_sp(self,x):
        return 1