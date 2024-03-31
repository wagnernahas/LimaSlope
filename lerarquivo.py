import ezdxf as ez
import os
import csv

def pega_pontos(caminho_arquivo):
    filename, file_extension = os.path.splitext(caminho_arquivo)
    if (file_extension == ".dxf"):
        return readDXF(caminho_arquivo)
    elif (file_extension == ".txt"):
        return readXYFile(caminho_arquivo)

def readDXF(caminho_arquivo):
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

def readXYFile(caminho_arquivo):
    points = []
    with open(caminho_arquivo) as inf:
        reader = csv.reader(inf, delimiter=" ")
        for row in reader:
            p = [float(row[0]), float(row[1]) ]
            points.append(p)
        return points