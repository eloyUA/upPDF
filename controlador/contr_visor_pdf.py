from tkinter import filedialog

from modelo.imagen_escaner import ImagenEscaner
from modelo.pdf_escaner_lec import PdfEscanerLectura
from vista.visor_pdf_eventos import EventosVisorPdf

class ControladorVisorPdf():
    def __init__(self, visor_pdf, eventos_visor: EventosVisorPdf) -> None:
        self.__visor_pdf = visor_pdf
        self.__eventos_visor = eventos_visor # Son los eventos a los que puede llamar
        self.__pdf = None # PdfEscanerLectura
        self.__num_pag_actual = 0

    def click_boton_buscar_archivo(self) -> None:
        if self.__pdf != None:
            return
        
        ruta = filedialog.askopenfilename(filetypes=(('pdf', '*.pdf'),))
        if len(ruta) == 0:
            return
        
        try:
            self.__pdf = PdfEscanerLectura(ruta)
        except Exception as e:
            pass # Mostrar alguna ventana de error
        else:
            self.__num_pag_actual = 1
            num_pag_max = self.__pdf.num_pag_totales()
            imagen = self.__pdf.get_imagen_pagina_mala_calidad(1).get_imagen()

            pos_barra = ruta.rfind('/')
            if pos_barra == -1:
                nombre_pdf = ruta
            else:
                nombre_pdf = ruta[pos_barra + 1:]

            self.__visor_pdf.desactivar_boton_buscar_archivo()
            self.__visor_pdf.actualizar_etiqueta_nombre_pdf(nombre_pdf)
            self.__visor_pdf.actualizar_imagen_pdf(imagen)
            self.__visor_pdf.actualizar_mostrador_paginas(1, num_pag_max)
            self.__visor_pdf.hacer_boton_eliminar_pdf_visible()

            self.__eventos_visor.evento_pdf_ya_introducido()
    
    def click_boton_eliminar_archivo(self) -> None:
        if self.__pdf != None:
            self.__pdf.cerrar()
        self.__pdf = None
        self.__num_pag_actual = 0

        self.__visor_pdf.activar_boton_buscar_archivo()
        self.__visor_pdf.actualizar_etiqueta_nombre_pdf('')
        self.__visor_pdf.actualizar_imagen_pdf(None)
        self.__visor_pdf.actualizar_mostrador_paginas(0, 0)
        self.__visor_pdf.hacer_boton_eliminar_pdf_invisible()

        self.__eventos_visor.evento_pdf_ya_quitado()

    # Métodos para actualizar la imagen del visor segun se avanza/retrocede
    def __actualizar_pagina(self) -> None:
        num_pag_max = self.__pdf.num_pag_totales()
        imagen = self.__pdf.get_imagen_pagina_mala_calidad(
            self.__num_pag_actual).get_imagen()

        self.__visor_pdf.actualizar_imagen_pdf(imagen)
        self.__visor_pdf.actualizar_mostrador_paginas(
            self.__num_pag_actual,
            num_pag_max
        )

    def click_boton_avanzar_pag(self) -> None:
        if self.__pdf == None:
            return
        if self.__num_pag_actual >= self.__pdf.num_pag_totales():
            return
        
        self.__num_pag_actual += 1
        self.__actualizar_pagina()
        self.__eventos_visor.evento_avanzar_pag_pdf()

    def click_boton_retroceder_pag(self) -> None:
        if self.__pdf == None:
            return
        if self.__num_pag_actual <= 1:
            return
        
        self.__num_pag_actual -= 1
        self.__actualizar_pagina()
        self.__eventos_visor.evento_retroceder_pag_pdf()

    def num_pag_actual(self) -> int:
        return self.__num_pag_actual

    def get_pdf(self) -> PdfEscanerLectura:
        return self.__pdf