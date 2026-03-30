import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constantes
radianos = np.pi / 180
conv_massa = 9.5464e-4
conv_vel = 149597870700.0 / (365 * 24 * 3600)


def eq_kepler_simplificada(M, e): # Convertida Fortran
    tol = 1.0E-12
    max_iter = 100
    AnomE = M  # Aproximação inicial

    for i in range(max_iter):
        delta = (M + e * np.sin(AnomE) - AnomE) / (1.0 - e * np.cos(AnomE))
        AnomE = AnomE + delta
        if abs(delta) < tol:
            break
    return AnomE

def anomalia_verdadeira(t, T0, P, e):
    # Anomalia média
    M = 2 * np.pi * (t - T0) / P
    E = eq_kepler_simplificada(M, e)
    # Anomalia verdadeira
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                        np.sqrt(1 - e) * np.cos(E / 2))
    return nu

def semi_amplitude_K(a, M_min, M_total, P, e):
    num = 2.0 * np.pi * a * M_min
    den = M_total * P * np.sqrt(1.0 - e * e)
    return num / den

# The parametrized function to be plotted
def velocidade_radial(m, a, e, T, M_t, w, i, t):
    M_min = m * np.sin(i * radianos)
    K = semi_amplitude_K(a, M_min, M_t, T, e)
    theta = np.zeros_like(t)
    for i, time in enumerate(t):
        f = anomalia_verdadeira(time, 0, T, e)
        theta[i] = f
    return K * (np.cos(theta + w*radianos) + e * np.cos(w * radianos)) * conv_vel

