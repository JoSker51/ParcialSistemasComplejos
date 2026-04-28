# Parcial 2 — Sistemas Complejos

Jose Santiago Gonzalez Enriquez

---

## Punto 1 — Complejidad de Internet: Entropía de Shannon (`punto1.py`)

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

## Punto 2 — Suma y multiplicación desde la función sucesor (`punto2.py`)

Implementación de aritmética básica partiendo únicamente de la **función sucesor** `S(n) = n + 1`, siguiendo la construcción de los **Números de Peano**.

- **Suma:** aplicar `S` b veces sobre a → `a + b = S(S(...S(a)...))`
- **Multiplicación:** sumar `a` consigo mismo `b` veces → `a × b = a + a + ... + a`

Esto ilustra cómo comportamientos complejos (operaciones aritméticas) emergen de una regla primitiva simple.

---

## Punto 3 — Interacción con Net Interactions (`punto3.py`)

# Redes de Interacción — Definición del concepto mediante el código

---

## ¿Qué es una red de interacción?

Una red de interacción es un modelo de computación gráfico. En lugar de ejecutar instrucciones secuenciales o reducir expresiones simbólicas, la computación ocurre mediante **agentes conectados por alambres** que se transforman localmente siguiendo reglas definidas.

Formalmente (Def. 7.1), una red se construye sobre una signatura Σ de símbolos, cada uno con una **aridad** fija. Un agente con aridad `n` tiene exactamente `n + 1` puertos: un **puerto principal** (distinguido) y `n` **puertos auxiliares**.

En el código, esto se modela así:

```python
class Agente:
    def __init__(self, simbolo: str, aridad: int):
        self.simbolo = simbolo
        self.aridad  = aridad
        self.puertos = [Puerto(self) for _ in range(aridad + 1)]

    @property
    def principal(self) -> Puerto:
        return self.puertos[0]

    def aux(self, i: int) -> Puerto:
        return self.puertos[i]
```

Los tres agentes del sistema de suma son:

| Agente | Símbolo | Aridad | Significado |
|--------|---------|--------|-------------|
| Cero   | `"0"`   | 0      | El número 0; solo tiene puerto principal |
| Sucesor | `"S"`  | 1      | S(x); un auxiliar conectado al interior |
| Suma   | `"add"` | 2      | add(x, y); dos auxiliares para cada argumento |

---

## El concepto de interacción

La **interacción** es el mecanismo central de reducción. Según la Definición 7.2 del libro, un **par activo** α ⊳◁ β se forma cuando el puerto principal de α está conectado directamente al puerto principal de β. Este par es el análogo de un *redex* en el lambda cálculo: es la unidad mínima de computación pendiente.

```python
def pares_activos(self) -> list[tuple[Agente, Agente]]:
    for ag in self.agentes:
        p = ag.principal
        if p.wire is not None:
            vecino = p.wire.agente
            if p.wire is vecino.principal:  # principal ↔ principal
                ...
```

La condición `p.wire is vecino.principal` es la verificación exacta de la Definición 7.2: el alambre del principal de `ag` debe terminar en el principal de `vecino`, no en un puerto auxiliar. Cualquier otra conexión no es un par activo y no puede reducirse.

> **La interacción ocurre única y exclusivamente entre puertos principales.**  
> Dos agentes conectados auxiliar-auxiliar o principal-auxiliar conviven en la red sin interactuar.

---

## Las reglas de interacción

Una regla de interacción (Def. 7.3) especifica qué red reemplaza a un par activo dado. El sistema impone dos restricciones:

1. La **interfaz se preserva**: los puertos libres antes y después de la reducción son los mismos.
2. Hay **a lo sumo una regla** por par no ordenado de agentes.

Para la suma, las dos reglas son:

### Regla 1 — caso base: `add ⊳◁ 0`

```
add(0, y) = y
```

Los agentes `add` y `0` se eliminan. El argumento `y` queda conectado directamente al resultado.

