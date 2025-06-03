# 💕 Maria Madalena - Conselheira do Amor

## 🌟 Visão Geral

Maria Madalena é uma conselheira amorosa inteligente construída com Streamlit e IA avançada. Ela oferece uma experiência personalizada de aconselhamento em relacionamentos, com autenticação segura de usuários, armazenamento persistente de conversas íntimas e orientações personalizadas baseadas no perfil de cada usuário.

## 💝 Funcionalidades Principais

### 1. Sistema de Autenticação
- Login seguro através de contas Google
- Autenticação gerenciada pelo Streamlit (`st.experimental_user`)
- Proteção das conversas pessoais
- Registro automático de novos usuários

### 2. Interface de Conversa Amorosa
- Design romântico e acolhedor
- Componentes nativos do Streamlit para conversas íntimas
- Respostas personalizadas em tempo real
- Ambiente seguro e confidencial para falar sobre amor

### 3. Sistema de Memória das Conversas
- Armazenamento completo do histórico de conversas amorosas
- Organização de conversas por usuário
- Capacidade de retomar conversas anteriores sobre relacionamentos
- Backup automático das interações íntimas

### 4. Perfil Personalizado para Aconselhamento
- Informações coletadas para personalização:
  * Nome/apelido
  * Idade
  * Identidade de gênero
  * Orientação sexual
  * Status de relacionamento
  * Email e foto do perfil
- Conselhos personalizados baseados no perfil

### 5. Sistema de Logs Confidencial
- Registro detalhado respeitando a privacidade
- Monitoramento de:
  * Acessos ao sistema
  * Criação de novas conversas
  * Atualizações de perfil amoroso

### 6. IA Especializada em Relacionamentos
- Utiliza a API da OpenAI com prompts especializados em amor
- Personalidade calorosa e empática da Maria Madalena
- Conselhos baseados em psicologia de relacionamentos
- Respostas sensíveis e inclusivas para todas as orientações

### 7. Páginas Essenciais
- **💕 Conversar:** Interface principal para chat com Maria Madalena
- **👤 Meu Perfil:** Gestão das informações pessoais
- **📜 Termos e Privacidade:** Políticas adaptadas para conselheira amorosa

### 8. Segurança e Confidencialidade
- Máxima proteção das conversas íntimas
- Termos adaptados para aconselhamento amoroso
- Disclaimers importantes sobre limitações da IA
- Orientações para buscar ajuda profissional quando necessário

## 🛠️ Configuração do Ambiente

### Requisitos do Sistema
- Python 3.7+
- Conta no Firebase para armazenar conversas
- Conta na OpenAI para a IA da Maria Madalena
- Ambiente para execução Streamlit

### Passo a Passo de Instalação

1. **Clone o Repositório:**
```bash
git clone <url_do_repositorio>
cd maria-madalena
```

2. **Configure o Ambiente Virtual:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Instale as Dependências:**
```bash
pip install -r requirements.txt
```

## 🔧 Configuração das APIs

### Firebase
1. Crie um projeto no Firebase Console
2. Configure o Firestore Database para armazenar conversas
3. Gere e baixe a chave privada
4. Configure as credenciais no projeto

### OpenAI
1. Crie uma conta na OpenAI
2. Gere uma API Key
3. Configure para usar GPT-4o-mini (otimizado para conversas)
4. Adicione as credenciais ao projeto

## 📁 Estrutura do Banco de Dados

### Coleção Principal: `maria-madalena-usuarios`
- Documentos por email do usuário
- Subcoleções:
  * `logs`: Registro de atividades
  * `chats`: Conversas amorosas armazenadas

### Estrutura de Dados do Usuário
```json
{
    "email": "string",
    "nome_completo": "string",
    "foto": "string (URL)",
    "idade": "number",
    "genero": "string",
    "orientacao_sexual": "string", 
    "relacionamento_status": "string",
    "data_cadastro": "timestamp",
    "ultimo_acesso": "timestamp",
    "primeiro_acesso_concluido": "boolean",
    "consentimento_conselheira": "boolean"
}
```

## 🚀 Como Executar

1. **Desenvolvimento Local:**
```bash
streamlit run app.py
```

2. **Deploy no Streamlit Cloud:**
- Configure os secrets no painel do Streamlit Cloud
- Conecte com seu repositório
- Deploy automático

## 🎨 Personalização da Maria Madalena

### Elementos Visuais
- Logos e ícones românticos em `arquivos/`
- Estilos CSS com tema amoroso
- Cores e emojis que transmitem carinho

### Personalidade da Conselheira
- Prompts especializados em relacionamentos
- Linguagem calorosa e empática
- Inclusividade para todas as orientações
- Conselhos práticos e sensíveis

### Campos de Perfil Amoroso
- Informações relevantes para aconselhamento
- Perguntas sensíveis e inclusivas
- Privacidade máxima dos dados íntimos

## 🔒 Segurança e Privacidade

- Autenticação via Google
- Proteção máxima das conversas íntimas
- Criptografia de dados sensíveis
- Políticas claras sobre uso de dados pessoais
- Disclaimers sobre limitações da IA

## 💡 Propósito e Limitações

### O que Maria Madalena Faz:
- Oferece conselhos gerais sobre relacionamentos
- Escuta com empatia questões do coração
- Dá suporte emocional e orientações práticas
- Ajuda com autoestima e confiança

### O que Maria Madalena NÃO Faz:
- Não substitui terapia profissional
- Não trata questões de saúde mental severas
- Não oferece conselhos médicos ou legais
- Não é adequada para crises ou emergências

### Quando Buscar Ajuda Profissional:
- Violência doméstica
- Depressão severa
- Pensamentos suicidas
- Problemas que requerem intervenção profissional

**Recursos de Emergência:**
- CVV: 188
- Emergência: 190

## 📚 Arquivos do Projeto

### Estrutura Principal
```
├── app.py                     # Entrada principal
├── requirements.txt           # Dependências
├── termos_e_privacidade.md   # Termos adaptados
├── .streamlit/
│   └── secrets.toml          # Configurações secretas
├── paginas/
│   ├── chatbot.py            # Maria Madalena chat
│   ├── perfil.py             # Perfil amoroso
│   ├── termos.py             # Página de termos
│   └── funcoes.py            # Utilitários
└── arquivos/                 # Recursos visuais
```

## 💕 Contribuindo para Maria Madalena

- Reporte bugs ou sugestões via Issues
- Contribuições para melhorar a experiência amorosa
- Mantenha o foco em relacionamentos saudáveis
- Preserve a confidencialidade e segurança

## 📄 Licença

Este projeto está sob a licença MIT. Maria Madalena foi criada com amor para ajudar pessoas nos assuntos do coração! 💕 