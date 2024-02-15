class Forca_distribuda:
    def __init__(self, forca: float, posicao: float):
        self.forca = forca 
        self.posicao = posicao
        self.tipo = "distribuida"
        def __repr__(self):
            return ("Carregamento distribuido de", self.forca, "distribuido de", self.posicao, "m")        
    
        
        
