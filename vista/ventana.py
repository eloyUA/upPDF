import customtkinter as ctk

from vista.vista_mejorar import VistaMejorar
from vista.vista_editar import VistaEditar
from vista.vista_combinar import VistaCombinar
from vista.vista_recortar import VistaRecortar
from vista.vista_info import VistaInfo
from vista.vista_menu import VistaMenu

from controlador.contr_menu import ControladorMenu
from controlador.contr_mejorar import ControladorMejorar
from controlador.contr_editar import ControladorEditar
from controlador.contr_combinar import ControladorCombinar
from controlador.contr_recortar import ControladorRecortar

from vista.config_vista import ConfigVista

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class Ventana(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        # Cargamos la configuracion inicial
        self.__config = ConfigVista()

        # Se configura la ventana principal
        self.title('upPDF')
        self.geometry(f'{self.__config.WIDTH}x{self.__config.HEIGHT}')
        self.minsize(width=self.__config.WIDTH, height=self.__config.HEIGHT)
        self.maxsize(width=self.__config.WIDTH, height=self.__config.HEIGHT)

        pos_x = (self.winfo_screenwidth() - self.__config.WIDTH) // 2
        pos_y = (self.winfo_screenheight() - self.__config.HEIGHT) // 2
        self.geometry('+{}+{}'.format(pos_x, pos_y))

        # Se cargan todos los widgets
        self.__vista_mejorar_PDF = VistaMejorar(self)
        self.__vista_editar_PDF = VistaEditar(self)
        self.__vista_combinar_PDF = VistaCombinar(self)
        self.__vista_recortar_PDF = VistaRecortar(self)
        self.__vista_info = VistaInfo(self)
        self.__vista_menu = VistaMenu(self)

        self.__controlador_menu = ControladorMenu(
            self.__vista_menu,
            self.__vista_mejorar_PDF,
            self.__vista_editar_PDF,
            self.__vista_combinar_PDF,
            self.__vista_recortar_PDF,
            self.__vista_info,
            self.__vista_mejorar_PDF
        )
        self.__vista_menu.cargar_controlador(self.__controlador_menu)
        self.__vista_menu.cargar_elementos()

        self.__controlador_mejorar = ControladorMejorar(self.__vista_mejorar_PDF)
        self.__vista_mejorar_PDF.cargar_controlador(self.__controlador_mejorar)
        self.__vista_mejorar_PDF.cargar_elementos()

        self.__controlador_editar = ControladorEditar(self.__vista_editar_PDF)
        self.__vista_editar_PDF.cargar_controlador(self.__controlador_editar)
        self.__vista_editar_PDF.cargar_elementos()

        self.__controlador_combinar = ControladorCombinar(self.__vista_combinar_PDF)
        self.__vista_combinar_PDF.cargar_controlador(self.__controlador_combinar)
        self.__vista_combinar_PDF.cargar_elementos()

        self.__controlador_recortar = ControladorRecortar(self.__vista_recortar_PDF)
        self.__vista_recortar_PDF.cargar_controlador(self.__controlador_recortar)
        self.__vista_recortar_PDF.cargar_elementos()

        self.__vista_info.cargar_elementos()