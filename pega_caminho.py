# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import tkinter as tk
from tkinter import END, filedialog


# janela = tk.Tk()
# figura = Figure()
# figura.clear()
# ax = figura.add_subplot(111)
# figura.subplots_adjust(left=0.10, right=0.95, bottom=0.10)

# ax.scatter([0,1,2,3,4,5], [0,1,2,3,4,5])#, label = "Terreno", color = "brown", linewidth = 2)
# canvas_grafico = FigureCanvasTkAgg(figura, janela)
# canvas_grafico.get_tk_widget().grid(row=0, column=0, sticky="NEWS")
# canvas_grafico.draw()

# janela.mainloop()

# lista = []
# for i in range (0, len(lista)):
#     print(i)

# from forca_pontual import Forca_pontual
# from forca_distribuida import Forca_distribuda
# from superficie_terreno import Superficie_Terreno
# from utils import compila_forcas

# supeficie_terreno_ex1 = Superficie_Terreno("C:/Users/pedro/OneDrive/TCC/Bishop Simplified Method/Exemplo_01/00_terreno.dxf")
# F1 = Forca_distribuda([10,20], [40,50])
# F2 = Forca_pontual(10, 40)
# lista_forcas = [F2, F1]

# teste = compila_forcas(supeficie_terreno_ex1.dominio, lista_forcas)
# comparacao = [[0 for i in range(0,2)] for j in range(0,len(supeficie_terreno_ex1.dominio))]

# print(teste)

filename = filedialog.askopenfilename(initialdir = "/",title = "Selecione o arquivo dxf", filetypes=[("DXF","*.dxf")])
print(filename)  
