from PIL import Image

from customtkinter import CTkButton
from customtkinter import CTkLabel
from customtkinter import CTkImage

from vista.componentes.frame_seccion import FrameSeccion
from vista.config_vista import ConfigVista
from controlador.contr_visor_pdf import ControladorVisorPdf

class VisorPdf():
    def __init__(self, frame_seccion: FrameSeccion):
        self.__frame_seccion = frame_seccion
        self.__config = ConfigVista()
        self.__controlador = None

    def cargar_controlador(self, controlador: ControladorVisorPdf) -> None:
        self.__controlador = controlador

    def cargar_elementos(self) -> None:
        """ Requisito: Antes hay que cargar el controlador """
        self.__cargar_boton_buscar_archivo()
        self.__cargar_boton_eliminar_pdf()
        self.__cargar_etq_nombre_pdf()
        self.__cargar_mostrador_pdf()
        self.__cargar_mostrador_num_pag()
        self.__cargar_btn_avanzar_hoja()
        self.__cargar_btn_retroceder_hoja()

    def __cargar_boton_buscar_archivo(self) -> None:
        self.__btn_arch = CTkButton(
            master=self.__frame_seccion,
            width=210,
            height=80,
            corner_radius=20,
            fg_color='#353535',
            hover_color='#404040',
            text='Click para seleccionar Pdf',
            font=(self.__config.TIPO_LETRA, 12),
            text_color='#bbb',
            command=self.__controlador.click_boton_buscar_archivo
        )
        self.__btn_arch.place(relx=0.52, rely=0.1)
        self.activar_boton_buscar_archivo()

    def __cargar_boton_eliminar_pdf(self) -> None:
        ruta_icono_pdf = self.__config.RUTA_ABS_PROGRAMA
        ruta_icono_pdf += '/vista/adjuntos/iconos/icono_pdf.png'
        img_indicador_pdf = CTkImage(
            light_image=Image.open(ruta_icono_pdf),
            dark_image=Image.open(ruta_icono_pdf),
            size=(35, 35)
        )
        self.__indicador_pdf = CTkLabel(
            master=self.__frame_seccion,
            width=35,
            height=35,
            text=None,
            image=img_indicador_pdf
        )

        ruta_btn_elim = self.__config.RUTA_ABS_PROGRAMA
        ruta_btn_elim += '/vista/adjuntos/iconos/btn_eliminar_pdf.png'
        img_eliminar = CTkImage(
            light_image=Image.open(ruta_btn_elim),
            dark_image=Image.open(ruta_btn_elim),
            size=(45, 20)
        )
        self.__btn_eliminar_pdf = CTkButton(
            master=self.__frame_seccion,
            width=45,
            height=20,
            corner_radius=7.5,
            fg_color='transparent',
            bg_color='transparent',
            hover_color='#242424',
            text=None,
            image=img_eliminar,
            command=self.__controlador.click_boton_eliminar_archivo
        )
        self.__btn_eliminar_pdf.configure(cursor='hand2')

    def __cargar_etq_nombre_pdf(self) -> None:
        self.__etq_nombre_pdf = CTkLabel(
            master=self.__frame_seccion,
            width=250,
            height=20,
            text=None,
            text_color='#bbb',
            font=(self.__config.TIPO_LETRA, 10)
        )
        self.__etq_nombre_pdf.place(relx=.05, rely=.11)

    def __cargar_mostrador_pdf(self) -> None:
        self.__mostrador_pdf = CTkLabel(
            master=self.__frame_seccion,
            width=250,
            height=357,
            fg_color='#353535',
            text=None,
            font=(self.__config.TIPO_LETRA, 12)
        )
        self.__mostrador_pdf.place(relx=0.05, rely=0.15)

    def __cargar_mostrador_num_pag(self) -> None:
        self.__mostrador_pag = CTkLabel(
            master=self.__frame_seccion,
            text_color='#bbb',
            text='0/0',
            font=(self.__config.TIPO_LETRA, 12)
        )
        self.__mostrador_pag.place(relx=0.23, rely=0.88)

    def __cargar_btn_avanzar_hoja(self) -> None:
        self.__btn_avanzar_hoja = CTkButton(
            master=self.__frame_seccion,
            width=50,
            fg_color='#353535',
            hover_color='#404040',
            text='>',
            font=(self.__config.TIPO_LETRA, 16),
            command=self.__controlador.click_boton_avanzar_pag
        )
        self.__btn_avanzar_hoja.place(relx=0.36, rely=0.9)
        self.__btn_avanzar_hoja.configure(cursor='hand2')

    def __cargar_btn_retroceder_hoja(self) -> None:
        self.__btn_retroceder_hoja = CTkButton(
            master=self.__frame_seccion,
            width=50,
            fg_color='#353535',
            hover_color='#404040',
            text='<',
            font=(self.__config.TIPO_LETRA, 16),
            command=self.__controlador.click_boton_retroceder_pag
        )
        self.__btn_retroceder_hoja.place(relx=0.05, rely=0.9)
        self.__btn_retroceder_hoja.configure(cursor='hand2')

    # Métodos para controlar el boton buscar archivo
    def activar_boton_buscar_archivo(self):
        self.__btn_arch.configure(state='normal', cursor='hand2')

    def desactivar_boton_buscar_archivo(self):
        self.__btn_arch.configure(state='disabled', cursor='arrow')

    # Métodos para controlar el boton eliminar pdf
    def hacer_boton_eliminar_pdf_invisible(self):
        self.__indicador_pdf.place_forget()
        self.__btn_eliminar_pdf.place_forget()

    def hacer_boton_eliminar_pdf_visible(self):
        self.__indicador_pdf.place(relx=0.88, rely=0.12)
        self.__btn_eliminar_pdf.place(relx=0.86, rely=0.18)
        
    # Otros metodos
    def actualizar_etiqueta_nombre_pdf(self, nombre: str):
        """ Pone el nombre del pdf encima del visor """
        self.__etq_nombre_pdf.configure(text=nombre)
    
    def actualizar_imagen_pdf(self, imagen: Image.Image | None) -> None:
        """ Se muestra la imagen por el visor """
        if imagen == None:
            self.__mostrador_pdf._image = None
        else:
            self.__mostrador_pdf._image = CTkImage(
                light_image=imagen,
                dark_image=imagen,
                size=(250, 357)
            )
        self.__mostrador_pdf._update_image()

    def actualizar_mostrador_paginas(self, pag_actual: int, pag_max: int):
        """ Se actualizan los numeros de pagina que hay debajo del visor """
        self.__mostrador_pag.configure(text='{}/{}'.format(pag_actual, pag_max))