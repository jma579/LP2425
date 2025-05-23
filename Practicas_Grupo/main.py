import os
import re
import sys
from colorama import init
from termcolor import colored


init()


DIRECTORIO = os.path.expanduser(".")
sys.path.append(DIRECTORIO)

from Lexer import *

from Parser import *
#from Clases import *

PRACTICA = "02"  # Practica que hay que evaluar
DEBUG = True  # Decir si se lanzan mensajes de debug
NUMLINEAS = 3  # Numero de lineas que se muestran antes y después de la no coincidencia
sys.path.append(DIRECTORIO)
DIR = os.path.join(DIRECTORIO, PRACTICA, "grading")
# Practicas_Grupo_Cool\01\grading\backslash.cool
FICHEROS = os.listdir(DIR)
TESTS = [
    fich
    for fich in FICHEROS
    if os.path.isfile(os.path.join(DIR, fich))
    and re.search(r"^[a-zA-Z].*\.(cool|test|cl)$", fich)
]
TESTS.sort()
#TESTS = ["escapedunprintables.cool"]

if True:
    buenos = 0
    malos = 0
    for fich in TESTS:
        lexer = CoolLexer()
        f = open(os.path.join(DIR, fich), "r", newline="")
        g = open(os.path.join(DIR, fich + ".out"), "r", newline="")
        if os.path.isfile(os.path.join(DIR, fich) + ".nuestro"):
            os.remove(os.path.join(DIR, fich) + ".nuestro")
        if os.path.isfile(os.path.join(DIR, fich) + ".bien"):
            os.remove(os.path.join(DIR, fich) + ".bien")
        texto = ""
        entrada = f.read()
        f.close()
        if PRACTICA == "01":
            texto = "\n\n".join(lexer.salida(entrada))
            texto = f'#name "{fich}"\n' + "\n" + texto
            resultado = g.read()
            g.close()
            if texto.strip().split() != resultado.strip().split():
                print(f"La diferencia(MB) está entre \n{texto.split()}\n y \n{resultado.split()}")
                malos += 1
                print(f"Revisa el fichero {fich}")
                if DEBUG:
                    texto = re.sub(r"#\d+\b", "", texto)
                    resultado = re.sub(r"#\d+\b", "", resultado)
                    nuestro = [linea for linea in texto.split("\n") if linea]
                    bien = [linea for linea in resultado.split("\n") if linea]
                    linea = 0
                    while (
                        nuestro[linea : linea + NUMLINEAS]
                        == bien[linea : linea + NUMLINEAS]
                    ):
                        linea += 1
                    print(
                        colored(
                            "\n".join(nuestro[linea : linea + NUMLINEAS]),
                            "white",
                            "on_red",
                        )
                    )
                    print(
                        colored(
                            "\n".join(bien[linea : linea + NUMLINEAS]),
                            "blue",
                            "on_green",
                        )
                    )
                    f = open(os.path.join(DIR, fich) + ".nuestro", "w")
                    g = open(os.path.join(DIR, fich) + ".bien", "w")
                    f.write(texto.strip())
                    g.write(resultado.strip())
                    f.close()
                    g.close()
            else:
                buenos += 1
        elif PRACTICA in ("02", "03"):
            parser = CoolParser()
            parser.nombre_fichero = fich
            parser.errores = []
            bien = "".join([c for c in g.readlines() if c and "#" not in c])
            bien_total = bien
            g.close()
            j = parser.parse(lexer.tokenize(entrada))
            try:
                # j.Tipo()
                if j and not parser.errores:
                    resultado = "\n\n".join(
                        [c for c in j.str(0).split("\n") if c and "#" not in c]
                    )
                else:
                    resultado = "\n".join(parser.errores)
                    resultado += "\n" + "Compilation halted due to lex and parse errors"
                if resultado.lower().strip().split() != bien.lower().strip().split():
                    malos += 1
                    print(f"Revisa el fichero {fich}")
                    if DEBUG:
                        nuestro = [linea for linea in resultado.split("\n") if linea]
                        bien = [linea for linea in bien.split("\n") if linea]
                        linea = 0
                        while (
                            nuestro[linea : linea + NUMLINEAS]
                            == bien[linea : linea + NUMLINEAS]
                        ):
                            linea += 1
                        print(
                            colored(
                                "\n".join(nuestro[linea : linea + NUMLINEAS]),
                                "white",
                                "on_red",
                            )
                        )
                        print(
                            colored(
                                "\n".join(bien[linea : linea + NUMLINEAS]),
                                "blue",
                                "on_green",
                            )
                        )
                        f = open(os.path.join(DIR, fich) + ".nuestro", "w")
                        g = open(os.path.join(DIR, fich) + ".bien", "w")
                        f.write(resultado.strip())
                        g.write(bien_total.strip())
                        f.close()
                        g.close()
                else:
                    buenos += 1
            except Exception as e:
                malos += 1
                print(f"Lanza excepción en {fich} con el texto {e}")

print(f"Ficheros bien: {buenos} / {buenos + malos}")
