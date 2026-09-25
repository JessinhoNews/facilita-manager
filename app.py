from io import BytesIO
import streamlit as st
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

st.set_page_config(page_title="Facilita Manager", page_icon="🏛️", layout="wide")
st.markdown("""
<style>
/* Texto geral */
html, body, [class*="css"] {
    color: #222222 !important;
}

/* Títulos e textos */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #222222;
}

/* Texto dentro dos selectboxes */
div[data-baseweb="select"] span {
    color: #222222 !important;
}

/* Texto das opções abertas do selectbox */
ul[role="listbox"] li {
    color: #222222 !important;
    background-color: #ffffff !important;
}

/* Campos de texto */
input, textarea {
    color: #222222 !important;
    background-color: #ffffff !important;
}

/* Texto dos botões */
button {
    color: #222222 !important;
}

/* Expansores */
[data-testid="stExpander"] summary p {
    color: #222222 !important;
}

/* Textos das métricas */
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"] {
    color: #222222 !important;
}
</style>
""", unsafe_allow_html=True)
# =========================================================
# IDENTIDADE VISUAL DA FACILITA
# =========================================================

st.markdown(
    """
    <style>
        /* Fundo geral da aplicação */
        .stApp {
            background-color: #f4f7fc;
        }

        /* Menu lateral */
        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #071d52 0%,
                #0b2d78 100%
            );
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        /* Área principal */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }

        /* Títulos */
        h1, h2, h3 {
            color: #092b72 !important;
        }

        /* Cartões de métricas */
        div[data-testid="stMetric"] {
            background-color: white;
            border: 1px solid #e1e8f2;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 3px 12px rgba(9, 43, 114, 0.06);
        }

        div[data-testid="stMetricLabel"] {
            color: #52627a !important;
        }

        div[data-testid="stMetricValue"] {
            color: #092b72 !important;
            font-weight: 700;
        }

        /* Botões */
        .stButton > button {
            background-color: #092b72;
            color: white;
            border: none;
            border-radius: 8px;
            min-height: 42px;
            font-weight: 600;
        }

        .stButton > button:hover {
            background-color: #f4b400;
            color: #092b72;
            border: none;
        }

        /* Campos de formulário */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        textarea {
            border-radius: 8px !important;
        }

        /* Abas */
        button[data-baseweb="tab"] {
            font-weight: 600;
        }

        /* Expanders */
        div[data-testid="stExpander"] {
            background-color: white;
            border: 1px solid #e1e8f2;
            border-radius: 10px;
        }

        /* Linha divisória */
        hr {
            border-color: #dce5f2;
        }

        /* Texto auxiliar */
        .texto-institucional {
            color: #64748b;
            font-size: 0.95rem;
        }

        /* Cartões personalizados */
        .cartao-facilita {
            background-color: white;
            border: 1px solid #e1e8f2;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 3px 12px rgba(9, 43, 114, 0.06);
        }
     /* =====================================================
   CORREÇÃO DE CONTRASTE
   ===================================================== */

/* Textos dentro dos cartões */
div[data-testid="stVerticalBlockBorderWrapper"] p {
    color: #334155 !important;
}

/* Textos gerais da área principal */
.main p {
    color: #334155;
}

/* Textos dos expanders */
div[data-testid="stExpander"] p {
    color: #334155 !important;
}

/* Títulos dentro dos cartões */
div[data-testid="stVerticalBlockBorderWrapper"] h1,
div[data-testid="stVerticalBlockBorderWrapper"] h2,
div[data-testid="stVerticalBlockBorderWrapper"] h3 {
    color: #092b72 !important;
}

/* Métricas do Dashboard */
div[data-testid="stMetric"] label {
    color: #52627a !important;
}

div[data-testid="stMetric"] div {
    color: #092b72 !important;
}

/* Textos dos campos */
label {
    color: #334155 !important;
}   
    </style>
    """,
    unsafe_allow_html=True,
)
# =========================================================
# SISTEMA DE LOGIN
# =========================================================

USUARIOS = {
    "alvaro": {
        "nome": "Álvaro Vinícius",
        "perfil": "Gerente",
        "senha": "Facilita@2026",
    },
    "italo": {
        "nome": "Ítalo",
        "perfil": "Publicador",
        "senha": "Facilita@2026",
    },
    "vitor": {
        "nome": "Vitor",
        "perfil": "Publicador",
        "senha": "Facilita@2026",
    },
    "jadsson": {
        "nome": "Jadsson",
        "perfil": "Publicador",
        "senha": "Facilita@2026",
    },
    "felipe": {
        "nome": "Felipe Rocha",
        "perfil": "Diretor Presidente",
        "senha": "Admfrmelo94",
    },
}


def verificar_login(usuario, senha):
    usuario = usuario.lower().strip()

    if usuario not in USUARIOS:
        return False

    return senha == USUARIOS[usuario]["senha"]


