import streamlit as st
from paginas.funcoes import obter_perfil_usuario, atualizar_perfil_usuario, registrar_acao_usuario

# Removido: st.set_page_config(layout="centered") 

st.title("💕 Meu Perfil - Maria Madalena")

# Estilo personalizado para o perfil
st.markdown("""
<style>
    .profile-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .profile-header {
        display: flex;
        align-items: center;
        margin-bottom: 30px;
    }
    .profile-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #fff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .profile-name {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin-left: 20px;
    }
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    .info-item {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .info-label {
        color: #7f8c8d;
        font-size: 14px;
        margin-bottom: 5px;
        font-weight: 600;
    }
    .info-value {
        color: #2c3e50;
        font-size: 16px;
        font-weight: 500;
    }
    .edit-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        border-left: 4px solid #e74c3c;
    }
</style>
""", unsafe_allow_html=True)

# Obter dados atuais do perfil
perfil = obter_perfil_usuario()
if perfil:
    # Container principal do perfil
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    
    # Cabeçalho do perfil com foto e nome
    st.markdown('<div class="profile-header">', unsafe_allow_html=True)
    
    # Foto do perfil
    foto_url = perfil.get("foto", "")
    if foto_url:
        st.markdown(f'<img src="{foto_url}" class="profile-avatar">', unsafe_allow_html=True)
    else:
        # Placeholder de avatar mais estilizado
        st.markdown('<div class="profile-avatar" style="background: linear-gradient(135deg, #e74c3c, #c0392b); display: flex; align-items: center; justify-content: center; font-size: 40px; color: white;">💕</div>', unsafe_allow_html=True)
    
    # Nome do usuário
    st.markdown(f'<div class="profile-name">{perfil.get("nome_completo", "Não informado")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Fecha profile-header
    
    # Grid de informações pessoais
    st.markdown('<div class="info-grid">', unsafe_allow_html=True)
    
    # Email
    st.markdown(f'''
        <div class="info-item">
            <div class="info-label">📧 Email</div>
            <div class="info-value">{perfil.get("email", "Não informado")}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Idade
    st.markdown(f'''
        <div class="info-item">
            <div class="info-label">🎂 Idade</div>
            <div class="info-value">{perfil.get("idade", "Não informada")} anos</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Gênero
    st.markdown(f'''
        <div class="info-item">
            <div class="info-label">👤 Identidade de Gênero</div>
            <div class="info-value">{perfil.get("genero", "Não informado")}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Orientação Sexual
    st.markdown(f'''
        <div class="info-item">
            <div class="info-label">🌈 Orientação Sexual</div>
            <div class="info-value">{perfil.get("orientacao_sexual", "Não informada")}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Status de Relacionamento
    st.markdown(f'''
        <div class="info-item">
            <div class="info-label">💝 Status de Relacionamento</div>
            <div class="info-value">{perfil.get("relacionamento_status", "Não informado")}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Data de cadastro
    if perfil.get("data_criacao"):
        from datetime import datetime
        try:
            if hasattr(perfil["data_criacao"], "date"):
                data_formatada = perfil["data_criacao"].date().strftime("%d/%m/%Y")
            else:
                data_formatada = perfil["data_criacao"]
        except:
            data_formatada = "Data não disponível"
        
        st.markdown(f'''
            <div class="info-item">
                <div class="info-label">📅 Membro desde</div>
                <div class="info-value">{data_formatada}</div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # Fecha info-grid
    st.markdown('</div>', unsafe_allow_html=True) # Fecha profile-card

    # Seção para editar informações
    st.markdown('<div class="edit-section">', unsafe_allow_html=True)
    st.markdown("### ✏️ Editar Minhas Informações")
    st.markdown("Aqui você pode atualizar suas informações pessoais para que Maria Madalena possa te ajudar melhor!")
    
    with st.expander("🔧 Clique aqui para editar suas informações", expanded=False):
        with st.form("editar_perfil"):
            col1, col2 = st.columns(2)
            
            with col1:
                novo_nome = st.text_input("Nome/Apelido", value=perfil.get("nome_completo", ""))
                nova_idade = st.number_input("Idade", min_value=16, max_value=120, value=int(perfil.get("idade", 18)))
                
                novo_genero = st.selectbox("Identidade de Gênero", [
                    "Prefiro não informar",
                    "Mulher cisgênero", 
                    "Homem cisgênero",
                    "Mulher transgênero",
                    "Homem transgênero", 
                    "Não-binário",
                    "Outro"
                ], index=0 if perfil.get("genero") in [None, "", "Não informado"] else [
                    "Prefiro não informar",
                    "Mulher cisgênero", 
                    "Homem cisgênero",
                    "Mulher transgênero",
                    "Homem transgênero", 
                    "Não-binário",
                    "Outro"
                ].index(perfil.get("genero", "Prefiro não informar")))
            
            with col2:
                nova_orientacao = st.selectbox("Orientação Sexual", [
                    "Prefiro não informar",
                    "Heterossexual",
                    "Homossexual",
                    "Bissexual",
                    "Pansexual",
                    "Assexual",
                    "Outro"
                ], index=0 if perfil.get("orientacao_sexual") in [None, "", "Não informada"] else [
                    "Prefiro não informar",
                    "Heterossexual",
                    "Homossexual",
                    "Bissexual",
                    "Pansexual",
                    "Assexual",
                    "Outro"
                ].index(perfil.get("orientacao_sexual", "Prefiro não informar")))
                
                novo_relacionamento = st.selectbox("Status de Relacionamento", [
                    "Prefiro não informar",
                    "Solteira(o)",
                    "Namorando",
                    "Casada(o)",
                    "União estável",
                    "Divorciada(o)",
                    "Viúva(o)",
                    "É complicado"
                ], index=0 if perfil.get("relacionamento_status") in [None, "", "Não informado"] else [
                    "Prefiro não informar",
                    "Solteira(o)",
                    "Namorando",
                    "Casada(o)",
                    "União estável",
                    "Divorciada(o)",
                    "Viúva(o)",
                    "É complicado"
                ].index(perfil.get("relacionamento_status", "Prefiro não informar")))
            
            if st.form_submit_button("💕 Salvar Alterações", type="primary", use_container_width=True):
                dados_atualizar = {
                    "nome_completo": novo_nome,
                    "idade": nova_idade,
                    "genero": novo_genero,
                    "orientacao_sexual": nova_orientacao,
                    "relacionamento_status": novo_relacionamento
                }
                
                if atualizar_perfil_usuario(dados_atualizar):
                    st.success("✅ Suas informações foram atualizadas com sucesso!")
                    st.info("💡 Maria Madalena agora pode te ajudar ainda melhor com essas informações atualizadas!")
                    registrar_acao_usuario("Atualizar Perfil", f"Usuário atualizou informações do perfil")
                    st.rerun()
                else:
                    st.error("❌ Houve um erro ao salvar suas informações. Tente novamente!")
    
    st.markdown('</div>', unsafe_allow_html=True) # Fecha edit-section
    
    # Informações sobre privacidade
    st.info("🔒 **Privacidade**: Suas informações pessoais são usadas apenas para personalizar os conselhos de Maria Madalena e nunca são compartilhadas com terceiros.")

else:
    st.error("⚠️ Não foi possível carregar as informações do seu perfil.")
    if st.button("🔄 Tentar Novamente", type="primary"):
        st.rerun()