```python
def regla_add_cero(add: Agente, cero: Agente, red: Red):
    puerto_y_cabeza = add.aux(2).wire
    desconectar(add.principal, cero.principal)
    desconectar(add.aux(2), puerto_y_cabeza)
    red.remover(add)
    red.remover(cero)
    # y queda expuesto: la red se reduce sin crear nuevos agentes
```

### Regla 2 — caso recursivo: `add ⊳◁ S`

```
add(S(x), y) = S(add(x, y))
```

Los agentes `add` y `S` se consumen. Se crean un nuevo `S` y un nuevo `add`, conectados a `x` e `y`, generando un nuevo par activo que será reducido en la siguiente iteración.

```python
def regla_add_sucesor(add: Agente, s: Agente, red: Red):
    puerto_x_interior = s.aux(1).wire
    puerto_y_cabeza   = add.aux(2).wire
    puerto_salida     = add.aux(1).wire

    # Destruir el par activo
    desconectar(add.principal, s.principal)
    desconectar(s.aux(1), puerto_x_interior)
    desconectar(add.aux(2), puerto_y_cabeza)
    red.remover(add)
    red.remover(s)

    # Crear nueva configuración
    s_nuevo   = red.agregar(Agente("S", 1))
    add_nuevo = red.agregar(Agente("add", 2))
    conectar(add_nuevo.aux(2), puerto_y_cabeza)
    conectar(add_nuevo.principal, puerto_x_interior)
    if puerto_salida is not None:
        conectar(s_nuevo.principal, puerto_salida)
```

---

## El ciclo de reducción

La función `reducir()` implementa la Definición 7.3: en cada paso se selecciona un par activo, se identifica qué regla aplica, y se ejecuta la transformación local. El proceso se repite hasta que no quedan pares activos.

```python
def reducir(red: Red, verbose=True) -> None:
    while True:
        pares = red.pares_activos()
        if not pares:
            break  # forma normal alcanzada
        alpha, beta = pares[0]
        clave = tuple(sorted([alpha.simbolo, beta.simbolo]))

        if clave == ("0", "add"):
            regla_add_cero(...)
        elif clave == ("S", "add"):
            regla_add_sucesor(...)
        else:
            break  # par bloqueado: sin regla definida
```

Cuando no quedan pares activos, la red está en **forma normal**. La Proposición 7.4 garantiza que esta forma normal es **única**: sin importar el orden en que se reduzcan los pares, el resultado siempre es el mismo. Esta propiedad (confluencia fuerte) es lo que hace que el modelo sea determinista.

---

## Ejemplo: `add(S(0), S(0))` → `S(S(0))`

La red inicial representa `1 + 1`. El único par activo es `add ⊳◁ S`.

```
Paso 1: add ⊳◁ S  →  S(add(0, S(0)))   [caso recursivo]
Paso 2: add ⊳◁ 0  →  S(S(0))           [caso base]
```

Al final, la red contiene exactamente dos agentes `S` y un agente `0`. El resultado se lee así:

```python
def leer_numero(red: Red) -> int:
    return sum(1 for ag in red.agentes if ag.simbolo == "S")
```

El número de agentes `S` restantes es la representación unaria del resultado: `S^n(0)` equivale al número natural `n`.

---

## Síntesis

El concepto de **interacción** queda definido por tres elementos que el código implementa directamente:

- **Un par activo** es la única forma en que dos agentes pueden interactuar, y requiere que ambos estén conectados por sus puertos principales.
- **Una regla de interacción** describe la transformación local que reemplaza ese par, preservando la interfaz de la red.
- **La reducción** es la aplicación sucesiva de reglas hasta alcanzar una forma normal, que es única por la propiedad de confluencia fuerte.

La computación no es secuencial ni centralizada: cada par activo puede reducirse independientemente, lo que hace de las redes de interacción un modelo naturalmente paralelo.

---

## Punto 4 — Constante de Feigenbaum δ en ingeniería (`punto4.py`)

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

## Punto 5 — Atractor de Lorenz con modelamiento basado en agentes (`punto5_lorenz.nlogo`)

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
