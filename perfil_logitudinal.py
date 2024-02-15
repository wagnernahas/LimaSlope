from nivel_agua import Nivel_Agua
from superficie_terreno import Superficie_Terreno
from camada import Camada
from nan import Nan

class Perfil_Longitudinal:
    
    def __init__(self, superficie_terreno: Superficie_Terreno, lista_camadas: list[Camada], nivel_agua = Nan()):
        self.superficie_terreno = superficie_terreno
        self.lista_camadas = lista_camadas
        self.nivel_agua = nivel_agua
        self.dominio = self.superficie_terreno.dominio