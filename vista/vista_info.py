from customtkinter import CTk
from customtkinter import CTkFrame
from customtkinter import CTkScrollableFrame
from customtkinter import CTkLabel

from vista.componentes.frame_seccion import FrameSeccion
from vista.config_vista import ConfigVista

class VistaInfo(FrameSeccion):
    def __init__(self, ventana: CTk):
        super().__init__(ventana, 'Manual de instrucciones')

        self.__ventana = ventana
        self.__RUTA_MANUAL = ConfigVista().RUTA_ABS_PROGRAMA
        self.__RUTA_MANUAL += '/vista/adjuntos/manual/instrucciones.txt'

    def cargar_elementos(self) -> None:
        self.__cargar_frame_intrucciones()
        self.__cargar_texto()

    def __cargar_frame_intrucciones(self) -> None:
        self.__frame_info = CTkFrame(
            master=self,
            corner_radius=15,
            fg_color='transparent',
            border_color='#aaa',
            border_width=1
        )
        self.__frame_info.place(relx=0.01, rely=0.1,
                                relwidth=0.95, relheight=0.85)
        
        self.__scrodable_frame_info = CTkScrollableFrame(
            master=self.__frame_info,
            corner_radius=15,
            fg_color='transparent'
        )
        self.__scrodable_frame_info.place(relx=0.01, rely=0.01,
                                        relwidth=0.97, relheight=0.97)
        
    def __cargar_texto(self) -> None:
        with open(self.__RUTA_MANUAL, 'r', encoding='utf-8') as f:
            texto = f.read()

        self.__etq_texto = CTkLabel(
            master=self.__scrodable_frame_info,
            text=texto,
            text_color='#ccc',
            font=(ConfigVista().TIPO_LETRA, 15),
            anchor='w',
            justify='left'
        )
        self.__etq_texto.pack()