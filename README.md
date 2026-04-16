# Parcial 2 — Sistemas Complejos

Soluciones al segundo parcial del curso de Sistemas Complejos. Cada punto aborda un concepto distinto de la teoría de sistemas complejos, implementado en Python.

---

## Punto 1 — Complejidad de Internet: Entropía de Shannon (`punto1.py`)

Internet es complejo porque millones de nodos intercambian tráfico de manera impredecible. Para cuantificar esa complejidad se usa la **Entropía de Shannon**: una medida de qué tan impredecible o distribuido es el tráfico en la red. Si el tráfico está repartido entre muchos nodos, la entropía es alta y el sistema es complejo. Si casi todo el tráfico va a un solo nodo (como en un ataque DDoS), la entropía cae y el sistema se vuelve trivialmente predecible.

```
H(X) = −∑ pᵢ · log₂(pᵢ)
```

Donde `pᵢ` es la probabilidad de que el tráfico se dirija a cada nodo (router/servidor).

Se simulan 4 escenarios:

| Escenario | Descripción | Entropía |
|---|---|---|
| Uniforme | Tráfico perfectamente distribuido | Máxima |
| Normal (Zipf) | Distribución realista de Internet | Alta |
| Congestión | Pocos nodos concentran el tráfico | Media |
| DDoS | Un nodo recibe el 95% del tráfico | Mínima |

También se calcula la **información mutua** entre nodos para medir el acoplamiento entre routers vecinos.

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

## Punto 5 — Atractor con modelamiento basado en agentes (`punto5.py`)

Un **atractor** es un estado al que un sistema dinámico regresa inevitablemente, sin importar desde dónde empiece. Para demostrarlo se usa el modelamiento basado en agentes: en vez de analizar una sola trayectoria, se simulan múltiples agentes independientes con condiciones iniciales muy distintas y se observa que todos convergen al mismo punto. Si el sistema tiene un atractor, esa convergencia ocurre siempre — eso es precisamente lo que lo define.

Se implementa un **modelamiento basado en agentes (ABM)** usando un péndulo amortiguado para demostrar el concepto de **atractor de punto fijo**.

Cada agente es un péndulo independiente con condiciones iniciales distintas (ángulo y velocidad). Todos evolucionan siguiendo la ecuación de movimiento:

```
α = −(g/L)·sin(θ) − b·ω
```

El amortiguamiento `b` drena energía progresivamente. Sin importar las condiciones iniciales, **todos los agentes convergen al punto (θ=0, ω=0)**, que es el atractor.

El espacio de fases muestra visualmente cómo trayectorias muy distintas espiralan hacia el mismo punto.

**Gráfico generado:** `atractor_pendulo.png`

---

## Requisitos

```bash
pip install numpy matplotlib
```

## Uso

Cada archivo es independiente y se ejecuta directamente:

```bash
python punto1.py
python punto2.py
python punto3.py
python punto4.py
python punto5.py
```
