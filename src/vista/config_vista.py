from pathlib import Path

class ConfigVista:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.TIPO_LETRA = 'Comfortaa Bold'
        self.RUTA_ABS_PROGRAMA = (str) (Path(__file__).parent.resolve())+'/..'