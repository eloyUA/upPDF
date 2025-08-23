import customtkinter as ctk

from vista.vista_mejorar import VistaMejorar
from vista.vista_editar import VistaEditar
from vista.vista_combinar import VistaCombinar
from vista.vista_recortar import VistaRecortar
from vista.vista_info import VistaInfo
from vista.vista_menu import VistaMenu
from vista.config_vista import ConfigVista

from controlador.contr_menu import ControladorMenu
from controlador.contr_mejorar import ControladorMejorar
from controlador.contr_editar import ControladorEditar
from controlador.contr_combinar import ControladorCombinar
from controlador.contr_recortar import ControladorRecortar
class Ventana(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.__cargar_configuracion()
        self.__cargar_config_ventana_principal()
        self.__cargar_widgets()

    def __cargar_configuracion(self) -> None:
        self.__config = ConfigVista()

    def __cargar_config_ventana_principal(self) -> None:
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')

        self.title('upPDF')
        self.geometry(f'{self.__config.WIDTH}x{self.__config.HEIGHT}')
        self.minsize(width=self.__config.WIDTH, height=self.__config.HEIGHT)
        self.maxsize(width=self.__config.WIDTH, height=self.__config.HEIGHT)

        pos_x = (self.winfo_screenwidth() - self.__config.WIDTH) // 2
        pos_y = (self.winfo_screenheight() - self.__config.HEIGHT) // 2
        self.geometry('+{}+{}'.format(pos_x, pos_y))

    def __cargar_widgets(self) -> None:
        self.__cargar_vistas()
        self.__cargar_controladores()

    def __cargar_vistas(self) -> None:
        self.__vista_mejorar = VistaMejorar(self)
        self.__vista_editar = VistaEditar(self)
        self.__vista_combinar = VistaCombinar(self)
        self.__vista_recortar = VistaRecortar(self)
        self.__vista_info = VistaInfo(self)
        self.__vista_menu = VistaMenu(self)

    def __cargar_controladores(self) -> None:
        self.__cargar_controlador_vista_menu()
        self.__cargar_controlador_vista_mejorar()
        self.__cargar_controlador_vista_editar()
        self.__cargar_controlador_vista_combinar()
        self.__cargar_controlador_vista_recortar()
        self.__cargar_controlador_vista_info()

    def __cargar_controlador_vista_menu(self) -> None:
        self.__controlador_menu = ControladorMenu(
            self.__vista_menu,
            self.__vista_mejorar,
            self.__vista_editar,
            self.__vista_combinar,
            self.__vista_recortar,
            self.__vista_info,
            self.__vista_mejorar
        )
        self.__vista_menu.cargar_controlador(self.__controlador_menu)
        self.__vista_menu.cargar_elementos()

    def __cargar_controlador_vista_mejorar(self) -> None:
        self.__controlador_mejorar = ControladorMejorar(self.__vista_mejorar)
        self.__vista_mejorar.cargar_controlador(self.__controlador_mejorar)
        self.__vista_mejorar.cargar_elementos()

    def __cargar_controlador_vista_editar(self) -> None:
        self.__controlador_editar = ControladorEditar(self.__vista_editar)
        self.__vista_editar.cargar_controlador(self.__controlador_editar)
        self.__vista_editar.cargar_elementos()

    def __cargar_controlador_vista_combinar(self) -> None:
        self.__controlador_combinar = ControladorCombinar(self.__vista_combinar)
        self.__vista_combinar.cargar_controlador(self.__controlador_combinar)
        self.__vista_combinar.cargar_elementos()

    def __cargar_controlador_vista_recortar(self) -> None:
        self.__controlador_recortar = ControladorRecortar(self.__vista_recortar)
        self.__vista_recortar.cargar_controlador(self.__controlador_recortar)
        self.__vista_recortar.cargar_elementos()

    def __cargar_controlador_vista_info(self) -> None:
        self.__vista_info.cargar_elementos()