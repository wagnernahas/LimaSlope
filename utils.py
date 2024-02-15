from math import isnan, tan
import ezdxf as ez
from matplotlib import colors
import numpy as np
import pandas as pd
import config
from fatia import Fatia
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.colors as pltc

from camada import Camada
from fatia import Fatia
from nivel_agua import Nivel_Agua
from perfil_logitudinal import Perfil_Longitudinal
from solo import Solo
from superficie_ruptura import Superficie_Ruptura
from superficie_ruptura_qualquer import Superficie_Ruptura_Qualquer
from superficie_terreno import Superficie_Terreno
from nivel_agua import Nivel_Agua
from scipy.constants._constants import alpha
from numpy import arctan
from mpmath.calculus.optimization import ANewton




def arred_incremento(n: float, inc: float) -> float:
    """Funcao que faz isso isso e isso
        Parametros:
            n: asdhklasjalksd
            inc: alsdhahsdl
        Retorno:
            float """
    return np.ceil(n / inc) * inc

def arred(n, casas_decimais):
    return np.ceil(n * 10**casas_decimais) / 10**casas_decimais

def gera_fatias(perfil_longitudinal, superficie_ruptura, dx, forcas_dominio):
    lista_fatias = []
    if np.isnan(superficie_ruptura.limites[0]):
        pass
    else:
        for i in range(1, np.int64(np.ceil((superficie_ruptura.limites[1] - superficie_ruptura.limites[0]) / dx) + 1)):
            fatia_aux = Fatia(i, perfil_longitudinal, superficie_ruptura, dx, forcas_dominio)
            lista_fatias.append(fatia_aux)
            if fatia_aux.sup_invalida == True:
                lista_fatias =[]
                break
            if lista_fatias[i - 1].xf == superficie_ruptura.limites[1]:
                break
    return lista_fatias

def metodo_bishop_simplificado(lista_fatias):
    
    FS_iteracao = 0
    FS_iteracao_resultado = metodo_fellenius(lista_fatias)
    bishop_FSolicitante = 0
    bishop_FResistente = 0

    while abs(FS_iteracao - FS_iteracao_resultado) > 0.0001:
        FS_iteracao = FS_iteracao_resultado
        for fatia in lista_fatias:
            m_alpha = np.cos(fatia.alpha) * (1 + np.tan(fatia.alpha) * np.tan(fatia.fi_base) / FS_iteracao)
            bishop_FSolicitante = bishop_FSolicitante + (fatia.peso * np.sin(fatia.alpha))
            bishop_FResistente = bishop_FResistente + (fatia.coesao_base * fatia.dx + (fatia.peso - tira_lista(fatia.poropressao) * fatia.dx) * np.tan(fatia.fi_base)) * (1 / m_alpha)
        FS_iteracao_resultado = bishop_FResistente / bishop_FSolicitante
    return arred(FS_iteracao_resultado, 3)

def tabela_bishop_simplificado(lista_fatias):
    
    tabela_bishop_simplificado = {}
    
    for fatia in lista_fatias:    
        tabela_bishop_simplificado[str(fatia)] = [fatia.dx, fatia.altura, fatia.dL, fatia.alpha, fatia.peso, *fatia.poropressao, fatia.fi_base, fatia.coesao_base] 
    
    df_bishop_simplificado = pd.DataFrame.from_dict(tabela_bishop_simplificado, orient = 'index', columns = ["b (m)", "h (m)", "l (m)", "α (rad)", "W (kN/m)", "u (kPa)", "Φ' base (rad)", "c' base (kPa)"])
    
    df_bishop_simplificado["sen(α)"] = np.sin(df_bishop_simplificado["α (rad)"])
    df_bishop_simplificado["W x sen(α) (kN/m)"] = df_bishop_simplificado["W (kN/m)"] * df_bishop_simplificado["sen(α)"]
    df_bishop_simplificado["cos(α)"] = np.cos(df_bishop_simplificado["α (rad)"])
    df_bishop_simplificado["W x cos(α) (kN/m)"] = df_bishop_simplificado["W (kN/m)"] * df_bishop_simplificado["cos(α)"]
    df_bishop_simplificado["W - (u x b) (kN/m)"] = df_bishop_simplificado["W (kN/m)"] - (df_bishop_simplificado["u (kPa)"] * df_bishop_simplificado["b (m)"])
    df_bishop_simplificado["(W - (u x b)) x  tan(Φ') (kN/m)"] = df_bishop_simplificado["W - (u x b) (kN/m)"] * np.tan(df_bishop_simplificado["Φ' base (rad)"])
    df_bishop_simplificado["b x c' (kN/m)"] = df_bishop_simplificado["b (m)"] * df_bishop_simplificado["c' base (kPa)"]
    df_bishop_simplificado["b x c' + (W - (u x b)) x  tan(Φ') (kN/m)"] = df_bishop_simplificado["(W - (u x b)) x  tan(Φ') (kN/m)"] + df_bishop_simplificado["b x c' (kN/m)"]
    
    FS_iteracao = metodo_fellenius(lista_fatias)
    df_bishop_simplificado["mα FS= ", FS_iteracao] = df_bishop_simplificado["cos(α)"] * (1 + np.tan(df_bishop_simplificado["α (rad)"]) * np.tan(df_bishop_simplificado["Φ' base (rad)"]) / FS_iteracao)
    df_bishop_simplificado["b x c' + (W - (u x b)) x  tan(Φ') / mα FS= ", FS_iteracao, "(kN/m)"] = df_bishop_simplificado["b x c' + (W - (u x b)) x  tan(Φ') (kN/m)"] / df_bishop_simplificado["mα FS= ", FS_iteracao]
    df_bishop_simplificado.loc["SOMA"] = df_bishop_simplificado.sum()
    FS_iteracao_resultado = df_bishop_simplificado["b x c' + (W - (u x b)) x  tan(Φ') / mα FS= ", FS_iteracao, "(kN/m)"].sum() / df_bishop_simplificado["W x sen(α) (kN/m)"].sum()
    FS_iteracao_resultado = tira_lista(FS_iteracao_resultado)
    
    while abs(FS_iteracao - FS_iteracao_resultado) > 0.001:
        FS_iteracao =  arred(FS_iteracao_resultado, 3)
        df_bishop_simplificado["mα FS= ", FS_iteracao] = df_bishop_simplificado["cos(α)"] * (1 + np.tan(df_bishop_simplificado["α (rad)"]) * np.tan(df_bishop_simplificado["Φ' base (rad)"]) / FS_iteracao)
        df_bishop_simplificado["b x c' + (W - (u x b)) x  tan(Φ') / mα FS= ", FS_iteracao, "(kN/m)"] = df_bishop_simplificado["b x c' + (W - (u x b)) x  tan(Φ') (kN/m)"] / df_bishop_simplificado["mα FS= ", FS_iteracao]
        FS_iteracao_resultado = df_bishop_simplificado["b x c' + (W - (u x b)) x  tan(Φ') / mα FS= ", FS_iteracao, "(kN/m)"].sum() / df_bishop_simplificado["W x sen(α) (kN/m)"].sum()
        FS_iteracao_resultado = tira_lista(FS_iteracao_resultado)


    return df_bishop_simplificado, arred(FS_iteracao_resultado, 3)

