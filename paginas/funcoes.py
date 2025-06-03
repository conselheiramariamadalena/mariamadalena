from datetime import datetime
import streamlit as st
from firebase_admin import firestore, credentials 
import firebase_admin
import os

# Nome da coleção principal de usuários definida como variável global
COLECAO_USUARIOS = "Maria-Madalena"

def inicializar_firebase():
    # Verifica se estamos em produção (Streamlit Cloud) ou desenvolvimento local
    if 'firebase' in st.secrets:
        cred = credentials.Certificate({
            "type": st.secrets.firebase.type,
            "project_id": st.secrets.firebase.project_id,
            "private_key_id": st.secrets.firebase.private_key_id,
            "private_key": st.secrets.firebase.private_key,
            "client_email": st.secrets.firebase.client_email,
            "client_id": st.secrets.firebase.client_id,
            "auth_uri": st.secrets.firebase.auth_uri,
            "token_uri": st.secrets.firebase.token_uri,
            "auth_provider_x509_cert_url": st.secrets.firebase.auth_provider_x509_cert_url,
            "client_x509_cert_url": st.secrets.firebase.client_x509_cert_url,
            "universe_domain": st.secrets.firebase.universe_domain
        })
    else:
        # Usa o arquivo local em desenvolvimento
        cred = credentials.Certificate("firebase-key.json")
        
    # Inicializa o Firebase apenas se ainda não foi inicializado
    try:
        firebase_admin.get_app() 
    except ValueError:
        firebase_admin.initialize_app(cred)

def login_usuario():
    """
    Registra ou atualiza dados do usuário no Firestore.
    Cria um novo registro se o usuário não existir, ou atualiza o último acesso se já existir.
    Retorna True se for o primeiro login, False caso contrário.
    """
    if not hasattr(st.experimental_user, 'email'):
        return False # Se não houver email, não tenta registrar o usuário
        
    db = firestore.client()
    doc_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email)
    doc = doc_ref.get()

    if not doc.exists:
        dados_usuario = {
            # Dados do Google Login
            "email": st.experimental_user.email,
            "nome_google": getattr(st.experimental_user, 'name', ''),
            "primeiro_nome_google": getattr(st.experimental_user, 'given_name', ''),
            "ultimo_nome_google": getattr(st.experimental_user, 'family_name', ''),
            "foto": getattr(st.experimental_user, 'picture', None),
            # Dados específicos do App (coletados no primeiro acesso)
            "nome_completo": "", 
            "idade": "",
            "genero": "",
            "orientacao_sexual": "",
            "relacionamento_status": "",
            # Controle e Metadados
            "data_cadastro": datetime.now(),
            "ultimo_acesso": datetime.now(),
            "primeiro_acesso_concluido": False # Flag para o formulário inicial
        }
        doc_ref.set(dados_usuario)
        registrar_acao_usuario("Cadastro", "Novo usuário registrado")
        if 'login_registrado' not in st.session_state:
             st.session_state['login_registrado'] = True # Marca como registrado para evitar loop
        return True # Indica que é o primeiro login
    else:
        doc_ref.update({"ultimo_acesso": datetime.now()})
        if 'login_registrado' not in st.session_state:
            registrar_acao_usuario("Login", "Usuário fez login")
            st.session_state['login_registrado'] = True
        return False # Indica que não é o primeiro login

def registrar_acao_usuario(acao: str, detalhes: str = ""):
    """
    Registra uma ação do usuário no Firestore.
    
    Args:
        acao: Nome da ação realizada
        detalhes: Detalhes adicionais da ação (opcional)
    """
    if not hasattr(st.experimental_user, 'email'):
        return  # Se não houver email, não registra a ação
        
    db = firestore.client()
    logs_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("logs")
    
    dados_log = {
        "acao": acao,
        "detalhes": detalhes,
        "data_hora": datetime.now()
    }
    
    logs_ref.add(dados_log)

def registrar_atividade_academica(tipo: str, modulo: str, detalhes: dict):
    """
    Registra uma atividade acadêmica específica do usuário.
    
    Args:
        tipo: Tipo da atividade (ex: 'chatbot_maria_madalena')
        modulo: Nome do módulo ou seção relacionada
        detalhes: Dicionário com detalhes específicos da atividade
    """
    if not hasattr(st.experimental_user, 'email'):
        return
        
    db = firestore.client()
    atividades_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("atividades_academicas")
    
    dados_atividade = {
        "tipo": tipo,
        "modulo": modulo,
        "detalhes": detalhes,
        "data_hora": datetime.now()
    }
    
    atividades_ref.add(dados_atividade)

