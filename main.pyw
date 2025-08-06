#!/usr/bin/env python3

'''
    La extension .pyw es como la .py pero python no abre una
    terminal para ejecutar la aplicación grafica.
'''

from vista.ventana import Ventana

if __name__ == '__main__':
    Ventana().mainloop()