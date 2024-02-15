import numpy as np
from config import INC
from perfil_logitudinal import Perfil_Longitudinal
from superficie_ruptura import Superficie_Ruptura

import matplotlib.pyplot as plt

class Fatia:
    def __init__(self, numero_fatia: int, perfil_longitudinal: Perfil_Longitudinal, superficie_ruptura, dx: float, forcas_dominio = None):
        self.numero_fatia = numero_fatia
        self.perfil_longitudinal = perfil_longitudinal
        self.superficie_ruptura = superficie_ruptura
        self.forcas_dominio = forcas_dominio
        self.dx = dx

        self.xi = self.superficie_ruptura.limites[0] + (numero_fatia - 1) * self.dx
        if (self.xi + self.dx) < self.superficie_ruptura.limites[1]:
            self.xf = self.xi + self.dx
        else:
            self.xf = self.superficie_ruptura.limites[1]
            self.dx = self.xf - self.xi
        self.xc = self.xi + (self.xf - self.xi) / 2
        

        self.yi_sup = self.perfil_longitudinal.superficie_terreno.funcao(self.xi)
        self.yi_inf = self.superficie_ruptura.funcao(self.xi)
        self.yi_inf = self.yi_inf[0]
        self.yf_sup = self.perfil_longitudinal.superficie_terreno.funcao(self.xf)
        self.yf_inf = self.superficie_ruptura.funcao(self.xf)[0]
        self.area_total = ((self.yi_sup - self.yi_inf) + (self.yf_sup - self.yf_inf)) * self.dx / 2
        #print('xi=', self.xi, 'xf=', self.xf, "yi_sup=", self.yi_sup, "yi_inf=", self.yi_inf, "yf_sup=", self.yf_sup,"yf_inf=", self.yf_inf)
        #print(self.superficie_ruptura.limites)
        m = (self.yf_inf - self.yi_inf)/(self.xf - self.xi)
        self.yc = self.yi_inf + m*(self.xc - self.xi)
        self.ym = -(self.yf_inf + self.yi_inf + self.yf_sup + self.yi_sup)/4
        self.xm = self.xc
        self.lista_camadas_red = self.reduz_camadas(self.perfil_longitudinal.lista_camadas)
        self.lista_camadas_red.append(self.perfil_longitudinal.superficie_terreno)
        
        self.sup_invalida = False
        #if self.lista_camadas_red[0].funcao(self.xc) > self.superficie_ruptura.funcao(self.xc):
        #    self.sup_invalida = True
        #elif self.numero_fatia == 1 and (self.yi_sup - self.yi_inf) > INC*2:
        #    self.sup_invalida = True
        #elif self.superficie_ruptura.limites[1] == self.xf and (self.yf_sup - self.yf_inf) > INC and (superficie_ruptura.y0 - self.yf_sup) > INC:
        #    self.sup_invalida = True
            
        self.peso = 0
        self.area_confere = 0
        
        for i in range(0, len(self.lista_camadas_red) - 1):
            if i == 0:
                yi_inter_inf = self.yi_inf
                yf_inter_inf = self.yf_inf
                yi_inter_sup = self.lista_camadas_red[i + 1].funcao(self.xi)
                yf_inter_sup = self.lista_camadas_red[i + 1].funcao(self.xf)


            else:
                yi_inter_inf = self.lista_camadas_red[i].funcao(self.xi)
                yf_inter_inf = self.lista_camadas_red[i].funcao(self.xf)
                yi_inter_sup = self.lista_camadas_red[i + 1].funcao(self.xi)
                yf_inter_sup = self.lista_camadas_red[i + 1].funcao(self.xf)

            yi_inter_inf = self.alonga_camada(yi_inter_inf, yf_inter_inf)
            yf_inter_inf = self.alonga_camada(yf_inter_inf, yi_inter_inf)
            yi_inter_sup = self.alonga_camada(yi_inter_sup, yf_inter_sup)
            yf_inter_sup = self.alonga_camada(yf_inter_sup, yi_inter_sup)

            yi_inter_inf = self.checa_logica_camada(yi_inter_inf, yi_inter_sup)
            yf_inter_inf = self.checa_logica_camada(yf_inter_inf, yf_inter_sup)


            yi_inter_inf = np.float64(yi_inter_inf)
            yf_inter_inf = np.float64(yf_inter_inf)
            yi_inter_sup = np.float64(yi_inter_sup)
            yf_inter_sup = np.float64(yf_inter_sup)


            area = ((yi_inter_sup - yi_inter_inf) + (yf_inter_sup - yf_inter_inf)) * self.dx / 2
            self.area_confere = self.area_confere + area
            self.peso = self.peso + (area * self.lista_camadas_red[i].solo.gama)
        if not forcas_dominio == None:
            for posicao in forcas_dominio:
                if posicao[0] > self.xi and posicao[0] < self.xf:
                    self.peso = self.peso + posicao[1]
                elif posicao[0] == self.xi or posicao[0] == self.xf:
                    self.peso = self.peso + posicao[1] / 2

        self.altura = ((self.yi_sup - self.yi_inf) + (self.yf_sup - self.yf_inf)) / 2
        self.alpha = np.arctan((self.yf_inf - self.yi_inf) / (self.xf - self.xi))
        self.dL = ((self.xi - self.xf) ** 2 + (self.yi_inf - self.yf_inf) ** 2) ** 0.5
        if np.isnan(self.perfil_longitudinal.nivel_agua.funcao(self.xc)):
            self.poropressao = [0]
        else:
            self.poropressao = (self.perfil_longitudinal.nivel_agua.funcao(self.xc) - self.superficie_ruptura.funcao(self.xc)) * 10
            if self.poropressao < 0:
                self.poropressao = [0]
        self.fi_base = self.lista_camadas_red[0].solo.fi
        self.coesao_base = self.lista_camadas_red[0].solo.coesao
        self.gama = self.lista_camadas_red[0].solo.gama
        self.beta = np.arctan((self.yf_sup - self.yi_sup) / (self.xf - self.xi))
        
        #Conferências
        self.diferença_absoluta_area = self.area_confere - self.area_total
        self.diferença_relativa_area = self.diferença_absoluta_area / self.area_total
        

    def __repr__(self):
        return "Fatia " + str(self.numero_fatia)
    
    def reduz_camadas(self, lista_camadas):
        lista_aux = []
        lista_aux_2 = []
        lista_aux_3 = []

        #print('xi=', self.xi, 'xf=', self.xf, "yi_sup=", self.yi_sup, "yi_inf=", self.yi_inf, "yf_sup=", self.yf_sup,"yf_inf=", self.yf_inf)

        if self.yi_sup < self.yf_sup:
            x_aux = self.xi
        else:
            x_aux = self.xf
        if self.yi_inf < self.yf_inf:
            y_aux = self.yi_inf
        else:
            y_aux = self.yf_inf

        for i in range(0, len(lista_camadas)):
            if not np.isnan(lista_camadas[i].funcao([x_aux])):
                lista_aux.append(lista_camadas[i])
        lista_aux = sorted(lista_aux, key = self.sort_camadas)
        #print(lista_aux)

        for i in range(0, len(lista_aux)):
            j = len(lista_aux) - i - 1
            lista_aux_2.append(lista_aux[j])
            #print(lista_aux[j].funcao([x_aux]), y_aux)
            if (lista_aux[j].funcao([x_aux])) < y_aux:
                break
        j = len(lista_aux_2) - 1
        for i in range(0, len(lista_aux_2)):
            lista_aux_3.append(lista_aux_2[- i - 1])

        return lista_aux_3

    def sort_camadas(self, camada):
      """Função para auxiliar a ordenação das camadas.
      Retorna o nível do limite inferior da camada para a posição inicial ou final da camada."""
      if self.yi_sup > self.yf_sup:
          x_aux = self.xi
      else:
        x_aux = self.xf
      return camada.funcao([x_aux])

    def alonga_camada (self, yi, yf):
      """Função que alonga a camada no caso dela não passar pela fatia inteira.
      Retorna o nível em que a camada cruza o limite da fatia, no caso de ser igual a np.nan, retorna o nível do outro limite da fatia."""
      if np.isnan(yi):
          yi = yf
      return yi

    def checa_logica_camada (self, y_inf, y_sup):
      """Função que checa se nenhum nível unferior é maior que um nível superior.
      Retorna o menor entre os dois níveis como nével inferior."""
      if y_inf > y_sup:
          y_inf = y_sup
      return y_inf
    
            