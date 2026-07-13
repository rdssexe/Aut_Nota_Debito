from datetime import datetime
import pandas as pd
import streamlit as st
 
ARQUIVO_EMAILS    = "cadastro_parceiros.xlsx"
ABA_LOCAL_EMAILS  = "ND - CORRETO"
COLUNA_PARCEIRO   = "Parceiro/Campanha"
COLUNA_EMAIL      = "Destinatário"
COLUNA_NOME_EMAIL = "Nome_Cliente"
 
ARQUIVO_NOTAS = "notas_debito.xlsx"
 
DICIONARIO_MESES = {
    "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
    "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
    "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
}
 
@st.cache_data
def carregar_contatos_locais() -> pd.DataFrame:
    df = pd.read_excel(ARQUIVO_EMAILS, sheet_name=ABA_LOCAL_EMAILS)
    return df
 
@st.cache_data
def carregar_notas_debito() -> pd.DataFrame:
    try:
        df = pd.read_excel(ARQUIVO_NOTAS)
        for col in ["ND/NU", "Data", "Parceiro", "Campanha"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        df = df.drop_duplicates(subset=["ND/NU", "Data", "Parceiro", "Campanha"])
        return df
    except Exception as e:
        raise Exception(f"Erro ao abrir o arquivo {ARQUIVO_NOTAS}: {e}")
 
def buscar_email(df_contatos: pd.DataFrame, parceiro: str) -> str | None:
    resultado = df_contatos[df_contatos[COLUNA_PARCEIRO] == parceiro]
    if not resultado.empty:
        return resultado[COLUNA_EMAIL].values[0]
    return None
 
def buscar_nome_cliente(df_contatos: pd.DataFrame, parceiro: str) -> str:
    """Busca o nome customizado na coluna Nome_Cliente. Se estiver vazio, usa o próprio nome do parceiro."""
    if COLUNA_NOME_EMAIL in df_contatos.columns:
        resultado = df_contatos[df_contatos[COLUNA_PARCEIRO] == parceiro]
        if not resultado.empty:
            nome_email = resultado[COLUNA_NOME_EMAIL].values[0]
            if pd.notna(nome_email) and str(nome_email).strip():
                return str(nome_email).strip()
    return parceiro
 
def obter_saudacao() -> str:
    hora_atual = datetime.now().hour
    return "Bom dia!" if hora_atual < 12 else "Boa tarde!"
 
def identificar_periodo_tabela(data_nota_formatada: str) -> tuple[str, str]:
    mes_identificado = DICIONARIO_MESES[datetime.now().strftime("%m")]
    ano_identificado = str(datetime.now().year)
    quinzena_texto = "1ª QUINZENA"
 
    if data_nota_formatada:
        data_limpa = str(data_nota_formatada).strip()
        try:
            if "-" in data_limpa and len(data_limpa.split("-")) == 3:
                partes = data_limpa.split("-")
                ano_identificado = partes[0]
                mes_numero = partes[1]
                dia_da_nota = int(partes[2])
            elif "/" in data_limpa and len(data_limpa.split("/")) == 3:
                partes = data_limpa.split("/")
                dia_da_nota = int(partes[0])
                mes_numero = partes[1]
                ano_identificado = partes[2]
            else:
                dia_da_nota = datetime.now().day
                mes_numero = datetime.now().strftime("%m")
 
            if mes_numero in DICIONARIO_MESES:
                mes_identificado = DICIONARIO_MESES[mes_numero]
 
            quinzena_texto = "1ª QUINZENA" if dia_da_nota <= 15 else "2ª QUINZENA"
        except:
            pass
 
    titulo_periodo = f"{quinzena_texto} DE {mes_identificado.upper()} - {ano_identificado}"
    return titulo_periodo, mes_identificado
 
def processar_regras_assunto(parceiro_selecionado: str, numero_nd: str, mes_selecionado: str) -> str:
    if "GLOBAL REWARD" in str(parceiro_selecionado).upper():
        nd_print = numero_nd if numero_nd else "[NÚMERO DA ND]"
        return f"{mes_selecionado.upper()} | Notas de débito {nd_print}"
 
    texto_quinzena = "Primeira Quinzena"
    if "2ª QUINZENA" in st.session_state.get("titulo_periodo_tabela_memoria", ""):
        texto_quinzena = "Segunda Quinzena"
 
    mes_final = str(mes_selecionado).strip().title()
    return f"Nota de débito - {texto_quinzena} de {mes_final} - {str(parceiro_selecionado).upper()}"
 
def salvar_ou_atualizar_parceiro(nome_parceiro: str, novo_email: str, novo_nome: str = None, novo_nome_email: str = None):
    import openpyxl
 
    nome_parceiro_limpo   = str(nome_parceiro).strip()
    novo_email_limpo      = str(novo_email).strip()
    novo_nome_limpo       = str(novo_nome).strip() if novo_nome else None
    novo_nome_email_limpo = str(novo_nome_email).strip() if novo_nome_email else None
 
    wb = openpyxl.load_workbook(ARQUIVO_EMAILS)
    if ABA_LOCAL_EMAILS in wb.sheetnames:
        ws = wb[ABA_LOCAL_EMAILS]
    else:
        ws = wb.create_sheet(title=ABA_LOCAL_EMAILS)
        ws.append([COLUNA_PARCEIRO, COLUNA_EMAIL, COLUNA_NOME_EMAIL])
 
    headers = {ws.cell(row=1, column=col).value: col for col in range(1, ws.max_column + 1)}
 
    col_parceiro_idx   = headers.get(COLUNA_PARCEIRO)
    col_email_idx      = headers.get(COLUNA_EMAIL)
    col_nome_email_idx = headers.get(COLUNA_NOME_EMAIL)
 
    if not col_parceiro_idx or not col_email_idx:
        col_parceiro_idx = 1
        col_email_idx = 2
 
    # Cria a coluna "Nome no Email" no final se não existir
    if not col_nome_email_idx:
        col_nome_email_idx = ws.max_column + 1
        ws.cell(row=1, column=col_nome_email_idx).value = COLUNA_NOME_EMAIL
 
    parceiro_encontrado = False
    for row in range(2, ws.max_row + 1):
        celula_parceiro = ws.cell(row=row, column=col_parceiro_idx).value
        if celula_parceiro and str(celula_parceiro).strip().upper() == nome_parceiro_limpo.upper():
            ws.cell(row=row, column=col_email_idx).value = novo_email_limpo
            if novo_nome_limpo:
                ws.cell(row=row, column=col_parceiro_idx).value = novo_nome_limpo
            if novo_nome_email_limpo:
                ws.cell(row=row, column=col_nome_email_idx).value = novo_nome_email_limpo
            parceiro_encontrado = True
            break
 
    if not parceiro_encontrado:
        proxima_linha = ws.max_row + 1
        ws.cell(row=proxima_linha, column=col_parceiro_idx).value = novo_nome_limpo or nome_parceiro_limpo
        ws.cell(row=proxima_linha, column=col_email_idx).value = novo_email_limpo
        if novo_nome_email_limpo:
            ws.cell(row=proxima_linha, column=col_nome_email_idx).value = novo_nome_email_limpo
 
    wb.save(ARQUIVO_EMAILS)
    wb.close()
    carregar_contatos_locais.clear()