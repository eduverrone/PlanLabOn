import streamlit as st

st.set_page_config(
    page_title="Sobre - Simulador",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Sobre o Simulador de Exoplanetas")

st.markdown("""
## 🌟 Visão Geral

Este projeto é um simulador educacional interativo para explorar conceitos de mecânica orbital e detecção de exoplanetas.

### 🎯 Objetivos Educacionais

- Visualizar órbitas planetárias em 3D
- Entender o método da velocidade radial para detecção de exoplanetas
- Explorar como parâmetros orbitais afetam as curvas de velocidade radial
- Compreender vetores de momento angular e inclinações orbitais

### 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para criação da interface web
- **Three.js**: Biblioteca JavaScript para renderização 3D
- **Matplotlib**: Geração de gráficos de velocidade radial
- **NumPy**: Cálculos numéricos

### 📊 Modelos Físicos Implementados

#### Velocidade Radial
A curva de velocidade radial é calculada usando:
- Leis de Kepler para movimento orbital
- Equação da semi-amplitude K
- Transformações para velocidade radial observada

#### Órbitas 3D
O simulador 3D implementa:
- Órbitas elípticas completas com parâmetros keplerianos
- Transformações de coordenadas 3D
- Cálculo e visualização de vetores de momento angular
- Plano perpendicular ao momento angular total

### 🔬 Referências

- [Kepler's Laws of Planetary Motion](https://en.wikipedia.org/wiki/Kepler%27s_laws_of_planetary_motion)
- [Radial Velocity Method](https://en.wikipedia.org/wiki/Doppler_spectroscopy)
- [Orbital Mechanics](https://en.wikipedia.org/wiki/Orbital_mechanics)

---

Desenvolvido para fins educacionais e demonstração de conceitos astronômicos.
""")

# Adicionar informações de contato
# st.sidebar.success("Selecione uma página acima para explorar!")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 16px;'>
    PlanLab - Laboratório Planetário
</div>
""", unsafe_allow_html=True)