def tabela(lista_fatias):
    
    tabela_fellenius = {}
    
    for fatia in lista_fatias:    
        tabela_fellenius[str(fatia)] = [fatia.dx, fatia.altura, fatia.dL, fatia.alpha, fatia.peso, *fatia.poropressao, fatia.fi_base, fatia.coesao_base, fatia.lista_camadas_red] 
    
    df_fellenius = pd.DataFrame.from_dict(tabela_fellenius, orient = 'index', columns = ["b (m)", "h (m)", "l (m)", "α (rad)", "W (kN/m)", "u (kPa)", "Φ' base (rad)", "c' base (kPa)", "camadas"])
    
    return df_fellenius

def tabela_fellenius(lista_fatias):
    
    tabela_fellenius = {}
    
    for fatia in lista_fatias:    
        tabela_fellenius[str(fatia)] = [fatia.dx, fatia.altura, fatia.dL, fatia.alpha, fatia.peso, *fatia.poropressao, fatia.fi_base, fatia.coesao_base, fatia.lista_camadas_red] 
    
    df_fellenius = pd.DataFrame.from_dict(tabela_fellenius, orient = 'index', columns = ["b (m)", "h (m)", "l (m)", "α (rad)", "W (kN/m)", "u (kPa)", "Φ' base (rad)", "c' base (kPa)", "camadas"])
    
    # df_fellenius["sen(α)"] = np.sin(df_fellenius["α (rad)"])
    # df_fellenius["W x sen(α) (kN/m)"] = df_fellenius["W (kN/m)"] * df_fellenius["sen(α)"]
    # df_fellenius["cos(α)"] = np.cos(df_fellenius["α (rad)"])
    # df_fellenius["W x cos(α) (kN/m)"] = df_fellenius["W (kN/m)"] * df_fellenius["cos(α)"]
    # df_fellenius["u x l (kN/m)"] = df_fellenius["u (kPa)"] * df_fellenius["l (m)"]
    # df_fellenius["W x cos(α) - u x l (kN/m)"] = df_fellenius["W x cos(α) (kN/m)"] - df_fellenius["u x l (kN/m)"]
    # df_fellenius["(W x cos(α) - u x l) x tan(Φ') (kN/m)"] = df_fellenius["W x cos(α) - u x l (kN/m)"] * np.tan(df_fellenius["Φ' base (rad)"]) 
    # df_fellenius["c' base x l (kN/m)"] = df_fellenius["c' base (kPa)"] * df_fellenius["l (m)"]
    # df_fellenius["(W x cos(α) - u x l) x tan(Φ') + c' base x l (kN/m)"] = df_fellenius["c' base x l (kN/m)"] + df_fellenius["(W x cos(α) - u x l) x tan(Φ') (kN/m)"]
    # df_fellenius.loc["SOMA"] = df_fellenius.sum()
    
    # fellenius_FResistente = df_fellenius["(W x cos(α) - u x l) x tan(Φ') + c' base x l (kN/m)"].sum()
    # fellenius_FSolicitante = df_fellenius["W x sen(α) (kN/m)"].sum()
    # fellenius_FS = fellenius_FResistente / fellenius_FSolicitante
    # fellenius_FS = tira_lista(fellenius_FS)
    return df_fellenius

