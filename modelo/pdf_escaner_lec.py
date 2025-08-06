import fitz

from typing import Tuple
from modelo.errores import ErrorAperturaPDF
from modelo.imagen_escaner import ImagenEscaner

class PdfEscanerLectura():
    def __init__(self, ruta: str) -> None:
        try:
            self.__doc = fitz.open(ruta)
        except Exception as e:
            raise ErrorAperturaPDF('No se pudo abrir el pdf.') from e
        else:
            self.__ruta = ruta
            self.__resolucion_buena = (1684, 2384)
            self.__resolucion_mala = (595, 842)

    def __obtener_imagen_pagina(self, num_pag: int,
                                buena_calidad: bool) -> fitz.Pixmap:
        """ El numero de pagina comienza en 0. """

        # Se calcula la escala para dejar la imagen de la pagina a
        # una calidad buena o mala.
        pix = self.__doc[num_pag].get_pixmap(matrix=fitz.Matrix(0.1, 0.1))
        ancho_img = pix.width * 10
        alto_img = pix.height * 10
        if buena_calidad:
            if ancho_img <= alto_img: # Vertical
                res_objetivo = self.__resolucion_buena
            else:
                res_objetivo = (self.__resolucion_buena[1],
                                self.__resolucion_buena[0])
                
            if (ancho_img >= res_objetivo[0] and
                alto_img >= res_objetivo[1]):
                esc = (1, 1)
            else:
                esc = (
                    res_objetivo[0] / ancho_img,
                    res_objetivo[1] / alto_img
                )
        else:
            if ancho_img <= alto_img: # Vertical
                res_objetivo = self.__resolucion_mala
            else:
                res_objetivo = (self.__resolucion_mala[1],
                                self.__resolucion_mala[0])
                
            esc = (
                res_objetivo[0] / ancho_img,
                res_objetivo[1] / alto_img
            )

        # Obtenemos la imagen y le quitamos las transparencias (RGBA) => RGB
        pix = self.__doc[num_pag].get_pixmap(matrix=fitz.Matrix(esc[0], esc[1]))
        if pix.alpha:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        return pix

    def get_imagen_pagina_buena_calidad(self, num_pag: int) -> ImagenEscaner:
        """ El numero de pagina comienza en 1. """
        return ImagenEscaner(self.__obtener_imagen_pagina(num_pag - 1, True))
    
    def get_imagen_pagina_mala_calidad(self, num_pag: int) -> ImagenEscaner:
        """ El numero de pagina comienza en 1. """
        return ImagenEscaner(self.__obtener_imagen_pagina(num_pag - 1, False))
    
    def get_tamaño_mm_pag(self, num_pag: int) -> Tuple[int, int]:
        """ 
            El numero de pag comienza en 1.
            [ancho en mm, alto en mm]
        """
        ancho_mm = round(self.__doc[num_pag - 1].rect.width * 25.4 / 72)
        alto_mm = round(self.__doc[num_pag - 1].rect.height * 25.4 / 72)
        pixmap = self.__doc[num_pag - 1].get_pixmap(matrix=fitz.Matrix(0.1, 0.1))
        if pixmap.width < pixmap.height and ancho_mm > alto_mm:
            return alto_mm, ancho_mm
        elif pixmap.width > pixmap.height and ancho_mm < alto_mm:
            return alto_mm, ancho_mm
        else:
            return ancho_mm, alto_mm

    def num_pag_totales(self) -> int:
        return len(self.__doc)

    def get_ruta(self) -> str:
        return self.__ruta

    def cerrar(self):
        self.__doc.close()