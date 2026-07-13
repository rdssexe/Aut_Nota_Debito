🤖 Automação de Notas de Débito — B2B
Sistema interno para envio automatizado de e-mails com notas de débito para parceiros/lojistas, desenvolvido em Python com Streamlit.

📋 O que o sistema faz

Carrega a base de parceiros e e-mails a partir de uma planilha Excel
Permite cadastrar e editar parceiros diretamente pela interface
Monta uma tabela HTML corporativa com as notas de débito selecionadas
Compacta os documentos anexos em .zip (com proteção por senha nos arquivos .xlsx)
Dispara o e-mail automaticamente via integração com serviço em nuvem


🗂️ Estrutura do Projeto
AUTOMAÇÃO/
├── .streamlit/
│   └── config.toml          # Configurações visuais do Streamlit
├── components/              # Blocos de interface (UI)
│   ├── __init__.py
│   ├── partner_manager.py   # Expander de cadastro e edição de parceiros
│   ├── note_selector.py     # Seleção dinâmica de notas de débito
│   ├── send_form.py         # Upload de arquivos e botão de envio
│   └── preview.py           # Pré-visualização do e-mail antes do envio
├── utils/                   # Funções de negócio (sem interface)
│   ├── __init__.py
│   ├── data_manager.py      # Leitura, busca e escrita nas planilhas Excel
│   ├── email_manager.py     # Montagem do HTML e disparo do e-mail
│   └── file_manager.py      # Compactação e proteção dos arquivos ZIP
├── app.py                   # Orquestrador principal da aplicação
├── cadastro_parceiros.xlsx  # Base de parceiros e e-mails
├── notas_debito.xlsx        # Base de notas de débito ativas
├── Requirements.txt         # Dependências do projeto
└── README.md

⚙️ Requisitos

Python 3.10 ou superior
Pip atualizado

Instalação das dependências
bashpip install -r Requirements.txt

▶️ Como rodar
Dentro da pasta do projeto, execute:
bashstreamlit run app.py
O sistema abrirá automaticamente no navegador em http://localhost:8501.

📁 Planilhas de Configuração
cadastro_parceiros.xlsx
Contém a base de parceiros e seus respectivos e-mails de destino.
ColunaDescriçãoParceiro/CampanhaNome do parceiro/lojistaDestinatárioE-mail(s) de destino (separados por vírgula se mais de um)

A aba utilizada é ND - CORRETO. Não renomeie nem exclua essa aba.

notas_debito.xlsx
Contém as notas de débito disponíveis para seleção no sistema.
ColunaDescriçãoND/NUNúmero da nota de débitoDataData da nota (aceita formato DD/MM/AAAA ou AAAA-MM-DD)ParceiroNome do parceiro vinculadoCampanhaDescrição da campanha

🔄 Fluxo de Uso

Selecione o parceiro/lojista — o sistema busca o e-mail automaticamente
Selecione as notas de débito ativas — é possível adicionar múltiplas
Faça o upload dos documentos obrigatórios (ND, Extrato ND, Relatório B2B)
Confira a pré-visualização do e-mail no final da página
Clique em Enviar — o sistema compacta os arquivos e dispara o e-mail


🔒 Segurança dos Arquivos
Todos os arquivos .xlsx anexados são automaticamente protegidos por senha antes de serem compactados no .zip. A senha padrão é definida internamente no file_manager.py.

Para alterar a senha padrão, edite o parâmetro senha_excel na função compactar_arquivos() em utils/file_manager.py.


📧 E-mails em Cópia Fixa
Há endereços de e-mail configurados como cópia fixa em todos os envios. Para alterá-los, edite a variável EMAILS_COPIA no arquivo utils/email_manager.py.

🛠️ Manutenção
Adicionar um novo parceiro
Use o expander "Cadastro e Edição de Parceiros/E-mails" diretamente na interface — não é necessário editar a planilha manualmente.
Adicionar uma nova nota de débito
Insira uma nova linha na planilha notas_debito.xlsx com as colunas ND/NU, Data, Parceiro e Campanha preenchidas, e reinicie a aplicação.
Alterar o layout do e-mail
O template HTML do e-mail está na função construir_corpo_html() em utils/email_manager.py.

📦 Dependências Principais
BibliotecaVersãoUsostreamlit1.57.0Interface webpandas3.0.3Leitura e manipulação das planilhasopenpyxl3.1.5Leitura e escrita dos arquivos .xlsxrequests2.34.2Disparo do e-mail via APInumpy2.4.5Suporte ao pandaspython-dateutil2.9.0Tratamento de datas