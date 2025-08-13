from typing import List, Tuple
from pypdf import PdfReader, PdfWriter
from modelo.errores import ErrorAperturaPDF

def combinar(rutas: List[str], ruta_final: str) -> None:
    escritor = PdfWriter()
    for ruta in rutas:
        try:
            lector = PdfReader(ruta)
        except Exception as e:
            raise ErrorAperturaPDF(
                'No se puede abrir uno de los pdf para combinar') from e
        else:
            for page in lector.pages:
                escritor.add_page(page)
    
    with open(ruta_final, 'wb') as f:
        escritor.write(f)

def recortar(ruta: str, recortes: List[Tuple[int, int]]) -> None:
    if ruta[-4:] == '.pdf':
        ruta_final_tratada = ruta[:len(ruta) - 4]
    else:
        ruta_final_tratada = ruta

    try:
        lector = PdfReader(ruta)
    except Exception as e:
        raise ErrorAperturaPDF(
            'No se puede abrir el pdf para recortarlo') from e
    else:
        for rec in recortes:
            escritor = PdfWriter()
            for num_pag in range(rec[0] - 1, rec[1]):
                escritor.add_page(lector.get_page(num_pag))
            
            with open(f'{ruta_final_tratada}-[{rec[0]},{rec[1]}].pdf', 'wb') as f:
                escritor.write(f)

def num_paginas_totales(ruta: str) -> int:
    """ Devuelve el numero de paginas totales del pdf """
    try:
        lector = PdfReader(ruta)
    except Exception as e:
        raise ErrorAperturaPDF(
            'No se puede abrir el pdf para saber su numero de paginas') from e
    else:
        paginas = lector.get_num_pages()
        lector.close()
        return paginas