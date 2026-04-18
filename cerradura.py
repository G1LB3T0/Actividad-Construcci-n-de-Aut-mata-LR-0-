"""
Implementacion de la funcion CERRADURA (Closure) para items LR(0)
Curso: Diseno de Lenguajes de Programacion

Solo implementa la funcion CERRADURA.
NO implementa la funcion GOTO (Ir_A).
"""


# ============================================================
# REPRESENTACION DE ITEMS LR(0)
# ============================================================
# Un item LR(0) es una produccion con un punto (.) que indica
# hasta donde hemos leido.
#
# Internamente se representa como una tupla:
#   (no_terminal, (simbolo1, simbolo2, ...), posicion_del_punto)
#
# Ejemplos:
#   E -> . E + T   se guarda como  ("E", ("E", "+", "T"), 0)
#   E -> E . + T   se guarda como  ("E", ("E", "+", "T"), 1)
#   E -> E + T .   se guarda como  ("E", ("E", "+", "T"), 3)
#   S -> .         se guarda como  ("S", (), 0)  (produccion epsilon)
# ============================================================


def crear_item(no_terminal, produccion, posicion_punto):
    """
    Crea un item LR(0).
    Retorna una tupla inmutable (para poder usar en conjuntos).
    """
    return (no_terminal, tuple(produccion), posicion_punto)


def obtener_simbolo_despues_del_punto(item):
    """
    Retorna el simbolo que esta inmediatamente despues del punto.
    Si el punto esta al final, retorna None (item de reduccion).

    Ejemplo:
        E -> E . + T  -->  retorna "+"
        E -> E + T .  -->  retorna None
    """
    no_terminal, produccion, posicion = item
    if posicion < len(produccion):
        return produccion[posicion]
    return None


def es_no_terminal(simbolo, gramatica):
    """
    Un simbolo es no-terminal si aparece como lado izquierdo
    en alguna produccion de la gramatica.
    """
    return simbolo in gramatica


def formatear_item(item):
    """
    Convierte un item a formato legible con el punto.
    Ejemplo: ("E", ("E", "+", "T"), 1) --> "E -> E . + T"
    """
    no_terminal, produccion, posicion = item
    if len(produccion) == 0:
        return f"{no_terminal} -> ."
    simbolos = list(produccion)
    simbolos_con_punto = simbolos[:posicion] + ["."] + simbolos[posicion:]
    return f"{no_terminal} -> {' '.join(simbolos_con_punto)}"


# ============================================================
# FUNCION CERRADURA (CLOSURE)
# ============================================================
# Algoritmo (tal como se ve en clase):
#
#   ConjuntoDeElementos CERRADURA(I) {
#       J = I;
#       repeat
#           for (cada elemento A -> alpha . B beta en J)
#               for (cada produccion B -> gamma de G)
#                   if (B -> . gamma no esta en J)
#                       agregar B -> . gamma a J;
#       until no se agreguen mas elementos a J en una ronda;
#       return J;
#   }
# ============================================================

def cerradura(items_iniciales, gramatica):
    """
    Calcula la cerradura (closure) de un conjunto de items LR(0).

    Parametros:
        items_iniciales: lista de items de entrada
        gramatica: diccionario con la gramatica

    Retorna:
        Conjunto (set) con todos los items de la cerradura completa
    """
    # Paso 1: J = I (empezamos con los items de entrada)
    resultado = set(items_iniciales)

    print("\n" + "=" * 60)
    print("CALCULANDO CERRADURA")
    print("=" * 60)
    print("\n  Items de entrada:")
    for item in items_iniciales:
        print(f"    {formatear_item(item)}")

    # Paso 2: Repetir hasta que no se agreguen mas items
    ronda = 0
    hubo_cambio = True

    while hubo_cambio:
        hubo_cambio = False
        ronda += 1
        nuevos_en_ronda = []

        # Para cada item en el conjunto actual
        for item in list(resultado):
            # Ver que simbolo esta despues del punto
            simbolo = obtener_simbolo_despues_del_punto(item)

            # Si es un no-terminal B, agregar todas sus producciones
            if simbolo is not None and es_no_terminal(simbolo, gramatica):
                for produccion in gramatica[simbolo]:
                    nuevo = crear_item(simbolo, produccion, 0)
                    if nuevo not in resultado:
                        resultado.add(nuevo)
                        nuevos_en_ronda.append(nuevo)
                        hubo_cambio = True

        # Mostrar que se agrego en esta ronda
        if nuevos_en_ronda:
            print(f"\n  Ronda {ronda} - Items agregados:")
            for item in nuevos_en_ronda:
                print(f"    + {formatear_item(item)}")

    if ronda == 1 and not any(obtener_simbolo_despues_del_punto(i) is not None
                              and es_no_terminal(obtener_simbolo_despues_del_punto(i), gramatica)
                              for i in items_iniciales):
        print("\n  No se agregaron items (el punto no esta antes de un no-terminal).")

    # Mostrar resultado final
    print(f"\n{'─' * 60}")
    print(f"  CERRADURA COMPLETA ({len(resultado)} items):")
    print(f"{'─' * 60}")
    items_ordenados = sorted(resultado, key=lambda x: (x[0], x[1], x[2]))
    for item in items_ordenados:
        marcador = ""
        if obtener_simbolo_despues_del_punto(item) is None:
            marcador = "  <-- item de reduccion"
        print(f"    {formatear_item(item)}{marcador}")
    print()

    return resultado


