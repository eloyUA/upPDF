from customtkinter import CTkOptionMenu
from tkinter import NORMAL

class SelectorSaturar(CTkOptionMenu):
    def __init__(self, master, width = 140, height = 28, corner_radius = None,
                bg_color = "transparent", fg_color = None, button_color = None,
                button_hover_color = None, text_color = None,
                text_color_disabled = None, dropdown_fg_color = None,
                dropdown_hover_color = None, dropdown_text_color = None,
                font = None, dropdown_font = None, variable = None,
                state = NORMAL, hover = True, command = None,
                dynamic_resizing = True, anchor = "w", **kwargs) -> None:
        
        self.__valores = [
            'Sin saturación',
            'Saturación del 10%',
            'Saturación del 20%',
            'Saturación del 30%',
            'Saturación del 40%',
            'Saturación del 50%'
        ]
        super().__init__(master, width, height, corner_radius, bg_color,
                        fg_color, button_color, button_hover_color, text_color,
                        text_color_disabled, dropdown_fg_color, dropdown_hover_color,
                        dropdown_text_color, font, dropdown_font, self.__valores,
                        variable, state, hover, lambda v: command(self.__decodificar_str(v)),
                        dynamic_resizing, anchor, **kwargs)

    def __codificar_valor(self, valor: int) -> str:
        """ 10, 20 30, 40, 50 """
        if not valor in [0, 10, 20, 30, 40, 50]:
            return
        
        if valor == 0:
            return 'Sin saturación'
        else:
            return f'Saturación del {valor}%'

    def __decodificar_str(self, cadena: str) -> int:
        """ Devuelve: 0, 10, 20, 30, 40, 50 """
        match cadena:
            case 'Sin saturación':
                return 0
            case 'Saturación del 10%':
                return 10
            case 'Saturación del 20%':
                return 20
            case 'Saturación del 30%':
                return 30
            case 'Saturación del 40%':
                return 40
            case 'Saturación del 50%':
                return 50
            case _:
                pass

    def set(self, valor: int):
        return super().set(self.__codificar_valor(valor))
    
    def get(self) -> int:
        return self.__decodificar_str(super().get())