def metodo_fellenius(lista_fatias):
    
    fellenius_FSolicitante = 0
    fellenius_FResistente = 0
    for fatia in lista_fatias:
        #print(fatia,"Peso",fatia.peso,"alpha", fatia.alpha,"coesão", fatia.coesao_base,"dL", fatia.dL,"U", fatia.poropressao,"FI", fatia.fi_base)    
        fellenius_FSolicitante = fellenius_FSolicitante + (fatia.peso * np.sin(fatia.alpha))
        fellenius_FResistente = fellenius_FResistente + (fatia.coesao_base * fatia.dL + (fatia.peso * np.cos(fatia.alpha) - tira_lista(fatia.poropressao) * fatia.dL) * np.tan(fatia.fi_base))
    fellenius_FS = arred(fellenius_FResistente / fellenius_FSolicitante, 3)
    return tira_lista(fellenius_FS)

def metodo_morgenstern_price(lista_fatias, superficie_ruptura):
    
    FS_mp_inicial = 1
    lambda_mp_inicial = 0.5
    elementos_mp = [[0 for i in range(0, 6)] for j in range(0, len(lista_fatias))]
    mi = 3
    nu = 0.5
    n = len(lista_fatias)
    dif_mp_lambda = 0.5
    dif_mp_FS = 1
    tol = 0.0001
    iteracao = 0

    lambda_mp_iteracao = lambda_mp_inicial
    FS_mp_iteracao_secundaria = FS_mp_inicial

    while dif_mp_FS > tol or dif_mp_lambda > tol:
        iteracao = iteracao + 1
        lambda_mp_inicial = lambda_mp_iteracao
        FS_mp_inicial = FS_mp_iteracao_secundaria
        if iteracao == 100:
            return arred(FS_mp_iteracao_secundaria,3)


        lim_esq = superficie_ruptura.limites[0]
        for i in range (0, n):
            lim_dir = lim_esq + lista_fatias[i].dx
            #U
            elementos_mp[i][0] = tira_lista(lista_fatias[i].poropressao) * lista_fatias[i].dx / np.cos(lista_fatias[i].alpha)
            #T
            elementos_mp[i][1] = lista_fatias[i].peso*np.sin(lista_fatias[i].alpha)
            #R
            elementos_mp[i][2] = (lista_fatias[i].peso*np.cos(lista_fatias[i].alpha) - elementos_mp[i][0]) * np.tan(lista_fatias[i].fi_base) + lista_fatias[i].coesao_base * lista_fatias[i].dx / np.cos(lista_fatias[i].alpha)
            #FI
            if i == 0:
                elementos_mp[i][3] = (np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_esq, mi, nu) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_esq, mi, nu) * np.sin(lista_fatias[i].alpha)) * FS_mp_inicial
                elementos_mp[i+1][3] = (np.sin(lista_fatias[i + 1].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.cos(lista_fatias[i + 1].alpha)) * np.tan(lista_fatias[i + 1].fi_base) + (np.cos(lista_fatias[i + 1].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.sin(lista_fatias[i + 1].alpha)) * FS_mp_inicial       
            elif i == (n-1):
                pass
            else:
                elementos_mp[i+1][3] = (np.sin(lista_fatias[i + 1].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.cos(lista_fatias[i + 1].alpha)) * np.tan(lista_fatias[i + 1].fi_base) + (np.cos(lista_fatias[i + 1].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.sin(lista_fatias[i + 1].alpha)) * FS_mp_inicial
            #PSI
            if i == 0:
                elementos_mp[i][4] = 1
                elementos_mp[i+1][4] = ((np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.sin(lista_fatias[i].alpha)) * FS_mp_inicial) / elementos_mp[i+1][3]
            elif i == (n-1):
                pass
            else:
                elementos_mp[i+1][4] = ((np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.sin(lista_fatias[i].alpha)) * FS_mp_inicial) / elementos_mp[i+1][3]
            
            lim_esq = lim_dir
        produtorio_psi = [1 for i in range(0, n)]
        for i in range(0, n):
            for j in range(0, i+1):
                produtorio_psi[i] = produtorio_psi[i] * elementos_mp[j][4]
        
        FS_mp_solicitante = 0
        FS_mp_resistente = 0
        for i in range(0, n):
            FS_mp_solicitante = FS_mp_solicitante + elementos_mp[i][1] * produtorio_psi[i]
            FS_mp_resistente = FS_mp_resistente + elementos_mp[i][2] * produtorio_psi[i]
        FS_mp_iteracao_primaria = FS_mp_resistente / FS_mp_solicitante
        
        #print("lambda",dif_mp_lambda, "FS",dif_mp_FS ,"FS_1it",FS_mp_iteracao_primaria)

        lim_esq = superficie_ruptura.limites[0]
        for i in range (0, n):
            lim_dir = lim_esq + lista_fatias[i].dx
        #FI
            if i == 0:
                elementos_mp[i][3] = (np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_esq, mi, nu) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_esq, mi, nu) * np.sin(lista_fatias[i].alpha)) * FS_mp_iteracao_primaria
                elementos_mp[i+1][3] = (np.sin(lista_fatias[i + 1].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.cos(lista_fatias[i + 1].alpha)) * np.tan(lista_fatias[i + 1].fi_base) + (np.cos(lista_fatias[i + 1].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.sin(lista_fatias[i + 1].alpha)) * FS_mp_iteracao_primaria       
            elif i == (n-1):
                pass
            else:
                elementos_mp[i+1][3] = (np.sin(lista_fatias[i + 1].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.cos(lista_fatias[i + 1].alpha)) * np.tan(lista_fatias[i + 1].fi_base) + (np.cos(lista_fatias[i + 1].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.sin(lista_fatias[i + 1].alpha)) * FS_mp_iteracao_primaria
            #PSI
            if i == 0:
                elementos_mp[i][4] = 1
                elementos_mp[i+1][4] = ((np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.sin(lista_fatias[i].alpha)) * FS_mp_iteracao_primaria) / elementos_mp[i+1][3]
            elif i == (n-1):
                pass
            else:
                elementos_mp[i+1][4] = ((np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_mp(lim_dir, mi, nu) * np.sin(lista_fatias[i].alpha)) * FS_mp_iteracao_primaria) / elementos_mp[i+1][3]
            lim_esq = lim_dir     

        produtorio_psi = [1 for i in range(0, n)]
        for i in range(0, n):
            for j in range(0, i+1):
                produtorio_psi[i] = produtorio_psi[i] * elementos_mp[j][4]
        
        FS_mp_solicitante = 0
        FS_mp_resistente = 0
        for i in range(0, n):
            FS_mp_solicitante = FS_mp_solicitante + elementos_mp[i][1] * produtorio_psi[i]
            FS_mp_resistente = FS_mp_resistente + elementos_mp[i][2] * produtorio_psi[i]
        FS_mp_iteracao_secundaria = FS_mp_resistente / FS_mp_solicitante

        

        for i in range(1, n+1):
            j = -i
            if i == 1:
                elementos_mp[j][5] = (FS_mp_iteracao_secundaria * elementos_mp[j][1] - elementos_mp[j][2]) / elementos_mp[j][3]
            else:
                elementos_mp[j][5] = (elementos_mp[j+1][4]* elementos_mp[j+1][5] * elementos_mp[j+1][3] + FS_mp_iteracao_secundaria * elementos_mp[j][1] - elementos_mp[j][2]) / elementos_mp[j][3]
            # print("lambda",lambda_mp_iteracao_primaria, "FS",FS_mp_inicial,elementos_mp[j][5])
           

        numerador_lambda = 0
        denominador_lambda = 0
        lim_dir = superficie_ruptura.limites[1]
        for i in range(1, n + 1):
            j = -i
            lim_esq = lim_dir - lista_fatias[j].dx
            if i == 1:
                numerador_lambda = numerador_lambda + (lista_fatias[j].dx * (elementos_mp[j][5]) * np.tan(lista_fatias[j].alpha))
                denominador_lambda = denominador_lambda + (lista_fatias[j].dx * (superficie_ruptura.funcao_mp(lim_esq, mi, nu) * elementos_mp[j][5]))
            elif i == n:
                numerador_lambda = numerador_lambda + (lista_fatias[j].dx * (elementos_mp[j][5] + elementos_mp[j+1][5]) * np.tan(lista_fatias[j].alpha))
                denominador_lambda = denominador_lambda + (lista_fatias[j].dx * (superficie_ruptura.funcao_mp(superficie_ruptura.limites[0], mi, nu) * elementos_mp[j][5] + superficie_ruptura.funcao_mp(lim_dir, mi, nu) * elementos_mp[j+1][5]))
            else:
                numerador_lambda = numerador_lambda + (lista_fatias[j].dx * (elementos_mp[j][5] + elementos_mp[j+1][5]) * np.tan(lista_fatias[j].alpha))
                denominador_lambda = denominador_lambda + (lista_fatias[j].dx * (superficie_ruptura.funcao_mp(lim_esq, mi, nu) * elementos_mp[j][5] + superficie_ruptura.funcao_mp(lim_dir, mi, nu) * elementos_mp[j+1][5]))
            lim_dir = lim_esq
        lambda_mp_iteracao = numerador_lambda / denominador_lambda
        dif_mp_FS = abs(FS_mp_inicial - FS_mp_iteracao_secundaria)
        dif_mp_lambda = abs(lambda_mp_inicial - lambda_mp_iteracao)
        
    return arred(FS_mp_iteracao_secundaria,3)

def metodo_spencer(lista_fatias, superficie_ruptura):
    
    FS_mp_inicial = 1
    lambda_mp_inicial = 0.5
    elementos_mp = [[0 for i in range(0, 6)] for j in range(0, len(lista_fatias))]
    mi = 0.5
    nu = 0.5
    n = len(lista_fatias)
    dif_mp_lambda = 0.5
    dif_mp_FS = 1
    tol = 0.0001
    iteracao = 0

    lambda_mp_iteracao = lambda_mp_inicial
    FS_mp_iteracao_secundaria = FS_mp_inicial

    while dif_mp_FS > tol or dif_mp_lambda > tol:
        iteracao = iteracao + 1
        lambda_mp_inicial = lambda_mp_iteracao
        FS_mp_inicial = FS_mp_iteracao_secundaria
        if iteracao == 100:
            return arred(FS_mp_iteracao_secundaria,3)

        lim_esq = superficie_ruptura.limites[0]
        for i in range (0, n):
            lim_dir = lim_esq + lista_fatias[i].dx
            #U
            elementos_mp[i][0] = tira_lista(lista_fatias[i].poropressao) * lista_fatias[i].dx / np.cos(lista_fatias[i].alpha)
            #T
            elementos_mp[i][1] = lista_fatias[i].peso*np.sin(lista_fatias[i].alpha)
            #R
            elementos_mp[i][2] = (lista_fatias[i].peso*np.cos(lista_fatias[i].alpha) - elementos_mp[i][0]) * np.tan(lista_fatias[i].fi_base) + lista_fatias[i].coesao_base * lista_fatias[i].dx / np.cos(lista_fatias[i].alpha)
            #FI
            if i == 0:
                elementos_mp[i][3] = (np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_esq) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_esq) * np.sin(lista_fatias[i].alpha)) * FS_mp_inicial
                elementos_mp[i+1][3] = (np.sin(lista_fatias[i + 1].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.cos(lista_fatias[i + 1].alpha)) * np.tan(lista_fatias[i + 1].fi_base) + (np.cos(lista_fatias[i + 1].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.sin(lista_fatias[i + 1].alpha)) * FS_mp_inicial       
            elif i == (n-1):
                pass
            else:
                elementos_mp[i+1][3] = (np.sin(lista_fatias[i + 1].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.cos(lista_fatias[i + 1].alpha)) * np.tan(lista_fatias[i + 1].fi_base) + (np.cos(lista_fatias[i + 1].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.sin(lista_fatias[i + 1].alpha)) * FS_mp_inicial
            #PSI
            if i == 0:
                elementos_mp[i][4] = 1
                elementos_mp[i+1][4] = ((np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.sin(lista_fatias[i].alpha)) * FS_mp_inicial) / elementos_mp[i+1][3]
            elif i == (n-1):
                pass
            else:
                elementos_mp[i+1][4] = ((np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.sin(lista_fatias[i].alpha)) * FS_mp_inicial) / elementos_mp[i+1][3]
            
            lim_esq = lim_dir
        produtorio_psi = [1 for i in range(0, n)]
        for i in range(0, n):
            for j in range(0, i+1):
                produtorio_psi[i] = produtorio_psi[i] * elementos_mp[j][4]
        
        FS_mp_solicitante = 0
        FS_mp_resistente = 0
        for i in range(0, n):
            FS_mp_solicitante = FS_mp_solicitante + elementos_mp[i][1] * produtorio_psi[i]
            FS_mp_resistente = FS_mp_resistente + elementos_mp[i][2] * produtorio_psi[i]
        FS_mp_iteracao_primaria = FS_mp_resistente / FS_mp_solicitante
        
        #print("lambda",dif_mp_lambda, "FS",dif_mp_FS ,"FS_1it",FS_mp_iteracao_primaria)

        lim_esq = superficie_ruptura.limites[0]
        for i in range (0, n):
            lim_dir = lim_esq + lista_fatias[i].dx
        #FI
            if i == 0:
                elementos_mp[i][3] = (np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_esq) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_esq) * np.sin(lista_fatias[i].alpha)) * FS_mp_iteracao_primaria
                elementos_mp[i+1][3] = (np.sin(lista_fatias[i + 1].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.cos(lista_fatias[i + 1].alpha)) * np.tan(lista_fatias[i + 1].fi_base) + (np.cos(lista_fatias[i + 1].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.sin(lista_fatias[i + 1].alpha)) * FS_mp_iteracao_primaria       
            elif i == (n-1):
                pass
            else:
                elementos_mp[i+1][3] = (np.sin(lista_fatias[i + 1].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.cos(lista_fatias[i + 1].alpha)) * np.tan(lista_fatias[i + 1].fi_base) + (np.cos(lista_fatias[i + 1].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.sin(lista_fatias[i + 1].alpha)) * FS_mp_iteracao_primaria
            #PSI
            if i == 0:
                elementos_mp[i][4] = 1
                elementos_mp[i+1][4] = ((np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.sin(lista_fatias[i].alpha)) * FS_mp_iteracao_primaria) / elementos_mp[i+1][3]
            elif i == (n-1):
                pass
            else:
                elementos_mp[i+1][4] = ((np.sin(lista_fatias[i].alpha) - lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.cos(lista_fatias[i].alpha)) * np.tan(lista_fatias[i].fi_base) + (np.cos(lista_fatias[i].alpha) + lambda_mp_inicial * superficie_ruptura.funcao_sp(lim_dir) * np.sin(lista_fatias[i].alpha)) * FS_mp_iteracao_primaria) / elementos_mp[i+1][3]
            lim_esq = lim_dir     

        produtorio_psi = [1 for i in range(0, n)]
        for i in range(0, n):
            for j in range(0, i+1):
                produtorio_psi[i] = produtorio_psi[i] * elementos_mp[j][4]
        
        FS_mp_solicitante = 0
        FS_mp_resistente = 0
        for i in range(0, n):
            FS_mp_solicitante = FS_mp_solicitante + elementos_mp[i][1] * produtorio_psi[i]
            FS_mp_resistente = FS_mp_resistente + elementos_mp[i][2] * produtorio_psi[i]
        FS_mp_iteracao_secundaria = FS_mp_resistente / FS_mp_solicitante

        

        for i in range(1, n+1):
            j = -i
            if i == 1:
                elementos_mp[j][5] = (FS_mp_iteracao_secundaria * elementos_mp[j][1] - elementos_mp[j][2]) / elementos_mp[j][3]
            else:
                elementos_mp[j][5] = (elementos_mp[j+1][4]* elementos_mp[j+1][5] * elementos_mp[j+1][3] + FS_mp_iteracao_secundaria * elementos_mp[j][1] - elementos_mp[j][2]) / elementos_mp[j][3]
            # print("lambda",lambda_mp_iteracao_primaria, "FS",FS_mp_inicial,elementos_mp[j][5])
           

        numerador_lambda = 0
        denominador_lambda = 0
        lim_dir = superficie_ruptura.limites[1]
        for i in range(1, n + 1):
            j = -i
            lim_esq = lim_dir - lista_fatias[j].dx
            if i == 1:
                numerador_lambda = numerador_lambda + (lista_fatias[j].dx * (elementos_mp[j][5]) * np.tan(lista_fatias[j].alpha))
                denominador_lambda = denominador_lambda + (lista_fatias[j].dx * (superficie_ruptura.funcao_sp(lim_dir) * elementos_mp[j][5]))
            elif i == n:
                numerador_lambda = numerador_lambda + (lista_fatias[j].dx * (elementos_mp[j][5] + elementos_mp[j+1][5]) * np.tan(lista_fatias[j].alpha))
                denominador_lambda = denominador_lambda + (lista_fatias[j].dx * (superficie_ruptura.funcao_sp(lim_dir) * elementos_mp[j][5] + superficie_ruptura.funcao_sp(lim_dir) * elementos_mp[j+1][5]))
            else:
                numerador_lambda = numerador_lambda + (lista_fatias[j].dx * (elementos_mp[j][5] + elementos_mp[j+1][5]) * np.tan(lista_fatias[j].alpha))
                denominador_lambda = denominador_lambda + (lista_fatias[j].dx * (superficie_ruptura.funcao_sp(lim_dir) * elementos_mp[j][5] + superficie_ruptura.funcao_sp(lim_dir) * elementos_mp[j+1][5]))
            lim_dir = lim_esq
        lambda_mp_iteracao = numerador_lambda / denominador_lambda
        dif_mp_FS = abs(FS_mp_inicial - FS_mp_iteracao_secundaria)
        dif_mp_lambda = abs(lambda_mp_inicial - lambda_mp_iteracao)
        
    return arred(FS_mp_iteracao_secundaria,3)

def metodo_sarma(lista_fatias, superficie_ruptura):
    
    FS_sp_inicial = 1
    K_sarma = 1
    Kc = 0
    lambda_sp_inicial = 0.5
    elementos_sp = [[0 for i in range(0, 6)] for j in range(0, len(lista_fatias))]
    n = len(lista_fatias)
    dif_sp_lambda = 1
    dif_sp_FS = 1
    tol = 0.0001

    lambda_sp_iteracao_primaria = lambda_sp_inicial
    lambda_sp_iteracao_secundaria = lambda_sp_iteracao_primaria
    
    FS_sp_iteracao_secundaria = FS_sp_inicial
    
    wt = 0
    wx = 0
    wy = 0
    for i in range (0, n):
        wt = wt + lista_fatias[i].peso
        wx = wx + lista_fatias[i].peso * lista_fatias[i].xm
        wy = wy + lista_fatias[i].peso * lista_fatias[i].ym
    xG = wx/wt  
    yG = wy/wt  
    print(xG,yG)      
    while (K_sarma - Kc ) > tol:
        lambda_sp_iteracao_primaria = lambda_sp_iteracao_secundaria
        FS_sp_inicial = FS_sp_iteracao_secundaria
        S1 = 0 
        for i in range (0, n):
            #A = 4.c'.Cosf'/g.H
            f = 1
            alpha = lista_fatias[i].alpha
            beta = 2*lista_fatias[i].alpha-lista_fatias[i].fi_base
            U = lista_fatias[i].poropressao
            ru = U[0] / 10
            Hi = lista_fatias[i].altura
            
            gama = lista_fatias[i].gama
            fi = lista_fatias[i].fi_base
            psi = np.arctan(np.tan(fi)/FS_sp_iteracao_secundaria)
            c= lista_fatias[i].coesao_base
            #valores medio na camada
            gama_b = lista_fatias[i].gama
            fi_b = 29.3*np.pi/180#lista_fatias[i].fi_base
            c_b= 39.24#lista_fatias[i].coesao_base
            b = lista_fatias[i].dL
            w = lista_fatias[i].peso
            
            A = 4 * lista_fatias[i].coesao_base * np.cos(lista_fatias[i].fi_base) / (lista_fatias[i].altura * lista_fatias[i].gama)
            B = (1 - 2*ru)*np.sin(lista_fatias[i].fi_base)
            li = lista_fatias[i].dL
            Ki = (1-np.sin(beta)*(B+A))/(1+np.sin(beta)*np.sin(lista_fatias[i].fi_base))
            
            ru_b = 2 * lista_fatias[i].poropressao[0] / ((lista_fatias[i].gama)*lista_fatias[i].altura)
            
            Qi = f *((Ki - ru_b)*(gama_b*Hi*Hi*np.tan(fi_b))/2+c_b*Hi)
       
            elementos_sp[i][0] = Qi
            
            E = 1/(np.cos(alpha))*1/(np.cos(alpha))
            Di = w * np.tan(psi-alpha)+(c*li*np.cos(psi)-U[0]*np.sin(psi))*(1/np.cos(psi-alpha))
            elementos_sp[i][1] = Di
            
            
            S1 = S1 + Di
        S2 = 0
        S3 = 0
        S4 = 0
        for i in range (0, n):
            psi = np.arctan(np.tan(fi)/FS_sp_iteracao_secundaria)
            alpha = lista_fatias[i].alpha
            Di = elementos_sp[i][1]
            w = lista_fatias[i].peso
            if i == 0:
                P1 = elementos_sp[i+1][0]
            elif i == n-1:
                P1 = -elementos_sp[i][0]
            else:
                P1 = (elementos_sp[i+1][0]-elementos_sp[i][0])
            S3 = S3 + P1*((lista_fatias[i].ym-yG)*np.tan(psi-alpha)+(lista_fatias[i].xm-xG))
            S2 = S2 + P1
            S4 = S4 + w*(lista_fatias[i].xm-xG) + Di*(lista_fatias[i].ym-yG)
            #print(P1)
        K_sarma = 0.0000001
    lamb = S4/S3
    k = (S1 -lamb*S2)/wt 
    print(k,FS_sp_iteracao_secundaria)
    return arred(FS_sp_iteracao_secundaria,3)

def pega_pontos(caminho_arquivo: str):
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

def sort_camadas_imagem_empate(camada):
    return 1 / (np.nanmin(camada.imagem))

def sort_camadas_imagem(camada):
    if np.nanmin(camada.imagem) == 0:
        return np.nanmax(camada.imagem), 1 / (np.nanmin(camada.imagem) + config.INC)
    else:
        return np.nanmax(camada.imagem), 1 / np.nanmin(camada.imagem)

def tira_lista(x):
    if type(x) == np.ndarray and len(x) == 1:
        x = x[0]
    elif type(x) == list and len(x) == 1:
        x = x[0]
    return x

def compila_forcas(dominio, lista_forcas):
    dominio_forcas = np.copy(dominio)
    dominio_forcas = [[i,0] for i in dominio_forcas]
    for forca in lista_forcas:
        if isinstance(forca.forca, list):
            for i in range(0, len(dominio)):
                if dominio[i] >= arred_incremento(forca.posicao[0],config.INC) and dominio[i] <= arred_incremento(forca.posicao[1],config.INC):
                    dominio_forcas[i][1] = dominio_forcas[i][1] + np.interp(dominio[i], forca.posicao, forca.forca) * config.INC 
        else:
            for i in range(0, len(dominio)):
                if config.INC/2 > np.abs(dominio[i] - arred_incremento(forca.posicao,config.INC)):
                    dominio_forcas[i][1] = dominio_forcas[i][1] + forca.forca
    return dominio_forcas

def plota_forcas(dominio, lista_forcas):
    forcas_comp = np.copy(dominio)
    forcas_comp = [[i,0] for i in forcas_comp]
    imagem_forcas = [0 for i in forcas_comp]
    dominio_forcas = [0 for i in forcas_comp]
    for forca in lista_forcas:
        if isinstance(forca.forca, list):
            for i in range(0, len(dominio)):
                if dominio[i] >= arred_incremento(forca.posicao[0],config.INC) and dominio[i] <= arred_incremento(forca.posicao[1],config.INC):
                    forcas_comp[i][1] = forcas_comp[i][1] + np.interp(dominio[i], forca.posicao, forca.forca)
        else:
            for i in range(0, len(dominio)):
                if config.INC/2 > np.abs(dominio[i] - arred_incremento(forca.posicao,config.INC)):
                    forcas_comp[i][1] = forcas_comp[i][1] + forca.forca

        for i in range(0, len(forcas_comp)):
            dominio_forcas[i] = forcas_comp[i][0]
            imagem_forcas[i] = forcas_comp[i][1]
    return dominio_forcas, imagem_forcas

def ordena_inicial_final(x_i, x_f):
    if x_i > x_f:
        aux = x_i
        x_i = x_f
        x_f = aux
    elif x_i == x_f:
        x_f = x_f + 0,1
    return x_i, x_f

def plota_grafico(perfil_longitudinal, superficie_ruptura, lista_fatias, x_heat_map, y_heat_map, FS_heat_map):
        
    fig = plt.figure(figsize = (8,4))
    axes = fig.add_axes([0,0,1,1])
    
    #print(perfil_longitudinal.lista_camadas)
    if len(perfil_longitudinal.lista_camadas) > 1:
        plt_camadas = sorted(perfil_longitudinal.lista_camadas, key = sort_camadas_imagem)
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
    plt.plot(superficie_ruptura.dominio, superficie_ruptura.imagem_raio_esquerda, color = "black", linewidth = 1, linestyle = "--")
    plt.plot(superficie_ruptura.dominio, superficie_ruptura.imagem_raio_direita, color = "black", linewidth = 1, linestyle = "--")

    for fatia in lista_fatias:
        plt.vlines(x = fatia.xf, ymin = fatia.yf_inf, ymax = fatia.yf_sup, color = 'black')

    plt.title('Slope Stability')
    plt.legend(loc = 0, fontsize = 'small')
    plt.xlabel('(m)')
    plt.ylabel('Cota (m)')
    plt.xlim([perfil_longitudinal.dominio[0], perfil_longitudinal.dominio[-1]])
    #plt.ylim(ylim_min, ylim_min + amplitude)
    plt.grid()

    plt.contourf(x_heat_map, y_heat_map, FS_heat_map, colors=['red', 'orange','yellow','green'])
    plt.colorbar()
    
    plt.show()

    return

def analisa_FS_pelo_raio(perfil_longitudinal, xc_i, xc_f, yc_i, yc_f, incremento_centro, raio_i, raio_f, incremento_raio, dx, forcas_dominio=None):


    xc_i = arred_incremento(xc_i, incremento_centro)
    xc_f = arred_incremento(xc_f, incremento_centro)
    yc_i = arred_incremento(yc_i, incremento_centro)
    yc_f = arred_incremento(yc_f, incremento_centro)
    raio_i = arred_incremento(raio_i, incremento_raio)
    raio_f = arred_incremento(raio_f, incremento_raio)

    #print("inicio x: ",xc_i, "fim x:", xc_f, "inicio y: ",yc_i, "fim y:", yc_f, "inicio r: ",raio_i, "fim r:", raio_f)

    (xc_i, xc_f) = ordena_inicial_final(xc_i, xc_f)
    (yc_i, yc_f) = ordena_inicial_final(yc_i, yc_f)
    (raio_i, raio_f) = ordena_inicial_final(raio_i, raio_f)

    delta_xc = xc_f - xc_i
    delta_yc = yc_f - yc_i
    n_posicoes_xc = round(delta_xc / incremento_centro)
    n_posicoes_yc = round(delta_yc / incremento_centro)
    
    delta_raio = raio_f - raio_i
    n_posicoes_raio = round(delta_raio / incremento_raio)


    FS = [[[[0 for l in range(0, 10)] for k in range(0, n_posicoes_raio)] for j in range(0, n_posicoes_yc)]for i in range(0, n_posicoes_xc)]

    local_menor_FS = [[0, 0, 0]]
    for i in range(0, n_posicoes_xc):
        for j in range(0, n_posicoes_yc):
            for k in range(0, n_posicoes_raio):
                FS[i][j][k][0] = xc_i + i * incremento_centro
                FS[i][j][k][1] = yc_i + j * incremento_centro
                FS[i][j][k][2] = raio_i + k * incremento_centro
                FS[i][j][k][3] = Superficie_Ruptura(perfil_longitudinal, FS[i][j][k][0], FS[i][j][k][1], FS[i][j][k][2])
                FS[i][j][k][4] = gera_fatias(perfil_longitudinal, FS[i][j][k][3], dx, forcas_dominio)
                if len(FS[i][j][k][4]) < 3:
                    FS[i][j][k][5] = np.nan
                    FS[i][j][k][6] = np.nan
                    FS[i][j][k][7] = np.nan
                    FS[i][j][k][8] = np.nan
                    FS[i][j][k][9] = np.nan
                else: 
                    FS[i][j][k][5] = metodo_fellenius(FS[i][j][k][4])
                    FS[i][j][k][6] = metodo_bishop_simplificado(FS[i][j][k][4])
                    FS[i][j][k][7] = metodo_morgenstern_price(FS[i][j][k][4], FS[i][j][k][3])
                    FS[i][j][k][8] = metodo_spencer(FS[i][j][k][4], FS[i][j][k][3])
                    FS[i][j][k][9] = metodo_sarma(FS[i][j][k][4], FS[i][j][k][3])
                    if i == 0 and j == 0 and k == 0:
                        pass
                    elif FS[i][j][k][6] < FS[local_menor_FS[0][0]][local_menor_FS[0][1]][local_menor_FS[0][2]][6]:
                        local_menor_FS = [[i, j, k]]
                    # elif FS[i][j][k][6] == FS[local_menor_FS[0][0]][local_menor_FS[0][1]][local_menor_FS[0][2]][6]:
                    #     local_menor_FS.append([i, j, k])
                    elif np.isnan(FS[local_menor_FS[0][0]][local_menor_FS[0][1]][local_menor_FS[0][2]][6]):
                        local_menor_FS = [[i, j, k]]                     
                    else:
                        pass
    return FS, local_menor_FS

def analisa_FS_pela_superficie(perfil_longitudinal, superficie_ruptura_qualquer , dx, forcas_comp=None):

    FS = [[[[0 for l in range(0, 10)] for k in range(0, 1)] for j in range(0, 1)]for i in range(0, 1)]

    FS[0][0][0][0] = None
    FS[0][0][0][1] = None
    FS[0][0][0][2] = None
    FS[0][0][0][3] = superficie_ruptura_qualquer
    FS[0][0][0][4] = gera_fatias(perfil_longitudinal, FS[0][0][0][3], dx, forcas_comp)
    if len(FS[0][0][0][4]) < 3:
        FS[0][0][0][5] = np.nan
        FS[0][0][0][6] = np.nan
        FS[0][0][0][7] = np.nan
        FS[0][0][0][8] = np.nan
        FS[0][0][0][9] = np.nan
    else: 
        FS[0][0][0][5] = "-" #metodo_fellenius(FS[0][0][0][4])
        FS[0][0][0][6] = "-" #metodo_bishop_simplificado(FS[0][0][0][4])
        FS[0][0][0][7] = metodo_morgenstern_price(FS[0][0][0][4], FS[0][0][0][3])
        FS[0][0][0][8] = metodo_spencer(FS[0][0][0][4], FS[0][0][0][3])
        FS[0][0][0][9] = metodo_sarma(FS[0][0][0][4], FS[0][0][0][3])
    local_menor_FS = [[0, 0, 0]]
    return FS, local_menor_FS

def mapa_calor(FS, raio):
    mapa_de_calor = np.zeros([len(FS), len(FS[0])])

    aux_x = []

    for k in range (0, len(FS[0][0])):
        for j in range (0, len(FS[0])):
            for i in range (0, len(FS)):
                if raio == FS[i][j][k][2]:
                    pos_raio = k

        pos_x = list(range(FS[0]))
                    
    for j in range (0, len(FS[0])):
        for i in range (0, len(FS)):
            aux_x.append(FS[i][j][pos_raio][6])
        mapa_de_calor.append(aux_x)
        aux_x = []
    mapa_de_calor = sns.heatmap(mapa_de_calor)
    plt.show()
    return mapa_de_calor



