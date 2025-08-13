
class ErrorAperturaPDF(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class ErrorImagenEscanerRGBA(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class ErrorPixelPosicionInvalida(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class ErrorGuardarPdf(Exception):
    def __init__(self, *args):
        super().__init__(*args)