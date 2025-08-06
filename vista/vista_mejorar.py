from customtkinter import CTk
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkCheckBox
from customtkinter import CTkProgressBar

from vista.componentes.frame_seccion import FrameSeccion
from vista.config_vista import ConfigVista
from controlador.contr_mejorar import ControladorMejorar
class VistaMejorar(FrameSeccion):
    def __init__(self, ventana: CTk):
        super().__init__(ventana, titulo='Mejorar automáticamente el Pdf')

        self.__ventana = ventana
        self.__config = ConfigVista()
        self.__controlador = None

    def cargar_controlador(self, controlador: ControladorMejorar) -> None:
        self.__controlador = controlador

    def cargar_elementos(self) -> None:
        """ Requisito: Antes cargar el controlador """
        self.__cargar_texto_opciones()
        self.__cargar_btn_recortar()
        self.__cargar_btn_invertir()
        self.__cargar_btn_filtrar()
        self.__cargar_btn_saturar()
        self.__cargar_btn_iniciar()
        self.__cargar_barra_progreso()

        self.deshabilitar_botones()
        self.poner_estado_botones_por_defecto()

    def __cargar_texto_opciones(self) -> None:
        self.__texto_opciones = CTkLabel(
            master=self,
            text='Procesos',
            text_color='#ccc',
            font=(self.__config.TIPO_LETRA, 16)
        )
        self.__texto_opciones.place(relx=0.52, rely=0.35)

    def __cargar_btn_recortar(self) -> None:
        self.__btn_recortar = CTkCheckBox(
            master=self,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text='Recorte de bordes.',
            text_color='#bbb',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_boton_opcion
        )
        self.__btn_recortar.place(relx=0.55, rely=0.42)

    def __cargar_btn_invertir(self) -> None:
        self.__btn_invertir = CTkCheckBox(
            master=self,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text='Inversión de las imágenes.',
            text_color='#bbb',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_boton_opcion
        )
        self.__btn_invertir.place(relx=0.55, rely=0.5)

    def __cargar_btn_filtrar(self) -> None:
        self.__btn_filtrar = CTkCheckBox(
            master=self,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text='Filtrado en los bordes.',
            text_color='#bbb',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_boton_opcion
        )
        self.__btn_filtrar.place(relx=0.55, rely=0.58)

    def __cargar_btn_saturar(self) -> None:
        self.__btn_saturar = CTkCheckBox(
            master=self,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text='Saturación de los colores.',
            text_color='#bbb',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_boton_opcion
        )
        self.__btn_saturar.place(relx=0.55, rely=0.66)

    def __cargar_btn_iniciar(self) -> None:
        self.__btn_iniciar = CTkButton(
            master=self,
            height=36,
            corner_radius=18,
            text='Iniciar proceso',
            fg_color='#106A43',
            font=(self.__config.TIPO_LETRA, 12),
            command=self.__controlador.click_boton_iniciar_proceso
        )
        self.__btn_iniciar.place(relx=0.6, rely=0.8)

    def __cargar_barra_progreso(self) -> None:
        self.__barra_progreso = CTkProgressBar(
            master=self,
            width=100,
            height=4,
            corner_radius=2,
            border_width=0
        )
        self.__barra_progreso.set(0)

    # Metodos para el control general de los botones
    def habilitar_botones(self) -> None:
        self.__btn_recortar.configure(state='normal', cursor='hand2')
        self.__btn_filtrar.configure(state='normal', cursor='hand2')
        self.__btn_invertir.configure(state='normal', cursor='hand2')
        self.__btn_saturar.configure(state='normal', cursor='hand2')
        self.__btn_iniciar.configure(state='normal',
                                    fg_color="#128F58", cursor='hand2')

    def deshabilitar_botones(self) -> None:
        self.__btn_recortar.configure(state='disabled', cursor='arrow')
        self.__btn_filtrar.configure(state='disabled', cursor='arrow')
        self.__btn_invertir.configure(state='disabled', cursor='arrow')
        self.__btn_saturar.configure(state='disabled', cursor='arrow')
        self.__btn_iniciar.configure(state='disabled',
                                    fg_color='#106A43', cursor='arrow')

    def poner_estado_botones_por_defecto(self) -> None:
        self.__btn_recortar.select()
        self.deshabilitar_boton_recortar()
        self.__btn_filtrar.deselect()
        self.__btn_invertir.deselect()
        self.__btn_saturar.deselect()

    # Metodos controlar la progress bar
    def hacer_visible_barra_progreso(self) -> None:
        self.__barra_progreso.set(0)
        self.__barra_progreso.place(relx=0.63, rely=0.89)

    def hacer_invisible_barra_progreso(self) -> None:
        self.__barra_progreso.place_forget()

    def establecer_posicion_barra_progreso(self, pos: float) -> None:
        """ La posicion tiene que estar entre [0, 1] """
        self.__barra_progreso.set(pos)

    # Metodos para controlar el boton recortar
    def marcar_boton_recortar(self) -> None:
        self.__btn_recortar.select()

    def desmarcar_boton_recortar(self) -> None:
        self.__btn_recortar.select()

    def habilitar_boton_recortar(self) -> None:
        self.__btn_recortar.configure(state='normal', cursor='hand2')

    def deshabilitar_boton_recortar(self) -> None:
        self.__btn_recortar.configure(state='disabled', cursor='arrow')

    def esta_habilitado_boton_recortar(self) -> bool:
        return self.__btn_recortar.cget("state") == 'normal'

    # Métodos para ver los estados de los botones
    def esta_boton_recortar_marcado(self) -> bool:
        return self.__btn_recortar.get()
    
    def esta_boton_invertir_marcado(self) -> bool:
        return self.__btn_invertir.get()
    
    def esta_boton_filtrar_marcado(self) -> bool:
        return self.__btn_filtrar.get()
    
    def esta_boton_saturar_marcado(self) -> bool:
        return self.__btn_saturar.get()