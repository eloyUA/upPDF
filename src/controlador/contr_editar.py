import threading

from enum import Enum

from vista.visor_pdf import VisorPdf
from vista.visor_pdf_eventos import EventosVisorPdf
from controlador.contr_visor_pdf import ControladorVisorPdf
from modelo.pdf_escaner_esc import PdfEscanerEscritura

class Opcion(Enum):
    ELIMINAR = 0
    RECORTAR = 1
    FILTRAR = 2
    SATURAR = 3
    INVERTIR = 4

class ControladorEditar(EventosVisorPdf):
    def __init__(self, vista_editar) -> None:
        self.__vista_editar = vista_editar
        self.__visor_pdf = VisorPdf(vista_editar)
        self.__controlador_visor = ControladorVisorPdf(self.__visor_pdf, self)
        self.__visor_pdf.cargar_controlador(self.__controlador_visor)
        self.__visor_pdf.cargar_elementos()

        # Atributo para saber que opciones tiene activada una pagina
        self.__modificaciones = []
        
        # Atributos para controlar el procesamiento del pdf
        self.__hilo = None
        self.__procesando_pdf = False
        self.__señal_detener_hilo = threading.Event()
        self.__semaforo = threading.Semaphore(1)

    def __cargar_modificaciones(self) -> None:
        """ Se cargan las modificaciones por defecto (ninguna) para cada pagina """
        self.__modificaciones.clear()
        for i in range(self.__controlador_visor.get_pdf().num_pag_totales()):
            self.__modificaciones.append({
                Opcion.ELIMINAR: 0,
                Opcion.RECORTAR: 0,
                Opcion.FILTRAR: 0,
                Opcion.SATURAR: 0,
                Opcion.INVERTIR: ''
            })
        # Si no se hace nada = 0 o ''
        # Si se hace algo = 1 u otro valor que no sea 0, o algo diferente de ''

    def __actualizar_opciones_segun_pagina(self) -> None:
        """
            Cuando el usuario avanza o retrocede una pagina, se llama a este
            metodo para actualizar el estado de los botones segun las opciones
            de modificacion de dicha pagina
        """
        num_pag = self.__controlador_visor.num_pag_actual()
        modificacion = self.__modificaciones[num_pag - 1]
        if modificacion[Opcion.ELIMINAR] != 0:
            self.__vista_editar.seleccionar_btn_eliminar()
            self.__vista_editar.deseleccionar_opciones_menos_eliminar()
            self.__vista_editar.deshabilitar_opciones_menos_eliminar()
        else:
            self.__vista_editar.deseleccionar_btn_eliminar()
            if modificacion[Opcion.RECORTAR] != 0:
                self.__vista_editar.seleccionar_btn_recortar()
            else:
                self.__vista_editar.deseleccionar_btn_recortar()

            if modificacion[Opcion.FILTRAR] != 0:
                self.__vista_editar.seleccionar_btn_filtrar()
            else:
                self.__vista_editar.deseleccionar_btn_filtrar()

            if modificacion[Opcion.SATURAR] != 0:
                self.__vista_editar.seleccionar_opcion_saturar(
                    modificacion[Opcion.SATURAR]
                )
            else:
                self.__vista_editar.deseleccionar_opcion_saturar()

            if modificacion[Opcion.INVERTIR] != '':
                self.__vista_editar.seleccionar_opcion_invertir(
                    modificacion[Opcion.INVERTIR]
                )
            else:
                self.__vista_editar.deseleccionar_opcion_invertir()
            self.__vista_editar.habilitar_botones()

    def __modificar_opcion_pagina(self, opcion: Opcion, valor: int | str) -> None:
        """ Modifica la opcion con el valor introducido de la pagina actual """
        num_pag = self.__controlador_visor.num_pag_actual()
        self.__modificaciones[num_pag - 1][opcion] = valor

    # Son los eventos que pueden ser llamados desde el visor pdf
    # Ejemplo, si el usuario introduce un pdf, el controlador del menu se
    # entera gracias a este metodo
    def evento_pdf_ya_introducido(self):
        with self.__semaforo:
            if self.__procesando_pdf:
                self.__señal_detener_hilo.set()

        self.__cargar_modificaciones()
        self.__vista_editar.actualizar_texto_opciones(1)
        self.__vista_editar.habilitar_botones()
        self.__vista_editar.poner_estado_botones_por_defecto()

    def evento_pdf_ya_quitado(self):
        self.__modificaciones.clear()
        self.__vista_editar.actualizar_texto_opciones(0)
        self.__vista_editar.deshabilitar_botones()
        self.__vista_editar.poner_estado_botones_por_defecto()

    def evento_avanzar_pag_pdf(self):
        self.__actualizar_opciones_segun_pagina()
    
    def evento_retroceder_pag_pdf(self):
        self.__actualizar_opciones_segun_pagina()

    # Son metodos propios del controlador
    def click_boton_eliminar_pagina(self) -> None:
        num_pag = self.__controlador_visor.num_pag_actual()
        if self.__vista_editar.esta_boton_eliminar_pag_marcado():
            self.__modificaciones[num_pag - 1] = {
                Opcion.ELIMINAR: 1,
                Opcion.RECORTAR: 0,
                Opcion.FILTRAR: 0,
                Opcion.SATURAR: 0,
                Opcion.INVERTIR: ''
            }
            self.__vista_editar.deseleccionar_opciones_menos_eliminar()
            self.__vista_editar.deshabilitar_opciones_menos_eliminar()
        else:
            self.__modificaciones[num_pag - 1][Opcion.ELIMINAR] = 0
            self.__vista_editar.habilitar_botones()

    def click_boton_recortar(self) -> None:
        valor = self.__vista_editar.esta_boton_recortar_marcado()
        self.__modificar_opcion_pagina(Opcion.RECORTAR, (int) (valor))
            
    def click_boton_filtrar(self) -> None:
        valor = self.__vista_editar.esta_boton_filtrar_marcado()
        self.__modificar_opcion_pagina(Opcion.FILTRAR, (int) (valor))

    def click_opcion_saturar(self, valor: int) -> None:
        self.__modificar_opcion_pagina(Opcion.SATURAR, valor)

    def click_opcion_invertir(self, valor: str) -> None:
        self.__modificar_opcion_pagina(Opcion.INVERTIR, valor)

    def __procesar_pdf(self) -> None:
        with self.__semaforo:
            self.__procesando_pdf = True

        self.__vista_editar.deshabilitar_botones()
        self.__vista_editar.hacer_visible_barra_progreso()
        self.__vista_editar.establecer_posicion_barra_progreso(0)

        try:
            pdf_escaner_esc = PdfEscanerEscritura()
            pdf_escaner_lec = self.__controlador_visor.get_pdf()

            num_pag = 1
            paginas_totales = pdf_escaner_lec.num_pag_totales()
            num_pag_fin = paginas_totales + 1
            while num_pag < num_pag_fin and not self.__señal_detener_hilo.is_set():
                modificacion = self.__modificaciones[num_pag - 1]
                tamaño_mm_pag = pdf_escaner_lec.get_tamaño_mm_pag(num_pag)
                img_escaner = pdf_escaner_lec.get_imagen_pagina_buena_calidad(num_pag)
                if modificacion[Opcion.ELIMINAR] == 0:
                    if modificacion[Opcion.RECORTAR] != 0:
                        img_escaner.recortar_bordes()
                    if modificacion[Opcion.FILTRAR] != 0:
                        img_escaner.filtrar()
                    if modificacion[Opcion.SATURAR] != 0:
                        img_escaner.saturar(1 + modificacion[Opcion.SATURAR] / 100)

                    if modificacion[Opcion.INVERTIR] == 'x':
                        img_escaner.invertir(eje_x=True, eje_y=False)
                    elif modificacion[Opcion.INVERTIR] == 'y':
                        img_escaner.invertir(eje_x=False, eje_y=True)
                    elif modificacion[Opcion.INVERTIR] == 'xy':
                        img_escaner.invertir(eje_x=True, eje_y=True)
                    pdf_escaner_esc.añadir_imagen_escaner(
                        img_escaner, tamaño_mm_pag)

                self.__vista_editar.establecer_posicion_barra_progreso(
                    num_pag / num_pag_fin)
                num_pag += 1

            if not self.__señal_detener_hilo.is_set():
                ruta_pdf_lec = pdf_escaner_lec.get_ruta()
                if ruta_pdf_lec[-4:] != '.pdf':
                    ruta_pdf_final = ruta_pdf_lec + ' (Editado).pdf'
                else:
                    ruta_pdf_final = ruta_pdf_lec[:-4] + ' (Editado).pdf'
                pdf_escaner_esc.guardar(ruta_pdf_final)
        except Exception as ex:
            pass
        finally:
            self.__controlador_visor.click_boton_eliminar_archivo()
            self.__vista_editar.establecer_posicion_barra_progreso(0)
            self.__vista_editar.hacer_invisible_barra_progreso()
        # Al llamar a este metodo del controlador del visor, este llama luego
        # al evento_pdf_ya_quitado del controlador de esta clase. Un poco lio :)

        with self.__semaforo:
            self.__procesando_pdf = False
        self.__señal_detener_hilo.clear()

    def click_boton_confirmar(self) -> None:
        self.__hilo = threading.Thread(target=self.__procesar_pdf)
        self.__hilo.start()