from vista.componentes.frame_seccion import FrameSeccion
from vista.vista_mejorar import VistaMejorar
from vista.vista_editar import VistaEditar
from vista.vista_combinar import VistaCombinar
from vista.vista_recortar import VistaRecortar
from vista.vista_info import VistaInfo

class ControladorMenu:
    def __init__(self, vista_menu, vista_mejorar: VistaMejorar,
                vista_editar: VistaEditar, vista_combinar: VistaCombinar,
                vista_recortar: VistaRecortar, vista_info: VistaInfo,
                vista_por_defecto: FrameSeccion) -> None:
        
        self.__vista_menu = vista_menu
        self.__vista_mejorar = vista_mejorar
        self.__vista_editar = vista_editar
        self.__vista_combinar = vista_combinar
        self.__vista_recortar = vista_recortar
        self.__vista_info = vista_info
        self.__vista_actual = vista_por_defecto

        self.__vista_actual.hacer_visible()

    def __cambiar_vista(self, vista_destino) -> None:
        if self.__vista_actual == vista_destino:
            return
        
        puntero = self.__vista_menu.get_puntero()
        if isinstance(vista_destino, VistaMejorar):
            puntero.mover_a_btn_mejorar()
            self.__vista_actual.hacer_invisible()
            self.__vista_mejorar.hacer_visible()
            self.__vista_actual = self.__vista_mejorar
        elif isinstance(vista_destino, VistaEditar):
            puntero.mover_a_btn_editar()
            self.__vista_actual.hacer_invisible()
            self.__vista_editar.hacer_visible()
            self.__vista_actual = self.__vista_editar
        elif isinstance(vista_destino, VistaCombinar):
            puntero.mover_a_btn_combinar()
            self.__vista_actual.hacer_invisible()
            self.__vista_combinar.hacer_visible()
            self.__vista_actual = self.__vista_combinar
        elif isinstance(vista_destino, VistaRecortar):
            puntero.mover_a_btn_recortar()
            self.__vista_actual.hacer_invisible()
            self.__vista_recortar.hacer_visible()
            self.__vista_actual = self.__vista_recortar
        elif isinstance(vista_destino, VistaInfo):
            puntero.mover_a_btn_info()
            self.__vista_actual.hacer_invisible()
            self.__vista_info.hacer_visible()
            self.__vista_actual = self.__vista_info

    def click_btn_mejorar(self) -> None:
        self.__cambiar_vista(self.__vista_mejorar)

    def click_btn_editar(self) -> None:
        self.__cambiar_vista(self.__vista_editar)

    def click_btn_combinar(self) -> None:
        self.__cambiar_vista(self.__vista_combinar)

    def click_btn_recortar(self) -> None:
        self.__cambiar_vista(self.__vista_recortar)
    
    def click_btn_info(self) -> None:
        self.__cambiar_vista(self.__vista_info)