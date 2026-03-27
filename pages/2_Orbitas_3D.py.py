import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(
    page_title="Órbitas 3D - Simulador",
    page_icon="🌌",
    layout="wide"
)

st.title("🌌 Simulador de Órbitas Planetárias 3D")
# st.markdown("Visualize e interaja com órbitas planetárias em um ambiente 3D completo.")

# Dividir em colunas
col1, col2 = st.columns([1000, 0.0000001])

with col1:
    try:
        with open('Plot_Orbitas3D.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Injetar script para melhor integração
        integration_script = """
        <script>
            // Comunicação com Streamlit (opcional)
            window.addEventListener('load', function() {
                console.log('Simulador 3D carregado no Streamlit');

                // Adicionar listener para eventos
                const sliders = document.querySelectorAll('input[type="range"]');
                sliders.forEach(slider => {
                    slider.addEventListener('input', function() {
                        // Aqui você pode enviar dados para o Streamlit se necessário
                        const data = {
                            type: 'param_change',
                            id: this.id,
                            value: this.value
                        };
                        console.log('Parâmetro alterado:', data);
                    });
                });
            });
        </script>
        """

        # Injetar script antes do fechamento do body
        html_content = html_content.replace('</body>', integration_script + '</body>')

        # Exibir componente
        components.html(
            html_content,
            height=750,
            scrolling=False
        )

    except FileNotFoundError:
        st.error("""
        ❌ **Arquivo não encontrado!**

        Certifique-se de que o arquivo `Plot_Orbitas3D.html` está na mesma pasta do aplicativo.

        Se você ainda não tem o arquivo, verifique se ele foi carregado corretamente no repositório.
        """)
    except Exception as e:
        st.error(f"❌ Erro ao carregar o simulador: {str(e)}")

# Adicionar um rodapé
# st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 16px;'>
    PlanLab - Laboratório Planetário
</div>
""", unsafe_allow_html=True)