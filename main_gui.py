import customtkinter as ctk
import math
from calculadora import evaluar_expresion

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CalculadoraGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SUPERCalculadora")
        self.geometry("400x600")

        # Pantalla de entrada
        self.entrada = ctk.CTkEntry(self, font=("Arial", 24))
        self.entrada.pack(padx=10, pady=10, fill="x")

        # Inicio con el cursor ya en la pantallita
        self.after(100, lambda: self.entrada.focus_force())

        # Pantalla de resultado
        self.resultado_label = ctk.CTkLabel(self, text="", font=("Arial", 20))
        self.resultado_label.pack(padx=10, pady=10)

        # Selector de modo de salida
        self.modo_salida = ctk.StringVar(value="DEC")   # Valor por defecto DECIMAL
        self.frame_modos = ctk.CTkFrame(self)
        self.frame_modos.pack(pady=5)
        self.modo_botones = [] # Guardamos los botones en una lista para acceder luego

        # Enter para calcular y delete
        self.bind("<Return>", lambda event: [self.calcular(), self.revisar_modo()])
        self.entrada.bind("<BackSpace>", self.borrar_tecla)
        self.bind("<Delete>", lambda event: self.borrar_todo())
        self.bind("<Escape>", lambda e: self.destroy())

        for i, modo in enumerate(["DEC", "BIN", "HEX", "OCT"]):
            btn = ctk.CTkRadioButton(
                self.frame_modos,
                text=modo,
                variable=self.modo_salida,
                value=modo
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
            self.modo_botones.append(btn)

        # Frame para los botones
        self.frame_botones = ctk.CTkFrame(self)
        self.frame_botones.pack(pady=10)

        # Creacion botones 0-9
        self.crear_botones()

        # Creacion operadores
        self.crear_botones_operaciones() 

        # Creacion trigonometrica
        self.crear_botones_funciones()

        # Creacion borrar
        self.crear_botones_del()

        # Boton de calcular
        #btn = ctk.CTkButton(self, text="Calcular", command=self.calcular)
        #btn.pack(pady=10)
        self.calcular_btn = ctk.CTkButton(self, text="Calcular", command=self.calcular)
        self.calcular_btn.pack(pady=10)


    # ("7", 0, 0)   ("simbolo", posicion Y, posicion X)
    def crear_botones(self):
        botones = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
            ("0", 3, 0), ("π", 5, 1), ("e", 5, 2),
            ("(", 5, 3), (")", 5, 4), (".", 3, 3)
        ]

        for (texto, fila, col) in botones:
            if texto == "π":
                cmd = lambda t="pi": self.agregar_numero(t)
            elif texto == "e":
                cmd = lambda t="e": self.agregar_numero(t)
            else:
                cmd = lambda t=texto: self.agregar_numero(t)

            btn = ctk.CTkButton(
                self.frame_botones,
                text=texto,
                width=40,
                height=30,
                font=("Arial", 20),
                #command=lambda t=texto: self.agregar_numero(t)
                command=cmd
            )
            btn.grid(row=fila, column=col, padx=5, pady=5)

    # ("7", 0, 0)   ("simbolo", posicion Y, posicion X)
    def crear_botones_operaciones(self):
        operaciones = [
            ("+", 2, 3), 
            ("-", 2, 4),
            ("*", 1, 3),
            ("/", 1, 4),
            ("**", 3, 4)
        ]
        
        for (simbolo, fila, col) in operaciones:
            btn = ctk. CTkButton(
                self.frame_botones,
                text=simbolo,
                width=40,
                height=30,
                font=("Arial", 20),
                command=lambda s=simbolo: self.agregar_operacion(s)
            )
            btn.grid(row=fila, column=col, padx=5, pady=5)

    # Frame para funciones matematicas
    def crear_botones_funciones(self):

        funciones = ["sin", "cos", "tan", "sqrt", "log", "ln", "abs"]
        self.frame_funciones = ctk. CTkFrame(self)
        self.frame_funciones.pack(pady=10)

        for i, func in enumerate(funciones):
            btn = ctk.CTkButton(
                self.frame_funciones,
                text=func,  
                width=40,
                height=30,
                font=("Arial", 16),
                command=lambda f=func: self.agregar_funcion(f)
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5) 
    def crear_botones_del(self):
        # Fila de control borrar todo
        boton_clear = ctk.CTkButton(
            self.frame_botones,
            text="AC",
            width=40,
            height=30,
            font=("Arial", 20),
            fg_color="#FF5555",
            hover_color="#CC4444",
            command=self.borrar_todo
        )
        boton_clear.grid(row=0, column=4, padx=5, pady=5)

        # Fila de control borrar 1
        boton_back = ctk.CTkButton(
            self.frame_botones,
            text="DEL",
            width=40,
            height=30,
            font=("Arial", 20),
            fg_color="#FF5555",
            hover_color="#9D3535",
            command=self.borrar_ultimo
        )
        boton_back.grid(row=0, column=3, padx=5, pady=5)


    def agregar_numero(self, numero):
        self.entrada.focus()
        self.entrada.insert(self.entrada.index(ctk.INSERT), numero)

    def agregar_operacion(self, operador):
        self.entrada.focus()
        self.entrada.insert(self.entrada.index(ctk.INSERT), operador)

    def borrar_ultimo(self):
        # Elimina el ultimo caracter
        actual = self.entrada.get()
        if actual: # Si no esta vacia
            self.entrada.delete(len(actual)-1, "end")

    def borrar_tecla(self, event=None):
        # Elimina el ultimo caracter
        actual = self.entrada.get()
        if actual: # Si no esta vacia
            self.entrada.delete(len(actual)-1, "end")
        return "break"

    def borrar_todo(self):
        # Elimina todo
        self.entrada.delete(0, "end")

    def agregar_funcion(self, funcion):
        # Añadimos parentesis para facilitar la escritura
        self.entrada.insert(ctk.END, f"{funcion}()")
        # Mueve el cursor a dentro del parentesis
        self.entrada.update() # Forzamos una actualizacion antes de mover el cursor
        texto_actual = self.entrada.get() # Obtenemos la posicion actual del texto
        pos = texto_actual.rfind(")") # Buscamos el ultimo parentesis ) y movemos el cursor justo antes
        self.entrada.icursor(pos) # Movemos el cursor dentro de los parentesis
        self.entrada.focus() # Forzamos que el campo de texto tenga el foco (para escribir dentro)

    def calcular(self):
        expr = self.entrada.get().strip().lower() # solo funciona con CTkEntry

        # Detectar comandos especiales
        if expr == "modo kawaii":
            self.activar_modo_kawaii()
            self.resultado_label.configure(text="🌸 ¡Modo kawaii activado! 🌸")
            self.entrada.delete(0, "end")
            return
        elif expr == "modo normal":
            self.reiniciar_modo()
            self.resultado_label.configure(text="Modo normal activado")
            self.entrada.delete(0, "end")
            return
        
        try:
            resultado = evaluar_expresion(expr)

            # Convertir segun el modo
            modo = self.modo_salida.get()
            if modo == "BIN":
                resultado = bin(int(resultado))
            elif modo == "HEX":
                resultado = hex(int(resultado))
            elif modo == "OCT":
                resultado = oct(int(resultado))
            else: # DEC
                resultado = str(resultado)

            self.resultado_label.configure(text=str(resultado))
        except Exception as e:
            self.resultado_label.configure(text=f"Error: {e}")

        
    # Colores especiales calculadora
    def revisar_modo(self):
        texto = self.entrada.get().strip().lower()

        if texto == "modo kawaii":
            self.activar_modo_kawaii()
            #self.entrada.delete(0, "end")
            #return

    def activar_modo_kawaii(self):
        # Cambiar fondo principal
        self.configure(fg_color="#FFD1DC")
        # Cambiar entrada
        self.entrada.configure(
            fg_color="#FFF0F5", 
            text_color="#FF69B4", 
            border_color="#FFB6C1"
        )

        # Cambiar fondo botones y operadores
        self.frame_botones.configure(fg_color="#FFE4E1")        
        self.frame_funciones.configure(fg_color="#FFE4E1")
        self.frame_modos.configure(
            fg_color="#FFE4E1",
            bg_color="#FFD1DC",       # Asegura contraste con fondo principal
            border_color="#FFB6C1",
            corner_radius=10
        )

        # Fondo de modos
        for btn in getattr(self, "modo_botones", []):
            btn.configure(
                fg_color="#FFB6C1", 
                hover_color="#FFC0CB", 
                text_color="#800080"
            )

        # Cambiar botones
        for hijo in self.frame_botones.winfo_children(): # Asumiendo que los botones estan en un frame
            texto = hijo.cget("text")
            # Si es un boton de borrado, usar rojo
            if texto in ["AC", "DEL"]:
                hijo.configure(
                    fg_color="#FF55E3",
                    hover_color="#C144CC",
                    text_color="#FFFFFF"
                )
                    
            else:    
                hijo.configure(
                    fg_color="#FFB6C1", 
                    hover_color="#FFC0CB", 
                    text_color="#800080"
                )
                
            
            
        # Cambiar funciones
        for hijo in self.frame_funciones.winfo_children(): # Asumiendo que los botones estan en un frame
            hijo.configure(
                fg_color="#FFB6C1", 
                hover_color="#FFC0CB", 
                text_color="#800080"
                )

        # Cambiar calcular
        self.calcular_btn.configure(
            fg_color="#FFB6C1", 
            hover_color="#FFC0CB", 
            text_color="#800080"
            )
        
        # Cambiar etiquestas de resultado
        self.resultado_label.configure(
            fg_color="#FFF0F5", 
            text_color="#FF69B4"
            )
        
    def reiniciar_modo(self):
        # Restaurar colores por defecto
        self.configure(fg_color=("#242424" if ctk.get_appearance_mode() == "Dark" else "#FFF0F5"))
        self.entrada.configure(
            fg_color="#2B2B2B",
            text_color="#FFF0F5",
            border_color="#565B5E"
        )

        self.frame_botones.configure(fg_color="#2B2B2B")    #FONDOS
        self.frame_funciones.configure(fg_color="#2B2B2B")  #FONDOS TRIGONOMETRIA
        self.frame_modos.configure(
            fg_color="#2B2B2B", # FONDO MODOS
            bg_color="#2B2B2B", # BORDES MODOS
            border_color="#2B2B2B"  # APARENTEMENTE NADA
        )

        # Restaurar botones
        for frame in [self.frame_botones, self.frame_funciones]:
            for hijo in frame.winfo_children():
                texto = hijo.cget("text")
                # si es un boton de borrado, usar rojo
                if texto in ["AC", "DEL"]:
                    hijo.configure(
                        fg_color="#FF5555",
                        hover_color="#9D3535",
                        text_color="#FFF0F5"
                    )
                else:    
                    hijo.configure(
                        fg_color="#1F6AA5",
                        hover_color="#144870",
                        text_color="#FFF0F5"
                )

        for btn in getattr(self, "modo_botones", []):
            btn.configure(
                fg_color="#1F6AA5",
                hover_color="#144870",
                text_color="#FFF0F5",
                #border_color="#BFBFBF"  # FONDO SELECCION MODOS
            )

        # boton calcular
        self.calcular_btn.configure(
            fg_color="#1F6AA5",
            hover_color="#114870",
            text_color="#FFF0F5"
        )

        self.resultado_label.configure(
            fg_color="#2B2B2B",
            text_color="#FFF0F5"
        )

if __name__ == "__main__":
    app = CalculadoraGUI()
    app.mainloop()
