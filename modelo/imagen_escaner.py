import numpy as np
import statistics as st
import pytesseract

from spellchecker import SpellChecker
from fitz import Pixmap
from math import sqrt
from PIL import Image, ImageEnhance
from modelo.errores import ErrorImagenEscanerRGBA

class ImagenEscaner():
    def __init__(self, pix: Pixmap):
        """ Requisito: Que no sea RGBA """
        if pix.alpha:
            raise ErrorImagenEscanerRGBA('Solo se pueden abrir imagenes RGB')
        
        vector_pix = np.frombuffer(pix.samples, dtype=np.uint8)
        matriz_pix = vector_pix.reshape(pix.height, pix.width, pix.n)
        self.__img = Image.fromarray(matriz_pix, mode='RGB')

    # Metodos para el recorte de los bordes
    def __hay_similitud_numeros(self, vector: np.ndarray) -> bool:
        media = np.mean(vector)
        desv_tip =  sqrt(st.variance(vector))

        dist_norm = st.NormalDist(mu=media, sigma=desv_tip)
        return dist_norm.cdf(desv_tip) - (1 - dist_norm.cdf(-desv_tip)) > 0.9

    def __obtener_linea_pixeles(self, matriz_pixeles: np.ndarray, indice: int,
                                zona: str) -> np.ndarray:
        """ zona: ['N', 'S', 'E', 'O'] (Norte, sur, este, oeste) """
        if not zona in ['N', 'S', 'E', 'O']:
            return
        
        match zona:
            case 'N':
                return matriz_pixeles[indice]
            case 'S':
                return matriz_pixeles[-indice - 1]
            case 'E':
                return matriz_pixeles[:, -indice - 1]
            case 'O':
                return matriz_pixeles[:, indice]

    def __detectar_franja(self, matriz_pixeles: np.ndarray, inicial: int,
                            final: int, sep: int, zona: str) -> int:
        """ zona: ['N', 'S', 'E', 'O'] (Norte, sur, este, oeste) """
        if not zona in ['N', 'S', 'E', 'O']:
            return
        
        linea_inicial = self.__obtener_linea_pixeles(matriz_pixeles, 0, zona)
        for i in range(inicial, final, sep):
            linea_actual = self.__obtener_linea_pixeles(matriz_pixeles, i, zona)
            
            diff = linea_inicial - linea_actual
            diff_rojo = np.mean(np.abs(diff[:, 0]))
            diff_verde = np.mean(np.abs(diff[:, 1]))
            diff_azul = np.mean(np.abs(diff[:, 2]))

            if (diff_rojo + diff_verde + diff_azul > 40 and
                self.__hay_similitud_numeros(diff[:, 0]) and
                self.__hay_similitud_numeros(diff[:, 1]) and
                self.__hay_similitud_numeros(diff[:, 2])):

                return i # Mas o menos por aquí esta el borde
        return -1

    def recortar_bordes(self, lim=0.045) -> None:
        """
            lim: (0.015, 0.5) Es la proporcion de la zona de los laterales
                              que se comprueba
        """
        if 0.015 <= lim >= 0.5:
            return
        
        m_pix = np.array(self.__img).astype(int)
        sep_vertical = round(len(m_pix) * 0.015)
        sep_horizontal = round(len(m_pix[0]) * 0.015)
        final_vertical = round(len(m_pix) * lim)
        final_horizontal = round(len(m_pix[0]) * lim)

        rec_N = self.__detectar_franja(m_pix, 0, final_vertical, sep_vertical, 'N')
        rec_S = self.__detectar_franja(m_pix, 0, final_vertical, sep_vertical, 'S')
        rec_E = self.__detectar_franja(m_pix, 0, final_horizontal, sep_horizontal, 'E')
        rec_O = self.__detectar_franja(m_pix, 0, final_horizontal, sep_horizontal, 'O')

        m_pix_rec = m_pix
        if rec_N != -1:
            m_pix_rec = m_pix_rec[rec_N:]
        if rec_S != -1:
            m_pix_rec = m_pix_rec[:-rec_S]
        if rec_E != -1:
            m_pix_rec = m_pix_rec[:, :-rec_E]
        if rec_O != -1:
            m_pix_rec = m_pix_rec[:, rec_O:]

        m_pix_rec = m_pix_rec.astype(np.uint8)
        self.__img = Image.fromarray(m_pix_rec, mode='RGB')

    # Métodos para invertir automaticamente o manualmente
    def __hay_palabras_coherentes(self, img: Image.Image) -> bool:
        d_es = SpellChecker(language='es')
        d_in = SpellChecker(language='en')

        numeros = 0
        coherentes = 0
        txt_split = str(pytesseract.image_to_string(img)).split()
        for secuencia in txt_split:
            if secuencia.isdigit():
                numeros += 1
            else:
                if (secuencia in d_es or secuencia in d_in):
                    coherentes += 1
        return coherentes / (len(txt_split) - numeros) >= 0.25

    def invertir_automaticamente(self) -> None:
        # Hacemos una copia de la imagen más pequeña
        img_res = self.__img.resize(
            (round(self.__img.width / 1.75), round(self.__img.height / 1.75)),
            resample=Image.LANCZOS
        )

        img_pix = np.array(img_res).astype(int)
        rec_h = len(img_pix[0]) // 6
        img = Image.fromarray(
            img_pix[:, rec_h:-rec_h].astype(np.uint8),
            mode='RGB'
        )

        # Procesamos la copia para detectar la inversion e invertimos la original
        if self.__hay_palabras_coherentes(img):
            return
        
        img_inv_x = img.transpose(Image.FLIP_LEFT_RIGHT)
        img_inv_xy = img_inv_x.transpose(Image.FLIP_TOP_BOTTOM)
        if self.__hay_palabras_coherentes(img_inv_xy):
            self.invertir(True, True)
            return
        
        if self.__hay_palabras_coherentes(img_inv_x):
            self.invertir(True, False)
            return
        
        img_inv_y = img.transpose(Image.FLIP_TOP_BOTTOM)
        if self.__hay_palabras_coherentes(img_inv_y):
            self.invertir(False, True)
            return

    def invertir(self, eje_x: bool, eje_y: bool) -> None:
        if eje_x:
            self.__img = self.__img.transpose(Image.FLIP_LEFT_RIGHT)

        if eje_y:
            self.__img = self.__img.transpose(Image.FLIP_TOP_BOTTOM)

    # Métodos para filtrar
    def filtrar(self):
        """ Se aumenta el contraste y la nitidez """
        contraste = ImageEnhance.Contrast(self.__img)
        img_mas_contraste = contraste.enhance(1.15)

        nitidez = ImageEnhance.Sharpness(img_mas_contraste)
        self.__img = nitidez.enhance(1.8)

    # Métodos para saturar
    def saturar(self, factor_saturacion: float) -> None:
        """ factor_saturacion = 1 (Imagen original) """
        saturador = ImageEnhance.Color(self.__img)
        self.__img = saturador.enhance(factor_saturacion)

    def rotar(self, angulo: float) -> None:
        self.__img = self.__img.rotate(angle=angulo)

    # Método para pasar la imagen desde ImagenEscaner a Image.Image
    def get_imagen(self) -> Image.Image:
        return self.__img