# ============================================================
# GRAMATICAS PRECARGADAS
# ============================================================




def gramatica_1():
    """
    Gramatica 1 (aumentada):
    S' -> S
    S  -> S S + | S S * | a
    """
    return {
        "S'": [["S"]],
        "S":  [["S", "S", "+"], ["S", "S", "*"], ["a"]],
    }


def gramatica_2():
    """
    Gramatica 2 (aumentada):
    S' -> S
    S  -> ( S ) | epsilon
    """
    return {
        "S'": [["S"]],
        "S":  [["(", "S", ")"], []],
    }


def gramatica_3():
    """
    Gramatica 3 (aumentada):
    S' -> S
    S  -> L
    L  -> a L | a
    """
    return {
        "S'": [["S"]],
        "S":  [["L"]],
        "L":  [["a", "L"], ["a"]],
    }


# ============================================================
# INGRESO DE GRAMATICA MANUAL
# ============================================================

def ingresar_gramatica():
    """Permite al usuario ingresar una gramatica desde teclado."""
    print("\n" + "=" * 60)
    print("  INGRESAR GRAMATICA")
    print("=" * 60)
    print("  Formato: A -> B C D")
    print("  Para epsilon: S -> epsilon")
    print("  Escriba 'fin' cuando termine")
    print()

    gramatica = {}
    simbolo_inicial = None

    while True:
        entrada = input("  Produccion (o 'fin'): ").strip()
        if entrada.lower() == 'fin':
            break
        if '->' not in entrada:
            print("    Error: use el formato A -> B C D")
            continue

        partes = entrada.split('->')
        nt = partes[0].strip()
        derecha = partes[1].strip()

        if simbolo_inicial is None:
            simbolo_inicial = nt

        produccion = [] if derecha.lower() in ('epsilon', '') else derecha.split()

        if nt not in gramatica:
            gramatica[nt] = []
        gramatica[nt].append(produccion)

    if not gramatica:
        print("  No se ingresaron producciones.")
        return None

    # Aumentar la gramatica automaticamente
    sim_aum = simbolo_inicial + "'"
    gramatica[sim_aum] = [[simbolo_inicial]]

    print(f"\n  Gramatica aumentada ({sim_aum} -> {simbolo_inicial}):")
    for nt, prods in gramatica.items():
        for prod in prods:
            print(f"    {nt} -> {' '.join(prod) if prod else 'epsilon'}")

    return gramatica


# ============================================================
# INGRESO DE ITEMS MANUAL
# ============================================================

def ingresar_items():
    """Permite al usuario ingresar items con el punto en cualquier posicion."""
    print("\n  Ingrese items en formato: E -> E . + T")
    print("  Para item epsilon: S -> .")
    print("  Escriba 'fin' cuando termine\n")

    items = []
    while True:
        entrada = input("  Item (o 'fin'): ").strip()
        if entrada.lower() == 'fin':
            break
        if '->' not in entrada:
            print("    Error: use el formato A -> alpha . beta")
            continue

        partes = entrada.split('->')
        nt = partes[0].strip()
        derecha = partes[1].strip().split()

        if '.' not in derecha:
            print("    Error: debe incluir el punto (.)")
            continue

        posicion = derecha.index('.')
        simbolos = [s for s in derecha if s != '.']
        item = crear_item(nt, simbolos, posicion)
        items.append(item)
        print(f"    OK: {formatear_item(item)}")

    return items


# ============================================================
# MOSTRAR GRAMATICA
# ============================================================

