from PIL import Image

from customtkinter import CTkLabel
from customtkinter import CTkImage

from vista.config_vista import ConfigVista

class PunteroMenu(CTkLabel):
    def __init__(self, vista_menu):
        ruta_indicador = ConfigVista().RUTA_ABS_PROGRAMA
        ruta_indicador += '/vista/adjuntos/iconos/indicador_estado.png'
        puntero_img = CTkImage(
            light_image=Image.open(ruta_indicador),
            dark_image=Image.open(ruta_indicador),
            size=(10, 10)
        )

        super().__init__(
            master=vista_menu,
            width=10,
            height=10,
            image=puntero_img,
            text=None
        )

        self.__posiciones = {
            'btn_mejorar': (.88, .373),
            'btn_editar': (.88, .505),
            'btn_combinar': (.88, .635),
            'btn_recortar': (.88, .770),
            'btn_info': (.88, .904),
        }

    def mover_a_btn_mejorar(self):
        self.place(
            relx=self.__posiciones['btn_mejorar'][0],
            rely=self.__posiciones['btn_mejorar'][1]
        )

    def mover_a_btn_editar(self):
        self.place(
            relx=self.__posiciones['btn_editar'][0],
            rely=self.__posiciones['btn_editar'][1]
        )

    def mover_a_btn_combinar(self):
        self.place(
            relx=self.__posiciones['btn_combinar'][0],
            rely=self.__posiciones['btn_combinar'][1]
        )

    def mover_a_btn_recortar(self):
        self.place(
            relx=self.__posiciones['btn_recortar'][0],
            rely=self.__posiciones['btn_recortar'][1]
        )

    def mover_a_btn_info(self):
        self.place(
            relx=self.__posiciones['btn_info'][0],
            rely=self.__posiciones['btn_info'][1]
        )