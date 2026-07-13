import streamlit as st
from utils.email_manager import EMAILS_COPIA
 
 
def renderizar_preview(
    email_lojista: str,
    assunto_email: str,
    titulo_periodo_tabela: str,
    corpo_html_final: str,
):
    st.divider()
    st.subheader("Pré-visualização do Conteúdo")
    with st.container(border=True):
        st.write(f"**📬 Para:** {email_lojista or '---'}")
        st.write(f"**👥 Em Cópia Fixa:** {EMAILS_COPIA}")
        st.write(f"**📌 Assunto Gerado:** {assunto_email}")
        st.write(f"**🔮 Período e Mês Extraídos:** `{titulo_periodo_tabela}`")
        st.write("**📊 Visualização da Tabela Corporativa:**")
        st.markdown(corpo_html_final, unsafe_allow_html=True)
 