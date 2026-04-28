# Parcial 2 — Sistemas Complejos

Jose Santiago Gonzalez Enriquez

---

## Punto 1 — Complejidad de Internet: Entropía de Shannon

Internet es un sistema complejo: millones de nodos intercambian tráfico de manera impredecible, interdependiente y a una escala que crece sin límite. Para demostrar esa complejidad formalmente se usa la **Entropía de Shannon** como métrica central, que cuantifica qué tan impredecible o distribuido es el tráfico en la red.
H(X) = −∑ pᵢ · log₂(pᵢ)

Donde `pᵢ` es la probabilidad de que el tráfico se dirija al nodo `i` (router/servidor).

### Argumento: tres condiciones de complejidad

El modelo no solo calcula entropía — la usa para verificar formalmente que Internet satisface las condiciones de un sistema complejo. Se proponen tres condiciones medibles:

**Condición 1 — Alta entropía estructural (`C > 0.6`)**

Se define la complejidad normalizada como:
C = H(X) / H_max,    donde H_max = log₂(n)

Si el tráfico estuviera concentrado en un solo nodo, `H → 0` y el sistema sería trivialmente predecible. En operación normal (distribución Zipf, que es la distribución real del tráfico en Internet), `C ≈ 92%`, muy por encima del umbral. Un ataque DDoS colapsa `C` a ~5%, eliminando la complejidad. Esto demuestra que la complejidad de Internet es una propiedad del estado distribuido de la red, no una característica fija.

**Condición 2 — Interdependencia entre nodos (`I(X;Y) > 0`)**

Si los nodos fueran independientes, conocer el estado de uno no diría nada sobre el estado de otro. La **información mutua** mide exactamente eso:
I(X;Y) = H(X) − H(X|Y)

Un valor `I(X;Y) > 0` demuestra que los nodos están acoplados: el tráfico en un router informa sobre el tráfico en sus vecinos. Esto es interdependencia estructural, una propiedad definitoria de los sistemas complejos. El modelo la calcula sobre una matriz de probabilidad conjunta entre nodos vecinos.

**Condición 3 — Escalabilidad ilimitada de la complejidad**

La entropía máxima crece logarítmicamente con el número de nodos:
H_max(n) = log₂(n)

Para una LAN de 10 nodos, `H_max ≈ 3.32 bits`. Para un fragmento de 200 nodos, `H_max ≈ 7.64 bits`. Para los ~5×10⁹ dispositivos activos en Internet, `H_max > 32 bits`. Esto significa que la complejidad potencial de Internet no tiene techo práctico — crece cada vez que un nuevo dispositivo se conecta. La complejidad no es accidental: está **garantizada estructuralmente** por la escala de la red.

### Las tres condiciones se verifican computacionalmente

El script evalúa las tres condiciones y emite un veredicto explícito. Las tres se cumplen bajo operación normal, confirmando que Internet es un sistema complejo bajo el modelo de Shannon.

### Escenarios simulados

| Escenario | Descripción | Entropía | Complejidad C |
|---|---|---|---|
| Uniforme | Tráfico perfectamente distribuido | Máxima | 100% |
| Normal (Zipf) | Distribución realista de Internet | Alta | ~92% |
| Congestión | Pocos nodos concentran el tráfico | Media | ~65% |
| DDoS | Un nodo recibe el 95% del tráfico | Mínima | ~5% |

Los escenarios de degradación (congestión, DDoS) no son solo ilustrativos: muestran que la complejidad de Internet puede **colapsar** cuando la distribución del tráfico se rompe, lo que refuerza que la entropía es un indicador real del estado del sistema.

**Gráficos generados:** `shannon_internet.png`, `entropia_vs_nodos.png`

---

## Punto 2 — Suma y multiplicación desde la función sucesor

Implementación de aritmética básica partiendo únicamente de la **función sucesor** `S(n) = n + 1`, siguiendo la construcción de los **Números de Peano**.

- **Suma:** aplicar `S` b veces sobre a → `a + b = S(S(...S(a)...))`
- **Multiplicación:** sumar `a` consigo mismo `b` veces → `a × b = a + a + ... + a`

Esto ilustra cómo comportamientos complejos (operaciones aritméticas) emergen de una regla primitiva simple.

---

## Punto 3 — Interacción con Net Interactions

Fundamento matemático: ¿qué es una red de interacción?
Una red de interacción es un modelo de computación gráfico. La computación
ocurre mediante agentes conectados por alambres que se transforman
localmente siguiendo reglas. No hay memoria global ni secuencia de
instrucciones: solo interacciones locales entre pares de agentes.
Formalmente (Def. 7.1), cada símbolo de la red tiene una aridad fija.
Un agente con aridad n tiene exactamente n + 1 puertos: un
puerto principal y n puertos auxiliares.


Tipos de datos inmutables
pythonclass Puerto(NamedTuple):
    id_agente: int
    indice:    int   # 0 = principal; 1..n = auxiliar

class Agente(NamedTuple):
    id:      int
    simbolo: str
    aridad:  int

    @property
    def principal(self) -> Puerto:
        return Puerto(self.id, 0)

    def aux(self, i: int) -> Puerto:
        return Puerto(self.id, i)
