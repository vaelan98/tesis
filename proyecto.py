import tkinter as tk
from tkinter import Tk, Label, Button
class VentanaEjemplo:
    def __init__(self, master):
        self.master = master
        master.title("Interfaz Varioguide")
        self.etiqueta = Label(master, text="Ventana captura de pantalla!")
        self.etiqueta.pack()
        self.botonSaludo = Button(master, text="tomar foto", command=self.saludar)
        self.botonSaludo.pack()
        self.botonCerrar = Button(master, text="Cerrar", command=master.quit)
        self.botonCerrar.pack()
    def saludar(self):
        print("¡Salir de opcion!")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "el valor del error es\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("tomar foto!")
class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

      
        self.contents = tk.StringVar()
      
        self.contents.set("valor del error")
       
        self.entrythingy["textvariable"] = self.contents

        self.entrythingy.bind('<Key-Return>',
                             self.print_contents)
      
    def print_contents(self, event):
        print("Hi. The valor of the error is:",
              self.contents.get())

root = tk.Tk()
myapp = App(root)


app = Application(master=root)
miVentana = VentanaEjemplo(root)
myapp.mainloop()