import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import END, filedialog
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from camada import Camada
from forca_distribuida import Forca_distribuda
from forca_pontual import Forca_pontual
from nivel_agua import Nivel_Agua
from superficie_ruptura_qualquer import Superficie_Ruptura_Qualquer
from nan import Nan
import numpy as np
import utils
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import matplotlib.colors as pltc
import base64
import xml

from perfil_logitudinal import Perfil_Longitudinal
from solo import Solo
from superficie_terreno import Superficie_Terreno
import superficie_ruptura_qualquer


nivel_agua = Nan()
lista_solos = []
lista_camadas = []
perfil_longitudinal = None
lista_carregamentos = []
superficie_ruptura_circular = True


bg_janela = "#515151"
bg_frame = "#232323"
cor_fonte = "white"
fonte_titulo =  "calibri 16"
fonte_normal = "calibri 14"
pad_ext = 10
pad_int = 10
pad_txt = 1
pad_frame_x = 7
pad_frame_y = 7
tam_entry = 5


#botões
estilo_bt = "flat"
bg_bt = "#4472C4"
cor_fonte_bt = cor_fonte

def importa_superficie_terreno():
    global superficie_terreno
    filename = filedialog.askopenfilename(initialdir = "/",title = "Selecione o arquivo dxf ou txt", filetypes=[("DXF","*.dxf"),("XYFiles","*.txt")])
    if filename != "":
        superficie_terreno = Superficie_Terreno(filename)
        habilitaEntrada()
        plotSuperficieTerreno()

def habilitaEntrada():
    bt_importar_nivel_agua.config(state=tk.NORMAL)
    bt_criar_solo.config(state=tk.NORMAL)
    bt_cria_carregamento.config(state=tk.NORMAL)
    bt_importa_sup_ruptura.config(state=tk.NORMAL)
    bt_importar_superficie_terreno.config(state=tk.DISABLED)
    
def desabilitaEntrada():
    bt_importar_nivel_agua.config(state=tk.DISABLED)
    bt_criar_solo.config(state=tk.DISABLED)
    bt_cria_carregamento.config(state=tk.DISABLED)
    bt_importa_sup_ruptura.config(state=tk.DISABLED)
    bt_importar_superficie_terreno.config(state=tk.NORMAL)
    bt_importar_camada.config(state=tk.NORMAL)
    bt_exporta_csv.config(state=tk.DISABLED)
    bt_exporta_grafico.config(state=tk.DISABLED)
    
def plotSuperficieTerreno():
    ax1.plot(superficie_terreno.dominio, superficie_terreno.imagem, label = "Terreno", color = "brown", linewidth = 2)
    ax1.legend(loc = 0, fontsize = 'small')
    ax1.set_xlim([superficie_terreno.dominio[0], superficie_terreno.dominio[-1]])
    canvas_grafico.draw()
    return

def importa_nivel_agua():
    global nivel_agua
    global superficie_terreno
    filename = filedialog.askopenfilename(initialdir = "/",title = "Selecione o arquivo dxf ou txt", filetypes=[("DXF","*.dxf"),("XYFiles","*.txt")])
    if filename != "":
        nivel_agua = Nivel_Agua(superficie_terreno, filename) 
        plotNivelAgua()

def plotNivelAgua():
    ax1.plot(nivel_agua.dominio, nivel_agua.imagem, label = "Nível d'água", color = "blue", linewidth = 1, alpha = 0.9)
    ax1.legend(loc = 0, fontsize = 'small')
    canvas_grafico.draw()
    return

def plotCamada(camada):
        ax1.plot(camada.dominio, camada.imagem, label = camada.solo.nomeclatura)
        #ax1.legend(loc = 0, fontsize = 'small')
        canvas_grafico.draw()
            
