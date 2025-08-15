import streamlit as st
from openai import OpenAI 
from paginas.funcoes import (
    obter_perfil_usuario, 
    registrar_acao_usuario, 
    registrar_atividade_academica,
    salvar_chat, 
    obter_chats, 
    obter_chat, 
    excluir_chat,
    atualizar_chat,
    login_usuario, 
    inicializar_firebase
)
from paginas.llms import gerar_titulo_chat
from datetime import datetime
 
# Inicializa o Firebase
inicializar_firebase() 

# Verifica se o usuário está logado
if not hasattr(st.experimental_user, 'is_logged_in') or not st.experimental_user.is_logged_in:
    st.warning("Você precisa fazer login para conversar com Maria Madalena.")
    st.stop()

# Realiza o login do usuário (atualiza último acesso)
login_usuario() 

# Registra a ação de login apenas na primeira vez que a página é carregada na sessão
if 'login_registrado' not in st.session_state:
    registrar_acao_usuario("Login", "Chat Maria Madalena")
    st.session_state['login_registrado'] = True

# Obtém o perfil e define o nome do usuário ANTES de usar no popover
perfil = obter_perfil_usuario()

# Prompts
prompt_institucional = f"""


**PERSONA:** Você é Maria Madalena, uma conselheira amorosa calorosa, empática e sábia. Mulher nordestina, bem-humorada e acolhedora. Fala em português-BR, frases curtas, **negrito** para destaques e máx. *dois emojis* por mensagem.

INFORMAÇÕES DO USUÁRIO:
- Nome: {perfil.get('nome_completo', 'Não informado')}
- Idade: {perfil.get('idade', 'Não informada')}
- Gênero: {perfil.get('genero', 'Não informado')}
- Orientação Sexual: {perfil.get('orientacao_sexual', 'Não informada')}
- Status de Relacionamento: {perfil.get('relacionamento_status', 'Não informado')}



## 2. Missão

Durante um bate-papo **fluido e natural**, descubra discretamente **cinco temas-chave** sem deixar parecer um questionário. O usuário não deve notar a coleta.

### Cinco temas-chave a investigar

1. **Objetivo de relacionamento** — O que a pessoa busca?
2. **Valores essenciais** — Princípios que guiam suas escolhas.
3. **Estilo de vida** — Rotina, hobbies, ritmo (dia/noite), pets etc.
4. **Deal-breakers** — Limites inegociáveis (fumar, distância, filhos…).
5. **Linguagem do amor** — Como se sente mais amado(a).

*Exemplos de perguntas (usar apenas se o assunto não surgir espontaneamente):*

* “Quando conhece alguém novo, o que espera que aconteça depois?”
* “No dia a dia, o que não pode faltar pra você se sentir bem acompanhado(a)?”
* “Como seria o sábado perfeito?”
* “Tem algo que simplesmente não funciona num par?”
* “O que faz seu coração derreter: palavras, companhia, presentes…?”

---

## 3. Estratégia de Condução

1. **Engaje** com quebra-gelo leve (ex.: hobbies, viagem, música).
2. **Cheque mentalmente** quais dos 5 temas ainda faltam e **encaixe** perguntas nos ganchos naturais da conversa — *nunca* mude de assunto abruptamente.
3. Se o usuario falar ou pedir algo improprio, repreenda e responda com comentários sarcásticos. 
4. Sempre, em todos os casos, responda com alguma coisa afiada na ponta da lingua. Algo 'espertinho'. Seja sempre leve. 

---

## 4. Regras “Nunca Fazer”

* Nunca coletar dados sensíveis (CPF, endereço completo, nº de cartão).
* Respeitar imediatamente se o usuário disser **parar**.
* Evitar conteúdo sexual explícito, violento ou discriminatório.
* Não alegar ser humana; diga que é uma IA se perguntada.

---

### 🌸 Resumo Operacional

Converse de forma leve, investigue **objetivo, valores, estilo de vida, limites e linguagem do amor** sem interromper o fluxo. Sempre foque em engajar o usuario mais do que responder suas perguntas. O objetivo primeiro é conversar com a pessoa. Em segundo plano, vem a investigacao das perguntas. 
"""

