import tkinter as tk
import keyboard
import threading

# Crear ventana Principal
ventana = tk.Tk()

# Cambiar título
ventana.title("Calculadora :)")

# Diseño de la ventana
ventana.geometry("330x450")
ventana.maxsize(350, 480)
ventana.minsize(250, 350)
ventana.configure(bg="lightblue", padx=10, pady=10)
ventana.iconbitmap(r"D:\_ArchivosUsuario\Desktop\Calculadora\assets\calculadora.ico")

# Expresiones
expresion = ""
valor_actual = False

# Variables de Colores
color_fondo_numero = "#b3cde0"
color_fondo_operacion = "#7A869A"
color_fondo_especial = "#9B90B6"
color_fondo_calcular = "#b0e57c"
color_fondo_presionado = "#6a51a3"
color_fondo_calcular_presionado = "#76c7c0"
color_texto_numero = "#333333"
color_texto_especial = "#ffffff"

# Configurar filas y columnas para que se expandan
for i in range(5):
    ventana.grid_rowconfigure(i, weight=1)

for i in range(4):
    ventana.grid_columnconfigure(i, weight=1)

# Crear widgets
entry1_texto = tk.StringVar()

# Crear entrada de texto
entry = tk.Entry(ventana, font=("Comic Sans MS", 32, 'bold'),
                 bg="#e8f0fe", fg="#000000", bd=10, relief="sunken", state="disabled",
                 justify="right", borderwidth=2, width=14, textvariable=entry1_texto)
entry.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

# Elementos en la cuadrícula de botones
lista_posiciones = [
    ("0", 4, 0),  # 0
    ("1", 1, 0),  # 1
    ("2", 1, 1),  # 2
    ("3", 1, 2),  # 3
    ("4", 2, 0),  # 4
    ("5", 2, 1),  # 5
    ("6", 2, 2),  # 6
    ("7", 3, 0),  # 7
    ("8", 3, 1),  # 8
    ("9", 3, 2),  # 9
    ("+", 1, 3),  # Suma
    ("-", 2, 3),  # Resta
    ("/", 3, 3),  # División
    ("*", 4, 3),  # Multiplicación
    (".", 4, 1),  # Coma
    ("C", 4, 2)   # Limpiar
]

# Crear los botones de la calculadora
def crear_botones():
    for texto, fila, columna in lista_posiciones:
        if texto in ['/', '*', '-', '+']:
            comando = lambda x=texto: pulsar_tecla(x)
            color_fondo = color_fondo_operacion
            color_texto = color_texto_especial
        elif texto == 'C':
            comando = limpiar
            color_fondo = color_fondo_especial
            color_texto = color_texto_especial
        elif texto == '.':
            comando = lambda x=texto: pulsar_tecla(x)
            color_fondo = color_fondo_especial
            color_texto = color_texto_especial
        else:
            comando = lambda x=texto: pulsar_tecla(x)
            color_fondo = color_fondo_numero
            color_texto = color_texto_numero

        tk.Button(ventana, text=texto, command=comando, relief="raised",
                  bg=color_fondo, fg=color_texto, activebackground=color_fondo_especial,
                  activeforeground=color_fondo_presionado, font=("Comic Sans MS", 15)).grid(
            row=fila, column=columna, sticky="nsew", padx=2, pady=2)

    # Botón igual para calcular
    tk.Button(ventana, font=("Comic Sans MS", 15, 'bold'), text="=", command=calcular,
              bd=1, activeforeground=color_texto_especial, activebackground=color_fondo_presionado).grid(
        row=5, column=0, columnspan=4, sticky="nsew")

# Función para calcular el resultado
def calcular():
    global expresion, valor_actual
    entry1_texto.set(expresion)
    try:
        resultado = eval(expresion)
        if resultado == int(resultado):
            resultado = int(resultado)
        entry1_texto.set(str(resultado))
        expresion = str(resultado)
        valor_actual = True
    except:
        entry1_texto.set("Error")
        expresion = ""
        valor_actual = False

# Función para limpiar la pantalla
def limpiar():
    global expresion, valor_actual
    expresion = ""
    entry1_texto.set(expresion)
    valor_actual = False

# Función para actualizar la expresión al pulsar una tecla
def pulsar_tecla(tecla):
    global expresion, valor_actual
    if len(expresion) < 10:
        if valor_actual:
            if tecla.isdigit() or tecla == ".":
                expresion = str(tecla)
            else:
                expresion += str(tecla)
            valor_actual = False
        else:
            expresion += str(tecla)
        entry1_texto.set(expresion)

# Función para borrar el último dígito
def borrar():
    global expresion
    if len(expresion) > 0:
        expresion = expresion[:-1]
    entry1_texto.set(expresion)

# Detectar teclas del teclado físico
def detectar_teclas():
    def on_key_event(tecla):
        if tecla.name in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                          '+', '-', '*', '/', '.', 'c', 'C', 'backspace']:
            if tecla.name.lower() == 'backspace':
                borrar()
            elif tecla.name.lower() == 'c':
                limpiar()
            else:
                pulsar_tecla(tecla.name)
        elif tecla.name == 'enter':  # Detectar la tecla Enter
            calcular()

    keyboard.on_press(on_key_event)  # Detectar cuando cualquier tecla es presionada

# Llamar a la función de detección de teclas en un hilo separado para no bloquear la interfaz
teclado_thread = threading.Thread(target=detectar_teclas, daemon=True)
teclado_thread.start()

# Ejecutar la interfaz gráfica
crear_botones()
ventana.mainloop()
