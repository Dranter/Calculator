from calculadora import evaluar_expresion
modo_salida = "dec" # Modo de salida por defecto

def main():
    global modo_salida

    print("Mi SUPERCalculadora")
    print("Escribe una expresión matemática y pulsa Enter.")
    print("PUEDES CAMBIAR el modo de visualizacion a DECIMAL, BINARIO, HEXADECIMAL u OCTADECIMAL") 
    print("escribiendo 'modo dec','modo bin, 'modo hex', 'modo oct'")
    print("Escribe 'salir' o pulsa Ctrl+C para cerrar.\n")

    while True:
        try:
            expr = input(f"Introduce expresión: [{modo_salida.upper()}] > ").strip()
            if expr.lower() == "salir":
                print("Saliendo de la calculadora...")
                break

            # Cambiar el modo de salida
            if expr.lower().startswith("modo "):
                nuevo_modo = expr.split()[1].lower()
                if nuevo_modo in ("dec", "hex", "bin", "oct"):
                    modo_salida = nuevo_modo
                    print(f"Modo de salida cambiado a: {modo_salida.upper()}\n")
                else:
                    print("Modo no valido. Usa modo dec, hex, bin u oct.\n")
                continue

            resultado = evaluar_expresion(expr)
            resultado = round(resultado, 10)
            
            if abs(resultado) < 1e-10:  # si es EXCESIVAMENTE pequeño, vuelvelo 0
                resultado = 0.0
            # Formateo salida segun el modo (hexa, binario...)
            if modo_salida == "dec":
                salida = str(resultado)
            elif modo_salida == "hex":
                salida = hex(int(resultado))
            elif modo_salida == "bin":
                salida = bin(int(resultado))
            elif modo_salida == "oct":
                salida = oct(int(resultado))

            #print(f"Resultado: {round(resultado, 10)}\n") #redondear al decimo decimal
            #print(f"Resultado: {resultado:.10f}\n") # 10 decimales (truncamiento)
            print(f"Resultado: {salida}\n") # salida dependiendo de el modo

        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print("\nSaliendo de la calculadora...")
            break

# permite importar funciones sin que se ejecuten automaticamente
# es decir, solo se ejecutara cuando escribamos python main.py
if __name__ == "__main__":
    main()