Un Wire (alambre) es un frozenset de dos puertos, inmutable y sin orden:
pythonWire = FrozenSet[Puerto]

def wire(p1: Puerto, p2: Puerto) -> Wire:
    return frozenset({p1, p2})
La Red es también inmutable. Toda "modificación" devuelve una nueva instancia:
pythonclass Red(NamedTuple):
    agentes:  Tuple[Agente, ...]
    alambres: FrozenSet[Wire]

    def conectar(self, p1: Puerto, p2: Puerto) -> Red:
        return Red(self.agentes, self.alambres | {wire(p1, p2)})

    def remover_agentes(self, ids: FrozenSet[int]) -> Red:
        nuevos_ags = tuple(a for a in self.agentes if a.id not in ids)
        nuevos_wrs = frozenset(
            w for w in self.alambres
            if not any(p.id_agente in ids for p in w)
        )
        return Red(nuevos_ags, nuevos_wrs)

El concepto de Interacción
Par activo (Def. 7.2)
Un par activo α ⊳◁ β existe cuando el puerto principal de α está
conectado directamente al puerto principal de β. Es la unidad mínima de
computación: el análogo funcional de un redex.

    pythondef pares_activos(self) -> Tuple[Tuple[Agente, Agente], ...]:
    for ag in self.agentes:
        vecino_puerto = self.conectado_a(ag.principal)
        if vecino_puerto is None:
            continue
        if vecino_puerto.indice != 0:      # solo principal ↔ principal
            continue
        vecino = self.agente_por_id(vecino_puerto.id_agente)
        ...

La interacción ocurre única y exclusivamente entre puertos principales.
Cualquier otra conexión convive en la red sin generar computación.


Las reglas como funciones de primera clase
Las reglas de interacción (Def. 7.3) son funciones puras almacenadas
en un diccionario. El par de símbolos (un frozenset, no ordenado) es la clave.
Esto garantiza la segunda condición del libro: a lo más una regla por par.

    pythondef construir_sistema(gen_id: Callable[[], int]) -> Dict[FrozenSet[str], Regla]:
    return {
        frozenset({"add", "0"}): lambda red, a, b: regla_add_cero(...),
        frozenset({"add", "S"}): lambda red, a, b: regla_add_sucesor(...),
        frozenset({"ε",   "0"}): lambda red, a, b: regla_erase(...),
        frozenset({"ε",   "S"}): lambda red, a, b: regla_erase(...),
    }
Cada regla es una función (Red, Agente, Agente) → Red: recibe una red
inmutable y devuelve una red nueva, sin tocar la original.
Regla 1 — caso base: add ⊳◁ 0
add(0, y) = y
pythondef regla_add_cero(red: Red, add: Agente, cero: Agente) -> Red:
    return red.remover_agentes(frozenset({add.id, cero.id}))
Los agentes add y 0 desaparecen. La red resultante expone el argumento
y intacto, preservando la interfaz (condición 1 de Def. 7.3).
Regla 2 — caso recursivo: add ⊳◁ S
add(S(x), y) = S(add(x, y))

    pythondef regla_add_sucesor(red: Red, add: Agente, s: Agente,
                      gen_id: Callable[[], int]) -> Red:
    puerto_x_interior = red.conectado_a(s.aux(1))
    puerto_y          = red.conectado_a(add.aux(2))
    puerto_salida     = red.conectado_a(add.aux(1))

    red2 = red.remover_agentes(frozenset({add.id, s.id}))

    s_nuevo   = Agente(gen_id(), "S",   1)
    add_nuevo = Agente(gen_id(), "add", 2)

    return (red2
            .agregar_agente(s_nuevo)
            .agregar_agente(add_nuevo)
            .conectar(add_nuevo.principal, puerto_x_interior)
            .conectar(add_nuevo.aux(2),    puerto_y)
            .conectar(s_nuevo.principal,   puerto_salida))
El estilo encadenado (.agregar().conectar().conectar()) es posible porque
cada método devuelve una nueva Red, nunca muta la existente.
Agente ε — borrador (Ejemplo 7.5)

    pythondef regla_erase(red: Red, epsilon: Agente, alpha: Agente,
                gen_id: Callable[[], int]) -> Red:
    puertos_aux = [red.conectado_a(alpha.aux(i)) for i in range(1, alpha.aridad + 1)]
    red2 = red.remover_agentes(frozenset({epsilon.id, alpha.id}))

    def colocar_epsilon(r: Red, p: Optional[Puerto]) -> Red:
        if p is None:
            return r
        eps = Agente(gen_id(), "ε", 0)
        return r.agregar_agente(eps).conectar(eps.principal, p)

    return reduce(colocar_epsilon, puertos_aux, red2)
El uso de reduce aquí expresa directamente la semántica: "para cada puerto
auxiliar de α, acumular un nuevo ε en la red".