def mostrar_gramatica(gramatica):
    """Imprime la gramatica de forma clara."""
    print("\n  Producciones:")
    for nt in gramatica:
        for prod in gramatica[nt]:
            print(f"    {nt} -> {' '.join(prod) if prod else 'epsilon'}")
    print()


# ============================================================
# DEMOSTRACIONES CON ITEMS EN DISTINTAS POSICIONES
# ============================================================




def demo_gramatica_problema(gramatica, nombre):
    """
    Demuestra la cerradura con una gramatica del problema 1,
    probando items con el punto en distintas posiciones.
    """
    print("\n" + "#" * 60)
    print(f"  DEMO: {nombre}")
    print("#" * 60)
    mostrar_gramatica(gramatica)

    # Encontrar simbolo aumentado
    sim_aum = None
    for nt in gramatica:
        if nt.endswith("'"):
            sim_aum = nt
            break

    # Prueba 1: Item inicial
    prod_inicial = gramatica[sim_aum][0]
    print(f"--- Prueba 1: {sim_aum} -> . {' '.join(prod_inicial)}")
    print("    Punto al inicio (posicion 0)")
    cerradura([crear_item(sim_aum, prod_inicial, 0)], gramatica)

    # Pruebas adicionales: buscar producciones interesantes
    prueba_num = 2
    items_probados = set()

    for nt in gramatica:
        if nt.endswith("'"):
            continue
        for prod in gramatica[nt]:
            # Probar con punto en cada posicion posible
            for pos in range(len(prod) + 1):
                item = crear_item(nt, prod, pos)
                item_str = formatear_item(item)

                # Evitar duplicados y limitar cantidad
                if item_str in items_probados or prueba_num > 4:
                    continue

                # Elegir items interesantes:
                # - punto antes de no-terminal (causa expansion)
                # - punto al final (item de reduccion)
                simbolo = obtener_simbolo_despues_del_punto(item)
                es_interesante = (
                    (simbolo is not None and es_no_terminal(simbolo, gramatica)) or
                    (simbolo is None and pos > 0)
                )

                if es_interesante:
                    items_probados.add(item_str)
                    if simbolo is not None:
                        print(f"\n--- Prueba {prueba_num}: {item_str}")
                        print(f"    Punto en posicion {pos}, antes de '{simbolo}' (no-terminal)")
                    else:
                        print(f"\n--- Prueba {prueba_num}: {item_str}")
                        print(f"    Punto al final (item de reduccion)")
                    cerradura([item], gramatica)
                    prueba_num += 1

            if prueba_num > 4:
                break
        if prueba_num > 4:
            break


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu():
    print("\n" + "=" * 60)
    print("  CERRADURA LR(0) - Calculadora")
    print("  Diseno de Lenguajes de Programacion")
    print("=" * 60)

    gramatica_actual = None

    while True:
        print("\n--- MENU ---")
        print("  1. Demo: Gramatica 1 (S -> SS+ | SS* | a)")
        print("  2. Demo: Gramatica 2 (S -> (S) | epsilon)")
        print("  3. Demo: Gramatica 3 (S -> L, L -> aL | a)")
        print("  4. Ingresar mi propia gramatica")
        print("  5. Ingresar items manualmente")
        print("  0. Salir")

        opcion = input("\n  Opcion: ").strip()

        if opcion == '0':
            print("\n  Fin del programa.\n")
            break

        elif opcion == '1':
            gramatica_actual = gramatica_1()
            demo_gramatica_problema(gramatica_actual, "Gramatica 1: S -> SS+ | SS* | a")

        elif opcion == '2':
            gramatica_actual = gramatica_2()
            demo_gramatica_problema(gramatica_actual, "Gramatica 2: S -> (S) | epsilon")

        elif opcion == '3':
            gramatica_actual = gramatica_3()
            demo_gramatica_problema(gramatica_actual, "Gramatica 3: S -> L, L -> aL | a")

        elif opcion == '4':
            gramatica_actual = ingresar_gramatica()
            if gramatica_actual:
                print("\n  Gramatica guardada. Use opcion 5 para probar items.")

        elif opcion == '5':
            if gramatica_actual is None:
                print("\n  Primero seleccione o ingrese una gramatica (opciones 1-4)")
                continue
            print("\n  Gramatica actual:")
            mostrar_gramatica(gramatica_actual)
            items = ingresar_items()
            if items:
                cerradura(items, gramatica_actual)

        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    menu()
