from __future__ import annotations
from typing      import NamedTuple, Optional, Callable, FrozenSet, Dict, Tuple
from itertools   import count
from functools   import reduce


class Puerto(NamedTuple):
    """
    Identificador de un puerto: (id_agente, indice_puerto).
    índice 0 = principal; 1..n = auxiliares.
    Inmutable por diseño: los puertos no cambian, las conexiones sí
    (como parte de una nueva Red).
    """
    id_agente: int
    indice:    int

class Agente(NamedTuple):
    """Nodo de la red: símbolo + aridad. Inmutable."""
    id:      int
    simbolo: str
    aridad:  int

    @property
    def principal(self) -> Puerto:
        return Puerto(self.id, 0)

    def aux(self, i: int) -> Puerto:
        assert 1 <= i <= self.aridad
        return Puerto(self.id, i)

# Un Wire es un par no ordenado de puertos (frozenset de 2 elementos).
Wire = FrozenSet[Puerto]

def wire(p1: Puerto, p2: Puerto) -> Wire:
    return frozenset({p1, p2})

def otro_extremo(w: Wire, p: Puerto) -> Puerto:
    """Dado un alambre y uno de sus extremos, devuelve el otro."""
    return next(q for q in w if q != p)

class Red(NamedTuple):
    """
    Una red es un par (agentes, alambres), ambos inmutables.
    Toda 'modificación' devuelve una nueva Red.
    """
    agentes:  Tuple[Agente, ...]
    alambres: FrozenSet[Wire]


    def agente_por_id(self, id_: int) -> Optional[Agente]:
        return next((a for a in self.agentes if a.id == id_), None)

    def alambre_en(self, p: Puerto) -> Optional[Wire]:
        """Devuelve el alambre que contiene el puerto p, o None."""
        return next((w for w in self.alambres if p in w), None)

    def conectado_a(self, p: Puerto) -> Optional[Puerto]:
        """Puerto al que está conectado p, o None si está libre."""
        w = self.alambre_en(p)
        return otro_extremo(w, p) if w else None

    def pares_activos(self) -> Tuple[Tuple[Agente, Agente], ...]:
        vistos: set = set()
        pares  = []
        for ag in self.agentes:
            vecino_puerto = self.conectado_a(ag.principal)
            if vecino_puerto is None:
                continue
            if vecino_puerto.indice != 0:          # no es un principal
                continue
            vecino = self.agente_por_id(vecino_puerto.id_agente)
            clave  = frozenset({ag.id, vecino.id})
            if clave not in vistos:
                vistos.add(clave)
                pares.append((ag, vecino))
        return tuple(pares)

    def leer_numero(self) -> int:
        return sum(1 for ag in self.agentes if ag.simbolo == "S")

    # ── Transformaciones puras (devuelven Red nueva) ─────────────────────────

    def con_agentes(self, agentes: Tuple[Agente, ...]) -> Red:
        return Red(agentes, self.alambres)

    def con_alambres(self, alambres: FrozenSet[Wire]) -> Red:
        return Red(self.agentes, alambres)

    def agregar_agente(self, ag: Agente) -> Red:
        return Red(self.agentes + (ag,), self.alambres)

    def remover_agentes(self, ids: FrozenSet[int]) -> Red:
        nuevos_ags = tuple(a for a in self.agentes if a.id not in ids)
        nuevos_wrs = frozenset(
            w for w in self.alambres
            if not any(p.id_agente in ids for p in w)
        )
        return Red(nuevos_ags, nuevos_wrs)

    def conectar(self, p1: Puerto, p2: Puerto) -> Red:
        return Red(self.agentes, self.alambres | {wire(p1, p2)})

    def desconectar_puerto(self, p: Puerto) -> Red:
        return Red(self.agentes, frozenset(w for w in self.alambres if p not in w))

    def __repr__(self):
        return (f"Red({len(self.agentes)} agentes | "
                f"{len(self.pares_activos())} pares activos | "
                f"{len(self.alambres)} alambres)")




def nuevo_generador() -> Callable[[], int]:
    gen = count(1)
    return lambda: next(gen)


def construir_numero(n: int, gen_id: Callable[[], int]) -> Tuple[Red, Agente]:

    cero = Agente(gen_id(), "0", 0)
    red  = Red((cero,), frozenset())

    def paso(estado: Tuple[Red, Agente], _) -> Tuple[Red, Agente]:
        red_actual, cabeza = estado
        s      = Agente(gen_id(), "S", 1)
        nueva  = red_actual.agregar_agente(s).conectar(s.aux(1), cabeza.principal)
        return (nueva, s)

    red_final, cabeza_final = reduce(paso, range(n), (red, cero))
    return red_final, cabeza_final



def regla_add_cero(red: Red, add: Agente, cero: Agente) -> Red:

    puerto_y = red.conectado_a(add.aux(2))

    red2 = red.remover_agentes(frozenset({add.id, cero.id}))

    return red2

def regla_add_sucesor(red: Red, add: Agente, s: Agente, gen_id: Callable[[], int]) -> Red:

    puerto_x_interior = red.conectado_a(s.aux(1))       
    puerto_y          = red.conectado_a(add.aux(2))      
    puerto_salida     = red.conectado_a(add.aux(1))      

    red2 = red.remover_agentes(frozenset({add.id, s.id}))

    
    s_nuevo   = Agente(gen_id(), "S",   1)
    add_nuevo = Agente(gen_id(), "add", 2)

    red3 = red2.agregar_agente(s_nuevo).agregar_agente(add_nuevo)

  
    red3 = red3.conectar(add_nuevo.principal, puerto_x_interior)
    red3 = red3.conectar(add_nuevo.aux(2),    puerto_y)
    if puerto_salida is not None:
        red3 = red3.conectar(s_nuevo.principal, puerto_salida)

    return red3