# CSS para controlar tamanho do gráfico
st.markdown("""
    <style>
        /* Controla o tamanho máximo do gráfico */
        .stPlotlyChart, .stImage {
            max-width: 900px;
            margin: 0 auto;
        }

        /* Opcional: remove o padding excessivo */
        .main > div {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Título e descrição
st.title("🪐 Simulador de Velocidade Radial")
# st.markdown("Ajuste os parâmetros abaixo para ver como a curva de velocidade radial muda.")

# Sidebar com controles
st.sidebar.header("Parâmetros Gerais")

MC = st.sidebar.slider("Massa da Estrela [M_Solar]",
                         min_value=0.1,max_value=10.0,value=1.0,step=0.01,
                        help="Massa da estrela em massas do Sol")

with st.sidebar.expander("Dados Planeta 1:"):
    M1 = st.slider("Massa mínima do Planeta 1 [M_Jup]",
        min_value=0.0, max_value=20.0, value=1.0, step=0.01,
        help="Massa Mínima do planeta em massas de Júpiter") * conv_massa

    T1 = st.slider("Período Orbital 1 [anos]",
        min_value=30, max_value=10000, value=365, step=1,
        help="Tempo para completar uma órbita")/365.0

    ecc1 = st.slider("Excentricidade 1",
                             min_value=0.0, max_value=0.99, value=0.15, step=0.01,
                             help="Excentricidade da órbita (0 = circular, 1 = parabólica)")

    w_arg1 = st.slider("Argumento do Periastro 1 [deg]",
                               min_value=0.0, max_value=360.0, value=0.0, step=0.5,
                               help="Orientação da órbita")

    inc1 = st.slider("Inclinação 1 [deg]",
                             min_value=0.01, max_value=180.0, value=90.0, step=0.5,
                             help="Inclinação do plano orbital")

    M1_Real = M1 / np.sin(inc1 * radianos)
    mu1 = 4.0 * np.pi ** 2 * (MC + M1_Real)
    semi_eixo1 = ((T1 ** 2 * mu1) / (4 * np.pi ** 2)) ** (1 / 3)

with st.sidebar.expander("Dados Planeta 2:"):
    M2 = st.slider("Massa mínima do Planeta 2 [M_Jup]",
                         min_value=0.0, max_value=20.0, value=0.0, step=0.01,
                         help="Massa Mínima do planeta em massas de Júpiter") * conv_massa

    T2 = st.slider("Período Orbital 2 [dias]",
                         min_value=30, max_value=10000, value=365, step=1,
                         help="Tempo para completar uma órbita")/365.0

    ecc2 = st.slider("Excentricidade 2",
                             min_value=0.0, max_value=0.99, value=0.15, step=0.01,
                             help="Excentricidade da órbita (0 = circular, 1 = parabólica)")

    w_arg2 = st.slider("Argumento do Periastro 2 [deg]",
                               min_value=0.0, max_value=360.0, value=0.0, step=0.5,
                               help="Orientação da órbita")

    inc2 = st.slider("Inclinação 2 [deg]",
                             min_value=0.01, max_value=180.0, value=90.0, step=0.50,
                             help="Inclinação do plano orbital")

    M2_Real = M2 / np.sin(inc2 * radianos)
    mu2 = 4.0 * np.pi ** 2 * (MC + M2_Real)
    semi_eixo2 = ((T2 ** 2 * mu2) / (4 * np.pi ** 2)) ** (1 / 3)

t_f = st.sidebar.slider("Tempo total [anos]",
                        min_value=1,max_value=20,value=3,step=1,
                        help="Tempo total de simulação (em anos)")

t = np.linspace(0, t_f, t_f*100)
# Calcular a curva de velocidade radial
rv = (velocidade_radial(M1, semi_eixo1, ecc1, T1, MC, w_arg1, inc1, t) +
      velocidade_radial(M2, semi_eixo2, ecc2, T2, MC, w_arg2, inc2, t))

# Criar o gráfico com tamanho controlado
fig, ax = plt.subplots(figsize=(10, 6))  # Ajuste conforme desejar (9:5.4 mantém proporção)
ax.plot(t, rv, 'b-', linewidth=2)
ax.set_xlabel('Time [yr]', fontsize=12)
ax.set_ylabel('RV [m/s]', fontsize=12)
ax.set_title('Curva de Velocidade Radial', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)

# Adicionar informações sobre a amplitude
K_max = np.max(np.abs(rv))
ax.text(0.02, 0.98, f'Amplitude Máxima: {K_max:.2f} m/s',
        transform=ax.transAxes, fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()

# Opção 1: Gráfico com largura controlada
# Use esta opção se quiser que o gráfico respeite o figsize
# st.pyplot(fig, width='content')

# Opção 2: Se quiser centralizar e limitar o tamanho máximo
# Descomente as linhas abaixo e comente a linha acima
col1, col2, col3 = st.columns([1, 50, 1])
with col2:
    st.pyplot(fig, width='stretch')

# Mostrar informações adicionais
col1, col2 = st.columns(2)

with col1:
    st.metric("Massa Real Planeta 1:", f"{M1_Real / conv_massa:.2f} M_Jup")
    st.metric("Massa Real Planeta 2:", f"{M2_Real / conv_massa:.2f} M_Jup")

with col2:
    st.metric("Semi-eixo Órbita 1:", f"{semi_eixo1:.2f} U.A.")
    st.metric("Semi-eixo Órbita 2:", f"{semi_eixo2:.2f} U.A.")

# with col3:
#     st.metric("Semi-eixo Maior", f"{semi_eixo1:.2f} UA")

# Explicação
with st.expander("ℹ️ Sobre este simulador"):
    st.markdown("""
    Este simulador mostra a **curva de velocidade radial** de uma estrela causada por um ou dois planetas.

    **Parâmetros:**
    - **Excentricidade**: Controla a forma da órbita (0 = circular, >0 = elíptica)
    - **Anomalia Verdadeira**: Posição inicial do planeta na órbita
    - **Argumento do Periastro**: Orientação da órbita
    - **Inclinação**: Inclinação do plano orbital (90° = órbita vista de lado)

    A curva mostra como a velocidade radial da estrela varia ao longo do tempo devido à atração gravitacional do planeta.
    """)
st.markdown("""
<div style='text-align: center; color: gray; font-size: 16px;'>
    PlanLab - Laboratório Planetário
</div>
""", unsafe_allow_html=True)