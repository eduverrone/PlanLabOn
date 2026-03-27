import streamlit as st

st.set_page_config(
    page_title="Simulador de Exoplanetas",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Página inicial
st.title("🪐 Simulador de Exoplanetas")
st.markdown("""
## Bem-vindo ao Simulador de Exoplanetas!

Esta aplicação oferece duas ferramentas complementares para explorar sistemas planetários:

### 📈 **Velocidade Radial**
Simule a curva de velocidade radial de uma estrela causada por um planeta em órbita.
- Ajuste parâmetros orbitais como excentricidade, inclinação e período
- Visualize como a amplitude da curva varia
- Ideal para entender o método de detecção de exoplanetas

### 🌌 **Órbitas 3D**
Visualize órbitas planetárias em um ambiente 3D interativo.
- Simule dois planetas orbitando uma estrela central
- Ajuste parâmetros orbitais em tempo real
- Visualize vetores de momento angular e inclinações
- Explore diferentes configurações orbitais

---

**Um projeto _PlanLab - Laboratório Planetário_**
""")

# Adicionar informações no sidebar
# st.sidebar.success("Selecione uma página acima para começar")
# st.sidebar.markdown("---")
# st.sidebar.markdown("### 📊 Sobre")
# st.sidebar.info(
#     "Este simulador foi desenvolvido para demonstração de conceitos de "
#     "mecânica orbital e detecção de exoplanetas."
# )