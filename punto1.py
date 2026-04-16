

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import Counter


# ─────────────────────────────────────────────
# 1. FUNCIONES DEL MODELO DE SHANNON
# ─────────────────────────────────────────────

def entropia_shannon(probabilidades):
    p = np.array(probabilidades, dtype=float)
    p = p[p > 0]
    H = -np.sum(p * np.log2(p))
    return H


def entropia_maxima(n_nodos):
    return np.log2(n_nodos)


def complejidad_normalizada(H, H_max):
    if H_max == 0:
        return 0.0
    return H / H_max


def entropia_conjunta(matriz_prob):
    p = np.array(matriz_prob, dtype=float)
    p_flat = p.flatten()
    p_flat = p_flat[p_flat > 0]
    return -np.sum(p_flat * np.log2(p_flat))


def entropia_condicional(matriz_prob):
    p = np.array(matriz_prob, dtype=float)
    H_xy = entropia_conjunta(p)
    p_y = p.sum(axis=0)
    H_y = entropia_shannon(p_y)
    return H_xy - H_y


def informacion_mutua(matriz_prob):
    p = np.array(matriz_prob, dtype=float)
    p_x = p.sum(axis=1)
    H_x = entropia_shannon(p_x)
    H_x_dado_y = entropia_condicional(p)
    return H_x - H_x_dado_y


# ─────────────────────────────────────────────
# 2. SIMULACIÓN DE ESCENARIOS DE INTERNET
# ─────────────────────────────────────────────

def simular_trafico(escenario, n_nodos=10, n_muestras=10000):
    if escenario == 'normal':
        pesos = np.array([1 / (i ** 0.8) for i in range(1, n_nodos + 1)])
        nombre = 'Red normal (distribución Zipf)'

    elif escenario == 'ddos':
        pesos = np.ones(n_nodos) * 0.05 / (n_nodos - 1)
        pesos[0] = 0.95
        nombre = 'Ataque DDoS (un nodo dominante)'

    elif escenario == 'congestion':
        pesos = np.ones(n_nodos) * 0.02
        pesos[0] = 0.5
        pesos[1] = 0.3
        pesos[2] = 0.12
        nombre = 'Congestión (cuello de botella)'

    elif escenario == 'uniforme':
        pesos = np.ones(n_nodos)
        nombre = 'Red uniforme (máxima complejidad)'

    else:
        raise ValueError(f"Escenario desconocido: {escenario}")

    probs = pesos / pesos.sum()
    return probs, nombre


def analizar_escenario(escenario, n_nodos=10):
    probs, nombre = simular_trafico(escenario, n_nodos)
    H = entropia_shannon(probs)
    H_max = entropia_maxima(n_nodos)
    C = complejidad_normalizada(H, H_max)

    return {
        'nombre': nombre,
        'escenario': escenario,
        'probabilidades': probs,
        'H': H,
        'H_max': H_max,
        'complejidad': C
    }


# ─────────────────────────────────────────────
# 3. VISUALIZACIÓN
# ─────────────────────────────────────────────

