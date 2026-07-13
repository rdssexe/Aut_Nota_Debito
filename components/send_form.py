import streamlit as st
from utils.file_manager import compactar_arquivos, gerar_nome_zip_limpo
from utils.email_manager import disparar_email_automatico_nuvem
 
 
def renderizar_envio_form(
    email_lojista: str,
    parceiro_selecionado: str,
    assunto_email: str,
    corpo_html_final: str,
    lista_final_nd: list,
):
    st.write("3. **Faça o upload dos documentos obrigatórios:**")
    arquivos_enviados = st.file_uploader(
        "Arraste a ND, o Extrato ND e o Relatório B2B juntos aqui:",
        accept_multiple_files=True,
    )
    if arquivos_enviados:
        st.write(f"📂 {len(arquivos_enviados)} arquivo(s) carregado(s).")
 
    st.divider()
 
    if st.button("Enviar"):
        erros = []
        if not any(lista_final_nd):
            erros.append("o número de pelo menos uma ND")
        if not arquivos_enviados:
            st.error("❌ Faltam informações: os arquivos obrigatórios.")
        if not email_lojista:
            erros.append("um e-mail válido")
 
        if erros:
            st.error(f"❌ Faltam informações: {', '.join(erros)}.")
        else:
            try:
                with st.spinner("Compactando documentos e realizando envio da tabela via API..."):
                    zip_bytes = compactar_arquivos(arquivos_enviados)
                    nome_zip = gerar_nome_zip_limpo(parceiro_selecionado)
 
                    disparar_email_automatico_nuvem(
                        destinatario=str(email_lojista),
                        assunto=assunto_email,
                        corpo_html=corpo_html_final,
                        zip_bytes=zip_bytes,
                        nome_zip=nome_zip
                    )
 
                st.success(f"🎉 Sucesso total! E-mail enviado com a tabela estruturada para {email_lojista}!")
                st.balloons()
                st.session_state["quantidade_linhas_nd"] = 1
                st.rerun()
            except Exception as e:
                st.error(f"❌ Falha ao tentar disparar e-mail automático: {e}")