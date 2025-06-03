import streamlit as st 
from paginas.funcoes import inicializar_firebase, obter_perfil_usuario, atualizar_perfil_usuario, login_usuario, registrar_acao_usuario
import os # Importar os

# Inicializa o Firebase
inicializar_firebase() 

st.set_page_config(
    page_title="Maria Madalena - Conselheira do Amor",  # Novo Título
    page_icon="arquivos/avatar_assistente.jpg", # Alterado para usar o avatar do assistente
    layout='wide',                       # Melhor aproveitamento do espaço
    initial_sidebar_state="expanded"
)
 
# Estilo CSS personalizado
st.markdown("""
<style>
    .login-container {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        max-width: 500px;
        margin: auto;
    }
    .welcome-text {
        color: #1f1f1f;
        text-align: center;
    }
    .subtitle-text {
        color: #666;
        font-size: 1.1em;
        margin-bottom: 20px;
    }
    .terms-text {
        font-size: 0.75em;
        color: #888;
        margin-top: 15px;
        text-align: center;
        line-height: 1.4;
    }
    .terms-link {
        color: #3399FF; /* Cor azul para o link */
        text-decoration: none;
        cursor: pointer;
    }
    .terms-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)


# Verificação de login
if not hasattr(st.experimental_user, 'is_logged_in') or not st.experimental_user.is_logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo centralizada
        st.image('arquivos/capa.jpg', width=200, use_container_width=True)
        st.markdown('<h1 class="welcome-text">💕 Maria Madalena - Conselheira do Amor 💕</h1>', unsafe_allow_html=True) # Novo Texto
        st.markdown('<p class="subtitle-text" style="text-align: center;">Faça login com sua conta Google para conversar com sua conselheira amorosa pessoal.</p>', unsafe_allow_html=True) # Novo Texto
        # Botão de login
        if st.button("Login com Google", type="primary", use_container_width=True, icon=':material/login:'):
            # Registra o usuário no Firestore se for o primeiro acesso (login_usuario faz isso)
            # REMOVIDO DAQUI: login_usuario() 
            st.login() # Função de login do Streamlit (redireciona)
        
        # Carrega conteúdo dos Termos para o Popover
        termos_content = "Não foi possível carregar os Termos de Uso e Política de Privacidade."
        try:
            termos_path = os.path.join(os.path.dirname(__file__), 'termos_e_privacidade.md')
            with open(termos_path, 'r', encoding='utf-8') as file:
                termos_content = file.read()
        except Exception as e:
            print(f"Erro ao carregar termos em app.py: {e}") # Log do erro
            # Mantém a mensagem padrão de erro
            
        # Popover com os termos carregados
        with st.popover("Ao fazer login, você concorda com nossos Termos de Uso e Política de Privacidade", use_container_width=True):
            st.markdown(termos_content, unsafe_allow_html=True)
            
 
else:
    # Logo
    st.logo('arquivos/capa.jpg')

    # Garante que o usuário está registrado/atualizado no Firestore ANTES de obter o perfil
    login_usuario() # ADICIONADO AQUI

    # Verifica o perfil para o flag de primeiro acesso
    perfil = obter_perfil_usuario()

    if perfil and not perfil.get("primeiro_acesso_concluido", False):
        # --- Formulário de Primeiro Acesso ---
        st.title("💕 Bem-vinda à Maria Madalena!")
        st.info("Para eu te ajudar melhor nos assuntos do coração, preciso conhecer você um pouquinho. Me conta sobre você:")
        
        with st.form(key="primeiro_acesso_form", clear_on_submit=False):
            nome_completo = st.text_input("Como você gostaria de ser chamada(o)?", key="form_nome", placeholder="Seu nome ou apelido")
            idade = st.number_input("Qual sua idade?", min_value=16, max_value=120, key="form_idade")
            
            genero = st.selectbox("Como você se identifica quanto ao gênero?", [
                "Prefiro não informar",
                "Mulher cisgênero", 
                "Homem cisgênero",
                "Mulher transgênero",
                "Homem transgênero", 
                "Não-binário",
                "Outro"
            ], key="form_genero")
            
            orientacao_sexual = st.selectbox("Qual sua orientação sexual?", [
                "Prefiro não informar",
                "Heterossexual",
                "Homossexual",
                "Bissexual",
                "Pansexual",
                "Assexual",
                "Outro"
            ], key="form_orientacao")
            
            relacionamento_status = st.selectbox("Qual seu status de relacionamento atual?", [
                "Prefiro não informar",
                "Solteira(o)",
                "Namorando",
                "Casada(o)",
                "União estável",
                "Divorciada(o)",
                "Viúva(o)",
                "É complicado"
            ], key="form_relacionamento")
            
            # Checkbox de consentimento
            st.markdown("### 💝 Antes de começarmos!")
            st.markdown("Sou Maria Madalena, sua conselheira amorosa pessoal! Estou aqui para te ajudar com questões do coração, relacionamentos e autoestima. Lembre-se que sou uma IA e minhas respostas são para orientação geral - para questões mais sérias, sempre procure um profissional qualificado.")
            consentimento = st.checkbox("Entendo que Maria Madalena é uma IA conselheira para orientação geral em assuntos amorosos e que para questões mais complexas devo procurar um profissional qualificado!")
            
            # Botão sempre ativo
            submitted = st.form_submit_button("Começar nossa conversa! 💕", type="primary")
            
            if submitted:
                if not consentimento:
                    st.error("Querida(o), preciso que você entenda minha natureza de IA conselheira antes de começarmos! ❤️")
                elif not nome_completo or not idade:
                    st.warning("Por favor, me conte pelo menos seu nome e idade para podermos conversar! 😊")
                else:
                    dados_atualizar = {
                        "nome_completo": nome_completo,
                        "idade": idade,
                        "genero": genero,
                        "orientacao_sexual": orientacao_sexual,
                        "relacionamento_status": relacionamento_status,
                        "primeiro_acesso_concluido": True,
                        "consentimento_conselheira": True
                    }
                    if atualizar_perfil_usuario(dados_atualizar):
                        st.success("Perfeito! Agora já posso te ajudar melhor! Você será redirecionada para nossa conversa.")
                        st.balloons()
                        st.rerun() # Força o recarregamento da página para sair do form
                    else:
                        st.error("Ops! Houve um probleminha ao salvar seus dados. Tenta novamente, por favor.")
    
    elif perfil: # Primeiro acesso concluído ou perfil carregado corretamente
        # --- Navegação Principal do App ---
        
        # Define a estrutura das páginas para Maria Madalena (apenas 3 páginas)
        paginas = {
            "Maria Madalena": [
                st.Page("paginas/chatbot.py", title="💕 Conversar", icon='💬', default=True), 
            ],
            "Minha Conta": [ 
                st.Page("paginas/perfil.py", title="Meu Perfil", icon='👤'), 
                st.Page("paginas/termos.py", title="Termos e Privacidade", icon='📜'), 
            ]
        }

        # Usa a estrutura de páginas final 
        pg = st.navigation(paginas)
        pg.run()

        # --- Botão de Logout Global na Sidebar ---
        with st.sidebar:
            st.divider() # Adiciona um divisor antes do botão
            if st.button("Logout",
                         key="logout_button_global", # Chave diferente para evitar conflito
                         type='secondary',
                         icon=':material/logout:',
                         use_container_width=True):
                registrar_acao_usuario("Logout", "Usuário fez logout do sistema (botão global)")
                st.logout()

    else: # Caso o perfil não possa ser carregado após o login
        st.error("⚠️ Ops! Não consegui carregar seu perfil. Tenta fazer login novamente?")
        if st.button("Tentar novamente", type="primary"):
            st.rerun()
 