def tela_login():

    st.markdown(
        """
        <style>
        .login-box {
            max-width: 430px;
            margin: 70px auto;
        }

        .login-titulo {
            text-align: center;
            color: #092b72;
            font-size: 30px;
            font-weight: 700;
        }

        .login-subtitulo {
            text-align: center;
            color: #64748b;
            margin-bottom: 25px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    esquerda, centro, direita = st.columns([1, 2, 1])

    with centro:

        st.image(
            "assets/logo-facilita.png",
            use_container_width=True,
        )

        st.markdown(
            '<div class="login-titulo">'
            'Facilita Manager'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="login-subtitulo">'
            'Sistema de Gestão da Facilita'
            '</div>',
            unsafe_allow_html=True,
        )

        usuario = st.text_input(
            "Usuário",
            placeholder="Digite seu usuário",
        )

        senha = st.text_input(
            "Senha",
            type="password",
            placeholder="Digite sua senha",
        )

        if st.button(
            "🔐 Entrar",
            use_container_width=True,
        ):

            usuario_limpo = usuario.lower().strip()

            if verificar_login(
                usuario_limpo,
                senha,
            ):

                dados = USUARIOS[usuario_limpo]

                st.session_state["autenticado"] = True
                st.session_state["usuario"] = usuario_limpo
                st.session_state["nome_usuario"] = dados["nome"]
                st.session_state["perfil_usuario"] = dados["perfil"]

                st.rerun()

            else:
                st.error(
                    "Usuário ou senha incorretos."
                )
# Banco de dados persistente no Supabase/PostgreSQL
DATABASE_URL = st.secrets.get("DATABASE_URL")

if not DATABASE_URL:
    st.error("DATABASE_URL não está configurado nos Secrets do Streamlit.")
    st.stop()

# Compatibilidade caso a URL venha como postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Cliente(Base):
	__tablename__ = "clientes"
	id = Column(Integer, primary_key=True, index=True)
	nome = Column(String(150), nullable=False)
	tipo = Column(String(50), nullable=False)
	cidade = Column(String(100), nullable=False)
	estado = Column(String(2), nullable=False)
	responsavel = Column(String(100), nullable=False)
	email = Column(String(150))
	telefone = Column(String(30))
	observacoes = Column(Text)


class Demanda(Base):
	__tablename__ = "demandas"
	id = Column(Integer, primary_key=True, index=True)
	cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
	titulo = Column(String(200), nullable=False)
	descricao = Column(Text)
	responsavel = Column(String(100), nullable=False)
	status = Column(String(50), nullable=False)
	prioridade = Column(String(30), nullable=False)
	prazo = Column(Date)
	data_criacao = Column(Date, nullable=False)
	observacoes = Column(Text)
# =========================================================
# AVALIAÇÕES / RELATÓRIOS MENSAIS
# =========================================================

class ItemAvaliacao(Base):
    __tablename__ = "itens_avaliacao"

    id = Column(Integer, primary_key=True)
    ordem = Column(Integer, nullable=False, default=0)
    codigo = Column(String(50), nullable=False)
    dimensao = Column(String(255), nullable=False)
    criterio = Column(Text, nullable=False)
    classificacao = Column(String(50), nullable=False)


class RelatorioAvaliacao(Base):
    __tablename__ = "relatorios_avaliacao"

    id = Column(Integer, primary_key=True)

    cliente_id = Column(Integer, nullable=False)

    mes_referencia = Column(String(7), nullable=False)

    item_id = Column(Integer, nullable=False)

    disponibilidade = Column(String(50))

    atualidade = Column(String(50))

    serie_historica = Column(String(50))

    observacoes = Column(Text)


class Almoxarifado(Base):
    __tablename__ = "almoxarifados"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, nullable=False)
    cliente = Column(String(150), nullable=False)
    email_orgao = Column(String(200))
    email_contabilidade = Column(String(200))
    responsavel = Column(String(50), nullable=False, default="Produção Própria")

    jan = Column(String(10), default="")
    fev = Column(String(10), default="")
    mar = Column(String(10), default="")
    abr = Column(String(10), default="")
    mai = Column(String(10), default="")
    jun = Column(String(10), default="")
    jul = Column(String(10), default="")
    ago = Column(String(10), default="")
    set = Column(String(10), default="")
    out = Column(String(10), default="")
    nov = Column(String(10), default="")
    dez = Column(String(10), default="")


class ControlePublicacao(Base):
    __tablename__ = "controle_publicacoes"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    tipo_relatorio = Column(String(100), nullable=False)
    periodo = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)
    publicado = Column(Boolean, default=False, nullable=False)
    data_publicacao = Column(Date, nullable=True)
    observacao = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)

RESPONSAVEIS = ["Vitor", "Ítalo", "Jadsson", "Álvaro Vinícius", "Não definido"]
STATUS = ["A Fazer", "Em Andamento", "Aguardando Cliente", "Concluído"]

PERIODICIDADES_PUBLICACAO = {
    "RREO — Relatório Resumido da Execução Orçamentária": [
        "1º Bimestre", "2º Bimestre", "3º Bimestre",
        "4º Bimestre", "5º Bimestre", "6º Bimestre",
    ],
    "RGF — Relatório de Gestão Fiscal": [
        "1º Quadrimestre", "2º Quadrimestre", "3º Quadrimestre",
    ],
    "RCI — Relatório de Controle Interno": [
        "1º Trimestre", "2º Trimestre", "3º Trimestre", "4º Trimestre",
    ],
    "RGA — Relatório de Gestão Anual": ["Anual"],
    "Balanço Geral": ["Anual"],
}


def clientes():
	with SessionLocal() as db:
		return db.query(Cliente).order_by(Cliente.nome).all()


def demandas():

    perfil = st.session_state.get("perfil_usuario", "")
    nome_usuario = st.session_state.get("nome_usuario", "")

    with SessionLocal() as db:

        rows = db.query(Demanda).order_by(Demanda.id.desc()).all()

        resultados = []

        for d in rows:

            cliente = (
                db.query(Cliente)
                .filter(Cliente.id == d.cliente_id)
                .first()
            )

            # Gerente pode visualizar todas as demandas
            if perfil in ["Gerente", "Diretor Presidente"]:
                resultados.append((d, cliente))

            # Publicador visualiza somente sua própria carteira
            elif (
                perfil == "Publicador"
                and cliente
                and cliente.responsavel == nome_usuario
            ):
                resultados.append((d, cliente))

        return resultados


def excluir(model, ident):
	with SessionLocal() as db:
		item = db.query(model).filter(model.id == ident).first()
		if item:
			db.delete(item)
			db.commit()
def importar_carteira_excel(caminho_arquivo):
    from openpyxl import load_workbook

    wb = load_workbook(caminho_arquivo, data_only=True)
    ws = wb["CARTEIRA"]
# =========================================================
# IMPORTAÇÃO DOS ITENS DE AVALIAÇÃO
# =========================================================

def importar_itens_avaliacao_excel(arquivo):
    import pandas as pd

    df = pd.read_excel(arquivo, header=2)

    importados = 0
    ignorados = 0

    with SessionLocal() as db:
        for indice, linha in df.iterrows():
            dimensao = linha.iloc[0]
            codigo = linha.iloc[1]
            criterio = linha.iloc[2]
            classificacao = linha.iloc[3]

            if pd.isna(dimensao) or pd.isna(criterio):
                continue

            dimensao = str(dimensao).strip()
            criterio = str(criterio).strip()

            if pd.isna(classificacao):
                classificacao = ""
            else:
                classificacao = str(classificacao).strip()

            if pd.isna(codigo):
                codigo = ""
            elif hasattr(codigo, "strftime"):
                codigo = codigo.strftime("%Y-%m-%d")
            else:
                codigo = str(codigo).strip()

            ordem_original = int(indice) + 1

            existente = (
                db.query(ItemAvaliacao)
                .filter(
                    ItemAvaliacao.codigo == codigo,
                    ItemAvaliacao.criterio == criterio
                )
                .first()
            )

            if existente:
                existente.ordem = ordem_original
                existente.dimensao = dimensao
                existente.classificacao = classificacao
                ignorados += 1
                continue

            item = ItemAvaliacao(
                ordem=ordem_original,
                codigo=codigo,
                dimensao=dimensao,
                criterio=criterio,
                classificacao=classificacao
            )

            db.add(item)
            importados += 1

        db.commit()

    return importados, ignorados

# =========================================================
# CONTROLE DE ACESSO
# =========================================================

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    tela_login()
    st.stop()
st.sidebar.image(
    "assets/logo-facilita.png",
    use_container_width=True,
)

pagina = st.sidebar.radio(
    "Navegação",
    [
        "Dashboard",
        "Clientes",
        "Demandas",
        "Kanban",
        "Carteiras",
        "Relatórios",
        "Controle de Publicações",
        "Almoxarifados",
        "Configurações",
    ],
)
st.sidebar.markdown("---")

st.sidebar.write(
    "👤 " + st.session_state.get("nome_usuario", "")
)

st.sidebar.caption(
    "Perfil: " + st.session_state.get("perfil_usuario", "")
)

if st.sidebar.button("🚪 Sair", use_container_width=True):
    st.session_state["autenticado"] = False
    st.session_state.pop("usuario", None)
    st.session_state.pop("nome_usuario", None)
    st.session_state.pop("perfil_usuario", None)
    st.rerun()
  

if pagina == "Dashboard":
    st.title("📊 Dashboard")
    st.caption("Visão geral da operação, demandas, carteiras e publicações.")

    perfil = st.session_state.get("perfil_usuario", "")
    nome_usuario = st.session_state.get("nome_usuario", "")
    hoje = date.today()

    # ---------------------------------------------------------
    # FILTROS DO DASHBOARD
    # ---------------------------------------------------------
    cs_todos = clientes()

    if perfil == "Publicador":
        responsaveis_dashboard = [nome_usuario]
        clientes_dashboard = [
            c for c in cs_todos if c.responsavel == nome_usuario
        ]
    else:
        responsaveis_dashboard = ["Todos"] + sorted({
            c.responsavel for c in cs_todos if c.responsavel
        })
        filtro_resp_dashboard = st.selectbox(
            "👤 Responsável pela carteira",
            responsaveis_dashboard,
            key="dashboard_responsavel",
        )
        if filtro_resp_dashboard == "Todos":
            clientes_dashboard = cs_todos
        else:
            clientes_dashboard = [
                c for c in cs_todos
                if c.responsavel == filtro_resp_dashboard
            ]

    if perfil == "Publicador":
        st.info(f"Visualização da carteira de **{nome_usuario}**.")

    ids_clientes = {c.id for c in clientes_dashboard}

    with SessionLocal() as db:
        demandas_dashboard = (
            db.query(Demanda)
            .filter(Demanda.cliente_id.in_(ids_clientes) if ids_clientes else False)
            .order_by(Demanda.id.desc())
            .all()
        )

        publicacoes_dashboard = (
            db.query(ControlePublicacao)
            .filter(ControlePublicacao.ano == hoje.year)
            .all()
        )

    # ---------------------------------------------------------
    # INDICADORES PRINCIPAIS
    # ---------------------------------------------------------
    abertas = [d for d in demandas_dashboard if d.status != "Concluído"]
    concluidas = [d for d in demandas_dashboard if d.status == "Concluído"]
    atrasadas = [
        d for d in abertas
        if d.prazo and d.prazo < hoje
    ]
    vencendo_7 = [
        d for d in abertas
        if d.prazo and hoje <= d.prazo <= hoje.fromordinal(hoje.toordinal() + 7)
    ]

    responsaveis_ativos = len({
        c.responsavel for c in clientes_dashboard if c.responsavel
    })

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("👥 Clientes", len(clientes_dashboard))
    m2.metric("📋 Demandas abertas", len(abertas))
    m3.metric("🚨 Atrasadas", len(atrasadas))
    m4.metric("✅ Concluídas", len(concluidas))
    m5.metric("👤 Responsáveis", responsaveis_ativos)

    st.divider()

    # ---------------------------------------------------------
    # PUBLICAÇÕES DO ANO
    # ---------------------------------------------------------
    total_previsto = (
        len(clientes_dashboard)
        * sum(len(periodos) for periodos in PERIODICIDADES_PUBLICACAO.values())
    )

    ids_visiveis = ids_clientes
    publicacoes_validas = [
        p for p in publicacoes_dashboard
        if p.cliente_id in ids_visiveis
        and p.tipo_relatorio in PERIODICIDADES_PUBLICACAO
        and p.periodo in PERIODICIDADES_PUBLICACAO[p.tipo_relatorio]
    ]
    total_publicado = sum(1 for p in publicacoes_validas if p.publicado)
    total_pendente = max(total_previsto - total_publicado, 0)
    percentual_pub = (
        total_publicado / total_previsto * 100
        if total_previsto else 0
    )

    st.subheader(f"📋 Publicações — {hoje.year}")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Previstas", total_previsto)
    p2.metric("Publicadas", total_publicado)
    p3.metric("Pendentes", total_pendente)
    p4.metric("Conclusão", f"{percentual_pub:.0f}%")
    st.progress(
        int(min(percentual_pub, 100)),
        text=f"{percentual_pub:.0f}% do controle anual concluído",
    )

    st.divider()

    # ---------------------------------------------------------
    # ALERTAS E DEMANDAS RECENTES
    # ---------------------------------------------------------
    col_alertas, col_recentes = st.columns([1, 1.5])

    with col_alertas:
        st.subheader("🔔 Alertas")

        if atrasadas:
            st.error(f"🚨 {len(atrasadas)} demanda(s) atrasada(s).")
            for d in atrasadas[:5]:
                cliente = next((c for c in clientes_dashboard if c.id == d.cliente_id), None)
                nome_cliente = cliente.nome if cliente else "Cliente não encontrado"
                st.write(
                    f"**{d.titulo}** — {nome_cliente} — "
                    f"prazo {d.prazo.strftime('%d/%m/%Y')}"
                )
        else:
            st.success("Nenhuma demanda atrasada.")

        if vencendo_7:
            st.warning(f"⏰ {len(vencendo_7)} demanda(s) vencem nos próximos 7 dias.")
        else:
            st.info("Nenhuma demanda vencendo nos próximos 7 dias.")

        if total_pendente:
            st.warning(f"📋 {total_pendente} publicação(ões) ainda pendente(s) no ano.")
        else:
            st.success("🎉 Todas as publicações previstas estão concluídas.")

    with col_recentes:
        st.subheader("📌 Demandas em aberto")
        if not abertas:
            st.info("Não existem demandas abertas para os filtros selecionados.")
        else:
            for d in abertas[:8]:
                cliente = next((c for c in clientes_dashboard if c.id == d.cliente_id), None)
                nome_cliente = cliente.nome if cliente else "Cliente não encontrado"
                prazo_txt = d.prazo.strftime("%d/%m/%Y") if d.prazo else "Sem prazo"
                prioridade_icon = {"Alta": "🔴", "Média": "🟠", "Baixa": "🟢"}.get(d.prioridade, "⚪")
                with st.container(border=True):
                    st.markdown(f"**{d.titulo}**")
                    st.caption(
                        f"🏛️ {nome_cliente} · 👤 {d.responsavel} · "
                        f"{prioridade_icon} {d.prioridade} · 📅 {prazo_txt}"
                    )
                    st.caption(f"Status: {d.status}")

    st.divider()

    # ---------------------------------------------------------
    # CARTEIRA POR RESPONSÁVEL
    # ---------------------------------------------------------
    st.subheader("🗂️ Carteira por responsável")

    if not clientes_dashboard:
        st.info("Nenhum cliente encontrado para os filtros selecionados.")
    else:
        grupos = {}
        for c in clientes_dashboard:
            grupos.setdefault(c.responsavel or "Não definido", []).append(c)

        for responsavel, grupo in sorted(grupos.items(), key=lambda x: x[0]):
            demanda_grupo = [
                d for d in demandas_dashboard
                if d.cliente_id in {c.id for c in grupo}
            ]
            abertas_grupo = sum(1 for d in demanda_grupo if d.status != "Concluído")
            atrasadas_grupo = sum(
                1 for d in demanda_grupo
                if d.status != "Concluído" and d.prazo and d.prazo < hoje
            )
            with st.container(border=True):
                a, b, c, d = st.columns(4)
                a.markdown(f"**👤 {responsavel}**")
                a.caption("Responsável")
                b.metric("Clientes", len(grupo))
                c.metric("Demandas abertas", abertas_grupo)
                d.metric("Atrasadas", atrasadas_grupo)

    st.divider()

    # ---------------------------------------------------------
    # DISTRIBUIÇÃO DAS DEMANDAS
    # ---------------------------------------------------------
    st.subheader("📊 Distribuição das demandas")

    col_status, col_prioridade = st.columns(2)

    with col_status:
        st.markdown("**Por status**")
        total_demandas = len(demandas_dashboard)
        for status in STATUS:
            quantidade = sum(1 for d in demandas_dashboard if d.status == status)
            percentual = quantidade / total_demandas * 100 if total_demandas else 0
            st.write(f"{status}: **{quantidade}** ({percentual:.0f}%)")
            st.progress(int(percentual))

    with col_prioridade:
        st.markdown("**Por prioridade**")
        total_demandas = len(demandas_dashboard)
        for prioridade in ["Alta", "Média", "Baixa"]:
            quantidade = sum(1 for d in demandas_dashboard if d.prioridade == prioridade)
            percentual = quantidade / total_demandas * 100 if total_demandas else 0
            st.write(f"{prioridade}: **{quantidade}** ({percentual:.0f}%)")
            st.progress(int(percentual))

elif pagina == "Clientes":
	st.title("👥 Clientes")
	cadastro, lista = st.tabs(["➕ Cadastrar cliente", "📋 Clientes cadastrados"])
	with cadastro:
		with st.form("cliente"):
			nome = st.text_input("Nome do órgão público*")
			tipo = st.selectbox("Tipo de órgão*", ["Prefeitura", "Câmara Municipal", "Outro"])
			cidade, estado = st.text_input("Cidade*"), st.selectbox("Estado*", ["SE", "BA", "AL", "PE", "PB", "CE", "PI", "MA", "RN", "Outro"])
			resp = st.selectbox("Responsável pela carteira*", RESPONSAVEIS)
			email, telefone = st.text_input("E-mail"), st.text_input("Telefone ou WhatsApp")
			obs = st.text_area("Observações")
			if st.form_submit_button("💾 Salvar cliente", use_container_width=True):
				if not nome.strip() or not cidade.strip():
					st.error("Informe o nome e a cidade.")
				else:
					with SessionLocal() as db:
						db.add(Cliente(nome=nome.strip(), tipo=tipo, cidade=cidade.strip(), estado=estado, responsavel=resp, email=email.strip(), telefone=telefone.strip(), observacoes=obs.strip()))
						db.commit()
					st.success("Cliente cadastrado com sucesso!")
					st.rerun()
	with lista:
		for cliente in clientes():
			with st.expander(f"{cliente.nome} — {cliente.cidade}/{cliente.estado}"):
				st.write(f"**Tipo:** {cliente.tipo}  |  **Responsável:** {cliente.responsavel}")
				st.write(f"**E-mail:** {cliente.email or 'Não informado'}  |  **Telefone:** {cliente.telefone or 'Não informado'}")
				if cliente.observacoes: st.write(f"**Observações:** {cliente.observacoes}")
				if st.button("🗑️ Excluir cliente", key=f"ec{cliente.id}"):
					excluir(Cliente, cliente.id); st.rerun()

elif pagina == "Demandas":
    st.title("📋 Demandas")

    cs = clientes()

    nova, lista = st.tabs([
        "➕ Nova demanda",
        "📋 Demandas cadastradas"
    ])

    with nova:
        if not cs:
            st.warning(
                "Cadastre pelo menos um cliente antes de criar uma demanda."
            )
        else:
            with st.form("demanda"):
                mapa = {
                    f"{c.nome} — {c.cidade}/{c.estado}": c.id
                    for c in cs
                }

                cliente = st.selectbox(
                    "Cliente*",
                    list(mapa.keys())
                )

                titulo = st.text_input(
                    "Título da demanda*"
                )

                descricao = st.text_area(
                    "Descrição da solicitação"
                )

                responsavel = st.selectbox(
                    "Responsável*",
                    RESPONSAVEIS[:-1]
                )

                status = st.selectbox(
                    "Status*",
                    STATUS
                )

                prioridade = st.selectbox(
                    "Prioridade*",
                    ["Alta", "Média", "Baixa"]
                )

                prazo = st.date_input(
                    "Prazo",
                    value=date.today()
                )

                obs = st.text_area(
                    "Observações internas"
                )

                salvar = st.form_submit_button(
                    "💾 Salvar demanda",
                    use_container_width=True
                )

                if salvar:
                    if not titulo.strip():
                        st.error(
                            "Informe o título da demanda."
                        )
                    else:
                        with SessionLocal() as db:
                            db.add(
                                Demanda(
                                    cliente_id=mapa[cliente],
                                    titulo=titulo.strip(),
                                    descricao=descricao.strip(),
                                    responsavel=responsavel,
                                    status=status,
                                    prioridade=prioridade,
                                    prazo=prazo,
                                    data_criacao=date.today(),
                                    observacoes=obs.strip()
                                )
                            )

                            db.commit()

                        st.success(
                            "Demanda cadastrada com sucesso!"
                        )

                        st.rerun()

    with lista:
        st.subheader("🔎 Filtros")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            filtro_status = st.selectbox(
                "Status",
                ["Todos"] + STATUS
            )

        with col2:
            filtro_responsavel = st.selectbox(
                "Responsável",
                ["Todos"] + RESPONSAVEIS[:-1]
            )

        with col3:
            filtro_prioridade = st.selectbox(
                "Prioridade",
                ["Todas", "Alta", "Média", "Baixa"]
            )

        with col4:
            opcoes_clientes = ["Todos"] + [
                f"{c.nome} — {c.cidade}/{c.estado}"
                for c in cs
            ]

            filtro_cliente = st.selectbox(
                "Cliente",
                opcoes_clientes
            )

        st.divider()

        resultados = []

        for demanda, cliente in demandas():

            if (
                filtro_status != "Todos"
                and demanda.status != filtro_status
            ):
                continue

            if (
                filtro_responsavel != "Todos"
                and demanda.responsavel != filtro_responsavel
            ):
                continue

            if (
                filtro_prioridade != "Todas"
                and demanda.prioridade != filtro_prioridade
            ):
                continue

            if filtro_cliente != "Todos":
                nome_cliente = (
                    f"{cliente.nome} — "
                    f"{cliente.cidade}/{cliente.estado}"
                    if cliente
                    else "Cliente não encontrado"
                )

                if nome_cliente != filtro_cliente:
                    continue

            resultados.append(
                (demanda, cliente)
            )

        st.write(
            f"**{len(resultados)} demanda(s) encontrada(s).**"
        )

        if not resultados:
            st.info(
                "Nenhuma demanda encontrada com esses filtros."
            )

        for demanda, cliente in resultados:

            nome_cliente = (
                cliente.nome
                if cliente
                else "Cliente não encontrado"
            )

            with st.expander(
                f"{demanda.titulo} — {nome_cliente}"
            ):

                st.write(
                    f"**Responsável:** "
                    f"{demanda.responsavel}"
                )

                st.write(
                    f"**Status:** "
                    f"{demanda.status}"
                )

                st.write(
                    f"**Prioridade:** "
                    f"{demanda.prioridade}"
                )

                if demanda.prazo:
                    st.write(
                        f"**Prazo:** "
                        f"{demanda.prazo.strftime('%d/%m/%Y')}"
                    )
                else:
                    st.write(
                        "**Prazo:** Não informado"
                    )

                if demanda.descricao:
                    st.write(
                        f"**Descrição:** "
                        f"{demanda.descricao}"
                    )

                if demanda.observacoes:
                    st.write(
                        f"**Observações:** "
                        f"{demanda.observacoes}"
                    )

                novo = st.selectbox(
                    "Alterar status",
                    STATUS,
                    index=STATUS.index(demanda.status),
                    key=f"s{demanda.id}"
                )

                if st.button(
                    "💾 Atualizar status",
                    key=f"u{demanda.id}"
                ):
                    with SessionLocal() as db:
                        db.query(Demanda).filter(
                            Demanda.id == demanda.id
                        ).update(
                            {"status": novo}
                        )

                        db.commit()

                    st.rerun()

                if st.button(
                    "🗑️ Excluir demanda",
                    key=f"ed{demanda.id}"
                ):
                    excluir(
                        Demanda,
                        demanda.id
                    )

                    st.rerun()
elif pagina == "Kanban":
    st.title("📌 Kanban de Demandas")

    todas_demandas = demandas()

    colunas = st.columns(4)

    for i, status in enumerate(STATUS):
        with colunas[i]:
            demandas_coluna = [
                (demanda, cliente)
                for demanda, cliente in todas_demandas
                if demanda.status == status
            ]

            st.subheader(
                f"{status} ({len(demandas_coluna)})"
            )

            if not demandas_coluna:
                st.info("Nenhuma demanda")

            for demanda, cliente in demandas_coluna:
                nome_cliente = (
                    cliente.nome
                    if cliente
                    else "Cliente não encontrado"
                )

                with st.container(border=True):
                    st.write(
                        f"**{demanda.titulo}**"
                    )

                    st.caption(
                        f"🏛️ {nome_cliente}"
                    )

                    st.caption(
                        f"👤 {demanda.responsavel}"
                    )

                    st.caption(
                        f"🔥 Prioridade: {demanda.prioridade}"
                    )

                    if demanda.prazo:
                        st.caption(
                            f"📅 Prazo: "
                            f"{demanda.prazo.strftime('%d/%m/%Y')}"
                        )

                    novo_status = st.selectbox(
                        "Mover para",
                        STATUS,
                        index=STATUS.index(demanda.status),
                        key=f"kanban_status_{demanda.id}"
                    )

                    if novo_status != demanda.status:
                        with SessionLocal() as db:
                            db.query(Demanda).filter(
                                Demanda.id == demanda.id
                            ).update(
                                {"status": novo_status}
                            )

                            db.commit()

                        st.rerun()


elif pagina == "Carteiras":
    st.title("🗂️ Carteiras")

    st.subheader("📥 Importar carteira 2026")

    st.write(
        "Use o arquivo Excel da divisão de carteiras para cadastrar "
        "automaticamente os clientes e seus respectivos responsáveis."
    )

    arquivo = st.file_uploader(
        "Selecione a planilha da carteira",
        type=["xlsx"],
    )

    if arquivo is not None:
        st.success(
            f"Arquivo selecionado: {arquivo.name}"
        )

        if st.button(
            "🚀 Importar carteira 2026",
            use_container_width=True
        ):
            importados, ignorados = importar_carteira_excel(
                arquivo
            )

            st.success(
                f"Importação concluída! "
                f"{importados} cliente(s) importado(s)."
            )

            if ignorados > 0:
                st.info(
                    f"{ignorados} cliente(s) já existia(m) "
                    "no sistema e foi(ram) atualizado(s)."
                )

            st.rerun()

    st.divider()

    st.subheader("👥 Carteiras atuais")

    cs = clientes()

    for responsavel in RESPONSAVEIS[:3]:
        grupo = [
            c
            for c in cs
            if c.responsavel == responsavel
        ]

        with st.expander(
            f"{responsavel} — {len(grupo)} cliente(s)"
        ):
            if not grupo:
                st.info(
                    "Nenhum cliente cadastrado."
                )

            for cliente in grupo:
                st.write(
                    f"• **{cliente.nome}** — {cliente.tipo}"
                )


elif pagina == "Relatórios":

    st.title("📈 Relatórios de Avaliação")

    # =========================================================
    # FUNÇÃO PARA GERAR PDF
    # =========================================================

    def gerar_pdf_relatorio(cliente_nome, mes_referencia, itens_pdf):

        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import (
            getSampleStyleSheet,
            ParagraphStyle,
        )
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
        )

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )

        styles = getSampleStyleSheet()

        titulo_style = ParagraphStyle(
            "TituloFacilita",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=22,
            spaceAfter=10,
        )

        subtitulo_style = ParagraphStyle(
            "SubtituloFacilita",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=11,
            leading=14,
            spaceAfter=15,
        )

        dimensao_style = ParagraphStyle(
            "DimensaoFacilita",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            spaceBefore=12,
            spaceAfter=8,
        )

        normal_style = ParagraphStyle(
            "NormalFacilita",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
        )

        small_style = ParagraphStyle(
            "SmallFacilita",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
        )

        elementos = []

        elementos.append(
            Paragraph(
                "FACILITA MANAGER",
                titulo_style,
            )
        )

        elementos.append(
            Paragraph(
                "RELATÓRIO MENSAL DE AVALIAÇÃO",
                subtitulo_style,
            )
        )

        dados_identificacao = [
            [
                Paragraph(
                    "<b>Cliente</b>",
                    normal_style,
                ),
                Paragraph(
                    str(cliente_nome),
                    normal_style,
                ),
            ],
            [
                Paragraph(
                    "<b>Mês de referência</b>",
                    normal_style,
                ),
                Paragraph(
                    str(mes_referencia),
                    normal_style,
                ),
            ],
        ]

        tabela_identificacao = Table(
            dados_identificacao,
            colWidths=[
                4 * cm,
                12 * cm,
            ],
        )

        tabela_identificacao.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.whitesmoke,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        elementos.append(tabela_identificacao)
        elementos.append(Spacer(1, 15))

        dimensao_atual = None

        for item in itens_pdf:

            dimensao = item["dimensao"]

            if dimensao != dimensao_atual:

                if dimensao_atual is not None:
                    elementos.append(
                        Spacer(1, 8)
                    )

                elementos.append(
                    Paragraph(
                        f"📂 {dimensao}",
                        dimensao_style,
                    )
                )

                dimensao_atual = dimensao

            codigo = item["codigo"] or ""
            criterio = item["criterio"]

            elementos.append(
                Paragraph(
                    f"<b>{codigo} — {criterio}</b>",
                    normal_style,
                )
            )

            classificacao = (
                item["classificacao"]
                or "Não informado"
            )

            elementos.append(
                Paragraph(
                    f"Classificação: {classificacao}",
                    small_style,
                )
            )

            tabela_avaliacao = [
                [
                    Paragraph(
                        "<b>Disponibilidade</b>",
                        small_style,
                    ),
                    Paragraph(
                        "<b>Atualidade</b>",
                        small_style,
                    ),
                    Paragraph(
                        "<b>Série histórica</b>",
                        small_style,
                    ),
                ],
                [
                    Paragraph(
                        str(
                            item["disponibilidade"]
                        ),
                        small_style,
                    ),
                    Paragraph(
                        str(
                            item["atualidade"]
                        ),
                        small_style,
                    ),
                    Paragraph(
                        str(
                            item["serie_historica"]
                        ),
                        small_style,
                    ),
                ],
            ]

            tabela = Table(
                tabela_avaliacao,
                colWidths=[
                    5.2 * cm,
                    5.2 * cm,
                    5.2 * cm,
                ],
            )

            tabela.setStyle(
                TableStyle(
                    [
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.grey,
                        ),
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.whitesmoke,
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP",
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                    ]
                )
            )

            elementos.append(tabela)
            elementos.append(Spacer(1, 5))

            observacoes = (
                item["observacoes"]
                or ""
            )

            if observacoes.strip():

                elementos.append(
                    Paragraph(
                        "<b>Observações técnicas – Facilita:</b> "
                        + observacoes,
                        small_style,
                    )
                )

            elementos.append(
                Spacer(1, 12)
            )

        doc.build(elementos)

        buffer.seek(0)

        return buffer

    # =========================================================
    # RELATÓRIOS SALVOS
    # =========================================================

    st.subheader("🗂️ Relatórios realizados")

    with SessionLocal() as db:

        clientes_disponiveis = (
            db.query(Cliente)
            .order_by(Cliente.nome.asc())
            .all()
        )

        relatorios_base = (
            db.query(
                RelatorioAvaliacao.cliente_id,
                RelatorioAvaliacao.mes_referencia,
            )
            .distinct()
            .all()
        )

    nomes_clientes = {
        cliente.id: cliente.nome
        for cliente in clientes_disponiveis
    }

    # =========================================================
    # FILTROS
    # =========================================================

    col_filtro1, col_filtro2 = st.columns(2)

    with col_filtro1:

        opcoes_filtro_cliente = [
            "Todos"
        ]

        opcoes_filtro_cliente += sorted(
            [
                nome
                for nome in nomes_clientes.values()
                if nome
            ]
        )

        filtro_cliente_relatorio = st.selectbox(
            "🔎 Filtrar por cliente",
            opcoes_filtro_cliente,
            key="filtro_cliente_relatorio",
        )

    with col_filtro2:

        meses_disponiveis = sorted(
            {
                mes
                for _, mes in relatorios_base
                if mes
            },
            reverse=True,
        )

        filtro_mes_relatorio = st.selectbox(
            "📅 Filtrar por mês",
            ["Todos"] + meses_disponiveis,
            key="filtro_mes_relatorio",
        )

    # =========================================================
    # APLICAR FILTROS
    # =========================================================

    relatorios_filtrados = []

    for cliente_id, mes in relatorios_base:

        nome_cliente = nomes_clientes.get(
            cliente_id,
            "Cliente não encontrado",
        )

        if (
            filtro_cliente_relatorio != "Todos"
            and nome_cliente != filtro_cliente_relatorio
        ):
            continue

        if (
            filtro_mes_relatorio != "Todos"
            and mes != filtro_mes_relatorio
        ):
            continue

        relatorios_filtrados.append(
            (
                cliente_id,
                mes,
                nome_cliente,
            )
        )

    st.divider()

    st.write(
        f"**{len(relatorios_filtrados)} "
        f"relatório(s) encontrado(s).**"
    )

    # =========================================================
    # LISTAGEM
    # =========================================================

    if not relatorios_filtrados:

        st.info(
            "Nenhum relatório encontrado "
            "com os filtros selecionados."
        )

    else:

        for (
            cliente_id,
            mes,
            nome_cliente,
        ) in relatorios_filtrados:

            with st.container(border=True):

                col1, col2, col3, col4, col5 = st.columns(
                    [4, 1.5, 1.4, 1.4, 1.4]
                )

                with col1:

                    st.markdown(
                        f"**🏛️ {nome_cliente}**"
                    )

                    st.caption(
                        f"📅 Referência: {mes}"
                    )

                # =================================================
                # ABRIR
                # =================================================

                with col2:

                    if st.button(
                        "👁️ Abrir",
                        key=(
                            f"abrir_relatorio_"
                            f"{cliente_id}_{mes}"
                        ),
                        use_container_width=True,
                    ):

                        st.session_state[
                            "relatorio_cliente_aberto"
                        ] = cliente_id

                        st.session_state[
                            "relatorio_mes_aberto"
                        ] = mes

                        st.session_state.pop(
                            "relatorio_cliente_editar",
                            None,
                        )

                        st.session_state.pop(
                            "relatorio_mes_editar",
                            None,
                        )

                        st.rerun()

                # =================================================
                # EDITAR
                # =================================================

                with col3:

                    if st.button(
                        "✏️ Editar",
                        key=(
                            f"editar_relatorio_"
                            f"{cliente_id}_{mes}"
                        ),
                        use_container_width=True,
                    ):

                        st.session_state[
                            "relatorio_cliente_editar"
                        ] = cliente_id

                        st.session_state[
                            "relatorio_mes_editar"
                        ] = mes

                        st.session_state.pop(
                            "relatorio_cliente_aberto",
                            None,
                        )

                        st.session_state.pop(
                            "relatorio_mes_aberto",
                            None,
                        )

                        st.rerun()

                # =================================================
                # EXCLUIR
                # =================================================

                with col4:

                    if st.button(
                        "🗑️ Excluir",
                        key=(
                            f"excluir_relatorio_"
                            f"{cliente_id}_{mes}"
                        ),
                        use_container_width=True,
                    ):

                        with SessionLocal() as db:

                            db.query(
                                RelatorioAvaliacao
                            ).filter(
                                RelatorioAvaliacao.cliente_id
                                == cliente_id,
                                RelatorioAvaliacao.mes_referencia
                                == mes,
                            ).delete(
                                synchronize_session=False
                            )

                            db.commit()

                        if (
                            st.session_state.get(
                                "relatorio_cliente_aberto"
                            )
                            == cliente_id
                            and
                            st.session_state.get(
                                "relatorio_mes_aberto"
                            )
                            == mes
                        ):

                            st.session_state.pop(
                                "relatorio_cliente_aberto",
                                None,
                            )

                            st.session_state.pop(
                                "relatorio_mes_aberto",
                                None,
                            )

                        if (
                            st.session_state.get(
                                "relatorio_cliente_editar"
                            )
                            == cliente_id
                            and
                            st.session_state.get(
                                "relatorio_mes_editar"
                            )
                            == mes
                        ):

                            st.session_state.pop(
                                "relatorio_cliente_editar",
                                None,
                            )

                            st.session_state.pop(
                                "relatorio_mes_editar",
                                None,
                            )

                        st.success(
                            "Relatório excluído com sucesso."
                        )

                        st.rerun()

    # =========================================================
    # RELATÓRIO ABERTO
    # =========================================================

    cliente_aberto = st.session_state.get(
        "relatorio_cliente_aberto"
    )

    mes_aberto = st.session_state.get(
        "relatorio_mes_aberto"
    )

    if cliente_aberto and mes_aberto:

        st.divider()

        with SessionLocal() as db:

            cliente_obj = (
                db.query(Cliente)
                .filter(
                    Cliente.id == cliente_aberto
                )
                .first()
            )

            respostas = (
                db.query(RelatorioAvaliacao)
                .filter(
                    RelatorioAvaliacao.cliente_id
                    == cliente_aberto,
                    RelatorioAvaliacao.mes_referencia
                    == mes_aberto,
                )
                .all()
            )

            itens_ids = [
                resposta.item_id
                for resposta in respostas
            ]

            itens = (
                db.query(ItemAvaliacao)
                .filter(
                    ItemAvaliacao.id.in_(itens_ids)
                )
                .order_by(
                    ItemAvaliacao.ordem.asc()
                )
                .all()
            )

        if not cliente_obj:

            st.error(
                "Cliente do relatório não foi encontrado."
            )

        elif not respostas:

            st.warning(
                "Não foram encontrados dados para este relatório."
            )

        else:

            col_titulo, col_fechar = st.columns(
                [5, 1]
            )

            with col_titulo:

                st.subheader(
                    "📄 Relatório aberto"
                )

                st.markdown(
                    f"### 🏛️ {cliente_obj.nome}"
                )

                st.caption(
                    f"📅 Mês de referência: {mes_aberto}"
                )

            with col_fechar:

                if st.button(
                    "✖️ Fechar",
                    key="fechar_relatorio_aberto",
                    use_container_width=True,
                ):

                    st.session_state.pop(
                        "relatorio_cliente_aberto",
                        None,
                    )

                    st.session_state.pop(
                        "relatorio_mes_aberto",
                        None,
                    )

                    st.rerun()

            # =================================================
            # PREPARAR DADOS
            # =================================================

            respostas_por_item = {
                resposta.item_id: resposta
                for resposta in respostas
            }

            itens_pdf = []

            for item in itens:

                resposta = respostas_por_item.get(
                    item.id
                )

                if not resposta:
                    continue

                itens_pdf.append(
                    {
                        "dimensao": item.dimensao,
                        "codigo": item.codigo,
                        "criterio": item.criterio,
                        "classificacao": (
                            item.classificacao
                        ),
                        "disponibilidade": (
                            resposta.disponibilidade
                            or "Não preenchido"
                        ),
                        "atualidade": (
                            resposta.atualidade
                            or "Não preenchido"
                        ),
                        "serie_historica": (
                            resposta.serie_historica
                            or "Não preenchido"
                        ),
                        "observacoes": (
                            resposta.observacoes
                            or ""
                        ),
                    }
                )

            # =================================================
            # EXPORTAR PDF
            # =================================================

            st.markdown(
                "### 📤 Exportação"
            )

            try:

                pdf = gerar_pdf_relatorio(
                    cliente_obj.nome,
                    mes_aberto,
                    itens_pdf,
                )

                nome_pdf = (
                    f"Relatorio_{cliente_obj.nome}_"
                    f"{mes_aberto}"
                    .replace(" ", "_")
                    .replace("/", "-")
                )

                st.download_button(
                    label="📄 Exportar relatório em PDF",
                    data=pdf,
                    file_name=f"{nome_pdf}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key=(
                        f"download_pdf_"
                        f"{cliente_aberto}_{mes_aberto}"
                    ),
                )

            except Exception as erro:

                st.error(
                    f"Erro ao gerar o PDF: {erro}"
                )

            st.divider()

            # =================================================
            # EXIBIR RELATÓRIO
            # =================================================

            dimensao_atual = None

            for item in itens_pdf:

                if item["dimensao"] != dimensao_atual:

                    dimensao_atual = item["dimensao"]

                    st.markdown(
                        f"### 📂 {dimensao_atual}"
                    )

                with st.container(border=True):

                    st.markdown(
                        f"**{item['codigo']} — "
                        f"{item['criterio']}**"
                    )

                    st.caption(
                        f"Classificação: "
                        f"{item['classificacao']}"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Disponibilidade",
                            item["disponibilidade"],
                        )

                    with col2:

                        st.metric(
                            "Atualidade",
                            item["atualidade"],
                        )

                    with col3:

                        st.metric(
                            "Série histórica",
                            item["serie_historica"],
                        )

                    if item["observacoes"].strip():

                        st.markdown(
                            "**Observações técnicas – Facilita:**"
                        )

                        st.write(
                            item["observacoes"]
                        )

    # =========================================================
    # EDIÇÃO / NOVA AVALIAÇÃO
    # =========================================================

    cliente_editar = st.session_state.get(
        "relatorio_cliente_editar"
    )

    mes_editar = st.session_state.get(
        "relatorio_mes_editar"
    )

    st.divider()

    if cliente_editar and mes_editar:

        st.subheader(
            "✏️ Editando relatório salvo"
        )

        with SessionLocal() as db:

            cliente_edicao = (
                db.query(Cliente)
                .filter(
                    Cliente.id == cliente_editar
                )
                .first()
            )

        if cliente_edicao:

            st.info(
                f"Você está editando o relatório de "
                f"**{cliente_edicao.nome}** referente a "
                f"**{mes_editar}**."
            )

        if st.button(
            "❌ Cancelar edição",
            key="cancelar_edicao_relatorio",
        ):

            st.session_state.pop(
                "relatorio_cliente_editar",
                None,
            )

            st.session_state.pop(
                "relatorio_mes_editar",
                None,
            )

            st.session_state.pop(
                "relatorio_form_cliente",
                None,
            )

            st.session_state.pop(
                "relatorio_form_mes",
                None,
            )

            st.rerun()

    else:

        st.subheader(
            "➕ Criar nova avaliação"
        )

        st.write(
            "Preencha a avaliação mensal de cada cliente "
            "com base nos critérios do modelo de transparência."
        )

    # =========================================================
    # BUSCAR CLIENTES E ITENS
    # =========================================================

    with SessionLocal() as db:

        lista_clientes = (
            db.query(Cliente)
            .order_by(Cliente.nome.asc())
            .all()
        )

        lista_itens = (
            db.query(ItemAvaliacao)
            .order_by(
                ItemAvaliacao.ordem.asc()
            )
            .all()
        )

    if not lista_clientes:

        st.warning(
            "Nenhum cliente cadastrado. "
            "Cadastre um cliente antes de criar uma avaliação."
        )

    elif not lista_itens:

        st.warning(
            "Nenhum critério de avaliação foi encontrado. "
            "Importe a planilha em Configurações."
        )

    else:

        # =====================================================
        # IDENTIFICAÇÃO
        # =====================================================

        st.subheader(
            "📋 Identificação da avaliação"
        )

        opcoes_clientes = {
            cliente.nome: cliente.id
            for cliente in lista_clientes
        }

        nomes_clientes_lista = list(
            opcoes_clientes.keys()
        )

        # -----------------------------------------------------
        # DEFINIR CLIENTE INICIAL
        # -----------------------------------------------------

        cliente_inicial = None

        if cliente_editar:

            for cliente in lista_clientes:

                if cliente.id == cliente_editar:

                    cliente_inicial = cliente.nome
                    break

        if cliente_inicial is None:

            cliente_inicial = (
                nomes_clientes_lista[0]
            )

        if (
            "relatorio_form_cliente"
            not in st.session_state
        ):

            st.session_state[
                "relatorio_form_cliente"
            ] = cliente_inicial

        # Se estiver editando, força o cliente correto
        if cliente_editar:

            st.session_state[
                "relatorio_form_cliente"
            ] = cliente_inicial

        cliente_selecionado = st.selectbox(
            "Cliente",
            nomes_clientes_lista,
            key="relatorio_form_cliente",
        )

        cliente_id_selecionado = (
            opcoes_clientes[
                cliente_selecionado
            ]
        )

        # -----------------------------------------------------
        # DEFINIR MÊS
        # -----------------------------------------------------

        if cliente_editar:

            if (
                "relatorio_form_mes"
                not in st.session_state
            ):

                st.session_state[
                    "relatorio_form_mes"
                ] = mes_editar

            else:

                st.session_state[
                    "relatorio_form_mes"
                ] = mes_editar

        elif (
            "relatorio_form_mes"
            not in st.session_state
        ):

            st.session_state[
                "relatorio_form_mes"
            ] = "09/2026"

        mes_referencia = st.text_input(
            "Mês de referência",
            max_chars=7,
            help=(
                "Use o formato MM/AAAA. "
                "Exemplo: 09/2026."
            ),
            key="relatorio_form_mes",
        )

        # =====================================================
        # VALIDAR MÊS
        # =====================================================

        mes_valido = (
            len(mes_referencia) == 7
            and mes_referencia[2] == "/"
            and mes_referencia[:2].isdigit()
            and mes_referencia[3:].isdigit()
        )

        if not mes_valido:

            st.warning(
                "Digite o mês no formato MM/AAAA. "
                "Exemplo: 09/2026."
            )

        else:

            # =================================================
            # CARREGAR RESPOSTAS EXISTENTES
            # =================================================

            with SessionLocal() as db:

                respostas_salvas = (
                    db.query(
                        RelatorioAvaliacao
                    )
                    .filter(
                        RelatorioAvaliacao.cliente_id
                        == cliente_id_selecionado,
                        RelatorioAvaliacao.mes_referencia
                        == mes_referencia,
                    )
                    .all()
                )

            respostas_por_item = {
                resposta.item_id: resposta
                for resposta in respostas_salvas
            }

            if respostas_salvas:

                if cliente_editar:

                    st.info(
                        f"📝 Este relatório possui "
                        f"{len(respostas_salvas)} item(ns) "
                        f"salvo(s). Os dados atuais foram "
                        f"carregados para edição."
                    )

                else:

                    st.info(
                        f"Este cliente já possui uma avaliação "
                        f"salva para {mes_referencia}. "
                        f"Se continuar e salvar, os dados "
                        f"existentes serão atualizados."
                    )

            # =================================================
            # ITENS
            # =================================================

            st.divider()

            st.subheader(
                "📝 Itens avaliativos"
            )

            st.caption(
                f"Cliente: {cliente_selecionado} | "
                f"Referência: {mes_referencia}"
            )

            dimensoes = {}

            for item in lista_itens:

                if item.dimensao not in dimensoes:

                    dimensoes[
                        item.dimensao
                    ] = []

                dimensoes[
                    item.dimensao
                ].append(item)

            valores_formulario = {}

            opcoes_avaliacao = [
                "Não preenchido",
                "ATENDE",
                "NÃO ATENDE",
                "Não se aplica",
            ]

            # =================================================
            # EXIBIR ITENS
            # =================================================

            for dimensao, itens_dimensao in dimensoes.items():

                st.markdown(
                    f"### 📂 {dimensao}"
                )

                for item in itens_dimensao:

                    resposta = (
                        respostas_por_item.get(
                            item.id
                        )
                    )

                    disponibilidade_atual = (
                        resposta.disponibilidade
                        if resposta
                        and resposta.disponibilidade
                        else "Não preenchido"
                    )

                    atualidade_atual = (
                        resposta.atualidade
                        if resposta
                        and resposta.atualidade
                        else "Não preenchido"
                    )

                    serie_atual = (
                        resposta.serie_historica
                        if resposta
                        and resposta.serie_historica
                        else "Não preenchido"
                    )

                    observacao_atual = (
                        resposta.observacoes
                        if resposta
                        and resposta.observacoes
                        else ""
                    )

                    st.markdown(
                        f"**{item.codigo} — "
                        f"{item.criterio}**"
                    )

                    st.caption(
                        f"Classificação: "
                        f"{item.classificacao}"
                    )

                    col1, col2, col3 = st.columns(3)

                    # -----------------------------------------
                    # DISPONIBILIDADE
                    # -----------------------------------------

                    with col1:

                        disponibilidade = st.selectbox(
                            "Disponibilidade",
                            opcoes_avaliacao,
                            index=(
                                opcoes_avaliacao.index(
                                    disponibilidade_atual
                                )
                                if disponibilidade_atual
                                in opcoes_avaliacao
                                else 0
                            ),
                            key=(
                                f"rel_disp_"
                                f"{cliente_id_selecionado}_"
                                f"{mes_referencia}_"
                                f"{item.id}"
                            ),
                        )

                    # -----------------------------------------
                    # ATUALIDADE
                    # -----------------------------------------

                    with col2:

                        atualidade = st.selectbox(
                            "Atualidade",
                            opcoes_avaliacao,
                            index=(
                                opcoes_avaliacao.index(
                                    atualidade_atual
                                )
                                if atualidade_atual
                                in opcoes_avaliacao
                                else 0
                            ),
                            key=(
                                f"rel_atual_"
                                f"{cliente_id_selecionado}_"
                                f"{mes_referencia}_"
                                f"{item.id}"
                            ),
                        )

                    # -----------------------------------------
                    # SÉRIE HISTÓRICA
                    # -----------------------------------------

                    with col3:

                        serie_historica = st.selectbox(
                            "Série histórica",
                            opcoes_avaliacao,
                            index=(
                                opcoes_avaliacao.index(
                                    serie_atual
                                )
                                if serie_atual
                                in opcoes_avaliacao
                                else 0
                            ),
                            key=(
                                f"rel_serie_"
                                f"{cliente_id_selecionado}_"
                                f"{mes_referencia}_"
                                f"{item.id}"
                            ),
                        )

                    # -----------------------------------------
                    # OBSERVAÇÕES
                    # -----------------------------------------

                    observacoes = st.text_area(
                        "Observações técnicas – Facilita",
                        value=observacao_atual,
                        key=(
                            f"rel_obs_"
                            f"{cliente_id_selecionado}_"
                            f"{mes_referencia}_"
                            f"{item.id}"
                        ),
                        height=80,
                    )

                    valores_formulario[
                        item.id
                    ] = {
                        "disponibilidade": (
                            disponibilidade
                        ),
                        "atualidade": (
                            atualidade
                        ),
                        "serie_historica": (
                            serie_historica
                        ),
                        "observacoes": (
                            observacoes
                        ),
                    }

                    st.divider()

            # =================================================
            # BOTÃO SALVAR
            # =================================================

            texto_botao = (
                "💾 Atualizar relatório"
                if cliente_editar
                else "💾 Salvar avaliação"
            )

            if st.button(
                texto_botao,
                type="primary",
                use_container_width=True,
                key="salvar_relatorio",
            ):

                with SessionLocal() as db:

                    salvos = 0

                    for (
                        item_id,
                        valores,
                    ) in valores_formulario.items():

                        registro = (
                            db.query(
                                RelatorioAvaliacao
                            )
                            .filter(
                                RelatorioAvaliacao.cliente_id
                                == cliente_id_selecionado,
                                RelatorioAvaliacao.mes_referencia
                                == mes_referencia,
                                RelatorioAvaliacao.item_id
                                == item_id,
                            )
                            .first()
                        )

                        if registro:

                            registro.disponibilidade = (
                                valores[
                                    "disponibilidade"
                                ]
                            )

                            registro.atualidade = (
                                valores[
                                    "atualidade"
                                ]
                            )

                            registro.serie_historica = (
                                valores[
                                    "serie_historica"
                                ]
                            )

                            registro.observacoes = (
                                valores[
                                    "observacoes"
                                ]
                            )

                        else:

                            novo_registro = (
                                RelatorioAvaliacao(
                                    cliente_id=(
                                        cliente_id_selecionado
                                    ),
                                    mes_referencia=(
                                        mes_referencia
                                    ),
                                    item_id=item_id,
                                    disponibilidade=(
                                        valores[
                                            "disponibilidade"
                                        ]
                                    ),
                                    atualidade=(
                                        valores[
                                            "atualidade"
                                        ]
                                    ),
                                    serie_historica=(
                                        valores[
                                            "serie_historica"
                                        ]
                                    ),
                                    observacoes=(
                                        valores[
                                            "observacoes"
                                        ]
                                    ),
                                )
                            )

                            db.add(
                                novo_registro
                            )

                        salvos += 1

                    db.commit()

                st.success(
                    f"✅ Relatório salvo com sucesso! "
                    f"{salvos} item(ns) processado(s)."
                )

                # Se estava editando, encerra o modo de edição
                if cliente_editar:

                    st.session_state.pop(
                        "relatorio_cliente_editar",
                        None,
                    )

                    st.session_state.pop(
                        "relatorio_mes_editar",
                        None,
                    )

                st.rerun()



elif pagina == "Controle de Publicações":
    st.title("📋 Controle de Publicações")
    st.caption("Acompanhe publicações por cliente, relatório, período e ano.")

    periodicidades = PERIODICIDADES_PUBLICACAO
    perfil_atual = st.session_state.get("perfil_usuario", "")
    nome_usuario_atual = st.session_state.get("nome_usuario", "")

    aba_lancamento, aba_resumo = st.tabs(["📝 Lançar publicação", "📊 Visão anual"])

    with aba_lancamento:
        c1, c2, c3 = st.columns([3, 2, 1.5])
        with c1:
            tipo_relatorio = st.selectbox("📄 Relatório", list(periodicidades), key="pub_tipo")
        with c2:
            periodo = st.selectbox("📅 Período", periodicidades[tipo_relatorio], key="pub_periodo")
        with c3:
            ano = st.number_input("Ano", min_value=2020, max_value=2100, value=date.today().year, step=1, key="pub_ano")

        c4, c5 = st.columns([3, 2])
        with c4:
            busca = st.text_input("🔎 Localizar cliente", key="pub_busca")
        with c5:
            filtro_resp = st.selectbox("👤 Responsável", ["Todos"] + RESPONSAVEIS, key="pub_resp")

        with SessionLocal() as db:
            clientes_pub = db.query(Cliente).order_by(Cliente.nome.asc()).all()
            registros = db.query(ControlePublicacao).filter(
                ControlePublicacao.tipo_relatorio == tipo_relatorio,
                ControlePublicacao.periodo == periodo,
                ControlePublicacao.ano == int(ano),
            ).all()

        if perfil_atual == "Publicador":
            clientes_pub = [c for c in clientes_pub if c.responsavel == nome_usuario_atual]
        if filtro_resp != "Todos":
            clientes_pub = [c for c in clientes_pub if c.responsavel == filtro_resp]
        if busca.strip():
            termo = busca.strip().lower()
            clientes_pub = [c for c in clientes_pub if termo in c.nome.lower()]

        registros_map = {r.cliente_id: r for r in registros}
        publicados = sum(1 for c in clientes_pub if registros_map.get(c.id) and registros_map[c.id].publicado)
        total = len(clientes_pub)
        pendentes = total - publicados
        percentual = publicados / total * 100 if total else 0

        a, b, c, d = st.columns(4)
        a.metric("👥 Clientes", total)
        b.metric("✅ Publicados", publicados)
        c.metric("⏳ Pendentes", pendentes)
        d.metric("📊 Conclusão", f"{percentual:.0f}%")
        st.progress(int(percentual), text=f"{percentual:.0f}% concluído")

        st.markdown(f"### {tipo_relatorio} — {periodo} — {int(ano)}")

        chave_base = f"pub_{tipo_relatorio}_{periodo}_{int(ano)}_"
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Marcar todos", use_container_width=True, key="pub_marcar_todos"):
                for cliente in clientes_pub:
                    st.session_state[chave_base + str(cliente.id)] = True
                st.rerun()
        with col_b:
            if st.button("⬜ Desmarcar todos", use_container_width=True, key="pub_desmarcar_todos"):
                for cliente in clientes_pub:
                    st.session_state[chave_base + str(cliente.id)] = False
                st.rerun()

        if not clientes_pub:
            st.info("Nenhum cliente encontrado com os filtros selecionados.")
        else:
            headers = st.columns([0.5, 4, 2, 1, 1.6])
            for col, title in zip(headers, ["Nº", "CLIENTE", "RESPONSÁVEL", "OK", "DATA"]):
                with col:
                    st.markdown(f"**{title}**")
            st.divider()

            for numero, cliente in enumerate(clientes_pub, 1):
                registro = registros_map.get(cliente.id)
                key_check = chave_base + str(cliente.id)
                key_date = "data_" + key_check
                if key_check not in st.session_state:
                    st.session_state[key_check] = bool(registro and registro.publicado)
                if key_date not in st.session_state:
                    st.session_state[key_date] = registro.data_publicacao if registro and registro.data_publicacao else date.today()

                cols = st.columns([0.5, 4, 2, 1, 1.6])
                with cols[0]:
                    st.write(numero)
                with cols[1]:
                    st.write(f"**{cliente.nome}**")
                with cols[2]:
                    st.write(cliente.responsavel)
                with cols[3]:
                    st.checkbox("OK", key=key_check, label_visibility="collapsed")
                with cols[4]:
                    if st.session_state[key_check]:
                        st.date_input("Data", key=key_date, label_visibility="collapsed")
                    else:
                        st.write("—")

            observacao = st.text_area(
                "📝 Observação geral",
                key=f"pub_obs_{tipo_relatorio}_{periodo}_{int(ano)}",
                height=90,
            )

            if st.button("💾 Salvar marcações", type="primary", use_container_width=True, key="pub_salvar"):
                with SessionLocal() as db:
                    for cliente in clientes_pub:
                        key_check = chave_base + str(cliente.id)
                        key_date = "data_" + key_check
                        publicado = bool(st.session_state.get(key_check, False))
                        registro = db.query(ControlePublicacao).filter(
                            ControlePublicacao.cliente_id == cliente.id,
                            ControlePublicacao.tipo_relatorio == tipo_relatorio,
                            ControlePublicacao.periodo == periodo,
                            ControlePublicacao.ano == int(ano),
                        ).first()
                        if registro is None:
                            registro = ControlePublicacao(
                                cliente_id=cliente.id,
                                tipo_relatorio=tipo_relatorio,
                                periodo=periodo,
                                ano=int(ano),
                            )
                            db.add(registro)
                        registro.publicado = publicado
                        registro.data_publicacao = st.session_state.get(key_date) if publicado else None
                        registro.observacao = observacao.strip() or None
                    db.commit()
                st.success("Controle de publicações atualizado com sucesso.")
                st.rerun()

    with aba_resumo:
        st.subheader("📊 Visão anual")
        ano_resumo = st.number_input("Ano", min_value=2020, max_value=2100, value=date.today().year, step=1, key="pub_resumo_ano")
        resp_resumo = st.selectbox("👤 Responsável", ["Todos"] + RESPONSAVEIS, key="pub_resumo_resp")
        busca_resumo = st.text_input("🔎 Localizar cliente", key="pub_resumo_busca")

        with SessionLocal() as db:
            clientes_resumo = db.query(Cliente).order_by(Cliente.nome.asc()).all()
            registros_ano = db.query(ControlePublicacao).filter(ControlePublicacao.ano == int(ano_resumo)).all()

        if perfil_atual == "Publicador":
            clientes_resumo = [c for c in clientes_resumo if c.responsavel == nome_usuario_atual]
        if resp_resumo != "Todos":
            clientes_resumo = [c for c in clientes_resumo if c.responsavel == resp_resumo]
        if busca_resumo.strip():
            termo = busca_resumo.strip().lower()
            clientes_resumo = [c for c in clientes_resumo if termo in c.nome.lower()]

        ids = {c.id for c in clientes_resumo}
        mapa = {(r.cliente_id, r.tipo_relatorio, r.periodo): r for r in registros_ano}
        previsto = len(clientes_resumo) * sum(len(v) for v in periodicidades.values())
        realizado = sum(
            1 for r in registros_ano
            if r.cliente_id in ids and r.publicado
            and r.tipo_relatorio in periodicidades
            and r.periodo in periodicidades[r.tipo_relatorio]
        )
        pct = realizado / previsto * 100 if previsto else 0

        a, b, c = st.columns(3)
        a.metric("📌 Previstas", previsto)
        b.metric("✅ Realizadas", realizado)
        c.metric("📊 Conclusão", f"{pct:.0f}%")
        st.progress(int(pct), text=f"{pct:.0f}% do controle anual concluído")
        st.divider()

        if not clientes_resumo:
            st.info("Nenhum cliente encontrado.")
        else:
            headers = st.columns([3.8, 1.4, 1.4, 1.4, 1.4, 1.4])
            for col, title in zip(headers, ["CLIENTE", "RREO", "RGF", "RCI", "RGA", "BALANÇO"]):
                with col:
                    st.markdown(f"**{title}**")
            st.divider()
            tipos = list(periodicidades.keys())
            for cliente in clientes_resumo:
                cols = st.columns([3.8, 1.4, 1.4, 1.4, 1.4, 1.4])
                with cols[0]:
                    st.write(f"**{cliente.nome}**")
                for idx, tipo in enumerate(tipos, 1):
                    total_tipo = len(periodicidades[tipo])
                    feitos = sum(
                        1 for periodo_tipo in periodicidades[tipo]
                        if (r := mapa.get((cliente.id, tipo, periodo_tipo))) and r.publicado
                    )
                    icone = "🟢" if feitos == total_tipo else ("🟡" if feitos else "⚪")
                    with cols[idx]:
                        st.write(f"{icone} {feitos}/{total_tipo}")

        st.divider()
        st.subheader("📄 Resumo por relatório")
        for tipo, periodos in periodicidades.items():
            total_tipo = len(clientes_resumo) * len(periodos)
            ids_clientes = {c.id for c in clientes_resumo}
            feitos_tipo = sum(
                1 for r in registros_ano
                if r.cliente_id in ids_clientes
                and r.publicado
                and r.tipo_relatorio == tipo
                and r.periodo in periodos
            )
            pct_tipo = feitos_tipo / total_tipo * 100 if total_tipo else 0
            with st.container(border=True):
                x, y, z = st.columns([5, 1.5, 1.5])
                x.markdown(f"**{tipo}**")
                x.caption(f"{len(periodos)} período(s) por cliente")
                y.metric("Realizadas", f"{feitos_tipo}/{total_tipo}")
                z.metric("Conclusão", f"{pct_tipo:.0f}%")

elif pagina == "Almoxarifados":

    st.title("📦 Almoxarifados")
    st.caption("Controle mensal dos almoxarifados dos clientes")

    MESES_ALMOXARIFADO = [
        ("jan", "JAN"), ("fev", "FEV"), ("mar", "MAR"),
        ("abr", "ABR"), ("mai", "MAI"), ("jun", "JUN"),
        ("jul", "JUL"), ("ago", "AGO"), ("set", "SET"),
        ("out", "OUT"), ("nov", "NOV"), ("dez", "DEZ"),
    ]

    RESPONSAVEIS_ALMOXARIFADO = [
        "Ítalo",
        "Jadsson News",
        "Vitor",
        "Produção Própria",
    ]

    st.markdown(
        """
        <style>
        .almox-header {
            background:#d9e2f3;
            border:1px solid #8c8c8c;
            padding:6px 2px;
            text-align:center;
            font-weight:700;
            font-size:11px;
        }
        .almox-cell {
            border:1px solid #b7b7b7;
            padding:7px 4px;
            min-height:32px;
            font-size:10px;
        }
        .almox-email {
            color:#2563eb !important;
            word-break:break-word;
        }
        .almox-ok {
            text-align:center;
            font-weight:700;
            color:#166534 !important;
            background:#dcfce7;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col_busca, col_resp, col_novo = st.columns([3, 2, 2])

    with col_busca:
        filtro_almox = st.text_input(
            "🔎 Buscar cliente",
            placeholder="Digite o nome do cliente",
            key="filtro_almox",
        )

    with col_resp:
        filtro_resp_almox = st.selectbox(
            "Responsável",
            ["Todos"] + RESPONSAVEIS_ALMOXARIFADO,
            key="filtro_resp_almox",
        )

    with col_novo:
        st.write("")
        criar_almox = st.button(
            "➕ Novo almoxarifado",
            use_container_width=True,
            type="primary",
        )

    if criar_almox:
        st.session_state["novo_almox"] = True

    if st.session_state.get("novo_almox", False):

        st.divider()
        st.subheader("➕ Novo almoxarifado")

        with st.form("form_novo_almox"):
            c1, c2 = st.columns(2)

            with c1:
                numero = st.number_input(
                    "Nº",
                    min_value=1,
                    step=1,
                    value=1,
                )
                cliente = st.text_input("Cliente*")
                email_orgao = st.text_input("E-mail do órgão")

            with c2:
                email_contabilidade = st.text_input(
                    "E-mail contabilidade"
                )
                responsavel = st.selectbox(
                    "Responsável",
                    RESPONSAVEIS_ALMOXARIFADO,
                )

            salvar = st.form_submit_button(
                "💾 Salvar almoxarifado",
                type="primary",
                use_container_width=True,
            )

        if salvar:
            if not cliente.strip():
                st.error("Informe o nome do cliente.")
            else:
                with SessionLocal() as db:
                    ultimo = (
                        db.query(Almoxarifado)
                        .order_by(Almoxarifado.numero.desc())
                        .first()
                    )
                    numero_final = (
                        ultimo.numero + 1
                        if ultimo
                        else numero
                    )

                    db.add(
                        Almoxarifado(
                            numero=numero_final,
                            cliente=cliente.strip(),
                            email_orgao=email_orgao.strip(),
                            email_contabilidade=email_contabilidade.strip(),
                            responsavel=responsavel,
                        )
                    )
                    db.commit()

                st.session_state["novo_almox"] = False
                st.success("Almoxarifado cadastrado.")
                st.rerun()

    with SessionLocal() as db:
        almoxarifados = (
            db.query(Almoxarifado)
            .order_by(Almoxarifado.numero.asc())
            .all()
        )

    filtrados = []
    for item in almoxarifados:
        if filtro_almox and filtro_almox.lower() not in item.cliente.lower():
            continue
        if filtro_resp_almox != "Todos" and item.responsavel != filtro_resp_almox:
            continue
        filtrados.append(item)

    st.divider()
    st.subheader("📋 Controle mensal")

    if not filtrados:
        st.info("Nenhum almoxarifado encontrado.")
    else:
        larguras = [
            0.4, 2.2, 2.5, 2.5,
            0.55, 0.55, 0.55, 0.55, 0.55, 0.55,
            0.55, 0.55, 0.55, 0.55, 0.55, 0.55,
        ]

        cabecalhos = [
            "Nº", "CLIENTE", "EMAIL DO ÓRGÃO",
            "EMAIL CONTABILIDADE",
            "JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
            "JUL", "AGO", "SET", "OUT", "NOV", "DEZ",
        ]

        cab = st.columns(larguras)
        for col, titulo in zip(cab, cabecalhos):
            with col:
                st.markdown(
                    f'<div class="almox-header">{titulo}</div>',
                    unsafe_allow_html=True,
                )

        for item in filtrados:

            if item.responsavel == "Ítalo":
                cor = "#f4b183"
                texto = "#000000"
            elif item.responsavel == "Jadsson News":
                cor = "#5b9bd5"
                texto = "#000000"
            elif item.responsavel == "Vitor":
                cor = "#8b174f"
                texto = "#ffffff"
            else:
                cor = "#a9d18e"
                texto = "#000000"

            cols = st.columns(larguras)

            with cols[0]:
                st.markdown(
                    f'<div class="almox-cell" style="text-align:center">{item.numero}</div>',
                    unsafe_allow_html=True,
                )

            with cols[1]:
                st.markdown(
                    f'<div class="almox-cell" style="background:{cor};color:{texto};font-weight:700">{item.cliente}</div>',
                    unsafe_allow_html=True,
                )

            with cols[2]:
                st.markdown(
                    f'<div class="almox-cell almox-email">{item.email_orgao or ""}</div>',
                    unsafe_allow_html=True,
                )

            with cols[3]:
                st.markdown(
                    f'<div class="almox-cell almox-email">{item.email_contabilidade or ""}</div>',
                    unsafe_allow_html=True,
                )

            for pos, (campo, mes) in enumerate(MESES_ALMOXARIFADO, start=4):

                valor = getattr(item, campo) or ""

                with cols[pos]:
                    if st.button(
                        "OK" if valor == "Ok" else "·",
                        key=f"almox_{item.id}_{campo}",
                        use_container_width=True,
                    ):
                        with SessionLocal() as db:
                            registro = (
                                db.query(Almoxarifado)
                                .filter(Almoxarifado.id == item.id)
                                .first()
                            )
                            if registro:
                                setattr(
                                    registro,
                                    campo,
                                    "" if getattr(registro, campo) == "Ok" else "Ok",
                                )
                                db.commit()
                        st.rerun()

            with st.expander(f"⚙️ Editar {item.cliente}"):

                with st.form(f"editar_almox_{item.id}"):

                    e1, e2 = st.columns(2)

                    with e1:
                        novo_numero = st.number_input(
                            "Nº",
                            min_value=1,
                            value=item.numero,
                            step=1,
                            key=f"numero_{item.id}",
                        )
                        novo_cliente = st.text_input(
                            "Cliente",
                            value=item.cliente,
                            key=f"cliente_{item.id}",
                        )
                        novo_email_orgao = st.text_input(
                            "E-mail do órgão",
                            value=item.email_orgao or "",
                            key=f"orgao_{item.id}",
                        )

                    with e2:
                        novo_email_cont = st.text_input(
                            "E-mail contabilidade",
                            value=item.email_contabilidade or "",
                            key=f"cont_{item.id}",
                        )

                        indice_resp = (
                            RESPONSAVEIS_ALMOXARIFADO.index(item.responsavel)
                            if item.responsavel in RESPONSAVEIS_ALMOXARIFADO
                            else 0
                        )

                        novo_resp = st.selectbox(
                            "Responsável",
                            RESPONSAVEIS_ALMOXARIFADO,
                            index=indice_resp,
                            key=f"resp_{item.id}",
                        )

                    salvar_edicao = st.form_submit_button(
                        "💾 Salvar alterações",
                        type="primary",
                        use_container_width=True,
                    )

                if salvar_edicao:
                    with SessionLocal() as db:
                        registro = (
                            db.query(Almoxarifado)
                            .filter(Almoxarifado.id == item.id)
                            .first()
                        )
                        if registro:
                            registro.numero = novo_numero
                            registro.cliente = novo_cliente.strip()
                            registro.email_orgao = novo_email_orgao.strip()
                            registro.email_contabilidade = novo_email_cont.strip()
                            registro.responsavel = novo_resp
                            db.commit()

                    st.success("Alterações salvas.")
                    st.rerun()

                if st.button(
                    "🗑️ Excluir",
                    key=f"delete_almox_{item.id}",
                ):
                    excluir(Almoxarifado, item.id)
                    st.rerun()

    st.divider()
    st.markdown("### 🎨 Legenda")

    l1, l2, l3, l4 = st.columns(4)

    with l1:
        st.markdown("🟧 **ÍTALO**")
    with l2:
        st.markdown("🟦 **JADSSON NEWS**")
    with l3:
        st.markdown("🟪 **VITOR**")
    with l4:
        st.markdown("🟩 **PRODUÇÃO PRÓPRIA**")

elif pagina == "Configurações":

    st.title("⚙️ Configurações")

    st.subheader("📊 Modelo de avaliação")

    st.write(
        "Importe a planilha modelo para cadastrar os critérios "
        "utilizados nos relatórios mensais."
    )

    arquivo_avaliacao = st.file_uploader(
        "Selecione a planilha de avaliação",
        type=["xlsx"],
        key="arquivo_avaliacao"
    )

    if arquivo_avaliacao is not None:

        st.success(
            f"Arquivo selecionado: {arquivo_avaliacao.name}"
        )

        if st.button(
            "📥 Importar critérios da planilha",
            use_container_width=True
        ):

            try:

                importados, ignorados = (
                    importar_itens_avaliacao_excel(
                        arquivo_avaliacao
                    )
                )

                st.success(
                    f"{importados} critério(s) importado(s) com sucesso!"
                )

                if ignorados > 0:

                    st.info(
                        f"{ignorados} critério(s) já existia(m) "
                        "e não foi(ram) duplicado(s)."
                    )

            except Exception as erro:

                st.error(
                    f"Erro ao importar a planilha: {erro}"
                )

    st.divider()

    st.subheader("🔔 Preferências")

    st.checkbox(
        "Ativar notificações internas"
    )

    st.checkbox(
        "Mostrar alertas de demandas atrasadas"
    )

    st.divider()

    st.write("**Sistema:** Facilita Manager")
    st.write("**Tecnologia:** Python + Streamlit + SQLAlchemy + SQLite")
    st.write("**Versão:** 0.3.0")