def cria_solo():
    global lista_solos, logo

    def adiciona_solo():
        lista_solos.append(Solo(entry_nomeclatura.get(), float(entry_gama.get()),float(entry_fi.get()), float(entry_coesao.get())))
        entry_nomeclatura.delete(0,END)
        entry_gama.delete(0,END)
        entry_fi.delete(0,END)
        entry_coesao.delete(0,END)
        bt_importar_camada.config(state=tk.NORMAL)
        return

    janela_solo = tk.Toplevel(janela_principal)
    janela_solo.title("Definindo novo solo")
    #janela_solo.overrideredirect(True)
    janela_solo.iconphoto(False, logo)
    janela_solo.geometry('312x180')
    janela_solo.resizable(width = False, height = False)
    janela_solo.grid_columnconfigure(0, weight=1)
    janela_solo.grid_rowconfigure(0, weight=1)
    janela_solo.config(bg=bg_janela)
    frame_solo = tk.Frame(janela_solo, bg=bg_frame, pady=pad_int, padx=pad_int)
    frame_solo.grid(row=0, column=0, padx=pad_ext, pady=pad_ext, sticky="NEWS")
    frame_solo.grid_columnconfigure([0], weight=1, uniform="fred")
    frame_solo.grid_columnconfigure([1], weight=1, uniform="fred")
    frame_solo.grid_rowconfigure([0, 1, 2, 3], weight=1)
    frame_solo.grid_rowconfigure(4, weight=1)
    

    label_nomeclatura = tk.Label(frame_solo,
                                text="Nomeclatura =",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_nomeclatura.grid(row=0, column=0, sticky="w", padx=pad_txt)

    frame_nomeclatura = tk.Frame(frame_solo, bg=bg_frame)
    frame_nomeclatura.grid(row=0, column=1, sticky="NEWS")
    frame_nomeclatura.grid_columnconfigure(0,weight=1)
    frame_nomeclatura.grid_rowconfigure(0,weight=1)
    frame_nomeclatura.grid_columnconfigure(1,weight=0)

    entry_nomeclatura = tk.Entry(frame_nomeclatura,
                           width=tam_entry)
    entry_nomeclatura.grid(row=0, column=0, sticky="ew")

    label_unidade = tk.Label(frame_nomeclatura,
                                text="kN/m³",
                                font=fonte_normal, fg=bg_frame, bg=bg_frame)
    label_unidade.grid(row=0, column=1, sticky="w", padx=pad_txt)



    label_gama = tk.Label(frame_solo,
                                text="Gama =",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_gama.grid(row=1, column=0, sticky="w", padx=pad_txt)

    frame_gama = tk.Frame(frame_solo, bg=bg_frame)
    frame_gama.grid(row=1, column=1, sticky="NEWS")
    frame_gama.grid_columnconfigure(0,weight=1)
    frame_gama.grid_columnconfigure(1,weight=0)
    frame_gama.grid_rowconfigure(0,weight=1)

    entry_gama = tk.Entry(frame_gama,
                           width=tam_entry)
    entry_gama.grid(row=0, column=0, sticky="ew")

    label_unidade = tk.Label(frame_gama,
                                text="kN/m³",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_unidade.grid(row=0, column=1, sticky="w", padx=pad_txt)



    label_fi = tk.Label(frame_solo,
                                text="Φ' =",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_fi.grid(row=2, column=0, sticky="w", padx=pad_txt)

    frame_fi = tk.Frame(frame_solo, bg=bg_frame)
    frame_fi.grid(row=2, column=1, sticky="NEWS")
    frame_fi.grid_columnconfigure(0,weight=1)
    frame_fi.grid_columnconfigure(1,weight=0)
    frame_fi.grid_rowconfigure(0,weight=1)

    entry_fi = tk.Entry(frame_fi,
                        width=tam_entry)
    entry_fi.grid(row=0, column=0, sticky="ew")

    label_unidade = tk.Label(frame_fi,
                                text="°           ",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_unidade.grid(row=0, column=1, sticky="w", padx=pad_txt)



    label_coesao = tk.Label(frame_solo,
                                text="c' =",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_coesao.grid(row=3, column=0, sticky="w", padx=pad_txt)

    frame_coesao = tk.Frame(frame_solo, bg=bg_frame)
    frame_coesao.grid(row=3, column=1, sticky="NEWS")
    frame_coesao.grid_columnconfigure(0,weight=1)
    frame_coesao.grid_columnconfigure(1,weight=0)
    frame_coesao.grid_rowconfigure(0,weight=1)

    entry_coesao = tk.Entry(frame_coesao,
                           width=tam_entry)
    entry_coesao.grid(row=0, column=0, sticky="ew")

    label_unidade = tk.Label(frame_coesao,
                                text="kN/m²",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_unidade.grid(row=0, column=1, sticky="w", padx=pad_txt)



    bt_sair_solo = tk.Button(frame_solo,
                             command=janela_solo.destroy,
                             text="Sair",
                             relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal
                            )
    bt_sair_solo.grid(row=4, column=0,sticky="ew", pady=(5,0), padx=(0,3))

    bt_adiciona_solo = tk.Button(frame_solo,
                             command=adiciona_solo,
                             text="Adicionar",
                             relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal
                            )
    bt_adiciona_solo.grid(row=4, column=1,sticky="ew", pady=(5,0), padx=(3,0))

    return

def importa_camada():
    global lista_solos, lista_camadas, superficie_terreno

    def mostra_parametros(event):
        #print("combobox selecionada", cb_nomeclatura.current())
        entry_gama.config(text=(lista_solos[cb_nomeclatura.current()].gama,"kN/m³"))
        entry_fi.config(text=(utils.arred(lista_solos[cb_nomeclatura.current()].fi *180 / np.pi,2), "°"))
        entry_coesao.config(text=(lista_solos[cb_nomeclatura.current()].coesao, "kN/m²"))

    def cria_camada():
        print(filename)
        camada = Camada(lista_solos[cb_nomeclatura.current()], superficie_terreno, filename)
        lista_camadas.append(camada)
        janela_seleciona_solo.destroy()
        plotCamada(camada)
        return

    filename = filedialog.askopenfilename(initialdir = "/",title = "Selecione o arquivo dxf ou txt", filetypes=[("DXF","*.dxf"),("XYFiles","*.txt")])
    if filename == "":
        return
    janela_seleciona_solo = tk.Toplevel(janela_principal)
    janela_seleciona_solo.title("Definindo o solo da camada")
    janela_seleciona_solo.geometry('312x180')
    janela_seleciona_solo.resizable(width = False, height = False)
    janela_seleciona_solo.iconphoto(False, logo)
    janela_seleciona_solo.grid_columnconfigure(0, weight=1)
    janela_seleciona_solo.grid_rowconfigure(0, weight=1)
    janela_seleciona_solo.config(bg=bg_janela)
    frame_seleciona_solo = tk.Frame(janela_seleciona_solo, bg=bg_frame, pady=pad_int, padx=pad_int)
    frame_seleciona_solo.grid(row=0, column=0, padx=pad_ext, pady=pad_ext, sticky="NEWS")
    frame_seleciona_solo.grid_columnconfigure([0], weight=1, uniform="fred")
    frame_seleciona_solo.grid_columnconfigure([1], weight=1, uniform="fred")
    frame_seleciona_solo.grid_rowconfigure([0, 1, 2, 3], weight=1)
    frame_seleciona_solo.grid_rowconfigure(4, weight=1)
    

    label_nomeclatura = tk.Label(frame_seleciona_solo,
                                text="Nomeclatura =",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_nomeclatura.grid(row=0, column=0, sticky="w", padx=pad_txt)

    solo_selecionado = tk.StringVar()
    cb_nomeclatura = ttk.Combobox(frame_seleciona_solo, textvariable=solo_selecionado,
                                state='readonly')
    cb_nomeclatura["values"] = lista_solos
    cb_nomeclatura.bind('<<ComboboxSelected>>', mostra_parametros)
    cb_nomeclatura.grid(row=0, column=1, sticky="ew")

    label_gama = tk.Label(frame_seleciona_solo,
                                text="Gama =",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_gama.grid(row=1, column=0, sticky="w", padx=pad_txt)

    entry_gama = tk.Label(frame_seleciona_solo, bg=bg_frame, fg="white", font=fonte_normal)
    entry_gama.grid(row=1, column=1, sticky="ew")

    label_fi = tk.Label(frame_seleciona_solo,
                                text="Φ' =",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_fi.grid(row=2, column=0, sticky="w", padx=pad_txt)

    entry_fi = tk.Label(frame_seleciona_solo, bg=bg_frame, fg="white", font=fonte_normal)
    entry_fi.grid(row=2, column=1, sticky="ew")

    label_coesao = tk.Label(frame_seleciona_solo,
                                text="c' =",
                                font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_coesao.grid(row=3, column=0, sticky="w", padx=pad_txt)

    entry_coesao = tk.Label(frame_seleciona_solo, bg=bg_frame, fg="white", font=fonte_normal)
    entry_coesao.grid(row=3, column=1, sticky="ew")

    bt_sair_solo = tk.Button(frame_seleciona_solo,
                             command=janela_seleciona_solo.destroy,
                             text="Sair",
                             relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal
                            )
    bt_sair_solo.grid(row=4, column=0,sticky="ew", pady=(5,0), padx=(0,3))

    bt_adiciona_solo = tk.Button(frame_seleciona_solo,
                             command=cria_camada,
                             text="Criar Camada",
                             relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal
                            )
    bt_adiciona_solo.grid(row=4, column=1,sticky="ew", pady=(5,0), padx=(3,0))

    return

def plotaCarregamentos():
    global lista_carregamentos, superficie_terreno, ax0
    carregamentos_comp = utils.plota_forcas(superficie_terreno.dominio, lista_carregamentos)
    ax0.clear()
    ax0.set_xlim([superficie_terreno.dominio[0], superficie_terreno.dominio[-1]])
    ax0.plot(carregamentos_comp[0], carregamentos_comp[1], color="black")
    ax0.fill_between(x=carregamentos_comp[0], y1=carregamentos_comp[1], color="black", hatch="|", alpha=0.2)
    ax0.set_title("Carregamentos")
    ax0.xaxis.set_major_locator(ticker.NullLocator())
    ax0.xaxis.set_minor_locator(ticker.NullLocator())
    canvas_grafico.draw()
    
def cria_carregamento():

    global lista_carregamentos, superficie_terreno, ax0

    def carregamento_pontual():
        label_fi_forca.config(text="q         =",
                              state=tk.NORMAL)
        
        entry_fi_forca.config(state=tk.NORMAL)
        entry_fi_forca.delete(0,END)

        label_unidade_fi.config(state=tk.NORMAL)
        
        label_ff_forca.config(state=tk.NORMAL,
                            fg=bg_frame)
        
        entry_ff_forca.config(state=tk.NORMAL,
                              bg=bg_frame,
                              borderwidth=0,
                              fg=bg_frame)
        
        label_unidade_ff.config(state=tk.NORMAL,
                                fg=bg_frame)  
              
        label_xi_forca.config(text="x         =",
                              state=tk.NORMAL)
        
        entry_xi_forca.config(state=tk.NORMAL)
        entry_xi_forca.delete(0,END)

        label_unidade_xi.config(state=tk.NORMAL)

        label_xf_forca.config(state=tk.NORMAL,
                            fg=bg_frame)
        
        entry_xf_forca.config(state=tk.NORMAL,
                              bg=bg_frame,
                              borderwidth=0,
                              fg=bg_frame)
        
        label_unidade_xf.config(state=tk.NORMAL,
                                fg=bg_frame)

    def carregamento_distribuido():
        label_fi_forca.config(text="q inicial =",
                              state=tk.NORMAL)
        
        entry_fi_forca.config(state=tk.NORMAL)
        entry_fi_forca.delete(0,END)

        label_unidade_fi.config(state=tk.NORMAL)
        
        label_ff_forca.config(state=tk.NORMAL,
                            fg=cor_fonte)
        
        entry_ff_forca.config(state=tk.NORMAL,
                              bg='white',
                              borderwidth=1,
                              fg="black")
        
        label_unidade_ff.config(state=tk.NORMAL,
                                fg=cor_fonte)  
              
        label_xi_forca.config(text="x inicial =",
                              state=tk.NORMAL)
        
        entry_xi_forca.config(state=tk.NORMAL)
        entry_xi_forca.delete(0,END)

        label_unidade_xi.config(state=tk.NORMAL)

        label_xf_forca.config(state=tk.NORMAL,
                            fg=cor_fonte)
        
        entry_xf_forca.config(state=tk.NORMAL,
                              bg="white",
                              borderwidth=1,
                              fg="black")
        
        label_unidade_xf.config(state=tk.NORMAL,
                                fg=cor_fonte)    



    def adiciona_carregamento():
        if tipo_de_carregamento.get() == "pontual":
            lista_carregamentos.append(Forca_pontual(float(entry_fi_forca.get()), float(entry_xi_forca.get())))
        elif tipo_de_carregamento.get() == "distribuido":   
            lista_carregamentos.append(Forca_distribuda([float(entry_fi_forca.get()), float(entry_ff_forca.get())], [float(entry_xi_forca.get()), float(entry_xf_forca.get())]))
        plotaCarregamentos()
        entry_fi_forca.delete(0, END)
        entry_ff_forca.delete(0, END)
        entry_xi_forca.delete(0, END)
        entry_xf_forca.delete(0, END)

        
    def zerar():
        global lista_carregamentos
        ax0.clear()
        lista_carregamentos = []
        canvas_grafico.draw()

    janela_forca = tk.Toplevel(janela_principal)
    janela_forca.title("Criando Carregamento")
    janela_forca.iconphoto(False, logo)
    janela_forca.geometry('400x335')
    janela_forca.resizable(width = False, height = False)
    janela_forca.iconphoto(False, logo)
    janela_forca.config(bg=bg_janela)
    janela_forca.grid_columnconfigure(0, weight=1)
    janela_forca.grid_rowconfigure(0, weight=1)
    
    frame_forca = tk.Frame(janela_forca, bg=bg_frame, pady=pad_int, padx=pad_int)
    frame_forca.grid(row=0, column=0, padx=pad_ext, pady=pad_ext, sticky="NEWS")
    frame_forca.grid_columnconfigure([0,1], weight=1)


    tipo_de_carregamento = StringVar()
    tipo_de_carregamento.set("False")

    label_tipo = tk.Label(frame_forca,
                            text="Tipo de carregamento",
                            anchor="n",
                            font=fonte_titulo, fg=cor_fonte, bg=bg_frame)
    label_tipo.grid(row=0, column=0, columnspan= 2, sticky="EW", pady=(0,10))

    rb_pontual = tk.Radiobutton(frame_forca,
                                command=carregamento_pontual,
                                variable = tipo_de_carregamento,
                                value="pontual",
                                activeforeground=cor_fonte,
                                activebackground=bg_frame,
                                font=fonte_normal, fg=bg_frame, bg=bg_frame)
    rb_pontual.grid(row=1, column=0)

    label_pontual = tk.Label(frame_forca,
                            text="Carregamento pontual",
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_pontual.grid(row=1, column=1, sticky="W")

    rb_distribuido = tk.Radiobutton(frame_forca,
                                variable = tipo_de_carregamento,
                                command= carregamento_distribuido,
                                value="distribuido",
                                activeforeground=cor_fonte,
                                activebackground=bg_frame,                                
                                font=fonte_normal ,fg=bg_frame, bg=bg_frame)
    rb_distribuido.grid(row=2, column=0)

    label_distribuido = tk.Label(frame_forca,
                            text="Carregamento distribuido",
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_distribuido.grid(row=2, column=1,sticky="W")

    frame_parametros_forcas = tk.Frame(frame_forca, bg=bg_frame)
    frame_parametros_forcas.grid(row=3,column=0,columnspan=2, sticky="NEWS")
    frame_parametros_forcas.grid_columnconfigure([0,1,2,3,4,5,6], weight=1)
    frame_parametros_forcas.grid_rowconfigure([0,1,2], weight=1)

    label_entrada_forca = tk.Label(frame_parametros_forcas,
                                text="Parâmetros",
                                anchor="n",
                                font=fonte_titulo, fg=cor_fonte, bg=bg_frame)
    label_entrada_forca.grid(row=0, column=0, columnspan= 6, sticky="EW", pady=(20,10))

    label_fi_forca = tk.Label(frame_parametros_forcas,
                            text="q inicial =",
                            state= tk.DISABLED,
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_fi_forca.grid(row=1, column=0, sticky="W")

    entry_fi_forca = tk.Entry(frame_parametros_forcas,
                            state= tk.DISABLED,
                            width=tam_entry)
    entry_fi_forca.grid(row=1, column=1, sticky="w")

    label_unidade_fi = tk.Label(frame_parametros_forcas,
                            text="kPa",
                            state= tk.DISABLED,
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_unidade_fi.grid(row=1, column=2, sticky="W")

    label_ff_forca = tk.Label(frame_parametros_forcas,
                            text="q final   =",
                            state= tk.DISABLED,
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_ff_forca.grid(row=2, column=0, sticky="W")

    entry_ff_forca = tk.Entry(frame_parametros_forcas,
                            state= tk.DISABLED,
                            width=tam_entry)
    entry_ff_forca.grid(row=2, column=1, sticky="w")

    label_unidade_ff = tk.Label(frame_parametros_forcas,
                            text="kPa",
                            state= tk.DISABLED,
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_unidade_ff.grid(row=2, column=2, sticky="W")

    label_xi_forca = tk.Label(frame_parametros_forcas,
                            text="x inicial =",
                            state= tk.DISABLED,
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_xi_forca.grid(row=1, column=3, sticky="W", padx=(30,0))

    entry_xi_forca = tk.Entry(frame_parametros_forcas,
                            state= tk.DISABLED,
                            width=tam_entry)
    entry_xi_forca.grid(row=1, column=4, sticky="w")

    label_unidade_xi = tk.Label(frame_parametros_forcas,
                            text="m",
                            state= tk.DISABLED,
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_unidade_xi.grid(row=1, column=5, sticky="W")

    label_xf_forca = tk.Label(frame_parametros_forcas,
                            text="x final   =",
                            state= tk.DISABLED,
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_xf_forca.grid(row=2, column=3, sticky="W", padx=(30,0))

    entry_xf_forca = tk.Entry(frame_parametros_forcas,
                            state= tk.DISABLED,
                            width=tam_entry)
    entry_xf_forca.grid(row=2, column=4, sticky="w")

    label_unidade_xf = tk.Label(frame_parametros_forcas,
                            text="m",
                            state= tk.DISABLED,
                            font=fonte_normal, fg=cor_fonte, bg=bg_frame)
    label_unidade_xf.grid(row=2, column=5, sticky="W")

    frame_comando_forcas = tk.Frame(frame_forca, bg=bg_frame)
    frame_comando_forcas.grid(row=4,column=0,columnspan=2, sticky="NEWS", pady=(20,0))
    frame_comando_forcas.grid_columnconfigure([0,1], weight=1, uniform="fred")
    frame_comando_forcas.grid_rowconfigure([0], weight=1)

    bt_zerar_forca = tk.Button(frame_comando_forcas,
                             command=zerar,
                             text="Zerar",
                             relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal
                            )
    bt_zerar_forca.grid(row=0, column=0,sticky="ew", pady=(5,0), padx=(0,3))

    bt_adiciona_forca = tk.Button(frame_comando_forcas,
                                command=adiciona_carregamento,
                                text="Adicionar",
                                relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal
                            )
    bt_adiciona_forca.grid(row=0, column=1,sticky="ew", pady=(5,0), padx=(3,0))

def run():
    global perfil_longitudinal, superficie_terreno, lista_camadas, nivel_agua, lista_carregamentos, FS, x_FS, y_FS, r_FS

    if superficie_ruptura_circular == True:
        x_inicial = float(entry_x_inicial.get())
        inc_c = float(entry_inc_centro.get())
        x_final = float(entry_x_final.get())
        y_inicial = float(entry_y_inicial.get())
        y_final = float(entry_y_final.get())
        r_inicial = float(entry_r_inicial.get())
        inc_r = float(entry_inc_raio.get())
        r_final = float(entry_r_final.get())
    dx = float(entry_dx.get())


    perfil_longitudinal = Perfil_Longitudinal(superficie_terreno, lista_camadas, nivel_agua)
    forcas_comp = utils.compila_forcas(superficie_terreno.dominio, lista_carregamentos)

    if superficie_ruptura_circular ==  True:
        [FS, [[x_FS, y_FS, r_FS]]] = utils.analisa_FS_pelo_raio(perfil_longitudinal, x_inicial, x_final, y_inicial, y_final, inc_c, r_inicial, r_final, inc_r, dx, forcas_comp)
    elif superficie_ruptura_circular ==  False:
        [FS, [[x_FS, y_FS, r_FS]]] = utils.analisa_FS_pela_superficie(perfil_longitudinal, superficie_ruptura_qualquer , dx, forcas_comp)


    label_FS1.config(text= utils.tira_lista(FS[x_FS][y_FS][r_FS][5]))
    label_FS2.config(text= utils.tira_lista(FS[x_FS][y_FS][r_FS][6]))
    label_FS3.config(text= utils.tira_lista(FS[x_FS][y_FS][r_FS][7]))
    label_FS4.config(text= utils.tira_lista(FS[x_FS][y_FS][r_FS][8]))
    label_FS5.config(text= utils.tira_lista(FS[x_FS][y_FS][r_FS][9]))
    label_FS_posicao.config(text=(f"x = {FS[x_FS][y_FS][r_FS][0]} m   y = {FS[x_FS][y_FS][r_FS][1]} m   r = {FS[x_FS][y_FS][r_FS][2]} m"))
    bt_exporta_csv.config(state=tk.NORMAL)
    bt_exporta_grafico.config(state=tk.NORMAL)



    if len(perfil_longitudinal.lista_camadas) > 1:
        plt_camadas = sorted(perfil_longitudinal.lista_camadas, key = utils.sort_camadas_imagem)
    else:
        plt_camadas = perfil_longitudinal.lista_camadas[:]
    plt_camadas.append(perfil_longitudinal.superficie_terreno)

    ax1.fill_between(x = perfil_longitudinal.dominio, y1 = perfil_longitudinal.nivel_agua.imagem, y2 = plt_camadas[0].imagem, color = "blue",hatch = "/" ,alpha = 0.05)

    for i in range(0, len(plt_camadas) - 1):
        for j in range(0, len(plt_camadas[i].imagem)):
            if np.isnan(plt_camadas[i].imagem[j]):
                for k in range(i + 1, len(plt_camadas)):
                    if not np.isnan(plt_camadas[k].imagem[j]):
                        plt_camadas[i].imagem[j] = plt_camadas[k].imagem[j]
                        break

    for i in range(0, len(plt_camadas) - 1):
        ax1.fill_between(x = perfil_longitudinal.dominio, y1 = plt_camadas[i].imagem, y2 = plt_camadas[i + 1].imagem, alpha = 0.2)#, label = plt_camadas[i].solo.nomeclatura)
    
    for fatia in FS[x_FS][y_FS][r_FS][4]:
        ax1.vlines(x = fatia.xf, ymin = fatia.yf_inf, ymax = fatia.yf_sup, color = 'black')

    #ax1.legend(loc = 0, fontsize = 'small')
    #plt.ylim(ylim_min, ylim_min + amplitude)

    if superficie_ruptura_circular == True:
        ax1.plot(FS[x_FS][y_FS][r_FS][3].dominio, FS[x_FS][y_FS][r_FS][3].imagem, color = "black")
        ax1.scatter(FS[x_FS][y_FS][r_FS][3].x0, FS[x_FS][y_FS][r_FS][3].y0, color = 'black', marker = '.', label = 'Centro')
        ax1.plot(FS[x_FS][y_FS][r_FS][3].dominio, FS[x_FS][y_FS][r_FS][3].imagem_raio_esquerda, color = "black", linewidth = 1, linestyle = "--")
        ax1.plot(FS[x_FS][y_FS][r_FS][3].dominio, FS[x_FS][y_FS][r_FS][3].imagem_raio_direita, color = "black", linewidth = 1, linestyle = "--")


        x_heat_map =[]
        y_heat_map = []
        for i in range(0, len(FS)):
            x_heat_map.append(FS[i][0][0][0])
        for j in range(0, len(FS[0])):
            y_heat_map.append(FS[0][j][0][1])

        FS_heat_map = np.zeros([len(y_heat_map), len(x_heat_map)])

        for i in range(0, len(FS)):
            for j in range(0, len(FS[0])):
                FS_heat_map[j, i] = FS[i][j][r_FS][6]

        # ax2 = ax1.inset_axes([0.5,0.5,0.5,0.5])
        # ax2.set_xlim(x_heat_map[0],x_heat_map[-1])
        # ax2.set_ylim(y_heat_map[0],y_heat_map[-1])
        # norm = pltc.Normalize(vmin=0, vmax=3)
        # cmap = pltc.LinearSegmentedColormap.from_list('FS_cmap',['red', 'red', 'red', 'red', 'orange', 'yellow', 'green', 'blue'])
        #cmap = pltc.ListedColormap(['red', 'red', 'red', 'red', 'orange', 'yellow', 'green', 'blue'])


        ax1.contourf(x_heat_map, y_heat_map, FS_heat_map,norm=norm, cmap=cmap)
        # fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax= ax1)
        

        #ajeitar eixos ---> https://matplotlib.org/stable/users/explain/axes/axes_ticks.html
    canvas_grafico.draw()

    return

def exporta_grafico():
    filenametosave = filedialog.asksaveasfilename(filetypes=[("PNG file", ".png")],
    defaultextension=".png")
    if filenametosave:    
        fig.savefig(filenametosave, edgecolor='black')

def exporta_csv_fatias():
    filenametosave = filedialog.asksaveasfilename(filetypes=[("cvs file", ".csv")],
    defaultextension=".csv")
    if filenametosave:
        utils.tabela(FS[x_FS][y_FS][r_FS][4]).to_csv(filenametosave)    

def zera_tudo():
    superficie_terreno = None
    lista_camadas = []
    lista_carregamentos = []
    lista_solos = []
    FS = None
    perfil_longitudinal = None 
    nivel_agua = None
    x_FS = None
    y_FS = None
    r_FS = None
    
    desabilitaEntrada()
    label_FS1.config(text= "-")
    label_FS2.config(text= "-")
    label_FS3.config(text= "-")
    label_FS4.config(text= "-")
    label_FS5.config(text= "-")
    label_FS_posicao.config(text=("x =          -          y =          -          r =          -          "))

    ax0.clear()
    ax0.set_title('Carregamentos')
    ax0.xaxis.set_major_locator(ticker.NullLocator())
    ax0.xaxis.set_minor_locator(ticker.NullLocator())

    ax1.clear()
    ax1.set_xlabel('(m)')   
    ax1.set_ylabel('Cota (m)')
    ax1.set_title('Perfil Longitudinal')
    canvas_grafico.draw()

    label_x_inicial.config(state=tk.NORMAL)
    entry_x_inicial.delete(0,END)
    entry_x_inicial.config(state=tk.NORMAL)
    label_m_x_inicial.config(state=tk.NORMAL)

    label_x_final.config(state=tk.NORMAL)
    entry_x_final.delete(0,END)
    entry_x_final.config(state=tk.NORMAL)
    label_m_x_final.config(state=tk.NORMAL)

    label_inc_centro.config(state=tk.NORMAL)
    entry_inc_centro.delete(0,END)
    entry_inc_centro.config(state=tk.NORMAL)
    label_m_inc_centro.config(state=tk.NORMAL)

    label_y_inicial.config(state=tk.NORMAL)
    entry_y_inicial.delete(0,END)
    entry_y_inicial.config(state=tk.NORMAL)
    label_m_y_inicial.config(state=tk.NORMAL)

    label_y_final.config(state=tk.NORMAL)
    entry_y_final.delete(0,END)
    entry_y_final.config(state=tk.NORMAL)
    label_m_y_final.config(state=tk.NORMAL)

    label_r_inicial.config(state=tk.NORMAL)
    entry_r_inicial.delete(0,END)
    entry_r_inicial.config(state=tk.NORMAL)
    label_m_r_inicial.config(state=tk.NORMAL)

    label_r_final.config(state=tk.NORMAL)
    entry_r_final.delete(0,END)
    entry_r_final.config(state=tk.NORMAL)
    label_m_r_final.config(state=tk.NORMAL)

    label_inc_raio.config(state=tk.NORMAL)
    entry_inc_raio.delete(0,END)
    entry_inc_raio.config(state=tk.NORMAL)
    label_m_inc_raio.config(state=tk.NORMAL)
 
    label_dx.config(state=tk.NORMAL)
    entry_dx.delete(0,END)
    entry_dx.config(state=tk.NORMAL)
    label_m_dx.config(state=tk.NORMAL)


def abrir_arquivo():
    global superficie_terreno
    global nivel_agua
    global superficie_ruptura_qualquer
    filenametoopen = filedialog.askopenfilename(initialdir = "/",title = "Selecione o arquivo xml", filetypes=[("XML","*.xml")])
    from lxml import etree
    if filenametoopen:
        zera_tudo()
        tree = etree.parse(filenametoopen)
        root = tree.getroot()
        if root.find('superficie_terreno') is not None :
            a = root.find('superficie_terreno') 
            lx = []
            sizex = int(a.find('sizex').text)
            for idx in range(0,sizex):
                st =  "coordx-"+str(idx)
                lx.append(float(a.find(st).text))
            sizey = int(a.find('sizey').text)
            ly = []
            for idx in range(0,sizey):
                st =  "coordy-"+str(idx)
                ly.append(float(a.find(st).text))      
            superficie_terreno = Superficie_Terreno()
            superficie_terreno.atribuicaodecoordenadaslidas(lx,ly)
            plotSuperficieTerreno()
            habilitaEntrada()
 
        if root.find('nivel_dagua') is not None :
            a = root.find('nivel_dagua') 
            lx = []
            sizex = int(a.find('sizex').text)
            for idx in range(0,sizex):
                st =  "coordx-"+str(idx)
                lx.append(float(a.find(st).text))
            sizey = int(a.find('sizey').text)
            ly = []
            for idx in range(0,sizey):
                st =  "coordy-"+str(idx)
                ly.append(float(a.find(st).text))
            nivel_agua = Nivel_Agua(superficie_terreno)
            nivel_agua.atribuicaodecoordenadaslidas(lx,ly)
            plotNivelAgua()

        if root.find('parametros') is not None :
            a = root.find('parametros') 
            entry_x_inicial.insert(0,a.find('entry_x_inicial').text)
            entry_x_final.insert(0,a.find('entry_x_final').text)
            entry_y_inicial.insert(0,a.find('entry_y_inicial').text)
            entry_y_final.insert(0,a.find('entry_y_final').text)
            entry_inc_centro.insert(0,a.find('entry_inc_centro').text)
            entry_r_inicial.insert(0,a.find('entry_r_inicial').text)
            entry_r_final.insert(0,a.find('entry_r_final').text)
            entry_inc_raio.insert(0,a.find('entry_inc_raio').text)
            entry_dx.delete(0,END)
            entry_dx.insert(0,a.find('entry_dx').text)

        if root.find('lista_solos') is not None :
            a = root.find('lista_solos') 
            sizesolos = int(a.find('sizesolos').text)
            for idx in range(0,sizesolos):
                st = "solo_" + str(idx)
                element = a.find(st)
                st = element.find("name").text
                gama = float(element.find("gama").text)
                fi = float(element.find("fi").text)
                coesao = float(element.find("coesao").text)
                lista_solos.append(Solo(st,gama,fi,coesao))
                
        if root.find('lista_camadas') is not None :
            a = root.find('lista_camadas') 
            sizecamadas = int(a.find('sizecamadas').text)
            for idx in range(0,sizecamadas):
                st = "camada_" + str(idx)
                element = a.find(st)
                namesolo = element.find("soloname").text

                lx = []
                sizex = int(element.find('sizex').text)
                for idx in range(0,sizex):
                    st =  "coordx-"+str(idx)
                    lx.append(float(element.find(st).text))
                sizey = int(element.find('sizey').text)
                ly = []
                for idx in range(0,sizey):
                    st =  "coordy-"+str(idx)
                    ly.append(float(element.find(st).text))
                
                for solo in lista_solos:
                    if solo.nomeclatura == namesolo:
                        cm = Camada(solo, superficie_terreno)
                        cm.atribuicaodecoordenadaslidas(lx,ly)
                        lista_camadas.append(cm)
                        plotCamada(cm)
                        break
        
        if root.find('lista_carregamentos') is not None :
            a = root.find('lista_carregamentos') 
            sizecarregamentos = int(a.find('sizecarregamentos').text)
            for idx in range(0,sizecarregamentos):
                st = "carregamentos_" + str(idx)  
                car = a.find(st) 
                element = car.find("tipo")
                if element.text == "distribuida":
                    print(element.text)
                    element = car.find("forca-0")
                    fi = float(element.text)
                    element = car.find("posicao-0")
                    xi = float(element.text)    
                    element = car.find("forca-1")
                    ff = float(element.text)
                    element = car.find("posicao-1")
                    xf = float(element.text) 
                    fd = Forca_distribuda([fi,ff],[xi, xf])
                    lista_carregamentos.append(fd)                       
                elif element.text == "pontual":
                    element = car.find("forca")
                    value = float(element.text)
                    element = car.find("posicao")
                    valuex = float(element.text) 
                    fp = Forca_pontual(value, valuex)
                    lista_carregamentos.append(fp)      
            plotaCarregamentos()             
            
        if root.find('superficie_ruptura_qualquer') is not None :            
            a = root.find('superficie_ruptura_qualquer') 
            lx = []
            sizex = int(a.find('sizex').text)
            for idx in range(0,sizex):
                st =  "coordx-"+str(idx)
                lx.append(float(a.find(st).text))
            sizey = int(a.find('sizey').text)
            ly = []
            for idx in range(0,sizey):
                st =  "coordy-"+str(idx)
                ly.append(float(a.find(st).text))      
            superficie_ruptura_qualquer = Superficie_Ruptura_Qualquer(superficie_terreno)
            superficie_ruptura_qualquer.atribuicaodecoordenadaslidas(lx,ly)
            plotSuperficieRupturaQualquer()                
                      
    return

def salvar_arquivo():
    filenametosave = filedialog.asksaveasfilename()
    if filenametosave:
        f = open(filenametosave, 'w')
        from lxml import etree
        
        root = etree.Element('root')
        
        printsuperficie = False
        printniveldagua = False
        printcamadas = False
        printsuperficiedefined = False
        printload = False
        printsolos = False
        try:
            superficie_terreno 
            printsuperficie = True
        except NameError:
            print("superficie não cadastrada")
        if printsuperficie:
            child1 = etree.SubElement(root, 'superficie_terreno')
            element = child1.makeelement("sizex", {})
            child1.append(element)
            element.text = str(len(superficie_terreno.coordenadas_x))            
            for idx,x in enumerate(superficie_terreno.coordenadas_x):
                element = child1.makeelement("coordx-"+str(idx), {})
                child1.append(element)
                element.text = str(x)   
            element = child1.makeelement("sizey", {})
            child1.append(element)
            element.text = str(len(superficie_terreno.coordenadas_y))   
            for idx,y in enumerate(superficie_terreno.coordenadas_y):
                element = child1.makeelement("coordy-"+str(idx), {})
                child1.append(element)
                element.text = str(y)

        try:
            printniveldagua = True
            if type(nivel_agua) == type(Nan()):
                printniveldagua = False
        except NameError:
            print("Nivel dagua não cadastrado")
        if printniveldagua:
            child2 = etree.SubElement(root, 'nivel_dagua')
            element = child2.makeelement("sizex", {})
            child2.append(element)
            element.text = str(len(nivel_agua.coordenadas_x))            
            for idx,x in enumerate(nivel_agua.coordenadas_x):
                element1 = child2.makeelement("coordx-"+str(idx), {})
                child2.append(element1)
                element1.text = str(x)   
            element = child2.makeelement("sizey", {})
            child2.append(element)
            element.text = str(len(nivel_agua.coordenadas_y))   
            for idx,y in enumerate(nivel_agua.coordenadas_y):
                element1 = child2.makeelement("coordy-"+str(idx), {})
                child2.append(element1)
                element1.text = str(y)          

            #for soil in lista_solos:
                
        if len(lista_camadas) > 0:
            child3 = etree.SubElement(root, 'lista_camadas')
            element = child3.makeelement("sizecamadas", {})
            child3.append(element)
            element.text = str(len(lista_camadas))     
            for idx,camadas in enumerate(lista_camadas):
                child4 = etree.SubElement(child3, "camada_" + str(idx))
                #child4 = etree.SubElement(child3, 'camada' + str(idx))
                element = child4.makeelement("soloname", {})
                child4.append(element)
                element.text = str(camadas.solo.nomeclatura)
                element = child4.makeelement("sizex", {})
                child4.append(element)
                element.text = str(len(camadas.coordenadas_x))            
                for idx,x in enumerate(camadas.coordenadas_x):
                    element1 = child4.makeelement("coordx-"+str(idx), {})
                    child4.append(element1)
                    element1.text = str(x)   
                element = child4.makeelement("sizey", {})
                child4.append(element)
                element.text = str(len(camadas.coordenadas_y))   
                for idx,y in enumerate(camadas.coordenadas_y):
                    element1 = child4.makeelement("coordy-"+str(idx), {})
                    child4.append(element1)
                    element1.text = str(y)  
                    
        if len(lista_carregamentos) > 0:
            child6 = etree.SubElement(root, 'lista_carregamentos')
            element = child6.makeelement("sizecarregamentos", {})
            child6.append(element)
            element.text = str(len(lista_carregamentos))     
            for idx,carregamento in enumerate(lista_carregamentos):
                element2 = etree.SubElement(child6, "carregamentos_" + str(idx))
                element = element2.makeelement("tipo")
                element2.append(element)
                element.text = str(carregamento.tipo) 
                if carregamento.tipo == "distribuida":
                    for idx,forca in enumerate(carregamento.forca):
                        element = element2.makeelement( "forca-"+str(idx), {})
                        element.text = str(carregamento.forca[idx])  
                        element2.append(element) 
                    for idx,posicao in enumerate(carregamento.posicao):
                        element = element2.makeelement("posicao-"+str(idx), {})
                        element.text = str(posicao)   
                        element2.append(element)
                elif carregamento.tipo == "pontual":
                    element = element2.makeelement("forca", {})
                    element.text = str(carregamento.forca) 
                    element2.append(element)
                    element = element2.makeelement("posicao", {})
                    element.text = str(carregamento.posicao) 
                    element2.append(element)      
                    
                                
        if superficie_ruptura_circular == False:
            child7 = etree.SubElement(root, 'superficie_ruptura_qualquer')
            element = child7.makeelement("sizex", {})
            child7.append(element)
            element.text = str(len(superficie_ruptura_qualquer.coordenadas_x))            
            for idx,x in enumerate(superficie_ruptura_qualquer.coordenadas_x):
                element = child7.makeelement("coordx-"+str(idx), {})
                child7.append(element)
                element.text = str(x)   
            element = child7.makeelement("sizey", {})
            child7.append(element)
            element.text = str(len(superficie_ruptura_qualquer.coordenadas_y))   
            for idx,y in enumerate(superficie_ruptura_qualquer.coordenadas_y):
                element = child7.makeelement("coordy-"+str(idx), {})
                child7.append(element)
                element.text = str(y)

        if len(lista_solos) > 0:
            child5 = etree.SubElement(root, 'lista_solos')
            element = child5.makeelement("sizesolos", {})
            child5.append(element)
            element.text = str(len(lista_solos))     
            for idx,solo in enumerate(lista_solos):
                element2 = etree.SubElement(child5, "solo_" + str(idx))
                element1 = element2.makeelement("name", {})
                element2.append(element1)
                element1.text = str(solo.nomeclatura)              
                element1 = element2.makeelement("gama", {})
                element2.append(element1)
                element1.text = str(solo.gama)   
                element1 = element2.makeelement("fi", {})
                element2.append(element1)
                element1.text = str(solo.fi*180/np.pi)   
                element1 = element2.makeelement("coesao", {})
                element2.append(element1)
                element1.text = str(solo.coesao)   
                
        child7 = etree.SubElement(root, 'parametros')
        element = child7.makeelement("entry_x_inicial", {})
        child7.append(element)
        element.text = entry_x_inicial.get()   
        element = child7.makeelement("entry_x_final", {})
        child7.append(element)
        element.text = entry_x_final.get()   
        element = child7.makeelement("entry_y_inicial", {})
        child7.append(element)
        element.text = entry_y_inicial.get()   
        element = child7.makeelement("entry_y_final", {})
        child7.append(element)
        element.text = entry_y_final.get()   
        element = child7.makeelement("entry_inc_centro", {})
        child7.append(element)
        element.text = entry_inc_centro.get()   
        element = child7.makeelement("entry_r_inicial", {})
        child7.append(element)
        element.text = entry_r_inicial.get()   
        element = child7.makeelement("entry_r_final", {})
        child7.append(element)
        element.text = entry_r_final.get()   
        element = child7.makeelement("entry_inc_raio", {})
        child7.append(element)
        element.text = entry_inc_raio.get()       
        element = child7.makeelement("entry_dx", {})
        child7.append(element)
        element.text = entry_dx.get()                           
                       
        et = etree.ElementTree(root)
        et.write(filenametosave, pretty_print=True)        
        f.close()     
    return 

def plotSuperficieRupturaQualquer():
    global superficie_ruptura_circular, superficie_ruptura_qualquer    
    label_x_inicial.config(state=tk.DISABLED)
    entry_x_inicial.delete(0, END)
    entry_x_inicial.config(state=tk.DISABLED)
    label_m_x_inicial.config(state=tk.DISABLED)
    label_x_final.config(state=tk.DISABLED)
    entry_x_final.delete(0, END)
    entry_x_final.config(state=tk.DISABLED)
    label_m_x_final.config(state=tk.DISABLED)
    label_inc_centro.config(state=tk.DISABLED)
    entry_inc_centro.delete(0, END)
    entry_inc_centro.config(state=tk.DISABLED)
    label_m_inc_centro.config(state=tk.DISABLED)
    label_y_inicial.config(state=tk.DISABLED)
    entry_y_inicial.delete(0, END)
    entry_y_inicial.config(state=tk.DISABLED)
    label_m_y_inicial.config(state=tk.DISABLED)
    label_y_final.config(state=tk.DISABLED)
    entry_y_final.delete(0, END)
    entry_y_final.config(state=tk.DISABLED)
    label_m_y_final.config(state=tk.DISABLED)
    label_r_inicial.config(state=tk.DISABLED)
    entry_r_inicial.delete(0, END)
    entry_r_inicial.config(state=tk.DISABLED)
    label_m_r_inicial.config(state=tk.DISABLED)
    label_r_final.config(state=tk.DISABLED)
    entry_r_final.delete(0, END)
    entry_r_final.config(state=tk.DISABLED)
    label_m_r_final.config(state=tk.DISABLED)
    label_inc_raio.config(state=tk.DISABLED)
    entry_inc_raio.delete(0, END)
    entry_inc_raio.config(state=tk.DISABLED)
    label_m_inc_raio.config(state=tk.DISABLED)
    ax1.plot(superficie_ruptura_qualquer.dominio, superficie_ruptura_qualquer.imagem, label="Superfície de ruptura", color='black')
    ax1.legend(loc=0, fontsize='small')
    superficie_ruptura_circular = False
    canvas_grafico.draw()

def importa_superficie_ruptura():
    global superficie_ruptura_qualquer
    filename = filedialog.askopenfilename(initialdir = "/",title = "Selecione o arquivo dxf ou txt", filetypes=[("DXF","*.dxf"),("XYFiles","*.txt")])
    
    if filename == "":
        return
    
    superficie_ruptura_qualquer = Superficie_Ruptura_Qualquer(superficie_terreno, filename)
    
    plotSuperficieRupturaQualquer()


icone_base64 = "iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAACxMAAAsTAQCanBgAAAeeSURBVHhe7ZxNjBRFFMeremZngTUo8UAkcNCAriYGFRXRwLp8ihhZA16N0fXgxYTVg1ETEhMNCRFOhgMKJqJejUZEFkVAiCEoi8EA0fUjiBA4oIsLu7MzXb7XUzXMR89Mf1XV6939JZPurgmT3v+v6nX1MNVskkkmmWSSCQuX29QhDrEZzG2/F/ZmMOFcZLmRY/xhdk2+nRpSJ0Dsz3Uyh78Fu0/CK+s1IgLC5+JD5mY38u6rF2QreVIlQBzIrYVT3gW7N5RafBDiPONuD+8qHJUtpEmNAHEwt565/GM44zbZ1Ixh+NMe510jB+UxWVIhIGT4ilRIIC8gYvgK8hJIC4gZvoK0BLICEgpfQVYCSQEJh68gKYGcAE3hK8hJICVAc/gKUhLICDAUvoKMBBICDIevICHBugBL4SusS7AqwHL4CqsSrAkgEr7CmgQrAoiFr7AiwbgAouErjEswKoB4+AqjEowJSEn4CmMSjAhIWfgKIxK0C0hp+ArtErQKSHn4Cq0StAkYJ+ErtEnQImCcha/QIiFxAeM0fEXiEhIVMM7DVyQqITEBEyR8RWISEhEwwcJXJCLBkdvIpCF8Ia5vK/dj0gGfslscmLJEHkci1giYoD2/llgjIfIISEv4jXp6AiNAEWskRBoBaSo73OcvdOE9J7HpR5lIIyH0aaQ9fM2ElhCqBFEPvzL42vCLrhEboctR4LNKQ/hxe3y+mGU7jz/E9g3e4R2vmHuaPXfP9yybKXrHIQg8EgKdclouuHH4Z2Qqe/PbNezUpZmypcS6uwZY74LD8igUgSS0LEFpqvlROfvvDLZhz/q68JH+wTvlXmgClaOmAtLS8+OUnhMXZkP469iFK9NlSzVDo+1yLxItJTQU4C2IE/wTyjW/sudHGQX9g53sjW+eYMP5WCG3ogNO7nNxoO0+eVyFrwBvKWhpNeL1ZaBEUMHXznTCjAL897tOPMC2HFnGCsWMbNUIZ9OhM3/qrW2uwX8ElNbhNl4KagnVy+OUnDE3wzYfXsE++ulB2WIIzucwt/0VeVSmToC0hIugSYF3r0ic8LGev9a/lu3//XbZYhghnoVOVPUX1I8Ab/k/rdKD4eNZxwn/7ys3sj6Y6Zy8eItssQDns9jXU2fJI496AULcJPdI4NV72FaGr0pRUHCm89Lup9m5IQJ/Wnuh6iR8rgHOJbljHb+a7wkJMRIMzXSC4+Sq8q0XkBs5xgS7Ko+sgCF7ZQeCrg07aPj4GUZnOsE4xR8Zvij3PeoEeI984QKnoFZQPbz26+JCiC/TrM10WsHFdrlXxqcEAW52IyRxXh4ZQ5UcP7JOkzcrsD7TacwAK+a3yf0yvgK85+1wtwdK0ZBs0o4K36/ENBNTCYmZjh9CnGUF3sO72YhsKeM/AgDveTsZdylIuCybtNEsfCRI3Sc106kEwy/ybr5s5E/ZUkVDAQhfPPYDSFihU0Kr8INAbqajKIc/Oihb6mgqANEtAYNvFH6r0oPv7zpxP7WZTokA4SMtBSAmRoIfzUbFmOvImc5C2UKIgOEjgQQgtiT4UZrp9FCc6YQKHwksAElKQpDS0giyMx0kZPhIKAGIiZHQqPSQnekgEcJHQgtAbJQjsjMdJGL4SCQBiCkJpZkOue90rhMjfCSyACSqhKBz/kLRYZu+W0nvOx1FzPCRWAIQnSNh5/FF7OAf8+QRMRIIH4ktANElYd9vkX+To5eEwkcSEYDokdBivmqAm6cNyz1JguEjiQlAkpaw/LbTcs8eyyrPIeHwkYCXw3CIQ20LWNHph0+v+x1MGAquwz6A6wBOQYdGp8hWM2DPX3rrGfbM/KOlH+dqCB/RIgBJSgIZCmxu0uEjiZagSnTOjoyCPV9T+Ii2EaBI9UjQVHYq0S4ASaUEA+EjRgQgqZJgKHzEmAAkFRIMho8YFYCQlmA4fMS4AISkBAvhI1YEIKQkWAof0XYf0Aoi9wkCwv8Zwl9oI3zE2ghQwEiY5xYzex0ucJUc/l+juU5hsecrrI0ABYyEX/b+2rnyv/yUd+EQv/lyvTd0QyB8xPoIUBi9JhAJHyEjADEigVD4CCkBiFYJxMJHyAlAtEggGD5CUgCSqASi4SNkBSCJSCAcPkJaAAISot8nEA8fsX4foHisty8Dr2nw4kLgDapgq3o3cLxPcDLFp+CeFTvLuAofISPgy+3v4GOpcA1Vx+oXXnZ4xc/nQMJAqK8tasJf3ds3C8SWn0cD+w6KXvX8hpxssgYZARA6Bwl4F4xrlLMYEmzLPwb1vjvi7nIv3OYMwHVjcU3PvwKvvAweQ8fPRsPWH8lAaQQIJWHPe1vysrnqWUW8a+xHlsnPh923oZv/VWqVCHaGcdHH3NFFPgvi8NdV6jML8FIPgRuTW2uQELDmxVfL9QYlYHlAEdBYt6yTL2aXedfo67wrP4eNObOZ697NstmZ/NHRTr4kv9VvKWibm4FLSnnZB2690QVlDmVYhYSAL7ZtElCnMXQvJDUahOs0PT++/No53j12snb5fy2f7dgs4JKiPktdzB1XCOu/dychAMnk2rH3YyAObLMQzvSvdngX5kQoODn4SC/8NhgM7fDq2Pv+VusjYBKrMPY/RQtkakURHR4AAAAASUVORK5CYII="

janela_principal = tk.Tk()
logo = tk.PhotoImage(data=base64.b64decode(icone_base64))
janela_principal.title("Lima Slope")
janela_principal.geometry('1280x750')
#janela_principal.attributes("-fullscreen", True)
janela_principal.iconphoto(False, logo)
janela_principal.config(bg=bg_janela)
janela_principal.grid_columnconfigure(0, weight=0)
janela_principal.grid_columnconfigure(1, weight=1)
janela_principal.grid_rowconfigure(0, weight=1)


#------------------------------------------------------------------------------------------------------#

coluna_input = tk.Frame(janela_principal, bg=bg_janela)
coluna_input.grid(row=0, column=0, padx=(pad_ext, pad_int/2), pady=pad_ext,sticky="NEWS")
coluna_input.grid_rowconfigure(0, weight=1)
coluna_input.grid_rowconfigure(1, weight=0)
coluna_input.grid_columnconfigure(0, weight= 1)


frame_entrada = tk.Frame(coluna_input, bg=bg_frame)
frame_entrada.grid(row=0, column=0, padx=0, pady=0, sticky="NESW", rowspan=1)
frame_entrada.columnconfigure(0, weight= 1)
frame_entrada.rowconfigure([0,1,2,3,4,5,6], weight=0)
frame_entrada.rowconfigure([7], weight=1)


# frame_camadas = tk.Frame(coluna_input, bg=bg_frame)
# frame_camadas.grid(row=1, column=0, padx=0, pady=10,sticky="NESW")
# frame_camadas.grid_columnconfigure(0, weight= 1)

frame_parametros = tk.Frame(coluna_input, bg=bg_frame,padx=pad_frame_x ,pady=pad_frame_y)
frame_parametros.grid(row=1, column=0, padx=0, pady=(10,0),sticky="NESW")
frame_parametros.grid_columnconfigure(0, weight= 1)

#-----------------------------------------------------------------------------------------------------#

coluna_output = tk.Frame(janela_principal, bg=bg_janela)
coluna_output.grid(row=0, column=1, padx=(pad_int/2, pad_ext), pady=(pad_ext, pad_ext),sticky="NEWS")
coluna_output.grid_rowconfigure(0, weight=1)
coluna_output.grid_rowconfigure(1, weight=0)
coluna_output.grid_columnconfigure(0, weight=1)

frame_grafico = tk.Frame(coluna_output, bg=bg_frame)
frame_grafico.grid(row=0, column=0, pady=(0, pad_int/2),sticky="NEWS")
frame_grafico.columnconfigure(0, weight=1)
frame_grafico.rowconfigure(0, weight=1)

resultado = tk.Frame(coluna_output, bg=bg_janela)
resultado.grid(row=1, column=0, pady=(pad_int/2, 0),sticky="NEWS")
resultado.columnconfigure(0, weight=1)
resultado.columnconfigure(1, weight=1)
resultado.rowconfigure(0, weight=1)

saida = tk.Frame(resultado, bg=bg_frame)
saida.grid(row=0, column=0, padx=(0, pad_int/2), sticky="NEWS")
saida.rowconfigure([0,1,2,3,4], weight=1)
saida.columnconfigure([0,1], weight=1, uniform="fred")


frame_exportar = tk.Frame(resultado, bg=bg_frame)
frame_exportar.grid(row=0, column=1, padx=(pad_int/2), sticky="NEWS")
frame_exportar.columnconfigure(0, weight=1)
frame_exportar.rowconfigure([0,1,2], weight=0)



















#------------------------------------------------------------------------------------------------------#

label_entrada = tk.Label(frame_entrada,
                    text="ENTRADA",
                    font=fonte_titulo, fg=cor_fonte, bg=bg_frame)
label_entrada.grid(row=0, column=0, sticky="w", padx=pad_txt)

bt_importar_superficie_terreno = tk.Button(frame_entrada,
                                        command=importa_superficie_terreno,
                                        text = "Importar Superfície do terreno",
                                        anchor="w", 
                                        relief = estilo_bt, bg = bg_frame, fg= cor_fonte, font=fonte_normal)
bt_importar_superficie_terreno.grid(row=1, column=0, sticky="EW", padx=pad_txt)

bt_importar_nivel_agua = tk.Button(frame_entrada,
                                        command=importa_nivel_agua,
                                        text = "Importar Nível d'água",
                                        anchor="w", 
                                        state= tk.DISABLED,
                                        relief = estilo_bt, bg = bg_frame, fg= cor_fonte, font=fonte_normal)
bt_importar_nivel_agua.grid(row=2, column=0, sticky="EW", padx=pad_txt)

bt_criar_solo = tk.Button(frame_entrada,
                                        command=cria_solo,
                                        text = "Criar Tipo de Solo",
                                        anchor="w",
                                        state= tk.DISABLED,
                                        relief = estilo_bt, bg = bg_frame, fg= cor_fonte, font=fonte_normal)
bt_criar_solo.grid(row=3, column=0, sticky="EW", padx=pad_txt)

bt_importar_camada = tk.Button(frame_entrada,
                                        command=importa_camada,
                                        text = "Importar Camada",
                                        anchor="w",
                                        #state= tk.DISABLED,
                                        relief = estilo_bt, bg = bg_frame, fg= cor_fonte, font=fonte_normal)
bt_importar_camada.grid(row=4, column=0, sticky="EW", padx=pad_txt)

bt_cria_carregamento = tk.Button(frame_entrada,
                                command=cria_carregamento,
                                text = "Criar carregamento",
                                anchor="w",
                                state= tk.DISABLED,
                                relief = estilo_bt, bg = bg_frame, fg= cor_fonte, font=fonte_normal)
bt_cria_carregamento.grid(row=5, column=0, sticky="EW", padx=pad_txt)

bt_importa_sup_ruptura = tk.Button(frame_entrada,
                                command=importa_superficie_ruptura,
                                text = "Importar Superfície de ruptura qualquer",
                                anchor="w",
                                state= tk.DISABLED,
                                relief = estilo_bt, bg = bg_frame, fg= cor_fonte, font=fonte_normal)
bt_importa_sup_ruptura.grid(row=6, column=0, sticky="EW", padx=pad_txt)

frame_bt_entrada = tk.Frame(frame_entrada, bg=bg_frame, padx=pad_frame_x ,pady=pad_frame_y)
frame_bt_entrada.grid(row=7, column=0, padx=0, pady=0, sticky="ESW")
frame_bt_entrada.grid_columnconfigure(0, weight= 1)

bt_zerar_tudo = tk.Button(frame_bt_entrada,
                            command= zera_tudo,
                            text = "Zerar",
                            width=7,
                            height= 1,
                            relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal)
bt_zerar_tudo.grid(row=0, column=0, columnspan=1, sticky="ws")

bt_abrir_arquivo = tk.Button(frame_bt_entrada,
                            command= abrir_arquivo,
                            text = "Abrir",
                            width=7,
                            height= 1,
                            relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal)
bt_abrir_arquivo.grid(row=0, column=1, columnspan=1, sticky="ws")
bt_salvar_arquivo = tk.Button(frame_bt_entrada,
                            command= salvar_arquivo,
                            text = "Salvar",
                            width=7,
                            height= 1,
                            relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal)
bt_salvar_arquivo.grid(row=0, column=2, columnspan=1, sticky="ws")
#------------------------------------------------------------------------------------------------------#

# label_entrada = tk.Label(frame_camadas,
#                     text="CAMADAS",
#                     font=fonte_titulo, fg=cor_fonte, bg=bg_frame)
# label_entrada.grid(row=0, column=0, sticky="w", padx=pad_txt)

#------------------------------------------------------------------------------------------------------# PARAMETROS
#ENTRADA

label_entrada = tk.Label(frame_parametros,
                    text="PARÂMETROS",
                    font=fonte_titulo, fg=cor_fonte, bg=bg_frame)
label_entrada.grid(row=0, column=0, columnspan= 4, sticky="w", padx=pad_txt)

#CENTRO DE RUPTURA

label_centro_sup_rup = tk.Label(frame_parametros,
                    text="Centro superfície de ruptura",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_centro_sup_rup.grid(row=1, column=0, columnspan= 4, sticky="n", padx=pad_txt)

#X INICIAL

label_x_inicial = tk.Label(frame_parametros,
                    text="x inicial = ",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_x_inicial.grid(row=2, column=0, sticky="w", padx=pad_txt)

entry_x_inicial = tk.Entry(frame_parametros,
                           width=tam_entry
                           )

entry_x_inicial.grid(row=2, column=1, sticky="w")

label_m_x_inicial = tk.Label(frame_parametros,
                    text="m",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_m_x_inicial.grid(row=2, column=2, sticky="w", padx=pad_txt)

#INCREMENTO CENTRO

label_inc_centro = tk.Label(frame_parametros,
                    text="inc. = ",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_inc_centro.grid(row=2, column=3, sticky="w", padx=(10, pad_txt))

entry_inc_centro = tk.Entry(frame_parametros,
                    width=tam_entry)
entry_inc_centro.grid(row=2, column=4, sticky="w")

label_m_inc_centro = tk.Label(frame_parametros,
                    text="m",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_m_inc_centro.grid(row=2, column=5, sticky="w", padx=pad_txt)

#X FINAL

label_x_final = tk.Label(frame_parametros,
                    text="x final = ",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_x_final.grid(row=3, column=0, sticky="w", padx=pad_txt)

entry_x_final = tk.Entry(frame_parametros,
                           width=tam_entry)
entry_x_final.grid(row=3, column=1, sticky="w")

label_m_x_final = tk.Label(frame_parametros,
                    text="m",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_m_x_final.grid(row=3, column=2, sticky="w", padx=pad_txt)

#Y INICIAL

label_y_inicial = tk.Label(frame_parametros,
                    text="y inicial = ",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_y_inicial.grid(row=4, column=0, sticky="w", padx=pad_txt)

entry_y_inicial = tk.Entry(frame_parametros,
                           width=tam_entry)
entry_y_inicial.grid(row=4, column=1, sticky="w")

label_m_y_inicial = tk.Label(frame_parametros,
                    text="m",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_m_y_inicial.grid(row=4, column=2, sticky="w", padx=pad_txt)

#Y FINAL

label_y_final = tk.Label(frame_parametros,
                    text="y final = ",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_y_final.grid(row=5, column=0, sticky="w", padx=pad_txt) 

entry_y_final = tk.Entry(frame_parametros,
                           width=tam_entry)
entry_y_final.grid(row=5, column=1, sticky="w")

label_m_y_final = tk.Label(frame_parametros,
                    text="m",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_m_y_final.grid(row=5, column=2, sticky="w", padx=pad_txt)


#RAIO SUPERFÍCIE DE RUPTURA

label_raio_sup_rup = tk.Label(frame_parametros,
                    text="Raio da superfície de ruptura",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_raio_sup_rup.grid(row=6, column=0, columnspan= 4, sticky="n", padx=pad_txt)


#RAIO INICIAL

label_r_inicial = tk.Label(frame_parametros,
                    text="Raio inicial = ",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_r_inicial.grid(row=7, column=0, sticky="w", padx=pad_txt)

entry_r_inicial = tk.Entry(frame_parametros,
                           width=tam_entry)
entry_r_inicial.grid(row=7, column=1, sticky="w")

label_m_r_inicial = tk.Label(frame_parametros,
                    text="m",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_m_r_inicial.grid(row=7, column=2, sticky="w", padx=pad_txt)


#INCREMENTO RAIO

label_inc_raio = tk.Label(frame_parametros,
                    text="inc. = ",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_inc_raio.grid(row=7, column=3, sticky="w", padx=(10,pad_txt))

entry_inc_raio = tk.Entry(frame_parametros,
                    width=tam_entry)
entry_inc_raio.grid(row=7, column=4, sticky="w")

label_m_inc_raio = tk.Label(frame_parametros,
                    text="m",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_m_inc_raio.grid(row=7, column=5, sticky="w", padx=pad_txt)



#RAIO FINAL

label_r_final = tk.Label(frame_parametros,
                    text="Raio final = ",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_r_final.grid(row=8, column=0, sticky="w", padx=pad_txt)

entry_r_final = tk.Entry(frame_parametros,
                           width=tam_entry)
entry_r_final.grid(row=8, column=1, sticky="w")

label_m_r_final = tk.Label(frame_parametros,
                    text="m",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_m_r_final.grid(row=8, column=2, sticky="w", padx=pad_txt)


#CONFIGURAÇÃO DAS FATIAS

label_config_fatias = tk.Label(frame_parametros,
                    text="Configuração das fatias",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_config_fatias.grid(row=9, column=0, columnspan= 4, sticky="n", padx=pad_txt)

#LARGURA DAS FATIAS

label_dx = tk.Label(frame_parametros,
                    text="dx =",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_dx.grid(row=10, column=0, sticky="w", padx=pad_txt) 

entry_dx = tk.Entry(frame_parametros,
                           width=tam_entry)
entry_dx.grid(row=10, column=1, sticky="w")

label_m_dx = tk.Label(frame_parametros,
                    text="m",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_m_dx.grid(row=10, column=2, sticky="w", padx=pad_txt)

#RUN

bt_run = tk.Button(frame_parametros,
                    command= run,
                    text = "Run",
                    width=7,
                    height= 1,
                    relief = estilo_bt, bg = bg_bt, fg= cor_fonte, font=fonte_normal)
bt_run.grid(row=11, column=4, columnspan=3, sticky="ew")

#--------------------------------------------Resultado----------------------------------------------#

label_metodo = tk.Label(saida,
                    text="Método",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_metodo.grid(column=0, row=0, sticky="NEWS")

label_FS = tk.Label(saida,
                    text="Fator de Segurança",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_FS.grid(column=1, row=0, sticky="NEWS")

label_metodo1 = tk.Label(saida,
                    text="Fellenius",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_metodo1.grid(column=0, row=1, sticky="NEWS")

label_FS1 = tk.Label(saida,
                    text="-",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_FS1.grid(column=1, row=1, sticky="NEWS")

label_metodo2 = tk.Label(saida,
                    text="Bishop simplificado",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_metodo2.grid(column=0, row=2, sticky="NEWS")

label_FS2 = tk.Label(saida,
                    text="-",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_FS2.grid(column=1, row=2, sticky="NEWS")

label_metodo3 = tk.Label(saida,
                    text="Morgenstern Price",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_metodo3.grid(column=0, row=3, sticky="NEWS")

label_FS3 = tk.Label(saida,
                    text="-",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_FS3.grid(column=1, row=3, sticky="NEWS")

label_metodo4 = tk.Label(saida,
                    text="Spencer",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_metodo4.grid(column=0, row=4, sticky="NEWS")

label_FS4 = tk.Label(saida,
                    text="-",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_FS4.grid(column=1, row=4, sticky="NEWS")

label_metodo5 = tk.Label(saida,
                    text="Sarma",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_metodo5.grid(column=0, row=5, sticky="NEWS")

label_FS5 = tk.Label(saida,
                    text="-",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_FS5.grid(column=1, row=5, sticky="NEWS")

label_posicao = tk.Label(saida,
                    text="Posição Crítica",
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_posicao.grid(column=0, row=6, sticky="NEWS")

label_FS_posicao = tk.Label(saida,
                    text=("x =          -          y =          -          r =          -          "),
                    borderwidth=2,
                    relief="ridge",
                    font=fonte_normal, fg=cor_fonte, bg=bg_frame)
label_FS_posicao.grid(column=1, row=6, sticky="NEWS")

#--------------------------------------------Resultado----------------------------------------------#

label_exportar = tk.Label(frame_exportar,
                    text="EXPORTAR",
                    font=fonte_titulo, fg=cor_fonte, bg=bg_frame)
label_exportar.grid(row=0, column=0, sticky="w", padx=pad_txt)

bt_exporta_csv = tk.Button(frame_exportar,
                            command=exporta_csv_fatias,
                            text = "Propriedades das fatias (.csv)",
                            anchor="w", 
                            state= tk.DISABLED,
                            relief = estilo_bt, bg = bg_frame, fg= cor_fonte, font=fonte_normal)
bt_exporta_csv.grid(row=1, column=0, sticky="EW", padx=pad_txt)

bt_exporta_grafico = tk.Button(frame_exportar,
                                command=exporta_grafico,
                                text = "Gráfico (.png)",
                                anchor="w", 
                                state= tk.DISABLED,
                                relief = estilo_bt, bg = bg_frame, fg= cor_fonte, font=fonte_normal)
bt_exporta_grafico.grid(row=2, column=0, sticky="EW", padx=pad_txt)


#--------------------------------------------Gráfico----------------------------------------------#


fig = Figure(constrained_layout=True)
gspec = fig.add_gridspec(nrows=7, ncols=1)
ax0 = fig.add_subplot(gspec[0,0])
ax0.xaxis.set_major_locator(ticker.NullLocator())
ax0.xaxis.set_minor_locator(ticker.NullLocator())
ax0.set_title('Carregamentos')


ax1 = fig.add_subplot(gspec[1:,0])
#ax1.grid()
ax1.set_xlabel('(m)')   
ax1.set_ylabel('Cota (m)')
ax1.set_title('Perfil Longitudinal')

norm = pltc.Normalize(vmin=0, vmax=3)
cmap = pltc.LinearSegmentedColormap.from_list('FS_cmap',['red', 'red', 'red', 'red', 'orange', 'yellow', 'green', 'blue'])
#cmap = pltc.ListedColormap(['red', 'red', 'red', 'red', 'orange', 'yellow', 'green', 'blue'])



fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax= ax1, label="FS")




canvas_grafico = FigureCanvasTkAgg(fig, frame_grafico)
canvas_grafico.get_tk_widget().grid(row=0, column=0, sticky="NEWS", padx=pad_frame_x, pady=pad_frame_y)
canvas_grafico.draw()

janela_principal.mainloop()

