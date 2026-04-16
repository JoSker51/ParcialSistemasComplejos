from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

_id_counter = 0
def nuevo_id():
    global _id_counter
    _id_counter += 1
    return _id_counter

class Puerto:
    def __init__(self, agente: 'Agente'):
        self.id     = nuevo_id()
        self.agente = agente
        self.wire: Optional['Puerto'] = None

    def libre(self) -> bool:
        return self.wire is None

    def __repr__(self):
        destino = f"→P{self.wire.id}[{self.wire.agente.simbolo}]" if self.wire else "libre"
        return f"P{self.id}[{self.agente.simbolo}]({destino})"

    def __hash__(self):   return hash(self.id)
    def __eq__(self, o):  return isinstance(o, Puerto) and self.id == o.id


class Agente:
    def __init__(self, simbolo: str, aridad: int):
        self.simbolo = simbolo
        self.aridad  = aridad
        self.puertos = [Puerto(self) for _ in range(aridad + 1)]

    @property
    def principal(self) -> Puerto:
        return self.puertos[0]

    def aux(self, i: int) -> Puerto:
        assert 1 <= i <= self.aridad
        return self.puertos[i]

    def __repr__(self):
        return f"Agente({self.simbolo})"

def conectar(p1: Puerto, p2: Puerto):
    assert p1.libre(), f"Puerto ocupado: {p1}"
    assert p2.libre(), f"Puerto ocupado: {p2}"
    p1.wire = p2
    p2.wire = p1

def desconectar(p1: Puerto, p2: Puerto):
    assert p1.wire is p2 and p2.wire is p1
    p1.wire = None
    p2.wire = None


class Red:
    def __init__(self):
        self.agentes: list[Agente] = []

    def agregar(self, ag: Agente) -> Agente:
        self.agentes.append(ag)
        return ag

    def remover(self, ag: Agente):
        self.agentes.remove(ag)

    def pares_activos(self) -> list[tuple[Agente, Agente]]:
        """
        Un par activo α ⊳◁ β existe cuando el principal de α
        está conectado al principal de β (Def. 7.2).
        """
        vistos = set()
        pares  = []
        for ag in self.agentes:
            p = ag.principal
            if p.wire is not None:
                vecino = p.wire.agente
                if p.wire is vecino.principal:
                    clave = tuple(sorted([id(ag), id(vecino)]))
                    if clave not in vistos:
                        vistos.add(clave)
                        pares.append((ag, vecino))
        return pares

    def __repr__(self):
        pares  = self.pares_activos()
        libres = [p for ag in self.agentes for p in ag.puertos if p.libre()]
        return (f"Red({len(self.agentes)} agentes | "
                f"{len(pares)} pares activos | "
                f"{len(libres)} puertos libres)")


def construir_numero(n: int, red: Red) -> Agente:
    """
    Construye S^n(0) en la red.
    Devuelve el agente cuyo principal está libre (la "cabeza" del número).
    """
    cero = red.agregar(Agente("0", 0))
    agente_actual = cero

    for _ in range(n):
        s = red.agregar(Agente("S", 1))
        conectar(s.aux(1), agente_actual.principal)
        agente_actual = s

    return agente_actual


def leer_numero(red: Red) -> int:
    return sum(1 for ag in red.agentes if ag.simbolo == "S")


def regla_add_cero(add: Agente, cero: Agente, red: Red):
    puerto_y_cabeza = add.aux(2).wire
    desconectar(add.principal, cero.principal)

    if not add.aux(1).libre():
        otro = add.aux(1).wire
        desconectar(add.aux(1), otro)

    desconectar(add.aux(2), puerto_y_cabeza)

    red.remover(add)
    red.remover(cero)


def regla_add_sucesor(add: Agente, s: Agente, red: Red):

    puerto_x_interior = s.aux(1).wire
    puerto_y_cabeza   = add.aux(2).wire
    puerto_salida     = add.aux(1).wire

    desconectar(add.principal, s.principal)


    desconectar(s.aux(1), puerto_x_interior)


    desconectar(add.aux(2), puerto_y_cabeza)
    if puerto_salida is not None:
        desconectar(add.aux(1), puerto_salida)


    red.remover(add)
    red.remover(s)


    s_nuevo   = red.agregar(Agente("S", 1))
    add_nuevo = red.agregar(Agente("add", 2))

   
    conectar(add_nuevo.aux(2), puerto_y_cabeza)


    conectar(add_nuevo.principal, puerto_x_interior)

    if puerto_salida is not None:
        conectar(s_nuevo.principal, puerto_salida)

def reducir(red: Red, verbose=True) -> None:
    paso = 0
    while True:
        pares = red.pares_activos()
        if not pares:
            break
        alpha, beta = pares[0]
        paso += 1

        clave = tuple(sorted([alpha.simbolo, beta.simbolo]))

        if verbose:
            print(f"  Paso {paso}: {alpha.simbolo} ⊳◁ {beta.simbolo}")

        if clave == ("0", "add"):
            add  = alpha if alpha.simbolo == "add" else beta
            cero = beta  if alpha.simbolo == "add" else alpha
            regla_add_cero(add, cero, red)
            if verbose:
                print(f"    → add(0, y) = y   [caso base]")

        elif clave == ("S", "add"):
            add = alpha if alpha.simbolo == "add" else beta
            s   = beta  if alpha.simbolo == "add" else alpha
            regla_add_sucesor(add, s, red)
            if verbose:
                print(f"    → add(S(x), y) = S(add(x, y))   [caso recursivo]")
                nuevos = red.pares_activos()
                if nuevos:
                    a, b = nuevos[0]
                    print(f"    → Nuevo par activo: {a.simbolo} ⊳◁ {b.simbolo}")

        else:
            if verbose:
                print(f"    → Par bloqueado (sin regla para {clave})")
            break

    if verbose:
        print(f"  ✓ Forma normal en {paso} pasos | {red}")


# ─────────────────────────────────────────────────────────────────────────────
#  PRUEBAS
# ─────────────────────────────────────────────────────────────────────────────

def sumar(x: int, y: int, verbose=True) -> int:
    global _id_counter
    _id_counter = 0

    red = Red()

    cabeza_x = construir_numero(x, red)
    cabeza_y = construir_numero(y, red)

    add = red.agregar(Agente("add", 2))

    conectar(add.aux(2), cabeza_y.principal)

    conectar(add.principal, cabeza_x.principal)

    if verbose:
        print(f"\n{'='*55}")
        print(f"  add(S^{x}(0), S^{y}(0))  →*  S^{x+y}(0)   [{x} + {y}]")
        print(f"{'='*55}")
        print(f"  {red}")

    reducir(red, verbose)

    resultado = leer_numero(red)
    esperado  = x + y

    simbolos = [ag.simbolo for ag in red.agentes]
    if verbose:
        print(f"  Agentes restantes: {simbolos}")
        print(f"  Resultado: S^{resultado}(0)  {'✓' if resultado == esperado else f'✗ esperado {esperado}'}\n")

    return resultado


if __name__ == "__main__":
    casos = [(1, 1), (2, 3), (0, 4), (3, 0), (2, 2)]
    todos_ok = True
    for x, y in casos:
        r = sumar(x, y, verbose=True)
        if r != x + y:
            todos_ok = False
    print("=" * 55)
    print(f"  {'Todos los casos correctos' if todos_ok else 'Hay errores'}")