El ciclo de reducción
La reducción (Def. 7.3) es una función pura que aplica pasos hasta alcanzar
la forma normal. paso_reduccion consulta el diccionario de reglas y devuelve
None si ya no hay pares activos:

    pythondef paso_reduccion(red, sistema, verbose) -> Optional[Red]:
    pares = red.pares_activos()
    if not pares:
        return None                        # forma normal
    alpha, beta = pares[0]
    regla = sistema.get(frozenset({alpha.simbolo, beta.simbolo}))
    return regla(red, alpha, beta) if regla else None

    def reducir(red, sistema, verbose=True) -> Red:
    paso = 0
    while True:
        resultado = paso_reduccion(red, sistema, verbose)
        if resultado is None:
            return red                     # forma normal alcanzada
        red  = resultado
        paso += 1
La Proposición 7.4 garantiza que esta forma normal es única: sin
importar el orden en que se reduzcan los pares, el resultado es siempre
el mismo (confluencia fuerte).

Construcción de números con reduce
Los números naturales se representan como S^n(0). La construcción usa
reduce de forma explícita, sin bucles mutables:

    pythondef construir_numero(n: int, gen_id: Callable[[], int]) -> Tuple[Red, Agente]:
    cero = Agente(gen_id(), "0", 0)
    red  = Red((cero,), frozenset())

    def paso(estado: Tuple[Red, Agente], _) -> Tuple[Red, Agente]:
        red_actual, cabeza = estado
        s     = Agente(gen_id(), "S", 1)
        nueva = red_actual.agregar_agente(s).conectar(s.aux(1), cabeza.principal)
        return (nueva, s)

    return reduce(paso, range(n), (red, cero))
Cada llamada a paso devuelve un nuevo par (red, cabeza) sin modificar
el anterior. reduce acumula la cadena S → S → ... → 0 puramente.
La multiplicación también usa reduce:

    pythondef multiplicar(x: int, y: int, verbose: bool = True) -> int:
    return reduce(lambda acc, _: sumar(acc, y, verbose=False), range(x), 0)

Síntesis
El concepto de interacción queda definido por tres elementos, todos
expresados mediante programación funcional:

Un par activo es un par de agentes conectados principal a principal.
Se detecta con una función pura sobre la red inmutable.
Una regla de interacción es una función de primera clase
(Red, Agente, Agente) → Red almacenada en un diccionario indexado
por el par de símbolos. Esto garantiza unicidad de regla por par (Def. 7.3).
La reducción es la aplicación sucesiva de esas funciones hasta
alcanzar una forma normal única (Prop. 7.4).

## Punto 4 — Constante de Feigenbaum δ en ingeniería

Se usa la **constante de Feigenbaum** (δ ≈ 4.6692) para predecir el comportamiento de sistemas no lineales antes de que entren en caos.

El modelo se basa en el **mapa logístico**:

```
x_{n+1} = r · xₙ · (1 − xₙ)
```

A medida que el parámetro `r` aumenta, el sistema pasa por bifurcaciones sucesivas hasta llegar al caos (r∞ ≈ 3.57). La fórmula predictiva es:

```
r₃ = r₂ + (r₂ − r₁) / δ
```

Dado que δ es universal, un ingeniero que observa dos bifurcaciones en su sistema (eléctrico, mecánico, hidráulico, etc.) puede predecir cuándo ocurrirá la siguiente y mantenerse en zona de operación segura.

**Gráfico generado:** `bifurcaciones_feigenbaum.png`

---

## Punto 5 — Atractor de Lorenz con modelamiento basado en agentes

Un **atractor** es una estructura en el espacio de fases hacia la cual un sistema dinámico converge inevitablemente, sin importar desde dónde empiece. Para demostrarlo se usa un **modelo basado en agentes (ABM)** en NetLogo: en lugar de analizar una sola trayectoria, se lanzan múltiples agentes con condiciones iniciales completamente distintas y se observa que todos terminan atrapados en la misma estructura — eso es exactamente la definición de atractor.

El sistema elegido es el **Atractor de Lorenz**, descrito por las ecuaciones:
dx/dt = σ(y − x)
dy/dt = x(ρ − z) − y
dz/dt = xy − βz

Con los parámetros clásicos: `σ=10, ρ=28, β=8/3`

### Rol de los agentes

Cada turtle es una partícula independiente en el espacio de fases `(x, y, z)`. En cada tick actualiza su posición integrando las ecuaciones de Lorenz por el método de Euler con paso `dt`. Ningún agente conoce la posición de los otros — evolucionan en paralelo, sin comunicación.

### Lo que se observa

Al ejecutar el modelo, los agentes parten de posiciones muy dispersas (controladas por el slider `dispersion-inicial`). Con el tiempo, **todos quedan atrapados en la misma estructura de doble lóbulo** (la "mariposa" de Lorenz), aunque sus trayectorias individuales sean distintas. Esto confirma que el atractor es una propiedad del sistema, no de las condiciones iniciales.

### Controles

| Slider | Descripción | Valor sugerido |
|---|---|---|
| `n-agentes` | Número de partículas independientes | 15 |
| `dt` | Paso de integración de Euler | 0.008 |
| `dispersion-inicial` | Dispersión de condiciones iniciales | 25 |

**Requiere:** NetLogo 6.4.0 o superior

---
