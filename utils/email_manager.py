import base64
import requests

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbxwXnxwgO1Qbjkj2FIxlZKsrQVIyiMJWa_2XUJeZI_XfA4pnV0lAiq7JAy6nCmgwpKlTA/exec"
EMAILS_COPIA = "rafaelasouza@magazineluiza.com.br, kemilly.silva@magazineluiza.com.br"

def gerar_linhas_html_tabela(lista_nd: list, lista_data: list, lista_campanha: list, parceiro: str) -> str:
    # Gera as linhas <tr> em HTML contendo os dados empilhados de todas as campanhas incluídas.
    linhas_html = ""
    for idx in range(len(lista_nd)):
        linhas_html += f"""
        <tr>
            <td style='border: 1px solid #333333; padding: 8px; text-align: center; font-weight: bold;'>{lista_nd[idx]}</td>
            <td style='border: 1px solid #333333; padding: 8px; text-align: center;'>{lista_data[idx]}</td>
            <td style='border: 1px solid #333333; padding: 8px; text-align: center;'>{parceiro.upper()}</td>
            <td style='border: 1px solid #333333; padding: 8px; text-align: center;'>{lista_campanha[idx]}</td>
        </tr>
        """
    return linhas_html

def construir_corpo_html(saudacao: str, titulo_tabela: str, num_nd: str, data_nota: str, nome_cliente: str, campanha: str) -> str:
    # Gera o design do e-mail em HTML aceitando injeção de linhas dinâmicas de tabelas (múltiplas notas).
    if str(num_nd).strip().startswith("<tr"):
        conteudo_tabela = num_nd
    else:
        conteudo_tabela = f"""
        <tr style="background-color: #FFFFFF; color: #000000;">
            <td style="padding: 8px; border: 1px solid #333333; font-weight: bold;">{num_nd}</td>
            <td style="padding: 8px; border: 1px solid #333333;">{data_nota}</td>
            <td style="padding: 8px; border: 1px solid #333333; text-align: center;">{nome_cliente}</td>
            <td style="padding: 8px; border: 1px solid #333333; text-align: center;">{campanha}</td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333; line-height: 1.6;">
        <p>{saudacao}</p>
        <p>Seguem anexos os relatórios, extratos e notas referente às notas de débito.</p>
        <p>A senha permanece a mesma do último fechamento.</p>
        
        <br>
        
        <table style="width: 100%; max-width: 900px; border-collapse: collapse; font-size: 12px; font-family: Arial, sans-serif; text-align: center;">
            <thead>
                <tr style="background-color: #1A3E62; color: white; font-weight: bold;">
                    <th colspan="4" style="padding: 8px; border: 1px solid #1A3E62; text-transform: uppercase;">
                        {titulo_tabela}
                    </th>
                </tr>
                <tr style="background-color: #1A3E62; color: white; font-weight: bold; font-size: 11px;">
                    <th style="padding: 8px; border: 1px solid #333333; width: 15%;">NOTA DE DÉBITO</th>
                    <th style="padding: 8px; border: 1px solid #333333; width: 15%;">DATA DA NOTA</th>
                    <th style="padding: 8px; border: 1px solid #333333; width: 35%;">NOME DO CLIENTE</th>
                    <th style="padding: 8px; border: 1px solid #333333; width: 35%;">DESCRIÇÃO CAMPANHA FIDELIDADE</th>
                </tr>
            </thead>
            <tbody>
                {conteudo_tabela}
            </tbody>
        </table>
        
        <p style="margin-top: 20px; color: #777777;">--</p>
    </body>
    </html>
    """
    return html

def disparar_email_automatico_nuvem(destinatario: str, assunto: str, corpo_html: str, zip_bytes: bytes, nome_zip: str):
    zip_base64 = base64.b64encode(zip_bytes).decode('utf-8')
    payload = {
        "destinatario": destinatario,
        "copia": EMAILS_COPIA,
        "assunto": assunto,
        "corpo": corpo_html,
        "nome_arquivo": nome_zip,
        "arquivo_base64": zip_base64
    }
    resposta = requests.post(WEBAPP_URL, json=payload)
    if resposta.status_code != 200 or "erro" in resposta.text:
        raise Exception(f"Falha na nuvem do Google: {resposta.text}")