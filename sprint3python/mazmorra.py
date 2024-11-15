from heroe import Heroe
from monstruo import Monstruo
from tesoro import Tesoro

class Mazmorra:
    def __init__(self, heroe):
        self.heroe = heroe
        self.monstruos = [
            Monstruo("Goblin", 8, 3, 20),
            Monstruo("Orco", 12, 5, 30),
            Monstruo("Dragón", 20, 10, 50)
        ]
        self.tesoro = Tesoro()

    def jugar(self):
        print("Héroe entra en la mazmorra.")
        for monstruo in self.monstruos:
            print(f"Te has encontrado con un {monstruo.nombre}.")
            self.enfrentar_enemigo(monstruo)
            if not self.heroe.esta_vivo():
                print("Héroe ha sido derrotado en la mazmorra.")
                return
            self.buscar_tesoro()
        print(f"¡{self.heroe.nombre} ha derrotado a todos los monstruos y ha conquistado la mazmorra!")

    def enfrentar_enemigo(self, enemigo):
        while enemigo.esta_vivo() and self.heroe.esta_vivo():
            print("¿Qué deseas hacer?")
            print("1. Atacar")
            print("2. Defender")
            print("3. Curarse")
            accion = input("Elige una opción: ")
            if accion == "1":
                self.heroe.atacar(enemigo)
            elif accion == "2":
                self.heroe.defenderse()
            elif accion == "3":
                self.heroe.curarse()
            else:
                print("Opción no válida.")
                continue
            if enemigo.esta_vivo():
                enemigo.atacar(self.heroe)
            self.heroe.reset_defensa()

    def buscar_tesoro(self):
        print("Buscando tesoro...")
        self.tesoro.encontrar_tesoro(self.heroe)
