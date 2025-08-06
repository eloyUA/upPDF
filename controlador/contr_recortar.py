import tkinter.filedialog as filedialog
import modelo.manejo_pdfs as manejo_pdfs

class ControladorRecortar():
    def __init__(self, vista_recortar):
        self.__vista_recortar = vista_recortar

        # Atributos para almacenar la ruta del pdf a recortar junto con los
        # recortes de las paginas [(pag_ini, pag_fin), ...]
        self.__ruta_pdf = ''
        self.__recortes = []
        self.__num_paginas = None

    def click_btn_archivo(self) -> None:
        if self.__ruta_pdf != '':
            return
        
        ruta = filedialog.askopenfilename(filetypes=(('pdf', '*.pdf'),))
        if len(ruta) == 0:
            return
        
        pos_barra = ruta.rfind('/')
        if pos_barra == -1:
            nombre_pdf = ruta
        else:
            nombre_pdf = ruta[pos_barra + 1:]
        self.__ruta_pdf = ruta
        self.__num_paginas = manejo_pdfs.num_paginas_totales(ruta)
        self.__recortes.clear()

        self.__vista_recortar.poner_nombre_pdf_btn_buscar_archivo(
            nombre_pdf + f" ({self.__num_paginas}pags)")
        self.__vista_recortar.hacer_visible_btn_eliminar_pdf()
        self.__vista_recortar.deshabilitar_btn_archivo()
        self.__vista_recortar.habilitar_input_recorte()

    def click_btn_eliminar_pdf(self) -> None:
        for i in range(len(self.__recortes)):
            self.__vista_recortar.quitar_ultimo_recorte()
        self.__recortes.clear()
        self.__ruta_pdf = ''

        self.__vista_recortar.poner_estado_por_defecto()

    def click_agregar_recorte(self) -> None:
        if self.__ruta_pdf == '':
            return
        
        try:
            desde = (int) (self.__vista_recortar.obtener_valor_caja_desde())
            hasta = (int) (self.__vista_recortar.obtener_valor_caja_hasta())
            if desde > hasta or desde <= 0 or hasta > self.__num_paginas:
                return
        except Exception as ex:
            ex.with_traceback()
        else:
            self.__recortes.append((desde, hasta))
            self.__vista_recortar.agregar_recorte(desde, hasta)

            if len(self.__recortes) == 1:
                self.__vista_recortar.habilitar_btn_recortar()
                self.__vista_recortar.habilitar_btn_borrar()

    def click_btn_recortar(self) -> None:
        if self.__ruta_pdf == '' or len(self.__recortes) == 0:
            return
        
        manejo_pdfs.recortar(self.__ruta_pdf, self.__recortes)
        self.click_btn_eliminar_pdf()

    def click_btn_borrar(self) -> None:
        if self.__ruta_pdf == '' or len(self.__recortes) == 0:
            return
        
        self.__recortes.pop(-1)
        self.__vista_recortar.quitar_ultimo_recorte()

        if len(self.__recortes) == 0:
            self.__vista_recortar.deshabilitar_btn_recortar()
            self.__vista_recortar.deshabilitar_btn_borrar()