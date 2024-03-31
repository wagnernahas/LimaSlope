import matplotlib.pyplot as plt
from perfil_logitudinal import Perfil_Longitudinal
from nivel_agua import Nivel_Agua
import utils
import numpy as np

def plota_grafico(perfil_longitudinal, superficie_ruptura, lista_fatias):
        
    plt.close("all")
    fig = plt.figure(figsize = (8,4))
    axes = fig.add_axes([0,0,1,1])

    #print(perfil_longitudinal.lista_camadas)
    if len(perfil_longitudinal.lista_camadas) > 1:
        plt_camadas = sorted(perfil_longitudinal.lista_camadas, key = utils.sort_camadas_imagem)
    else:
        plt_camadas = perfil_longitudinal.lista_camadas[:]
    plt_camadas.append(perfil_longitudinal.superficie_terreno)

    plt.fill_between(x = perfil_longitudinal.dominio, y1 = perfil_longitudinal.nivel_agua.imagem, y2 = plt_camadas[0].imagem, color = "blue",hatch = "/" ,alpha = 0.05)

    for i in range(0, len(plt_camadas) - 1):
        for j in range(0, len(plt_camadas[i].imagem)):
            if np.isnan(plt_camadas[i].imagem[j]):
                for k in range(i + 1, len(plt_camadas)):
                    if not np.isnan(plt_camadas[k].imagem[j]):
                        plt_camadas[i].imagem[j] = plt_camadas[k].imagem[j]
                        break

    for i in range(0, len(plt_camadas) - 1):
        plt.plot(plt_camadas[i].dominio, plt_camadas[i].imagem)
        plt.fill_between(x = perfil_longitudinal.dominio, y1 = plt_camadas[i].imagem, y2 = plt_camadas[i + 1].imagem, label = plt_camadas[i].solo.nomeclatura, alpha = 0.2)

    plt.plot(perfil_longitudinal.dominio, perfil_longitudinal.superficie_terreno.imagem, label = "Terreno", color = "brown", linewidth = 2)
    plt.plot(perfil_longitudinal.nivel_agua.dominio, perfil_longitudinal.nivel_agua.imagem, color = "blue", label = "NA", linewidth = 1, alpha = 0.9)
    plt.plot(superficie_ruptura.dominio, superficie_ruptura.imagem, color = "black")
    plt.scatter(superficie_ruptura.x0, superficie_ruptura.y0, color = 'black', marker = '.', label = 'Centro')
    plt.plot(superficie_ruptura.dominio, superficie_ruptura.imagem_raio, color = "black", linewidth = 1, linestyle = "--")

    for fatia in lista_fatias:
        plt.vlines(x = fatia.xf, ymin = fatia.yf_inf, ymax = fatia.yf_sup, color = 'black')

    plt.title('Slope Stability')
    plt.legend(loc = 0, fontsize = 'small')
    plt.xlabel('(m)')
    plt.ylabel('Cota (m)')
    plt.xlim([perfil_longitudinal.dominio[0], perfil_longitudinal.dominio[-1]])
    #plt.ylim(ylim_min, ylim_min + amplitude)
    plt.grid()
    plt.show()

    return