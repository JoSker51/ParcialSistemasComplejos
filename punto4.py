

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────────
# 1. CONSTANTES
# ─────────────────────────────────────────────

DELTA = 4.669201609102990  # Constante de Feigenbaum
R_INF = 3.569945671870944  # Valor de r donde comienza el caos

# Bifurcaciones
BIFURCACIONES = [3.0000, 3.4495, 3.5441, 3.5644, 3.5688, 3.5697]


# ─────────────────────────────────────────────
# 2. MAPA LOGÍSTICO
# ─────────────────────────────────────────────

def mapa_logistico(r, x0=0.5, iteraciones=1000, ultimos=200):
    x = x0
    resultados = []
    for i in range(iteraciones):
        x = r * x * (1 - x)
        if i >= iteraciones - ultimos:
            resultados.append(x)
    return resultados


# ─────────────────────────────────────────────
# 3. PREDICCIÓN CON δ
# ─────────────────────────────────────────────

def predecir_bifurcacion(r1, r2):
    delta_intervalo = r2 - r1
    r3 = r2 + delta_intervalo / DELTA
    return r3


def calcular_tabla_bifurcaciones(bifurcaciones):
    tabla = []
    for i in range(len(bifurcaciones) - 1):
        r_n = bifurcaciones[i]
        r_siguiente = bifurcaciones[i + 1]
        intervalo = r_siguiente - r_n
        prediccion = r_n + intervalo / DELTA
        tabla.append({
            "n": i + 1,
            "r_n": r_n,
            "intervalo": intervalo,
            "prediccion_siguiente": prediccion,
            "r_real_siguiente": r_siguiente,
            "error": abs(prediccion - r_siguiente)
        })
    return tabla


def zona_operacion(r):
    if r < BIFURCACIONES[0]:
        return "Estable (punto fijo)", True
    elif r < BIFURCACIONES[1]:
        return "Ciclo-2 (oscilación controlada)", True
    elif r < BIFURCACIONES[2]:
        return "Ciclo-4 (advertencia)", False
    elif r < R_INF:
        return "Pre-caos (peligroso)", False
    else:
        return "CAOS (evitar)", False


# ─────────────────────────────────────────────
# 4. DIAGRAMA DE BIFURCACIONES
# ─────────────────────────────────────────────

def graficar_bifurcaciones(r_min=2.4, r_max=4.0, pasos=1200):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#FAFAF8')
    ax.set_facecolor('#F5F4F0')

   
    ax.axvspan(r_min, BIFURCACIONES[1], alpha=0.08, color='green', label='Zona segura')

    ax.axvspan(BIFURCACIONES[1], BIFURCACIONES[2], alpha=0.10, color='orange')

    ax.axvspan(BIFURCACIONES[2], r_max, alpha=0.08, color='red')

    r_vals = np.linspace(r_min, r_max, pasos)
    for r in r_vals:
        atractor = mapa_logistico(r, iteraciones=800, ultimos=150)
        ax.plot([r] * len(atractor), atractor,
                ',', color='#185FA5', alpha=0.3, markersize=0.5)

    colores_bif = ['#1D9E75', '#EF9F27', '#D85A30', '#D4537E', '#7F77DD', '#E24B4A']
    for i, rb in enumerate(BIFURCACIONES):
        ax.axvline(rb, color=colores_bif[i], linewidth=1.2,
                   linestyle='--', alpha=0.85)
        ax.text(rb + 0.005, 0.92 - (i % 2) * 0.07,
                f'r{i+1}={rb}', color=colores_bif[i],
                fontsize=8, transform=ax.get_xaxis_transform())

    ax.axvline(R_INF, color='#A32D2D', linewidth=2, linestyle='-', label=f'Caos r∞ = {R_INF:.4f}')
    ax.text(R_INF + 0.01, 0.5, 'r∞\n(caos)', color='#A32D2D',
            fontsize=9, transform=ax.get_xaxis_transform(), ha='left')

    parches = [
        mpatches.Patch(color='green', alpha=0.4, label='Zona segura (estable / ciclo-2)'),
        mpatches.Patch(color='orange', alpha=0.5, label='Advertencia (ciclo-4)'),
        mpatches.Patch(color='red', alpha=0.4, label='Peligro / caos'),
    ]
    ax.legend(handles=parches, loc='lower right', fontsize=9)

    ax.set_xlabel('Parámetro de control r', fontsize=11)
    ax.set_ylabel('Estado del sistema x', fontsize=11)
    ax.set_title('Diagrama de bifurcaciones — Mapa logístico\n'
                 'Aplicación de la constante de Feigenbaum δ en ingeniería',
                 fontsize=12)
    ax.set_xlim(r_min, r_max)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig('bifurcaciones_feigenbaum.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\nGráfico guardado como 'bifurcaciones_feigenbaum.png'")


# ─────────────────────────────────────────────
# 5. PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  CONSTANTE DE FEIGENBAUM δ — APLICACIÓN EN INGENIERÍA")
    print("=" * 60)
    print(f"\n  δ = {DELTA}")
    print(f"  r∞ (inicio del caos) = {R_INF}")

    print("\n" + "-" * 60)
    print("  TABLA DE BIFURCACIONES Y PREDICCIONES CON δ")
    print("-" * 60)
    print(f"  {'n':>3} | {'r_n':>8} | {'Intervalo Δ':>12} | {'Predicción r_n+1':>17} | {'Error':>10}")
    print("  " + "-" * 56)

    tabla = calcular_tabla_bifurcaciones(BIFURCACIONES)
    for fila in tabla:
        print(f"  {fila['n']:>3} | {fila['r_n']:>8.4f} | {fila['intervalo']:>12.6f} | "
              f"{fila['prediccion_siguiente']:>17.6f} | {fila['error']:>10.6f}")

    print("\n" + "-" * 60)
    print("  EJEMPLO: SISTEMA DE BOMBEO NO LINEAL")
    print("-" * 60)

    r1_obs = 2.8
    r2_obs = 3.4
    r3_pred = predecir_bifurcacion(r1_obs, r2_obs)

    print(f"\n  Bifurcación 1 medida: r₁ = {r1_obs}")
    print(f"  Bifurcación 2 medida: r₂ = {r2_obs}")
    print(f"  Δ = r₂ - r₁ = {r2_obs - r1_obs:.4f}")
    print(f"\n  Predicción con δ:")
    print(f"    r₃ = r₂ + Δ/δ = {r2_obs} + {(r2_obs - r1_obs):.4f}/{DELTA:.4f}")
    print(f"    r₃ ≈ {r3_pred:.4f}")
    print(f"\n  → El ingeniero debe operar con r < {r3_pred:.4f}")
    print(f"    para mantenerse en régimen estable.")

    print("\n" + "-" * 60)
    print("  EVALUACIÓN DE ZONA DE OPERACIÓN")
    print("-" * 60)

    valores_prueba = [2.5, 3.2, 3.49, 3.55, 3.58]
    for r in valores_prueba:
        zona, seguro = zona_operacion(r)
        estado = "✓ SEGURO" if seguro else "✗ RIESGO"
        print(f"  r = {r:.2f} → {zona:40s} [{estado}]")

    print("\n" + "-" * 60)
    print("  Generando diagrama de bifurcaciones...")
    graficar_bifurcaciones()


if __name__ == "__main__":
    main()
