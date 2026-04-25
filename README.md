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

Implementación del concepto de **Interacción** usando el modelo de *Net Interactions* como base matemática, con **programación funcional** en Python.

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
