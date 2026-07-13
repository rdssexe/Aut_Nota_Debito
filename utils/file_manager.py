import io
import zipfile
import openpyxl
import msoffcrypto
import unicodedata
import re
 
 
def compactar_arquivos(arquivos, senha_excel: str = "nd2025") -> bytes:
    # Compacta os arquivos enviados pelo Streamlit em um (.ZIP)
    # Identifica se o arquivo é um Excel (.xlsx) e aplica a senha de proteção nele automaticamente.
    buffer_zip = io.BytesIO()
    with zipfile.ZipFile(buffer_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for arquivo in arquivos:
            nome_arquivo = arquivo.name
            conteudo_arquivo = arquivo.getvalue()
            # 1. Definimos que, por padrão, o conteúdo final é o arquivo original
            conteudo_final = conteudo_arquivo
 
            # Se o arquivo terminar com .xlsx (Excel), o sistema vai agir nele
            if nome_arquivo.lower().endswith(".xlsx"):
                try:
                    # Primeiro protege as abas com openpyxl
                    wb = openpyxl.load_workbook(io.BytesIO(conteudo_arquivo))
                    for aba in wb.worksheets:
                        aba.protection.password = senha_excel
                        aba.protection.enable()
                    buffer_sem_senha = io.BytesIO()
                    wb.save(buffer_sem_senha)
                    wb.close()
                    buffer_sem_senha.seek(0)
 
                    # Depois criptografa o arquivo com senha de abertura
                    buffer_com_senha = io.BytesIO()
                    office_file = msoffcrypto.OfficeFile(buffer_sem_senha)
                    office_file.encrypt(senha_excel, buffer_com_senha)
 
                    # 2. Atualizamos o conteúdo final com os bytes do arquivo já protegido
                    conteudo_final = buffer_com_senha.getvalue()
                except Exception as e:
                    # Se der erro, avisa no terminal mas mantém o arquivo original seguro
                    print(f"Erro na proteção do arquivo {nome_arquivo}: {e}")
                    conteudo_final = conteudo_arquivo
 
            # Grava o arquivo na estrutura do .ZIP (garantindo que vai com a senha se for Excel)
            zf.writestr(nome_arquivo, conteudo_final)
 
    buffer_zip.seek(0)
    return buffer_zip.read()
 
 
def gerar_nome_zip_limpo(nome_parceiro):
    """Remove acentos, espaços e caracteres especiais para não quebrar a API do Google."""
    # 1. Transforma em letras maiúsculas e remove espaços nas pontas
    nome = str(nome_parceiro).strip().upper()
    # 2. Remove acentos (Ex: MÁGICA vira MAGICA)
    nome = ''.join(c for c in unicodedata.normalize('NFD', nome) if unicodedata.category(c) != 'Mn')
    # 3. Substitui espaços normais por underlines (_)
    nome = nome.replace(" ", "_")
    # 4. Remove QUALQUER coisa que não seja letra, número ou underline (deleta barras, aspas, etc.)
    nome = re.sub(r'[^A-Z0-9_]', '', nome)
    # 5. Retorna o nome limpo com a extensão .zip
    return f"ND_{nome}.zip"  