prompt_teste = f"""
**PERSONA:** Você é Maria Madalena, conselheira amorosa super calorosa, ácida e nordestina — seu jeito reflete o sotaque e os traços nordestinos de forma sutil, autêntica e natural (sem caricatura ou exageros, mas o sotaque nordestino precisa estar presente, seja em palavras, expressões ou estruturas que remetam à fala nordestina real. Nada de piada de dicionário, mas a voz tem que ser nordeste!).
Sua vibe é informal, fala abertamente em **PORTUGÊS BRASILEIRO** com referências e marcações regionais do Nordeste. A comunicação deve ser 100% em português brasileiro natural, com toques do Nordeste, tanto no vocabulário quanto em expressões. Use bom humor, faça piadas ácidas sobre a situação do usuário sem excessos, e tire onda apenas quando fizer sentido, sempre mantendo um jeito acolhedor. Não exagere nas piadas, nem no regionalismo — mas o sotaque nordestino, mesmo leve, deve aparecer.
Frases curtas, espontâneas, português-BR (APENAS) popular com sotaque e jeitos nordestinos, **negrito** para destaques e no máx. *dois emojis* por mensagem.

INFORMAÇÕES DO USUÁRIO:
- Nome: {perfil.get('nome_completo', 'Não informado')}
- Idade: {perfil.get('idade', 'Não informada')}
- Gênero: {perfil.get('genero', 'Não informado')}
- Orientação Sexual: {perfil.get('orientacao_sexual', 'Não informada')}
- Status de Relacionamento: {perfil.get('relacionamento_status', 'Não informado')}


## 2. Missão

Bate-papo **solto, leve e bem natural**, conversa de verdade sem roteiro engessado. Continue a conversa fluidamente, puxando sempre pelo que o usuário disser, evitando forçar novas perguntas ou mudar de tema sem contexto. Durante o papo, descubra de forma leve e espontânea **cinco temas-chave** — sem clima de interrogatório, sem forçar perguntas. Use piadas e comentários ácidos quando apropriado, sempre para descontrair, priorizando perguntas que surgem naturalmente a partir da conversa.

### Cinco temas-chave a investigar

  1. **Objetivo de relacionamento** — O que tá querendo pro coração?
  2. **Valores essenciais** — O que manda nas tuas decisões?
  3. **Estilo de vida** — Como é tua rotina, quais perrengues ou rolês?
  4. **Deal-breakers** — O que não rola nem amarrado (ex.: fumar, distância, filhos…)?
  5. **Linguagem do amor** — O que faz teu coração amolecer?

*Exemplos de perguntas (só use se a conversa morrer, e ainda assim adapte conforme o andamento do papo):*
  * “Quando topa alguém novo por aí, espera o quê depois? Vai casar ou já quer sair batendo o pé?”
  * “Pra tu se sentir bem acompanhado(a), o que não pode faltar? Café e fofoca tá valendo?”
  * “Sábado perfeito: sofazinho e novela, ou rolê e confusão no meio da rua?”
  * “Tem alguma coisa que já corta o barato na hora, visse?”
  * “Pra te ganhar, basta uma palavra bonita ou tem que suar pra valer?”

---

## 3. Estratégia ácida de Condução
  1. **Comece quebrando o gelo** com zoeira leve (ex: hobbies diferentes, viagem de perrengue, música ruim favorita) — mas sempre puxe pelo que a pessoa disser antes de trazer perguntas novas.
  2. **Pesque mentalmente** quais temas faltam descobrir e jogue uma pergunta marota só se encaixar na conversa — *JAMAIS* mude de assunto do nada. Evite perguntas com aparência de interrogatório ou enviesadas.
  3. Se o usuário falar ou pedir algo impróprio, puxe logo uma resposta sarcástica e mude de assunto.
  4. Responda com ironia, frases ácidas e bom humor, mas não force o tom. Seja espontânea, sem forçar piadas.
  5. **Nunca use frases tipo “brincadeiras à parte” ou “falando sério”** — mantenha o tom divertido e descontraído até o fim.

---

## 4. Regras
* Nada de pedir dado pessoal (CPF, endereço, cartão, etc).
* Se o usuário disser **parar**, pare e respeite.
* Foge de conteúdo explícito, violento ou preconceituoso.
* Se perguntada, diga que é a IA de um app, sem enrolação.

---

### Resumo Operacional
Puxe conversa leve, faça piada ácida com a situação amorosa do usuário na medida certa, sem exagerar, mas o sotaque e o jeito nordestino têm que estar sempre presentes de forma leve e natural. Não é caricatura, é verdade do Nordeste. A conversa deve ser sempre em português-brasileiro natural, misturado com vocabulário, expressões e trejeitos nordestinos. Descubra **objetivo, valores, rotina, limites e linguagem do amor** de forma fluida, sem forçar perguntas. Nunca mude de assunto abruptamente: aproveite o que o usuário fala para levar a conversa adiante, sem enviesar pra tema nenhum.
Engaje mais do que apenas responda. O foco é dar risada e puxar papo — descobrir os temas é só um bônus.
"""

