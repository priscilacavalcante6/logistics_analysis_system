import streamlit as st

# Configurações do Dashboard
st.set_page_config(page_title="Dashboard de Análise Logística", page_icon="icons8-analytics-48.png", layout="wide")

# Estilizando a página de login
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;  /* Fundo claro */
        }
        .header {
            background-color: #333333;  /* Cabeçalho cinza escuro */
            color: #ffffff;
            padding: 20px 0;
            text-align: center;
            font-size:20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        # .login-container {
        #     background-color: #ffffff;
        #     padding: 20px;
        #     border-radius: 8px;
        #     box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        #     width: 100%;
        #     max-width: 200px;  /* Caixa de login menor */
        #     margin: 40px auto;  /* Centraliza verticalmente e horizontalmente */
        #     text-align: center;
        # }
        .login-title {
            font-size: 28px;
            color: #333;
            margin-bottom: 15px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .login-button {
            background-color: #5cb85c;
            color: white;
            padding: 12px 20px;
            border-radius: 5px;
            border: none;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            margin-top: 15px;
        }
        .login-button:hover {
            background-color: #4cae4c;
        }
        .stTextInput, .stPasswordInput {
            width: 100%;
            padding: 12px 15px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .stTextInput:focus, .stPasswordInput:focus {
            border-color: #5cb85c;
            box-shadow: 0 0 5px rgba(92, 184, 92, 0.5);
        }
        .logo {
            max-width: 100px;  /* Ajuste do tamanho do logotipo */
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Simulação de credenciais (substitua pelo seu sistema de autenticação)
credenciais = {"admin": "1234", "user": "senha"}

# Sessão para armazenar o estado do login
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# Função de login
def login():
    # Cabeçalho
    
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("logo1.png", use_container_width=False, width=150, caption="Logo da Empresa")
    with col2:
        st.markdown('<div class="header" style="font-size: 24px; padding: 10px 0;">Sistema de Análise Logística</div>', unsafe_allow_html=True)


    
    # Caixa de login
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="login-title">Login</h2>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        usuario_input = st.text_input("Usuário", max_chars=20)
        senha_input = st.text_input("Senha", type="password", max_chars=20)
        submit = st.form_submit_button("Entrar", help="Clique para acessar")

    if submit:
        if usuario_input in credenciais and credenciais[usuario_input] == senha_input:
            st.session_state["usuario"] = usuario_input
            st.success(f"✅ Logado como: {st.session_state['usuario']}")
            st.session_state["login_sucesso"] = True
            st.rerun()  # Atualiza a página para refletir o login
        else:
            st.error("❌ Usuário ou senha incorretos!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Verificando se o usuário está logado
if st.session_state.get("login_sucesso", False):
    # Redireciona para o painel de logística se o login for bem-sucedido
    import painel_logistica  # A partir do momento que o login for realizado, o painel é carregado
else:
    # Caso não tenha login, exibe o formulário de login
    login()
