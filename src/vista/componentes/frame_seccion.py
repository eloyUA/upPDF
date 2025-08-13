from customtkinter import CTk
from customtkinter import CTkFrame
from customtkinter import CTkLabel

from vista.config_vista import ConfigVista

class FrameSeccion(CTkFrame):
    def __init__(self, ventana: CTk, titulo: str | None=None) -> None:
        
        super().__init__(
            master=ventana,
            fg_color='transparent'
        )

        if titulo != None:
            self.__titulo = CTkLabel(
                master=self,
                text=titulo,
                text_color='#ccc',
                font=(ConfigVista().TIPO_LETRA, 20)
            )
            self.__titulo.place(relx=0.01, rely=0.02)

    def hacer_visible(self):
        self.place(relx=0.3, rely=0.1, relwidth=0.65, relheight=0.82)

    def hacer_invisible(self):
        self.place_forget()