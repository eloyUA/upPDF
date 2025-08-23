import threading

from modelo.pdf_escaner_esc import PdfEscanerEscritura
from modelo.pdf_escaner_lec import PdfEscanerLectura

from controlador.contr_visor_pdf import ControladorVisorPdf

from vista.visor_pdf import VisorPdf
from vista.visor_pdf_eventos import EventosVisorPdf

class ControladorMejorar(EventosVisorPdf):
    def __init__(self, vista_mejorar) -> None:
        self.__vista_mejorar = vista_mejorar
        self.__cargar_widget_visor_pdf()
        self.__cargar_sistema_concurrente()

    def __cargar_widget_visor_pdf(self) -> None:
        self.__visor_pdf = VisorPdf(self.__vista_mejorar)
        self.__controlador_visor = ControladorVisorPdf(self.__visor_pdf, self)
        self.__visor_pdf.cargar_controlador(self.__controlador_visor)
        self.__visor_pdf.cargar_elementos()

    def __cargar_sistema_concurrente(self) -> None:
        self.__hilo = None
        self.__procesando_pdf = False
        self.__señal_detener_hilo = threading.Event()
        self.__semaforo = threading.Semaphore(1)

    # Son eventos llamados por el controlador del visor pdf (Se sobrescriben)
    # Ejemplo, si el usuario introduce un pdf, el controlador del menu se
    # entera gracias a este metodo
    def evento_pdf_ya_introducido(self) -> None:
        self.__vista_mejorar.habilitar_botones()
        self.__vista_mejorar.poner_estado_botones_por_defecto()

    def evento_pdf_ya_quitado(self) -> None:
        with self.__semaforo:
            if self.__procesando_pdf:
                self.__señal_detener_hilo.set()

        self.__vista_mejorar.deshabilitar_botones()
        self.__vista_mejorar.poner_estado_botones_por_defecto()

    def evento_avanzar_pag_pdf(self):
        pass
    
    def evento_retroceder_pag_pdf(self):
        pass

    # Son los metodos propios del controlador
    def click_boton_opcion(self) -> None:
        if (not(self.__vista_mejorar.esta_boton_filtrar_marcado()) and 
            not(self.__vista_mejorar.esta_boton_invertir_marcado()) and
            not(self.__vista_mejorar.esta_boton_saturar_marcado())):
            self.__vista_mejorar.marcar_boton_recortar()
            self.__vista_mejorar.deshabilitar_boton_recortar()
        elif not self.__vista_mejorar.esta_habilitado_boton_recortar():
            self.__vista_mejorar.habilitar_boton_recortar()

    def click_boton_iniciar_proceso(self) -> None:
        self.__hilo = threading.Thread(target=self.__hilo_iniciar_proceso)
        self.__hilo.start()

    def __hilo_iniciar_proceso(self) -> None:
        self.__vista_mejorar.deshabilitar_botones()
        self.__vista_mejorar.establecer_posicion_barra_progreso(0)
        self.__vista_mejorar.hacer_visible_barra_progreso()

        try:
            pdf_escaner_esc = PdfEscanerEscritura()
            pdf_escaner_lec = self.__controlador_visor.get_pdf()
            self.__procesar_imagenes_pdf(pdf_escaner_lec, pdf_escaner_esc)
            self.__guardar_pdf_escritura(pdf_escaner_lec, pdf_escaner_esc)
        except Exception as ex:
            ex.with_traceback()
        finally:
            self.__controlador_visor.click_boton_eliminar_archivo()
            self.__vista_mejorar.hacer_invisible_barra_progreso()
            self.__vista_mejorar.establecer_posicion_barra_progreso(0)
            self.__señal_detener_hilo.clear()

    def __procesar_imagenes_pdf(self, pdf_esc_lec: PdfEscanerLectura,
                                pdf_esc_escritura: PdfEscanerEscritura) -> None:
        num_pag = 1
        num_pag_totales = pdf_esc_lec.num_pag_totales()
        num_pag_fin =  num_pag_totales + 1
        while num_pag < num_pag_fin and not self.__señal_detener_hilo.is_set():
            tamaño_mm_pag = pdf_esc_lec.get_tamaño_mm_pag(num_pag)
            img_escaner = pdf_esc_lec.get_imagen_pagina_buena_calidad(num_pag)
            if self.__vista_mejorar.esta_boton_recortar_marcado():
                img_escaner.recortar_bordes()
            if self.__vista_mejorar.esta_boton_invertir_marcado():
                img_escaner.invertir_automaticamente()
            if self.__vista_mejorar.esta_boton_filtrar_marcado():
                img_escaner.filtrar()
            if self.__vista_mejorar.esta_boton_saturar_marcado():
                img_escaner.saturar(factor_saturacion=1.25)
            
            pdf_esc_escritura.añadir_imagen_escaner(
                img_escaner, tamaño_mm_pag)
            self.__vista_mejorar.establecer_posicion_barra_progreso(
                num_pag / num_pag_fin)
            num_pag += 1

    def __guardar_pdf_escritura(self, pdf_esc_lec: PdfEscanerLectura,
                                pdf_esc_escritura: PdfEscanerEscritura) -> None:
        if not self.__señal_detener_hilo.is_set():
            ruta_pdf_lec = pdf_esc_lec.get_ruta()
            if ruta_pdf_lec[-4:] != '.pdf':
                ruta_pdf_final = ruta_pdf_lec + ' (Mejorado).pdf'
            else:
                ruta_pdf_final = ruta_pdf_lec[:-4] + ' (Mejorado).pdf'
            pdf_esc_escritura.guardar(ruta_pdf_final)