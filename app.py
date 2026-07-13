import streamlit as st
 
from utils.data_manager import (
    carregar_contatos_locais,
    carregar_notas_debito,
    buscar_email,
    buscar_nome_cliente,
    obter_saudacao,
    identificar_periodo_tabela,
    processar_regras_assunto,
)
from utils.email_manager import construir_corpo_html, gerar_linhas_html_tabela
from components.partner_manager import renderizar_gerenciador_parceiros
from components.note_selector import renderizar_seletor_notas
from components.send_form import renderizar_envio_form
from components.preview import renderizar_preview
 
st.set_page_config(page_title="Automação de Envios - B2B", page_icon="🤖")
st.title("Envio de Notas de Débito")
st.write("Selecione o parceiro para o e-mail e as notas ativas para preenchimento dinâmico.")
 
# 1. Carregamento das planilhas
df_contatos = None
df_notas = None
try:
    df_contatos = carregar_contatos_locais()
    df_notas = carregar_notas_debito()
    st.success("Planilhas de parceiros e notas carregadas com sucesso!")
except Exception as e:
    st.error(f"❌ Erro ao ler arquivos de configuração: {e}")
    st.stop()
 
# 2. Gerenciador de parceiros
renderizar_gerenciador_parceiros(df_contatos)
 
st.divider()
 
# 3. Seleção do parceiro e e-mail
st.subheader("1. Selecione o Parceiro para buscar o Destinatário")
lista_parceiros_base = sorted(df_contatos["Parceiro/Campanha"].dropna().unique())
parceiro_selecionado = st.selectbox("Selecione o Parceiro (Lojista):", lista_parceiros_base)
 
email_lojista = buscar_email(df_contatos, parceiro_selecionado)
if email_lojista:
    st.info(f"📧 **E-mail do lojista identificado:** {str(email_lojista).replace(chr(10), ' | ')}")
else:
    st.warning(f"⚠️ Nenhum e-mail encontrado na base de contatos para {parceiro_selecionado}.")
 
# 4. Mapeamento das notas
opcoes_notas = []
mapeamento_notas = {}
for idx, linha in df_notas.iterrows():
    texto_formatado = f"{linha['ND/NU']} | {linha['Parceiro']} | {linha['Campanha']}"
    opcoes_notas.append(texto_formatado)
    mapeamento_notas[texto_formatado] = linha
 
if not opcoes_notas:
    st.error("⚠️ A planilha notas_debito.xlsx está vazia ou não pôde ser lida.")
    st.stop()
 
# 5. Seleção das notas
lista_final_nd, lista_final_data, lista_final_campanha = renderizar_seletor_notas(opcoes_notas, mapeamento_notas)
 
st.divider()
 
# 6. Montagem do conteúdo do e-mail
titulo_periodo_tabela, mes_identificado = identificar_periodo_tabela(lista_final_data[0] if lista_final_data else "")
st.session_state["titulo_periodo_tabela_memoria"] = titulo_periodo_tabela

nd_assunto_texto = ", ".join(filter(None, lista_final_nd))
assunto_email = processar_regras_assunto(parceiro_selecionado, nd_assunto_texto, mes_identificado)
 
# 1. Buscamos o nome tratado da nova coluna 'Nome_Cliente' primeiro
nome_cliente_tratado = buscar_nome_cliente(df_contatos, parceiro_selecionado).upper()

# 2. Passamos esse nome tratado para gerar as linhas da tabela interna do HTML
linhas_html_dinamicas = gerar_linhas_html_tabela(lista_final_nd, lista_final_data, lista_final_campanha, nome_cliente_tratado)

# 3. Construímos o corpo do e-mail
corpo_html_final = construir_corpo_html(
    saudacao=obter_saudacao(),
    titulo_tabela=titulo_periodo_tabela,
    num_nd=linhas_html_dinamicas,
    data_nota="",
    nome_cliente=nome_cliente_tratado,
    campanha=""
)
 
# 7. Upload e envio
renderizar_envio_form(email_lojista, parceiro_selecionado, assunto_email, corpo_html_final, lista_final_nd)
 
# 8. Pré-visualização
renderizar_preview(email_lojista, assunto_email, titulo_periodo_tabela, corpo_html_final)