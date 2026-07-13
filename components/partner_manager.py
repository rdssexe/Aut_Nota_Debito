import streamlit as st
from utils.data_manager import buscar_email, buscar_nome_cliente, salvar_ou_atualizar_parceiro, COLUNA_NOME_EMAIL, COLUNA_PARCEIRO
import pandas as pd
 
 
def _buscar_nome_email_puro(df_contatos, parceiro: str) -> str:
    """Retorna APENAS o valor da coluna 'Nome_Cliente', sem fallback."""
    if COLUNA_NOME_EMAIL in df_contatos.columns:
        resultado = df_contatos[df_contatos[COLUNA_PARCEIRO] == parceiro]
        if not resultado.empty:
            val = resultado[COLUNA_NOME_EMAIL].values[0]
            if pd.notna(val) and str(val).strip():
                return str(val).strip()
    return ""
 
 
def renderizar_gerenciador_parceiros(df_contatos):
    with st.expander("🛠️ Cadastro e Edição de Parceiros/E-mails"):
        st.write("Adicione novos lojistas ou update e-mails da base de contatos de forma definitiva.")

        modo_gerenciador = st.radio(
            "Escolha a ação desejada:",
            ["✏️ Editar Parceiro Existente", "➕ Cadastrar Novo Parceiro"],
            horizontal=True
        )

        lista_atual_parceiros = sorted(df_contatos["Parceiro/Campanha"].dropna().unique())

        if modo_gerenciador == "✏️ Editar Parceiro Existente":
            parceiro_para_editar = st.selectbox("Selecione o parceiro que deseja alterar:", lista_atual_parceiros)
            email_atual = buscar_email(df_contatos, parceiro_para_editar) or ""
            nome_email_atual = _buscar_nome_email_puro(df_contatos, parceiro_para_editar)

            # Campo para editar o nome do parceiro na planilha
            novo_nome_input = st.text_input(
                f"Novo nome para '{parceiro_para_editar}' (deixe em branco para manter o atual):",
                value="",
                placeholder=parceiro_para_editar
            )

            # Campo para definir o nome que aparece no corpo do e-mail (Coluna Nome_Cliente)
            novo_nome_email_input = st.text_input(
                f"Nome do cliente no e-mail (atual: '{nome_email_atual or 'não definido'}'):",
                value="",
                placeholder=nome_email_atual or parceiro_para_editar
            )

            novo_email_input = st.text_input(
                f"Digite o novo e-mail para {parceiro_para_editar}:",
                value=str(email_atual)
            )

            if st.button("💾 Salvar Alteração no Excel"):
                if not novo_email_input.strip():
                    st.error("❌ O e-mail não pode ficar em branco.")
                else:
                    try:
                        novo_nome       = novo_nome_input.strip() if novo_nome_input.strip() else None
                        # Captura o valor digitado no input ou mantém o atual se ficar em branco
                        novo_nome_email = novo_nome_email_input.strip() if novo_nome_email_input.strip() else (nome_email_atual or None)
                        
                        salvar_ou_atualizar_parceiro(parceiro_para_editar, novo_email_input, novo_nome, novo_nome_email)

                        nome_exibido = novo_nome or parceiro_para_editar
                        st.success(f"🎉 Sucesso! O parceiro '{nome_exibido}' foi atualizado!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Erro ao salvar: {ex}")

        elif modo_gerenciador == "➕ Cadastrar Novo Parceiro":
            novo_parceiro_nome = st.text_input("Nome do Novo Parceiro / Campanha:")
            novo_parceiro_nome_email = st.text_input(
                "Nome do cliente no e-mail (opcional, vai para a coluna 'Nome_Cliente'):",
                placeholder="Ex: Magazine Luiza"
            )
            novo_parceiro_email = st.text_input("E-mail(s) do Novo Parceiro (separe por vírgula se for mais de um):")

            if st.button("➕ Confirmar Novo Cadastro"):
                if not novo_parceiro_nome.strip() or not novo_parceiro_email.strip():
                    st.error("❌ Preencha tanto o nome do parceiro quanto o e-mail corporativo.")
                elif novo_parceiro_nome.strip().upper() in [p.upper() for p in lista_atual_parceiros]:
                    st.error("⚠️ Este parceiro já existe! Use a opção 'Editar Parceiro Existente'.")
                else:
                    try:
                        nome_email = novo_parceiro_nome_email.strip() if novo_parceiro_nome_email.strip() else None
                        # Passa o nome_email explicitamente para salvar na nova coluna
                        salvar_ou_atualizar_parceiro(novo_parceiro_nome, novo_parceiro_email, novo_nome_email=nome_email)
                        st.success(f"🎉 Parceiro '{novo_parceiro_nome}' cadastrado com sucesso direto na planilha!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Erro ao cadastrar: {ex}")