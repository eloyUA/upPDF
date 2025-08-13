import modelo.manejo_pdfs as manejo_pdfs

from tkinter import filedialog

class ControladorCombinar():
    def __init__(self, vista_combinar):
        self.__vista_combinar = vista_combinar
        
        # Contiene las rutas completas de los pdf a combinar
        self.__rutas_pdfs = []

    def click_btn_agregar(self) -> None:
        ruta = filedialog.askopenfilename(filetypes=(('pdf', '*.pdf'),))
        if len(ruta) == 0:
            return
        
        # Agregamos el nombre del pdf a la vista
        pos_barra = ruta.rfind('/')
        if pos_barra == -1:
            nombre_pdf = ruta
        else:
            nombre_pdf = ruta[pos_barra + 1:]
        self.__vista_combinar.agregar_pdf(nombre_pdf)
        self.__rutas_pdfs.append(ruta)

        # Habilitamos o desabilitamos ciertos botones
        if len(self.__rutas_pdfs) == 1:
            self.__vista_combinar.habilitar_btn_eliminar()
        elif len(self.__rutas_pdfs) == 2:
            self.__vista_combinar.habilitar_btn_combinar()

    def click_btn_eliminar(self) -> None:
        if len(self.__rutas_pdfs) == 0:
            return
        
        self.__vista_combinar.quitar_ultimo_pdf()
        self.__rutas_pdfs.pop(-1)

        if len(self.__rutas_pdfs) == 0:
            self.__vista_combinar.deshabilitar_btn_eliminar()
        elif len(self.__rutas_pdfs) == 1:
            self.__vista_combinar.deshabilitar_btn_combinar()

    def click_btn_combinar(self) -> None:
        if len(self.__rutas_pdfs) <= 1:
            return
        
        # Combinamos los pdfs
        ruta_final = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos pdf", "*.pdf")],
            title="Guardar como"
        )
        manejo_pdfs.combinar(self.__rutas_pdfs, ruta_final)

        # Dejamos todo por defecto
        for i in range(len(self.__rutas_pdfs)):
            self.__vista_combinar.quitar_ultimo_pdf()
        self.__rutas_pdfs.clear()

        self.__vista_combinar.poner_estado_por_defecto()