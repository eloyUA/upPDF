from fpdf import FPDF
from typing import Tuple
from modelo.imagen_escaner import ImagenEscaner
from modelo.errores import ErrorGuardarPdf

class PdfEscanerEscritura():
    def __init__(self):
        self.__pdf = FPDF(unit='mm')

    def añadir_imagen_escaner(self, img_escaner: ImagenEscaner,
                            tamaño_mm_pag: Tuple[int, int]) -> None:
        self.__pdf.add_page(
            format=tamaño_mm_pag,
        )
        self.__pdf.image(
            name=img_escaner.get_imagen(),
            x=0, 
            y=0,
            w=tamaño_mm_pag[0],
            h=tamaño_mm_pag[1]
        )

    def guardar(self, ruta: str) -> None:
        """ Requisitos: Debe tener ya el nombre y la extension del pdf """
        if ruta[-4:] != '.pdf':
            raise ErrorGuardarPdf('No se reconoce el nombre de la extension')
        
        self.__pdf.output(ruta)