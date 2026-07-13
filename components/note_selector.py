import streamlit as st
 
 
def renderizar_seletor_notas(opcoes_notas: list, mapeamento_notas: dict) -> tuple[list, list, list]:
    st.subheader("2. Selecione as Notas de Débito Ativas")
 
    if "quantidade_linhas_nd" not in st.session_state:
        st.session_state["quantidade_linhas_nd"] = 1
 
    lista_final_nd = []
    lista_final_data = []
    lista_final_campanha = []
 
    for i in range(st.session_state["quantidade_linhas_nd"]):
        st.markdown(f"### **📝 Item #{i+1}**")
        chave_seletor = f"seletor_nota_{i}"
 
        def atualizar_linha_especifica(index=i):
            nota_escolhida = st.session_state[f"seletor_nota_{index}"]
            dados_linha = mapeamento_notas[nota_escolhida]
            st.session_state[f"numero_nd_{index}"] = dados_linha["ND/NU"]
            st.session_state[f"data_nota_{index}"] = dados_linha["Data"]
            st.session_state[f"campanha_{index}"] = dados_linha["Campanha"]
 
        if chave_seletor not in st.session_state:
            primeira_nota = mapeamento_notas[opcoes_notas[0]]
            st.session_state[f"numero_nd_{i}"] = primeira_nota["ND/NU"]
            st.session_state[f"data_nota_{i}"] = primeira_nota["Data"]
            st.session_state[f"campanha_{i}"] = primeira_nota["Campanha"]
            st.session_state[chave_seletor] = opcoes_notas[0]
 
        st.selectbox(
            f"Pesquise digitando ou selecione a nota para o Item #{i+1}:",
            opcoes_notas,
            key=chave_seletor,
            on_change=atualizar_linha_especifica
        )
 
        col_a, col_b = st.columns([2, 2])
        with col_a:
            v_nd = st.text_input(f"Número da ND (Item {i+1}):", key=f"numero_nd_{i}")
        with col_b:
            v_data = st.text_input(f"📅 Data da Nota (Item {i+1}):", key=f"data_nota_{i}")
 
        v_campanha = st.text_input(f"📢Nome da Campanha (Item {i+1}):", key=f"campanha_{i}")
        st.markdown("---")
 
        lista_final_nd.append(v_nd)
        lista_final_data.append(v_data)
        lista_final_campanha.append(v_campanha)
 
    _render_note_buttons()
 
    return lista_final_nd, lista_final_data, lista_final_campanha
 
 
def _render_note_buttons():
    def adicionar_nova_linha():
        st.session_state["quantidade_linhas_nd"] += 1
 
    def remover_ultima_linha():
        ultimo_idx = st.session_state["quantidade_linhas_nd"] - 1
        for chave in [f"seletor_nota_{ultimo_idx}", f"numero_nd_{ultimo_idx}", f"data_nota_{ultimo_idx}", f"campanha_{ultimo_idx}"]:
            if chave in st.session_state:
                del st.session_state[chave]
        st.session_state["quantidade_linhas_nd"] -= 1
 
    col_btn1, col_btn2, _ = st.columns([2.5, 2, 4])
    with col_btn1:
        st.button("➕ Incluir outra campanha", on_click=adicionar_nova_linha, use_container_width=True)
    with col_btn2:
        if st.session_state["quantidade_linhas_nd"] > 1:
            st.button("❌ Remover Último Item", on_click=remover_ultima_linha, use_container_width=True)