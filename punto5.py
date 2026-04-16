import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Parámetros físicos
g = 9.8       # gravedad
L = 1.0       # longitud del péndulo
b = 0.3       # amortiguamiento
dt = 0.05     # paso de tiempo


class AgentePendulo:
    def __init__(self, theta0, omega0):
        self.theta = theta0
        self.omega = omega0
        self.historial_theta = [theta0]
        self.historial_omega = [omega0]

    def actualizar(self):
        alpha = -(g / L) * np.sin(self.theta) - b * self.omega
        self.omega = self.omega + alpha * dt
        self.theta = self.theta + self.omega * dt

        self.historial_theta.append(self.theta)
        self.historial_omega.append(self.omega)

agentes = [
    AgentePendulo(theta0=np.radians(150), omega0=0.0),   # muy abierto
    AgentePendulo(theta0=np.radians(90),  omega0=1.0),   # posición media
    AgentePendulo(theta0=np.radians(45),  omega0=-1.5),  # con velocidad
    AgentePendulo(theta0=np.radians(170), omega0=0.5),   # casi vertical
    AgentePendulo(theta0=np.radians(20),  omega0=2.0),   # poco ángulo
    AgentePendulo(theta0=np.radians(120), omega0=-2.0),  # velocidad negativa
]

colores = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']

pasos = 400
for _ in range(pasos):
    for agente in agentes:
        agente.actualizar()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Atractor de Punto Fijo — Péndulo Amortiguado\nModelamiento Basado en Agentes',
             fontsize=13, fontweight='bold')


ax1 = axes[0]
ax1.set_title('Ángulo vs Tiempo')
ax1.set_xlabel('Tiempo (ticks)')
ax1.set_ylabel('θ (radianes)')

for i, agente in enumerate(agentes):
    ax1.plot(agente.historial_theta, color=colores[i],
             alpha=0.7, linewidth=1.2,
             label=f'Agente {i+1}')

ax1.axhline(y=0, color='black', linestyle='--', linewidth=1.5,
            label='Atractor (θ=0)')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

ax2 = axes[1]
ax2.set_title('Espacio de Fases (θ vs ω)\nTodas las trayectorias convergen al atractor')
ax2.set_xlabel('θ — Posición angular')
ax2.set_ylabel('ω — Velocidad angular')

for i, agente in enumerate(agentes):
    ax2.plot(agente.historial_theta, agente.historial_omega,
             color=colores[i], alpha=0.6, linewidth=1.2,
             label=f'Agente {i+1}')
    ax2.scatter(agente.historial_theta[0], agente.historial_omega[0],
                color=colores[i], s=80, zorder=5, marker='o')

ax2.scatter(0, 0, color='black', s=200, zorder=6,
            marker='*', label='ATRACTOR (0, 0)')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('atractor_pendulo.png', dpi=150, bbox_inches='tight')
plt.show()

print("Simulación completa.")
print(f"Todos los agentes convergen a θ=0, ω=0 (el atractor)")
for i, agente in enumerate(agentes):
    print(f"  Agente {i+1}: θ final = {agente.historial_theta[-1]:.4f}, "
          f"ω final = {agente.historial_omega[-1]:.4f}")