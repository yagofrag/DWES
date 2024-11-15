from operaciones import suma, resta, multiplicacion, division

def calculadora():
    while True:
        try:
            num1 = float(input("Introduce el primer número: "))
            num2 = float(input("Introduce el segundo número: "))
        except ValueError:
            print("Por favor, introduce valores numéricos.")
            continue

        operacion = input("Elige una operación (suma, resta, multiplicacion, division): ").strip().lower()

        if operacion == "suma":
            resultado = suma(num1, num2)
        elif operacion == "resta":
            resultado = resta(num1, num2)
        elif operacion == "multiplicacion":
            resultado = multiplicacion(num1, num2)
        elif operacion == "division":
            resultado = division(num1, num2)
        else:
            print("Operación no válida. Intenta de nuevo.")
            continue

        print(f"El resultado de la {operacion} es: {resultado}")

        continuar = input("¿Quieres hacer otra operación? (s/n): ").strip().lower()
        if continuar != "s":
            print("Hasta luego!")
            break

if __name__ == "__main__":
    calculadora()