# Define prompt
if perfil.get("tipo de prompt") == 'prompt_A':
    system_prompt_mariamadalena = prompt_institucional
else:
    system_prompt_mariamadalena = prompt_teste
# Usa o primeiro nome para a saudação, com fallback para o given_name do login ou 'Querida(o)'
nome_usuario = perfil.get("nome_completo", getattr(st.experimental_user, 'given_name', 'Querida(o)'))
# Pega só o primeiro nome se for nome completo
if ' ' in nome_usuario:
    nome_usuario = nome_usuario.split(' ')[0]
# Verifica e exibe a mensagem de boas-vindas no primeiro login
if st.session_state.get('show_welcome_message', False):
    with st.popover("Bem-vinda! 💕", use_container_width=True):
        st.markdown(f"Olá, **{nome_usuario}**! Sou Maria Madalena, sua conselheira amorosa pessoal!")
        st.markdown("Estou aqui para te ajudar com questões do coração, relacionamentos e autoestima. Pode me contar tudo! 💕")
        st.button("Vamos conversar!", use_container_width=True, key="welcome_close")
    # Remove o flag para não mostrar novamente
    del st.session_state['show_welcome_message']

# Configurações iniciais
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

# Define o avatar do usuário: usa a foto do perfil se for uma URL válida, senão usa o avatar padrão
user_picture = getattr(st.experimental_user, 'picture', None)
if user_picture and isinstance(user_picture, str) and user_picture.startswith(('http://', 'https://')):
    avatar_user = user_picture
else:
    avatar_user = 'arquivos/avatar_usuario.jpg'

# Define o avatar do assistente
avatar_assistant = 'arquivos/avatar_assistente.jpg'

# Mensagem inicial personalizada da Maria Madalena
def obter_mensagem_inicial():
    """Gera mensagem inicial personalizada com base no perfil do usuário"""
    mensagens_iniciais = [
        f"Oi {nome_usuario}! 💕 Sou Maria Madalena, sua conselheira amorosa. Como está seu coração hoje?",
        f"Olá {nome_usuario}! ✨ Que bom te ver aqui! Em que posso te ajudar nos assuntos do coração?",
        f"Oi {nome_usuario}! 💖 Sou Maria Madalena e estou aqui para te ouvir. Me conta o que está acontecendo na sua vida amorosa!",
        f"Olá {nome_usuario}! 🌹 Sua conselheira amorosa está aqui! Quer conversar sobre relacionamentos, autoestima ou questões do coração?"
    ]
    import random
    return random.choice(mensagens_iniciais)

MENSAGEM_INICIAL = obter_mensagem_inicial()

# Inicialização do histórico de mensagens e chat ativo
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "assistant",
            "content": MENSAGEM_INICIAL
        }
    ]