def obter_perfil_usuario():
    """
    Obtém os dados de perfil do usuário atual do Firestore.
    
    Returns:
        dict: Dicionário com os dados do perfil do usuário ou None se não encontrado/erro.
    """
    if not hasattr(st.experimental_user, 'email'):
        return None
        
    db = firestore.client()
    doc_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email)
    try:
        doc = doc_ref.get()
        if doc.exists:
            dados = doc.to_dict()
            return {
                # Campos essenciais mantidos
                "email": dados.get("email", ""),
                "foto": dados.get("foto", ""), 
                # Campos específicos da Maria Madalena
                "nome_completo": dados.get("nome_completo", ""),
                "idade": dados.get("idade", ""),
                "genero": dados.get("genero", ""),
                "orientacao_sexual": dados.get("orientacao_sexual", ""),
                "relacionamento_status": dados.get("relacionamento_status", ""),
                # Flag de controle
                "primeiro_acesso_concluido": dados.get("primeiro_acesso_concluido", False),
                # Campos derivados do Google (mantidos para referência, se útil)
                "nome_google": dados.get("nome_google", ""), 
                "primeiro_nome_google": dados.get("primeiro_nome_google", ""),
                # Data de criação para exibir no perfil
                "data_criacao": dados.get("data_cadastro", None),
            }
        else:
            # Usuário logado mas sem registro no Firestore (situação anormal)
            st.error("Seu registro não foi encontrado no banco de dados. Contate o suporte.")
            return None 
    except Exception as e:
        print(f"Erro ao obter perfil para {st.experimental_user.email}: {e}")
        st.warning("Não foi possível carregar os dados do seu perfil.")
        return None

def atualizar_perfil_usuario(dados_perfil):
    """
    Atualiza os dados de perfil do usuário atual.
    
    Args:
        dados_perfil: Dicionário com os dados do perfil a serem atualizados
    
    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário
    """
    if not hasattr(st.experimental_user, 'email'):
        return False  # Retorna False se não houver email
        
    db = firestore.client()
    doc_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email)
    
    try:
        doc_ref.update(dados_perfil)
        return True
    except Exception as e:
        print(f"Erro ao atualizar perfil para {st.experimental_user.email}: {e}")
        return False

def salvar_chat(nome_chat, mensagens):
    """
    Salva um chat no Firestore.
    
    Args:
        nome_chat: Nome do chat
        mensagens: Lista de mensagens do chat
        
    Returns:
        str: ID do documento criado ou None se falhou
    """
    if not hasattr(st.experimental_user, 'email'):
        return None
        
    db = firestore.client()
    chats_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("chats")
    
    try:
        dados_chat = {
            "nome": nome_chat,
            "mensagens": mensagens,
            "data_criacao": datetime.now(),
            "data_atualizacao": datetime.now()
        }
        
        doc_ref = chats_ref.add(dados_chat)
        return doc_ref[1].id  # Retorna o ID do documento criado
    except Exception as e:
        print(f"Erro ao salvar chat: {e}")
        return None

def obter_chats():
    """
    Obtém a lista de chats do usuário atual.
    
    Returns:
        list: Lista de dicionários com dados dos chats
    """
    if not hasattr(st.experimental_user, 'email'):
        return []
        
    db = firestore.client()
    chats_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("chats")
    
    try:
        docs = chats_ref.order_by("data_atualizacao", direction=firestore.Query.DESCENDING).get()
        chats = []
        for doc in docs:
            chat_data = doc.to_dict()
            chats.append({
                "id": doc.id,
                "nome": chat_data.get("nome", "Chat sem nome"),
                "data_criacao": chat_data.get("data_criacao"),
                "data_atualizacao": chat_data.get("data_atualizacao")
            })
        return chats
    except Exception as e:
        print(f"Erro ao obter chats: {e}")
        return []

def obter_chat(chat_id):
    """
    Obtém um chat específico pelo ID.
    
    Args:
        chat_id: ID do chat a ser obtido
        
    Returns:
        dict: Dados do chat ou None se não encontrado
    """
    if not hasattr(st.experimental_user, 'email'):
        return None
        
    db = firestore.client()
    chat_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("chats").document(chat_id)
    
    try:
        doc = chat_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"Erro ao obter chat {chat_id}: {e}")
        return None

def excluir_chat(chat_id):
    """
    Exclui um chat específico pelo ID.
    
    Args:
        chat_id: ID do chat a ser excluído
        
    Returns:
        bool: True se excluído com sucesso, False caso contrário
    """
    if not hasattr(st.experimental_user, 'email'):
        return False
        
    db = firestore.client()
    chat_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("chats").document(chat_id)
    
    try:
        chat_ref.delete()
        return True
    except Exception as e:
        print(f"Erro ao excluir chat {chat_id}: {e}")
        return False

def atualizar_chat(chat_id, mensagens):
    """
    Atualiza um chat específico com novas mensagens.
    
    Args:
        chat_id: ID do chat a ser atualizado
        mensagens: Lista atualizada de mensagens
        
    Returns:
        bool: True se atualização foi bem-sucedida, False caso contrário
    """
    if not hasattr(st.experimental_user, 'email'):
        return False
        
    db = firestore.client()
    chat_ref = db.collection(COLECAO_USUARIOS).document(st.experimental_user.email).collection("chats").document(chat_id)
    
    try:
        chat_ref.update({
            "mensagens": mensagens,
            "data_atualizacao": datetime.now()
        })
        return True
    except Exception as e:
        print(f"Erro ao atualizar chat {chat_id}: {e}")
        return False










