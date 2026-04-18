# Cerradura LR(0) — Calculadora

Implementación en Python de la función **CERRADURA** (Closure) para ítems LR(0), utilizada en el análisis sintáctico ascendente.

> Curso: **Diseño de Lenguajes de Programación**

## Descripción

Este programa calcula la **cerradura** de un conjunto de ítems LR(0) sobre una gramática libre de contexto. La cerradura es una operación fundamental en la construcción de autómatas LR y tablas de análisis sintáctico.

### ¿Qué es un ítem LR(0)?

Un ítem LR(0) es una producción con un punto (`.`) que indica hasta dónde se ha leído la entrada. Por ejemplo:

| Ítem | Significado |
|------|-------------|
| `E -> . E + T` | Aún no hemos leído nada de esta producción |
| `E -> E . + T` | Ya leímos `E`, esperamos `+` |
| `E -> E + T .` | Producción completamente reconocida (ítem de reducción) |

### ¿Qué hace la función CERRADURA?

Dado un conjunto de ítems *I*, la cerradura agrega todos los ítems necesarios cuando el punto está antes de un no-terminal. El algoritmo se repite hasta que no se pueden agregar más ítems.

## Gramáticas incluidas

El programa incluye **3 gramáticas precargadas** listas para probar:

| Opción | Gramática | Producciones |
|--------|-----------|--------------|
| 1 | Gramática 1 | `S -> SS+ \| SS* \| a` |
| 2 | Gramática 2 | `S -> (S) \| ε` |
| 3 | Gramática 3 | `S -> L`, `L -> aL \| a` |

También permite **ingresar gramáticas personalizadas** y probar ítems manualmente.

## Requisitos

- Python 3.6 o superior
- Sin dependencias externas

## Uso

```bash
python cerradura.py
```

Se abrirá un menú interactivo:

```
--- MENU ---
  1. Demo: Gramatica 1 (S -> SS+ | SS* | a)
  2. Demo: Gramatica 2 (S -> (S) | epsilon)
  3. Demo: Gramatica 3 (S -> L, L -> aL | a)
  4. Ingresar mi propia gramatica
  5. Ingresar items manualmente
  0. Salir
```

### Ingresar una gramática propia

Seleccione la opción **4** e ingrese producciones en el formato:

```
A -> B C D
S -> epsilon
```

La gramática se aumenta automáticamente.

### Ingresar ítems manualmente

Seleccione la opción **5** e ingrese ítems con el punto:

```
E -> E . + T
E -> . T
```

## Ejemplo de salida

```
============================================================
CALCULANDO CERRADURA
============================================================

  Items de entrada:
    E' -> . E

  Ronda 1 - Items agregados:
    + E -> . E + T
    + E -> . T

  Ronda 2 - Items agregados:
    + T -> . T * F
    + T -> . F

  Ronda 3 - Items agregados:
    + F -> . ( E )
    + F -> . id

────────────────────────────────────────────────────────────
  CERRADURA COMPLETA (7 items):
────────────────────────────────────────────────────────────
    E -> . E + T
    E -> . T
    E' -> . E
    F -> . ( E )
    F -> . id
    T -> . F
    T -> . T * F
```

## Estructura del proyecto

```
.
└── cerradura.py    # Script principal con toda la implementación
```

## Licencia

Proyecto académico — uso educativo.