if 'chat_ativo_id' not in st.session_state:
    st.session_state.chat_ativo_id = None

if 'chat_ativo_nome' not in st.session_state:
    st.session_state.chat_ativo_nome = "Nova Conversa"

# Título da página
st.title("💕 Maria Madalena - Conselheira do Amor")
st.markdown("*Sua conselheira amorosa pessoal está aqui para te ajudar! 💖*")

# Sidebar com histórico de chats
with st.sidebar: 
    
    # Botão de novo chat
    if st.button("✨ Nova Conversa", key="novo_chat", use_container_width=True, type="primary"):
        nova_mensagem_inicial = obter_mensagem_inicial()  # Gera nova mensagem
        st.session_state.mensagens = [
            {
                "role": "assistant",
                "content": nova_mensagem_inicial
            }
        ]
        st.session_state.chat_ativo_id = None
        st.session_state.chat_ativo_nome = "Nova Conversa"
        registrar_acao_usuario("Nova Conversa", "Usuário iniciou nova conversa com Maria Madalena")
        st.rerun()
    
    # Exibir chats existentes
    chats = obter_chats() 
    
    # CSS personalizado para alinhar botões à esquerda
    st.markdown("""
        <style>
        /* Estiliza os botões de chat anterior usando o prefixo da chave */
        [class*="st-key-chat_"] button {
            text-align: left !important;
            justify-content: flex-start !important;
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicia uma div com uma classe específica para os botões de chat
    st.markdown('<div class="chat-button-section">', unsafe_allow_html=True)
    
    if len(chats) == 0:
        st.info("Você ainda não tem conversas salvas com Maria Madalena! 💕")
    
    for chat in chats:
        col1, col2 = st.columns([7, 1])
        with col1:
            if st.button(f"{chat['nome']}", key=f"chat_{chat['id']}", use_container_width=True):
                chat_data = obter_chat(chat['id'])
                if chat_data and 'mensagens' in chat_data:
                    st.session_state.mensagens = chat_data['mensagens']
                    st.session_state.chat_ativo_id = chat['id']
                    st.session_state.chat_ativo_nome = chat['nome']
                    registrar_acao_usuario("Abrir Conversa", f"Usuário abriu a conversa {chat['nome']}")
                    st.rerun()
        with col2:
            if st.button("🗑️", key=f"excluir_{chat['id']}"):
                excluir_chat(chat['id'])
                registrar_acao_usuario("Excluir Conversa", f"Usuário excluiu a conversa {chat['nome']}")
                # Se o chat excluído for o ativo, iniciar um novo chat
                if st.session_state.chat_ativo_id == chat['id']:
                    nova_mensagem_inicial = obter_mensagem_inicial()
                    st.session_state.mensagens = [
                        {
                            "role": "assistant",
                            "content": nova_mensagem_inicial
                        }
                    ]
                    st.session_state.chat_ativo_id = None
                    st.session_state.chat_ativo_nome = "Nova Conversa"
                st.rerun()
    
    # Fecha a div
    st.markdown('</div>', unsafe_allow_html=True)

# Exibição do histórico de mensagens
for mensagem in st.session_state.mensagens:
    role = mensagem["role"]
    # Define o avatar a ser exibido baseado no role
    if role == "user":
        display_avatar = avatar_user
    elif role == "assistant":
        display_avatar = avatar_assistant
    else:
        display_avatar = None
        
    with st.chat_message(role, avatar=display_avatar):
        # Aplica as substituições para formato de matemática do Streamlit apenas nas mensagens do assistente
        if role == "assistant":
            display_content = mensagem["content"].replace('\\[', '$$').replace('\\]', '$$')\
                                               .replace('\\(', '$').replace('\\)', '$')
            st.markdown(display_content)
        else:
            st.write(mensagem["content"])

# Input e processamento de mensagens
prompt = st.chat_input(placeholder="Me conta o que está no seu coração... 💕")

if prompt:
    # Registra a pergunta do usuário
    registrar_atividade_academica(
        tipo="chatbot_maria_madalena",
        modulo="Conselheira Amorosa",
        detalhes={
            "acao": "pergunta",
            "tamanho_pergunta": len(prompt),
            "chat_id": st.session_state.chat_ativo_id,
            "chat_nome": st.session_state.chat_ativo_nome
        }
    )
    
    # Adiciona mensagem do usuário
    st.session_state.mensagens.append({
        "role": "user",
        "content": prompt
    })
    
    # Mostra mensagem do usuário
    with st.chat_message("user", avatar=avatar_user):
        st.write(prompt)

    # Processa resposta do assistente
    with st.chat_message("assistant", avatar=avatar_assistant):
        try:
            # Prepara o sistema prompt personalizado para Maria Madalena
            system_prompt = system_prompt_mariamadalena

            # Prepara mensagens para a API
            messages = [{"role": "system", "content": system_prompt}]
            
            # Adiciona apenas as últimas 10 mensagens para manter contexto sem ultrapassar limites
            recent_messages = st.session_state.mensagens[-10:]
            for msg in recent_messages:
                if msg["role"] != "system":
                    messages.append({
                        "role": msg["role"], 
                        "content": msg["content"]
                    })
            
            # Chama a API da OpenAI
            resposta_stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.8,  # Um pouco mais criativa para conselhos amorosos
                max_tokens=1000,
                stream=True
            )
            
            # Exibe resposta em tempo real
            resposta_completa = ""
            container = st.empty()
            
            for chunk in resposta_stream:
                if chunk.choices[0].delta.content is not None:
                    resposta_completa += chunk.choices[0].delta.content
                    container.markdown(resposta_completa + "▌")
            
            # Remove o cursor e mostra resposta final
            container.markdown(resposta_completa)
            
            # Adiciona resposta ao histórico
            st.session_state.mensagens.append({
                "role": "assistant",
                "content": resposta_completa
            })
            
            # SALVAMENTO AUTOMÁTICO APÓS CADA RESPOSTA
            # Se não há chat ativo, cria um novo
            if st.session_state.chat_ativo_id is None:
                # Gera título da conversa baseado no conteúdo
                try:
                    titulo = gerar_titulo_chat(st.session_state.mensagens)
                    if not titulo:
                        titulo = f"Conversa de {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                except:
                    titulo = f"Conversa de {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                
                # Salva a nova conversa
                chat_id = salvar_chat(titulo, st.session_state.mensagens)
                if chat_id:
                    st.session_state.chat_ativo_id = chat_id
                    st.session_state.chat_ativo_nome = titulo
                    registrar_acao_usuario("Nova Conversa Salva", f"Conversa salva automaticamente: {titulo}")
            else:
                # Atualiza conversa existente
                atualizar_chat(st.session_state.chat_ativo_id, st.session_state.mensagens)
                registrar_acao_usuario("Conversa Atualizada", f"Conversa {st.session_state.chat_ativo_nome} atualizada")
            
            # Registra a resposta
            registrar_atividade_academica(
                tipo="chatbot_maria_madalena",
                modulo="Conselheira Amorosa",
                detalhes={
                    "acao": "resposta",
                    "tamanho_resposta": len(resposta_completa),
                    "chat_id": st.session_state.chat_ativo_id,
                    "chat_nome": st.session_state.chat_ativo_nome
                }
            )
            
        except Exception as e:
            st.error(f"Ops, querida! Tive um probleminha técnico: {str(e)}")
            st.error("Tenta novamente, por favor! 💕")

# Informações úteis na sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💡 **Dicas para nossa conversa:**")
    st.markdown("• Seja honesta(o) sobre seus sentimentos")
    st.markdown("• Não tenha vergonha de compartilhar")
    st.markdown("• Lembre-se: sou uma IA conselheira")
    st.markdown("• Para questões sérias, procure um profissional")
    st.markdown("---")
    st.markdown("💕 *Maria Madalena está aqui para te apoiar!*")
