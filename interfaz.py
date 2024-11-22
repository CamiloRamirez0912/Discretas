from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from mapa_tunja import MapaTunja

class InterfazMapaTunja:
    def __init__(self):
        self.mapa_tunja = MapaTunja()
        self.root = Tk()
        self.root.title("Mapa Interactivo de Tunja")
        self.direccion_var = StringVar()
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Widgets de la GUI
        Label(self.root, text="Ingresa una dirección:").grid(row=0, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.direccion_var, width=40).grid(row=0, column=1, padx=10, pady=10)
        Button(self.root, text="Mostrar en el mapa", command=self._mostrar_mapa).grid(row=1, column=0, columnspan=2, pady=10)

    def _mostrar_mapa(self):
        direccion = self.direccion_var.get()
        if direccion:
            try:
                self.mapa_tunja.mostrar_mapa(direccion)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")
        else:
            messagebox.showerror("Error", "Por favor, ingresa una dirección válida.")

    def iniciar(self):
        self.root.mainloop()
