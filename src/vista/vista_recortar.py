from PIL import Image

from customtkinter import CTk
from customtkinter import CTkButton
from customtkinter import CTkLabel
from customtkinter import CTkFrame
from customtkinter import CTkScrollableFrame
from customtkinter import CTkEntry
from customtkinter import CTkImage

from vista.componentes.frame_seccion import FrameSeccion
from vista.config_vista import ConfigVista
from controlador.contr_recortar import ControladorRecortar

class VistaRecortar(FrameSeccion):
    def __init__(self, ventana: CTk):
        super().__init__(ventana, titulo='Recorte de páginas dentro del Pdf')

        self.__ventana = ventana
        self.__config = ConfigVista()
        self.__controlador = None

        # Atributo que contiene todos los CTkLabel de cada recorte
        self.__etqs_recortes = []

    def cargar_controlador(self, controlador: ControladorRecortar) -> None:
        self.__controlador = controlador

    def cargar_elementos(self) -> None:
        """ Requisitos: Se ha tenido que cargar el controlador """
        self.__cargar_btn_archivo()
        self.__cargar_btn_eliminar_archivo()
        self.__cargar_frame_recortes()
        self.__cargar_subtitulo()
        self.__cargar_btn_agregar_recorte()
        self.__cargar_caja_texto_desde()
        self.__cargar_caja_texto_hasta()
        self.__cargar_btn_recortar()
        self.__cargar_btn_borrar()
        self.poner_estado_por_defecto()

    def __cargar_btn_archivo(self) -> None:
        self.__btn_archivo = CTkButton(
            master=self,
            width=435,
            height=60,
            corner_radius=30,
            fg_color='#353535',
            hover_color='#404040',
            text_color='#bbb',
            text='Elegir un archivo Pdf',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_btn_archivo
        )
        self.__btn_archivo.place(relx=0.15, rely=0.14)
        self.__btn_archivo.configure(cursor='hand2')

    def __cargar_btn_eliminar_archivo(self) -> None:
        ruta_icono = self.__config.RUTA_ABS_PROGRAMA
        ruta_icono += '/vista/adjuntos/iconos/icono_pdf.png'
        img_indicador_pdf = CTkImage(
            light_image=Image.open(ruta_icono),
            dark_image=Image.open(ruta_icono),
            size=(35, 35)
        )
        self.__indicador_pdf = CTkLabel(
            master=self,
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
            master=self,
            width=45,
            height=20,
            corner_radius=7.5,
            fg_color='transparent',
            bg_color='transparent',
            hover_color='#242424',
            text=None,
            image=img_eliminar,
            command=self.__controlador.click_btn_eliminar_pdf
        )
        self.__btn_eliminar_pdf.configure(cursor='hand2')

    def __cargar_frame_recortes(self) -> None:
        self.__frame_recortes = CTkFrame(
            master=self,
            corner_radius=15,
            fg_color='transparent',
            border_color='#aaa',
            border_width=1
        )
        self.__frame_recortes.place(relx=0.01, rely=0.35,
                                relwidth=0.95, relheight=0.57)
        
        self.__scrodable_frame_recortes = CTkScrollableFrame(
            master=self.__frame_recortes,
            fg_color='transparent'
        )
        self.__scrodable_frame_recortes.place(relx=0.03, rely=0.15,
                                        relwidth=0.96, relheight=0.6)
        
    def __cargar_subtitulo(self) -> None:
        self.__titulo_div_pags = CTkLabel(
            master=self.__frame_recortes,
            text_color='#ccc',
            text='Divisiones de páginas',
            font=(self.__config.TIPO_LETRA, 16)
        )
        self.__titulo_div_pags.place(relx=0.03, rely=0.05)

    def __cargar_btn_agregar_recorte(self) -> None:
        self.__btn_agregar_recorte = CTkButton(
            master=self.__frame_recortes,
            width=40,
            height=40,
            corner_radius=12,
            fg_color='#303030',
            hover_color='#404040',
            text_color='#bbb',
            text='+',
            font=(self.__config.TIPO_LETRA, 16),
            command=self.__controlador.click_agregar_recorte
        )
        self.__btn_agregar_recorte.place(relx=0.35, rely=0.8)
        self.__btn_agregar_recorte.configure(cursor='hand2')

    def __cargar_caja_texto_desde(self) -> None:
        self.__caja_texto_desde = CTkEntry(
            master=self.__frame_recortes,
            width=80,
            height=40,
            corner_radius=20,
            border_width=0,
            fg_color='#303030',
            text_color='#bbb',
            placeholder_text_color='#aaa',
            placeholder_text='Desde',
            justify='center',
            font=(self.__config.TIPO_LETRA, 11)
        )
        self.__caja_texto_desde.place(relx=0.06, rely=0.8)

    def __cargar_caja_texto_hasta(self) -> None:
        self.__caja_texto_hasta = CTkEntry(
            master=self.__frame_recortes,
            width=80,
            height=40,
            corner_radius=20,
            border_width=0,
            fg_color='#303030',
            text_color='#bbb',
            placeholder_text_color='#aaa',
            placeholder_text='Hasta',
            justify='center',
            font=(self.__config.TIPO_LETRA, 11)
        )
        self.__caja_texto_hasta.place(relx=0.2, rely=0.8)

    def __cargar_btn_recortar(self) -> None:
        self.__btn_recortar = CTkButton(
            master=self.__frame_recortes,
            width=120,
            height=40,
            corner_radius=20,
            text='Recortar',
            fg_color='#128F58',
            hover_color='#119E61',
            font=(self.__config.TIPO_LETRA, 13),
            command=self.__controlador.click_btn_recortar
        )
        self.__btn_recortar.place(relx=0.6, rely=0.8)

    def __cargar_btn_borrar(self) -> None:
        self.__btn_eliminar_recorte = CTkButton(
            master=self.__frame_recortes,
            width=80,
            height=40,
            corner_radius=20,
            fg_color='#603535',
            hover_color='#6D3636',
            text='Borrar',
            font=(self.__config.TIPO_LETRA, 12),
            command=self.__controlador.click_btn_borrar
        )
        self.__btn_eliminar_recorte.place(relx=0.82, rely=0.8)

    # Metodos para agregar o quitar recortes
    def agregar_recorte(self, ini: int, fin: int) -> None:
        """ Se añade una caja en el frame con los datos del recorte """
        etq = CTkLabel(
            master=self.__scrodable_frame_recortes,
            width=145,
            height=30,
            corner_radius=15,
            fg_color='#353535',
            text=f'Desde la {ini}, hasta la {fin}',
            text_color='#bbb',
            font=(self.__config.TIPO_LETRA, 11)
        )
        long = len(self.__etqs_recortes)
        etq.grid(row=(long) // 3, column=(long) % 3,
                pady=(10, 0), padx=(5, 10))
        self.__etqs_recortes.append(etq)

        # Se resetea la informacion de las cajas de texto desde y hasta
        self.__caja_texto_desde.delete(0, 'end')
        self.__caja_texto_desde._activate_placeholder()
        self.__ventana.focus_force()
        
        self.__caja_texto_hasta.delete(0, 'end')
        self.__caja_texto_hasta._activate_placeholder()
        self.__ventana.focus_force()

    def quitar_ultimo_recorte(self) -> None:
        """ Se quita la caja del ultimo recorte en el frame """
        if len(self.__etqs_recortes) == 0:
            return
        
        etq = self.__etqs_recortes.pop(-1)
        etq.destroy()

    # Metodos para controlar el texto del boton buscar archivo
    def poner_nombre_pdf_btn_buscar_archivo(self, nombre_pdf: str) -> None:
        """
            El texto del boton para buscar el pdf se sustituye por el
            argumento nombre_pdf
        """
        self.__btn_archivo.configure(text=nombre_pdf)

    def poner_texto_original_btn_buscar_archivo(self) -> None:
        """ 
            El nombre del pdf que aparece como texto en el boton se sustituye
            por su texto que tenia originalmente
        """
        self.__btn_archivo.configure(text='Elegir un archivo Pdf')

    # Métodos para controlar el boton para eliminar el pdf
    def hacer_visible_btn_eliminar_pdf(self) -> None:
        self.__indicador_pdf.place(relx=0.85, rely=0.15)
        self.__btn_eliminar_pdf.place(relx=0.83, rely=0.22)

    def hacer_invisible_btn_eliminar_pdf(self) -> None:
        self.__indicador_pdf.place_forget()
        self.__btn_eliminar_pdf.place_forget()

    def poner_estado_por_defecto(self) -> None:
        self.habilitar_btn_archivo()
        self.hacer_invisible_btn_eliminar_pdf()
        self.poner_texto_original_btn_buscar_archivo()
        self.deshabilitar_input_recorte()
        self.deshabilitar_btn_recortar()
        self.deshabilitar_btn_borrar()

    # Metodos para habilitar los botones
    def habilitar_btn_archivo(self) -> None:
        self.__btn_archivo.configure(state='normal', cursor='hand2')

    def habilitar_input_recorte(self) -> None:
        self.__btn_agregar_recorte.configure(state='normal', cursor='hand2')
        self.__caja_texto_desde.configure(state='normal')
        self.__caja_texto_hasta.configure(state='normal')

    def habilitar_btn_recortar(self) -> None:
        self.__btn_recortar.configure(state='normal', cursor='hand2',
                                    fg_color='#128F58')

    def habilitar_btn_borrar(self) -> None:
        self.__btn_eliminar_recorte.configure(state='normal', cursor='hand2',
                                    fg_color='#603535')

    # Metodos para deshabilitar los botones
    def deshabilitar_btn_archivo(self) -> None:
        self.__btn_archivo.configure(state='disabled', cursor='arrow')

    def deshabilitar_input_recorte(self) -> None:
        self.__btn_agregar_recorte.configure(state='disabled', cursor='arrow')
        
        self.__caja_texto_desde.delete(0, 'end')
        self.__caja_texto_desde._activate_placeholder()
        self.__caja_texto_desde.configure(state='disabled')
        
        self.__caja_texto_hasta.delete(0, 'end')
        self.__caja_texto_hasta._activate_placeholder()
        self.__caja_texto_hasta.configure(state='disabled')
        

    def deshabilitar_btn_recortar(self) -> None:
        self.__btn_recortar.configure(state='disabled', cursor='arrow',
                                    fg_color='#106A43')

    def deshabilitar_btn_borrar(self) -> None:
        self.__btn_eliminar_recorte.configure(state='disabled', cursor='arrow',
                                    fg_color='#453030')
    
    # Metodos para obtener los valores de las cajas de texto
    def obtener_valor_caja_desde(self) -> str:
        return self.__caja_texto_desde.get()
    
    def obtener_valor_caja_hasta(self) -> str:
        return self.__caja_texto_hasta.get()