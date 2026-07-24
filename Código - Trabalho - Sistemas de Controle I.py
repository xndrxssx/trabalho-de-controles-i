import control as ct
import matplotlib.pyplot as plt
import numpy as np

# 1. Parâmetros das Engrenagens
N1, N2 = 10, 20
N3, N4 = 10, 20

# Relações de transmissão
n1 = N1 / N2  # 0.5
n2 = N3 / N4  # 0.5
n_total = n1 * n2  # 0.25 (1/4)

# 2. Reflexão de Inércias e Amortecimento para o Eixo do Motor
J1 = 1.0  # kg.m^2
J2, J3 = 2.0, 2.0  # kg.m^2
J4 = 16.0  # kg.m^2
D = 32.0  # N.m.s/rad

Jm = J1 + (J2 + J3) * (n1**2) + J4 * (n_total**2)  # Jm = 3.0
Dm = D * (n_total**2)  # Dm = 2.0

# 3. Constantes Elétricas do Motor (obtidas do gráfico Torque x Velocidade)
ea = 5.0  # Volts
T_bloqueado = 5.0  # N.m
w_rpm = 600 / np.pi  # RPM
w_vazio = w_rpm * (2 * np.pi / 60)  # Convertendo para rad/s (20 rad/s)

Kt_Ra = T_bloqueado / ea  # Kt/Ra = 1.0
Kce = ea / w_vazio  # Kce = 0.25

# 4. Construção da Função de Transferência G(s) = Theta_2(s) / Ea(s)
# Numerador do motor: Kt / (Ra * Jm)
num_m = [Kt_Ra / Jm]

# Denominador do motor: s^2 + [1/Jm * (Dm + (Kt*Kce)/Ra)] * s
pol_pole = (1 / Jm) * (Dm + Kt_Ra * Kce)  # 0.75
den_m = [1.0, pol_pole, 0.0]

# FT do Motor: Theta_m(s) / Ea(s)
G_motor = ct.tf(num_m, den_m)

# FT na Saída: Theta_2(s) / Ea(s) = n_total * G_motor(s)
G_final = n_total * G_motor

print('=== FUNÇÃO DE TRANSFERÊNCIA FINAL G(s) ===')
print(G_final)

# 5. Simulação da Resposta ao Degrau (Exemplo: Tensão aplicada de 5V)
tempo = np.linspace(0, 10, 1000)
tensao_degrau = 5.0

t, y = ct.step_response(tensao_degrau * G_final, T=tempo)

# 6. Plotagem da Posição Angular da Carga Theta_2(t)
plt.figure(figsize=(9, 5))
plt.plot(
    t,
    y,
    label=r'$\theta_2(t)$ - Deslocamento Angular na Saída (rad)',
    color='#1f77b4',
    linewidth=2.5,
)
plt.title(
    'Resposta Temporal ao Degrau de 5V - Problema 43 (Nise Cap. 2)',
    fontsize=12,
    pad=10,
)
plt.xlabel('Tempo (s)', fontsize=10)
plt.ylabel('Posição Angular $\theta_2(t)$ (rad)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper left')
plt.tight_layout()

# Salvando a imagem do gráfico para o relatório/GitHub
plt.savefig('grafico_problema_43.png', dpi=300)
plt.show()