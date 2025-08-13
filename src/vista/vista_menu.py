from PIL import Image
import os
from customtkinter import CTk
from customtkinter import CTkFrame
from customtkinter import CTkImage
from customtkinter import CTkButton
from customtkinter import CTkLabel

from vista.componentes.puntero_menu import PunteroMenu
from vista.config_vista import ConfigVista
from controlador.contr_menu import ControladorMenu

class VistaMenu(CTkFrame):
    def __init__(self, ventana: CTk) -> None:
        
        super().__init__(
            master=ventana,
            border_width=1, 
            corner_radius=20,
            fg_color='#404040',
            border_color='#ddd'
        )
        self.place(relx=0.05, rely=0.11)

        self.__ventana = ventana
        self.__config = ConfigVista()
        self.__controlador_menu = None

    def cargar_controlador(self, controlador: ControladorMenu) -> None:
        self.__controlador_menu = controlador

    def cargar_elementos(self) -> None:
        """ Requisito: Cargar antes el controlador """
        self.__cargar_logo()
        self.__cargar_btn_mejorar()
        self.__cargar_btn_editar()
        self.__cargar_btn_combinar()
        self.__cargar_btn_recortar()
        self.__cargar_btn_info()
        self.__cargar_puntero()

    def __cargar_logo(self):
        ruta_img = self.__config.RUTA_ABS_PROGRAMA
        ruta_img += '/vista/adjuntos/iconos/logo_programa.png'
        logo_img = CTkImage(
            light_image=Image.open(ruta_img),
            dark_image=Image.open(ruta_img),
            size=(160, 100)
        )
        self.__logo_etq = CTkLabel(master=self, image=logo_img, text=None)
        self.__logo_etq.pack(pady=20, padx=20)

    def __cargar_btn_mejorar(self):
        self.__btn_mejorar = CTkButton(
            master=self,
            text='Mejorar',
            width=140,
            height=42,
            corner_radius=21,
            font=(self.__config.TIPO_LETRA, 13.5),
            command=self.__controlador_menu.click_btn_mejorar
        )
        self.__btn_mejorar.configure(cursor='hand2')
        self.__btn_mejorar.pack(pady=20, padx=20)
    
    def __cargar_btn_editar(self):
        self.__btn_editar = CTkButton(
            master=self,
            text='Editar',
            width=140,
            height=42,
            corner_radius=21,
            font=(self.__config.TIPO_LETRA, 13.5),
            command=self.__controlador_menu.click_btn_editar
        )
        self.__btn_editar.configure(cursor='hand2')
        self.__btn_editar.pack(padx=20)

    def __cargar_btn_combinar(self):
        self.__btn_combinar = CTkButton(
            master=self,
            text='Combinar', 
            width=140,
            height=42,
            corner_radius=21,
            font=(self.__config.TIPO_LETRA, 13.5),
            command=self.__controlador_menu.click_btn_combinar
        )
        self.__btn_combinar.configure(cursor='hand2')
        self.__btn_combinar.pack(padx=20, pady=20)

    def __cargar_btn_recortar(self):
        self.__btn_recortar = CTkButton(
            master=self,
            text='Recortar',
            width=140,
            height=42,
            corner_radius=21,
            font=(self.__config.TIPO_LETRA, 13.5),
            command=self.__controlador_menu.click_btn_recortar
        )
        self.__btn_recortar.configure(cursor='hand2')
        self.__btn_recortar.pack(padx=20)

    def __cargar_btn_info(self):
        self.__btn_info = CTkButton(
            master=self,
            text='Instrucciones',
            width=140,
            height=42,
            corner_radius=21,
            font=(self.__config.TIPO_LETRA, 13.5),
            command=self.__controlador_menu.click_btn_info
        )
        self.__btn_info.configure(cursor='hand2')
        self.__btn_info.pack(pady=20, padx=20)

    def __cargar_puntero(self):
        self.__puntero = PunteroMenu(self)
        self.__puntero.mover_a_btn_mejorar()

    def get_puntero(self) -> PunteroMenu:
        return self.__puntero