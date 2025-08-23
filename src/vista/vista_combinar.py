from customtkinter import CTk
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkScrollableFrame
from customtkinter import CTkButton

from vista.componentes.frame_seccion import FrameSeccion
from vista.config_vista import ConfigVista

from controlador.contr_combinar import ControladorCombinar

class VistaCombinar(FrameSeccion):
    def __init__(self, ventana: CTk):
        super().__init__(ventana, titulo='Combinación de diversos Pdf\'s')

        self.__config = ConfigVista()
        self.__controlador = None
        
        self.__ctkLabels_nombres_pdfs = []

    def cargar_controlador(self, controlador: ControladorCombinar) -> None:
        self.__controlador = controlador

    def cargar_elementos(self) -> None:
        """ Requisitos: Se ha tenido que cargar el controlador """
        self.__cargar_frame_mostrador_pdfs()
        self.__cargar_btn_anadir()
        self.__cargar_btn_combinar()
        self.__cargar_btn_eliminar()
        self.poner_estado_por_defecto()

    def __cargar_frame_mostrador_pdfs(self) -> None:
        self.__frame_pdfs = CTkFrame(
            master=self,
            corner_radius=15,
            fg_color='transparent',
            border_color='#aaa',
            border_width=1
        )
        self.__frame_pdfs.place(relx=0.01, rely=0.1,
                                relwidth=0.95, relheight=0.82)
        
        self.__scrodable_frame_pdfs = CTkScrollableFrame(
            master=self.__frame_pdfs,
            corner_radius=15,
            fg_color='transparent'
        )
        self.__scrodable_frame_pdfs.place(relx=0.01, rely=0.01,
                                        relwidth=0.97, relheight=0.82)

    def __cargar_btn_anadir(self) -> None:
        self.__btn_anadir = CTkButton(
            master=self.__frame_pdfs,
            width=50,
            height=50,
            corner_radius=15,
            fg_color='#353535',
            hover_color='#404040',
            text_color='#bbb',
            text='+',
            font=(self.__config.TIPO_LETRA, 16),
            command=self.__controlador.click_btn_agregar
        )
        self.__btn_anadir.place(relx=0.23, rely=0.85)

    def __cargar_btn_combinar(self) -> None:
        self.__btn_combinar = CTkButton(
            master=self.__frame_pdfs,
            width=120,
            height=40,
            corner_radius=20,
            text='Combinar',
            fg_color='#128F58',
            hover_color='#119E61',
            font=(self.__config, 13),
            command=self.__controlador.click_btn_combinar
        )
        self.__btn_combinar.place(relx=0.33, rely=0.86)

    def __cargar_btn_eliminar(self) -> None:
        self.__btn_eliminar = CTkButton(
            master=self.__frame_pdfs,
            width=120,
            height=40,
            corner_radius=20,
            text='Eliminar',
            fg_color="#603535",
            hover_color="#6D3636",
            font=(self.__config, 13),
            command=self.__controlador.click_btn_eliminar
        )
        self.__btn_eliminar.place(relx=0.53, rely=0.86)

    def poner_estado_por_defecto(self) -> None:
        self.habilitar_btn_anadir()
        self.deshabilitar_btn_combinar()
        self.deshabilitar_btn_eliminar()

    # Metodos para añadir y eliminar pdfs a la zona de trabajo
    def agregar_pdf(self, nombre_pdf: str) -> None:
        indice = len(self.__ctkLabels_nombres_pdfs) + 1
        etq = CTkLabel(
            master=self.__scrodable_frame_pdfs,
            width=400,
            height=40,
            corner_radius=20,
            fg_color='#353535',
            text_color='#bbb',
            text=f'{indice}º - {nombre_pdf}',
            font=(self.__config.TIPO_LETRA, 12)
        )
        etq.pack(padx=20, pady=10)
        self.__ctkLabels_nombres_pdfs.append(etq)

    def quitar_ultimo_pdf(self) -> None:
        if len(self.__ctkLabels_nombres_pdfs) == 0:
            return
        etq = self.__ctkLabels_nombres_pdfs.pop(-1)
        etq.destroy()

    # Metodos para habilitar los botones
    def habilitar_btn_anadir(self) -> None:
        self.__btn_anadir.configure(state='normal', cursor='hand2')

    def habilitar_btn_combinar(self) -> None:
        self.__btn_combinar.configure(state='normal', cursor='hand2',
                                    fg_color='#128F58')

    def habilitar_btn_eliminar(self) -> None:
        self.__btn_eliminar.configure(state='normal', cursor='hand2',
                                    fg_color='#603535')

    # Metodos para desabilitar los botones
    def deshabilitar_btn_anadir(self) -> None:
        self.__btn_anadir.configure(state='disabled', cursor='arrow')

    def deshabilitar_btn_combinar(self) -> None:
        self.__btn_combinar.configure(state='disabled', cursor='arrow',
                                    fg_color='#106A43')

    def deshabilitar_btn_eliminar(self) -> None:
        self.__btn_eliminar.configure(state='disabled', cursor='arrow',
                                    fg_color='#453030')