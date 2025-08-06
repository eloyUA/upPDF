from customtkinter import CTkOptionMenu
from tkinter import NORMAL

class SelectorInvertir(CTkOptionMenu):
    def __init__(self, master, width = 140, height = 28, corner_radius = None,
                bg_color = "transparent", fg_color = None, button_color = None,
                button_hover_color = None, text_color = None,
                text_color_disabled = None, dropdown_fg_color = None,
                dropdown_hover_color = None, dropdown_text_color = None,
                font = None, dropdown_font = None, variable = None,
                state = NORMAL, hover = True, command = None,
                dynamic_resizing = True, anchor = "w", **kwargs) -> None:
        
        self.__valores = [
            'Sin inversión',
            'Inversión horizontal',
            'Inversión vertical',
            'Inversión de ambas'
        ]
        super().__init__(master, width, height, corner_radius, bg_color,
                        fg_color, button_color, button_hover_color, text_color,
                        text_color_disabled, dropdown_fg_color, dropdown_hover_color,
                        dropdown_text_color, font, dropdown_font, self.__valores,
                        variable, state, hover, lambda v: command(self.__decodificar_str(v)),
                        dynamic_resizing, anchor, **kwargs)

    def __codificar_valor(self, valor: str) -> str:
        """ '', 'x', 'y', 'xy' """
        match valor:
            case '':
                return 'Sin inversión'
            case 'x':
                return 'Inversión horizontal'
            case 'y':
                return 'Inversión vertical'
            case 'xy':
                return 'Inversión de ambas'
            case _:
                pass

    def __decodificar_str(self, cadena: str) -> str:
        """ Devuelve: '', 'x', 'y', 'xy' """
        match cadena:
            case 'Sin inversión':
                return ''
            case 'Inversión horizontal':
                return 'x'
            case 'Inversión vertical':
                return 'y'
            case 'Inversión de ambas':
                return 'xy'
            
    def set(self, valor: str):
        return super().set(self.__codificar_valor(valor))
    
    def get(self) -> str:
        return self.__decodificar_str(super().get())