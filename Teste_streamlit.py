import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constantes
radianos = np.pi / 180
conv_massa = 9.5464e-4
conv_vel = 149597870700.0 / (365 * 24 * 3600)


def semi_amplitude_K(a, M_min, M_total, P, e):
    num = 2.0 * np.pi * a * M_min
    den = M_total * P * np.sqrt(1.0 - e * e)
    return num / den


def velocidade_radial(m, a, e, T, M_t, f, w, i, t):
    M_min = m * np.sin(i * radianos)
    K = semi_amplitude_K(a, M_min, M_t, T, e)
    return K * (np.cos(2 * np.pi * t / T + (f + w) * radianos) + e * np.cos(w * radianos)) * conv_vel


# Configuração da página
st.set_page_config(
    page_title="Velocidade Radial Simulator",
    page_icon="🪐",
    layout="wide"
)

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

# Parâmetros fixos
MC = 1.38  # Massa da estrela em massas solares
M1 = 1 * conv_massa  # Massa do planeta em massas solares
a1 = 1  # Semi-eixo maior em UA
T1 = 1  # Período em anos

# Time array
t = np.linspace(0, 3, 300)

# Sidebar com controles
st.sidebar.header("Parâmetros Orbitais")

ecc = st.sidebar.slider(
    "Excentricidade",
    min_value=0.0,
    max_value=0.99,
    value=0.3,
    step=0.01,
    help="Excentricidade da órbita (0 = circular, 1 = parabólica)"
)

f_anom = st.sidebar.slider(
    "Anomalia Verdadeira [deg]",
    min_value=0,
    max_value=360,
    value=0,
    step=1,
    help="Posição angular do planeta na órbita"
)

w_arg = st.sidebar.slider(
    "Argumento do Periastro [deg]",
    min_value=0,
    max_value=360,
    value=0,
    step=1,
    help="Orientação da órbita"
)

inc = st.sidebar.slider(
    "Inclinação [deg]",
    min_value=0,
    max_value=180,
    value=90,
    step=1,
    help="Inclinação do plano orbital"
)

# Parâmetros adicionais (opcionais - expandir)
with st.sidebar.expander("Outros Parâmetros"):
    MC = st.number_input(
        "Massa da Estrela [M_Solar]",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        help="Massa da estrela em massas do Sol"
    )

    massa_planeta = st.number_input(
        "Massa do Planeta [M_Jup]",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        help="Massa do planeta em massas de Júpiter"
    ) * conv_massa

    periodo = st.number_input(
        "Período Orbital [anos]",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="Tempo para completar uma órbita"
    )
    mu1 = 4.0*np.pi**2 * (MC + massa_planeta)
    semi_eixo = ((periodo**2 * mu1) / (4 * np.pi ** 2)) ** (1 / 3)

# Calcular a curva de velocidade radial
rv = velocidade_radial(massa_planeta, semi_eixo, ecc, periodo, MC, f_anom, w_arg, inc, t)

# Criar o gráfico com tamanho controlado
fig, ax = plt.subplots(figsize=(9, 5.4))  # Ajuste conforme desejar (9:5.4 mantém proporção)
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
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.pyplot(fig, width='stretch')

# Mostrar informações adicionais
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Massa do Planeta", f"{massa_planeta / conv_massa:.2f} M_Jup")

with col2:
    st.metric("Período Orbital", f"{periodo:.2f} anos")

with col3:
    st.metric("Semi-eixo Maior", f"{semi_eixo:.2f} UA")

# Explicação
with st.expander("ℹ️ Sobre este simulador"):
    st.markdown("""
    Este simulador mostra a **curva de velocidade radial** de uma estrela causada por um planeta orbitando.

    **Parâmetros:**
    - **Excentricidade**: Controla a forma da órbita (0 = circular, >0 = elíptica)
    - **Anomalia Verdadeira**: Posição inicial do planeta na órbita
    - **Argumento do Periastro**: Orientação da órbita
    - **Inclinação**: Inclinação do plano orbital (90° = órbita vista de lado)

    A curva mostra como a velocidade radial da estrela varia ao longo do tempo devido à atração gravitacional do planeta.
    """)