def graficar_todo(n_nodos=10):
    escenarios = ['uniforme', 'normal', 'congestion', 'ddos']
    resultados = [analizar_escenario(e, n_nodos) for e in escenarios]

    colores = ['#1D9E75', '#185FA5', '#EF9F27', '#A32D2D']

    fig = plt.figure(figsize=(14, 10), facecolor='#FAFAF8')
    gs = gridspec.GridSpec(2, 2, hspace=0.45, wspace=0.35)
    fig.suptitle('Complejidad de Internet — Modelo de Entropía de Shannon\n'
                 'H(X) = −∑ pᵢ · log₂(pᵢ)',
                 fontsize=13, y=0.98, color='#1a1a1a')

    nodos = [f'N{i+1}' for i in range(n_nodos)]

    ax1 = fig.add_subplot(gs[0, :])
    x = np.arange(n_nodos)
    ancho = 0.2
    for i, (res, color) in enumerate(zip(resultados, colores)):
        offset = (i - 1.5) * ancho
        bars = ax1.bar(x + offset, res['probabilidades'] * 100,
                       width=ancho, color=color, alpha=0.85,
                       label=f"{res['nombre']}\nH={res['H']:.3f} bits  C={res['complejidad']:.2%}")
    ax1.set_xlabel('Nodo de red (router / servidor)', fontsize=10)
    ax1.set_ylabel('Probabilidad de tráfico (%)', fontsize=10)
    ax1.set_title('Distribución del tráfico según el escenario', fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(nodos)
    ax1.legend(fontsize=8, loc='upper right', ncol=2)
    ax1.set_facecolor('#F5F4F0')
    ax1.grid(True, alpha=0.2, axis='y')

    ax2 = fig.add_subplot(gs[1, 0])
    nombres_cortos = ['Uniforme', 'Normal\n(Zipf)', 'Congestión', 'DDoS']
    H_vals = [r['H'] for r in resultados]
    H_max = resultados[0]['H_max']

    barras = ax2.barh(nombres_cortos, H_vals, color=colores, alpha=0.85, height=0.5)
    ax2.axvline(H_max, color='#1a1a1a', linewidth=1.5,
                linestyle='--', alpha=0.6, label=f'H_max = {H_max:.3f} bits')
    for bar, val in zip(barras, H_vals):
        ax2.text(val + 0.03, bar.get_y() + bar.get_height() / 2,
                 f'{val:.3f} bits', va='center', fontsize=9)
    ax2.set_xlabel('Entropía H(X) en bits', fontsize=10)
    ax2.set_title('Entropía de Shannon por escenario', fontsize=11)
    ax2.legend(fontsize=9)
    ax2.set_facecolor('#F5F4F0')
    ax2.grid(True, alpha=0.2, axis='x')

    ax3 = fig.add_subplot(gs[1, 1])
    C_vals = [r['complejidad'] for r in resultados]

    barras3 = ax3.bar(nombres_cortos, C_vals, color=colores, alpha=0.85, width=0.5)
    ax3.axhline(1.0, color='#1D9E75', linewidth=1.5,
                linestyle='--', alpha=0.7, label='Complejidad máxima (C=1)')
    ax3.axhline(0.5, color='#EF9F27', linewidth=1,
                linestyle=':', alpha=0.6, label='Umbral de advertencia (C=0.5)')
    for bar, val in zip(barras3, C_vals):
        ax3.text(bar.get_x() + bar.get_width() / 2, val + 0.01,
                 f'{val:.1%}', ha='center', fontsize=9, fontweight='bold')
    ax3.set_ylabel('Complejidad normalizada C = H / H_max', fontsize=9)
    ax3.set_title('Complejidad normalizada por escenario', fontsize=11)
    ax3.set_ylim(0, 1.15)
    ax3.legend(fontsize=8)
    ax3.set_facecolor('#F5F4F0')
    ax3.grid(True, alpha=0.2, axis='y')

    plt.savefig('shannon_internet.png', dpi=150, bbox_inches='tight',
                facecolor='#FAFAF8')
    plt.show()
    print("\nGráfico guardado como 'shannon_internet.png'")


def graficar_entropia_vs_nodos():
    n_vals = np.arange(1, 201)
    H_max_vals = np.log2(n_vals)

    fig, ax = plt.subplots(figsize=(9, 4), facecolor='#FAFAF8')
    ax.set_facecolor('#F5F4F0')
    ax.plot(n_vals, H_max_vals, color='#185FA5', linewidth=2)
    ax.fill_between(n_vals, H_max_vals, alpha=0.12, color='#185FA5')

    refs = [(10, 'LAN local'), (100, 'Red empresarial'), (200, 'Fragmento de Internet')]
    for n, label in refs:
        h = np.log2(n)
        ax.plot(n, h, 'o', color='#D85A30', markersize=7)
        ax.annotate(f'{label}\nn={n}, H={h:.2f} bits',
                    xy=(n, h), xytext=(n + 5, h - 0.4),
                    fontsize=8, color='#D85A30',
                    arrowprops=dict(arrowstyle='->', color='#D85A30', lw=0.8))

    ax.set_xlabel('Número de nodos activos (n)', fontsize=10)
    ax.set_ylabel('Entropía máxima H_max = log₂(n)  [bits]', fontsize=10)
    ax.set_title('Crecimiento de la complejidad máxima con el número de nodos\n'
                 'A más nodos participan, mayor es la complejidad potencial de Internet',
                 fontsize=11)
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('entropia_vs_nodos.png', dpi=150, bbox_inches='tight',
                facecolor='#FAFAF8')
    plt.show()
    print("Gráfico guardado como 'entropia_vs_nodos.png'")


# ─────────────────────────────────────────────
# 4. PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

def main():
    N_NODOS = 10

    print("=" * 65)
    print("  COMPLEJIDAD DE INTERNET — TEORÍA DE LA INFORMACIÓN (SHANNON)")
    print("=" * 65)
    print(f"\n  Modelo: H(X) = -∑ pᵢ · log₂(pᵢ)")
    print(f"  Número de nodos simulados: {N_NODOS}")
    print(f"  Entropía máxima posible: H_max = log₂({N_NODOS}) = {np.log2(N_NODOS):.4f} bits\n")

    print("-" * 65)
    print(f"  {'Escenario':<35} {'H (bits)':>10} {'H_max':>8} {'Complejidad':>12}")
    print("  " + "-" * 63)

    for escenario in ['uniforme', 'normal', 'congestion', 'ddos']:
        res = analizar_escenario(escenario, N_NODOS)
        print(f"  {res['nombre']:<35} {res['H']:>10.4f} {res['H_max']:>8.4f} {res['complejidad']:>11.2%}")

    print("\n" + "-" * 65)
    print("  INFORMACIÓN MUTUA ENTRE DOS NODOS VECINOS")
    print("-" * 65)

    matriz_conjunta = np.array([
        [0.30, 0.10, 0.05],
        [0.10, 0.20, 0.08],
        [0.05, 0.07, 0.05]
    ])
    matriz_conjunta /= matriz_conjunta.sum() 

    H_xy = entropia_conjunta(matriz_conjunta)
    H_x_dado_y = entropia_condicional(matriz_conjunta)
    I_xy = informacion_mutua(matriz_conjunta)

    print(f"\n  Entropía conjunta  H(X,Y)  = {H_xy:.4f} bits")
    print(f"  Entropía condicional H(X|Y) = {H_x_dado_y:.4f} bits")
    print(f"  Información mutua  I(X;Y)  = {I_xy:.4f} bits")
    print(f"\n  Interpretación:")
    print(f"  Si I(X;Y) ≈ 0 → nodos independientes (sin acoplamiento)")
    print(f"  Si I(X;Y) alto → conocer el estado de Y reduce mucho")
    print(f"  la incertidumbre sobre X (nodos fuertemente acoplados).")
    print(f"  En Internet, esto modela la correlación de tráfico")
    print(f"  entre routers vecinos o rutas interdependientes.")

    #Visualizaciones
    print("\n" + "-" * 65)
    print("  Generando visualizaciones...")
    graficar_todo(N_NODOS)
    graficar_entropia_vs_nodos()


if __name__ == "__main__":
    main()