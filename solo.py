import numpy as np

class Solo:
    
    def __init__(self,nomeclatura: str, gama: float, fi: float, coesao: float = 0):
        self.nomeclatura = nomeclatura
        self.gama = gama
        self.fi = fi * np.pi / 180
        self.coesao = coesao
    def __repr__(self):
        return self.nomeclatura