def regla_erase(red: Red, epsilon: Agente, alpha: Agente, gen_id: Callable[[], int]) -> Red:

    puertos_aux = [red.conectado_a(alpha.aux(i)) for i in range(1, alpha.aridad + 1)]

    red2 = red.remover_agentes(frozenset({epsilon.id, alpha.id}))

    def colocar_epsilon(r: Red, p: Optional[Puerto]) -> Red:
        if p is None:
            return r
        eps = Agente(gen_id(), "ε", 0)
        return r.agregar_agente(eps).conectar(eps.principal, p)

    return reduce(colocar_epsilon, puertos_aux, red2)


Regla = Callable[[Red, Agente, Agente], Red]

def construir_sistema(gen_id: Callable[[], int]) -> Dict[FrozenSet[str], Regla]:

    return {
        frozenset({"add", "0"}): lambda red, a, b: (
            regla_add_cero(red, a if a.simbolo == "add" else b,
                                b if a.simbolo == "add" else a)
        ),
        frozenset({"add", "S"}): lambda red, a, b: (
            regla_add_sucesor(red, a if a.simbolo == "add" else b,
                                   b if a.simbolo == "add" else a, gen_id)
        ),
        frozenset({"ε", "0"}):   lambda red, a, b: (
            regla_erase(red, a if a.simbolo == "ε" else b,
                             b if a.simbolo == "ε" else a, gen_id)
        ),
        frozenset({"ε", "S"}):   lambda red, a, b: (
            regla_erase(red, a if a.simbolo == "ε" else b,
                             b if a.simbolo == "ε" else a, gen_id)
        ),
    }

def paso_reduccion(red: Red, sistema: Dict[FrozenSet[str], Regla],
                   verbose: bool) -> Optional[Red]:
    pares = red.pares_activos()
    if not pares:
        return None

    alpha, beta = pares[0]
    clave = frozenset({alpha.simbolo, beta.simbolo})
    regla = sistema.get(clave)

    if regla is None:
        if verbose:
            print(f"    → Par bloqueado: {alpha.simbolo} ⊳◁ {beta.simbolo}")
        return None

    if verbose:
        print(f"  Interacción: {alpha.simbolo} ⊳◁ {beta.simbolo}")

    return regla(red, alpha, beta)

def reducir(red: Red, sistema: Dict[FrozenSet[str], Regla],
            verbose: bool = True) -> Red:
    paso = 0
    while True:
        resultado = paso_reduccion(red, sistema, verbose)
        if resultado is None:
            if verbose:
                print(f"  ✓ Forma normal en {paso} pasos | {red}")
            return red
        red   = resultado
        paso += 1


def sumar(x: int, y: int, verbose: bool = True) -> int:
    gen_id  = nuevo_generador()
    sistema = construir_sistema(gen_id)

    red_x, cabeza_x = construir_numero(x, gen_id)
    red_y, cabeza_y = construir_numero(y, gen_id)

    # Unir las dos redes
    red = Red(red_x.agentes + red_y.agentes,
              red_x.alambres | red_y.alambres)

    # Agregar el agente add y conectarlo
    add = Agente(gen_id(), "add", 2)
    red = (red
           .agregar_agente(add)
           .conectar(add.principal, cabeza_x.principal)
           .conectar(add.aux(2),    cabeza_y.principal))

    if verbose:
        print(f"\n{'='*55}")
        print(f"  add(S^{x}(0), S^{y}(0))  →*  S^{x+y}(0)   [{x} + {y}]")
        print(f"{'='*55}")
        print(f"  {red}")

    red_normal = reducir(red, sistema, verbose)
    resultado  = red_normal.leer_numero()
    esperado   = x + y

    if verbose:
        simbolos = [ag.simbolo for ag in red_normal.agentes]
        print(f"  Agentes restantes: {simbolos}")
        print(f"  Resultado: S^{resultado}(0)  "
              f"{'✓' if resultado == esperado else f'✗ esperado {esperado}'}\n")

    return resultado

def multiplicar(x: int, y: int, verbose: bool = True) -> int:
    resultado = reduce(lambda acc, _: sumar(acc, y, verbose=False), range(x), 0)

    if verbose:
        print(f"\n{'='*55}")
        print(f"  mult(S^{x}(0), S^{y}(0))  →*  S^{x*y}(0)   [{x} × {y}]")
        print(f"{'='*55}")
        esperado = x * y
        print(f"  Resultado: S^{resultado}(0)  "
              f"{'✓' if resultado == esperado else f'✗ esperado {esperado}'}\n")

    return resultado



if __name__ == "__main__":
    casos_suma = [(1, 1), (2, 3), (0, 4), (3, 0), (2, 2)]
    todos_ok   = all(sumar(x, y, verbose=True) == x + y for x, y in casos_suma)
    print("=" * 55)
    print(f"  {'Todos los casos de suma correctos' if todos_ok else 'Hay errores en la suma'}")

    print("\n" + "=" * 55)
    print("  MULTIPLICACIÓN DESDE LA SUMA")
    print("=" * 55)
    casos_mult = [(2, 3), (3, 3), (0, 5), (4, 1)]
    for x, y in casos_mult:
        multiplicar(x, y, verbose=True)