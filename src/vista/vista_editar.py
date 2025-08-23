from customtkinter import CTk
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkCheckBox
from customtkinter import CTkProgressBar

from vista.componentes.selector_saturar import SelectorSaturar
from vista.componentes.selector_invertir import SelectorInvertir
from vista.componentes.frame_seccion import FrameSeccion
from vista.config_vista import ConfigVista

from controlador.contr_editar import ControladorEditar

class VistaEditar(FrameSeccion):
    def __init__(self, ventana: CTk):
        super().__init__(ventana, titulo='Edición y personalización del Pdf')

        self.__config = ConfigVista()
        self.__controlador = None

    def cargar_controlador(self, controlador: ControladorEditar) -> None:
        self.__controlador = controlador

    def cargar_elementos(self) -> None:
        """ Requisitos: Antes hay que cargar el controlador """
        self.__cargar_texto_opciones()
        self.__cargar_btn_eliminar_pag()
        self.__cargar_btn_recortar()
        self.__cargar_btn_filtrar()
        self.__cargar_opcion_saturar()
        self.__cargar_opcion_invertir()
        self.__cargar_btn_confirmar()
        self.__cargar_barra_progreso()

        self.deshabilitar_botones()
        self.poner_estado_botones_por_defecto()

    def __cargar_texto_opciones(self):
        self.__texto_opciones = CTkLabel(
            master=self,
            text='Edición (imagen - 0)',
            text_color='#ccc',
            font=(self.__config.TIPO_LETRA, 16)
        )
        self.__texto_opciones.place(relx=0.52, rely=0.35)

    def __cargar_btn_eliminar_pag(self) -> None:
        self.__btn_eliminar_pag = CTkCheckBox(
            master=self,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text='Eliminar página.',
            hover_color='#503535',
            fg_color='#703535',
            text_color='#bbb',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_boton_eliminar_pagina
        )
        self.__btn_eliminar_pag.place(relx=0.55, rely=0.42)

    def __cargar_btn_recortar(self) -> None:
        self.__btn_recortar = CTkCheckBox(
            master=self,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text='Recorte de bordes.',
            text_color='#bbb',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_boton_recortar
        )
        self.__btn_recortar.place(relx=0.55, rely=0.5)

    def __cargar_btn_filtrar(self) -> None:
        self.__btn_filtrar = CTkCheckBox(
            master=self,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text='Filtrado en los bordes.',
            text_color='#bbb',
            font=(self.__config, 13),
            command=self.__controlador.click_boton_filtrar
        )
        self.__btn_filtrar.place(relx=0.55, rely=0.58)

    def __cargar_opcion_saturar(self) -> None:
        self.__opcion_saturacion = SelectorSaturar(
            master=self,
            width=100,
            height=30,
            corner_radius=8,
            fg_color='#353535',
            button_color='#404040',
            button_hover_color='#106A43',
            text_color='#bbb',
            dropdown_font=(self.__config.TIPO_LETRA, 13),
            dropdown_hover_color='#106A43',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_opcion_saturar
        )
        self.__opcion_saturacion.place(relx=0.55, rely=0.68)

    def __cargar_opcion_invertir(self) -> None:
        self.__opcion_inversion = SelectorInvertir(
            master=self,
            width=100,
            height=30,
            corner_radius=8,
            fg_color='#353535',
            button_color='#404040',
            button_hover_color='#106A43',
            text_color='#bbb',
            dropdown_font=(self.__config.TIPO_LETRA, 13),
            dropdown_hover_color='#106A43',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_opcion_invertir
        )
        self.__opcion_inversion.place(relx=0.55, rely=0.78)

    def __cargar_btn_confirmar(self) -> None:
        self.__btn_confirmar = CTkButton(
            master=self,
            height=36,
            corner_radius=18,
            text='Confirmar',
            fg_color='#106A43',
            font=(self.__config.TIPO_LETRA, 12),
            command=self.__controlador.click_boton_confirmar
        )
        self.__btn_confirmar.place(relx=0.6, rely=0.88)
    
    def __cargar_barra_progreso(self) -> None:
        self.__barra_progreso = CTkProgressBar(
            master=self,
            width=100,
            height=4,
            corner_radius=2,
            border_width=0
        )
        self.__barra_progreso.set(0)

    # Métodos que gestionan a todos los botones
    def habilitar_botones(self) -> None:
        self.__btn_eliminar_pag.configure(state='normal', cursor='hand2')
        self.__btn_recortar.configure(state='normal', cursor='hand2')
        self.__btn_filtrar.configure(state='normal', cursor='hand2')
        self.__opcion_saturacion.configure(state='normal', cursor='hand2')
        self.__opcion_inversion.configure(state='normal', cursor='hand2')
        self.__btn_confirmar.configure(state='normal',
                                        fg_color='#128F58', cursor='hand2')

    def deshabilitar_botones(self) -> None:
        self.deshabilitar_opciones_menos_eliminar()
        self.__btn_eliminar_pag.configure(state='disabled', cursor='arrow')
        self.__btn_confirmar.configure(state='disabled',
                                        fg_color="#106A43", cursor='arrow')

    def poner_estado_botones_por_defecto(self) -> None:
        self.__deseleccionar_botones()

    def __deseleccionar_botones(self) -> None:
        self.deseleccionar_btn_eliminar()
        self.deseleccionar_btn_recortar()
        self.deseleccionar_btn_filtrar()
        self.deseleccionar_opcion_saturar()
        self.deseleccionar_opcion_invertir()

    # Metodos que afectan a todos los botones menos al de eliminar pag y confirmar
    def deshabilitar_opciones_menos_eliminar(self) -> None:
        self.__btn_recortar.configure(state='disabled', cursor='arrow')
        self.__btn_filtrar.configure(state='disabled', cursor='arrow')
        self.__opcion_saturacion.configure(state='disabled', cursor='arrow')
        self.__opcion_inversion.configure(state='disabled', cursor='arrow')

    def deseleccionar_opciones_menos_eliminar(self) -> None:
        self.deseleccionar_btn_recortar()
        self.deseleccionar_btn_filtrar()
        self.deseleccionar_opcion_saturar()
        self.deseleccionar_opcion_invertir()

    # Metodos para seleccionar los botones
    def seleccionar_btn_eliminar(self) -> None:
        self.__btn_eliminar_pag.select()

    def seleccionar_btn_recortar(self) -> None:
        self.__btn_recortar.select()

    def seleccionar_btn_filtrar(self) -> None:
        self.__btn_filtrar.select()

    def seleccionar_opcion_saturar(self, valor: int) -> None:
        """ 10, 20 30, 40, 50 """
        self.__opcion_saturacion.set(valor)

    def seleccionar_opcion_invertir(self, valor: str) -> None:
        """ 'x', 'y', 'xy' """
        self.__opcion_inversion.set(valor)

    # Metodos para deseleccionar los botones
    def deseleccionar_btn_eliminar(self) -> None:
        self.__btn_eliminar_pag.deselect()

    def deseleccionar_btn_recortar(self) -> None:
        self.__btn_recortar.deselect()

    def deseleccionar_btn_filtrar(self) -> None:
        self.__btn_filtrar.deselect()

    def deseleccionar_opcion_saturar(self) -> None:
        self.__opcion_saturacion.set(0)

    def deseleccionar_opcion_invertir(self) -> None:
        self.__opcion_inversion.set('')

    # Metodos controlar la progress bar
    def hacer_visible_barra_progreso(self) -> None:
        self.__barra_progreso.set(0)
        self.__barra_progreso.place(relx=0.63, rely=0.97)

    def hacer_invisible_barra_progreso(self) -> None:
        self.__barra_progreso.place_forget()

    def establecer_posicion_barra_progreso(self, pos: float) -> None:
        """ La posicion tiene que estar entre [0, 1] """
        self.__barra_progreso.set(pos)

    # Metodos para ver si ciertos botones estan activados
    def esta_boton_eliminar_pag_marcado(self) -> bool:
        return self.__btn_eliminar_pag.get()
    
    def esta_boton_recortar_marcado(self) -> bool:
        return self.__btn_recortar.get()
    
    def esta_boton_filtrar_marcado(self) -> bool:
        return self.__btn_filtrar.get()
    
    # Otros metodos
    def actualizar_texto_opciones(self, num_pag: int):
        self.__texto_opciones.configure(text=f'Edición (imagen - {num_pag})')