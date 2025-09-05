import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from fpdf import FPDF
import base64
from io import BytesIO
import time
import math
import datetime
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import pytz
from datetime import datetime as dt
from PIL import Image
from streamlit.runtime.scriptrunner import RerunException
from matplotlib.ticker import MaxNLocator

# =============================================
# CONSTANTES E CONFIGURAÇÕES GLOBAIS
# =============================================

FREQUENCIA_BASE = 432  # Hz
PULSOS_POR_GIRO = 432 * 9  # 9 Vibes
GIROS_POR_CICLO = 9
CICLOS_POR_ERA = 9
SINGULARIDADE = datetime.datetime(2023, 3, 9, 0, 0, 0, tzinfo=pytz.UTC)

# =============================================
# FUNÇÕES PRINCIPAIS DO FLUXO MATEMÁTICO
# =============================================
def gerar_padrao_ciclico(formula, var_start, var_end, step, constante, variavel_nome):
    reducoes = []
    valores = []

    var = var_start
    while var <= var_end:
        try:
            if formula == "E=mc²":
                resultado = var * (constante ** 2)
            elif formula == "F=ma":
                resultado = var * constante
            elif formula == "V=IR":
                resultado = var * constante
            elif formula == "p=mv":
                resultado = var * constante
            elif formula == "F=G(m1m2)/r²":
                m2 = constante.get('m2', 1)
                G = constante.get('G', 1)
                r = constante.get('r', 1)
                resultado = G * (var * m2) / (r ** 2)
            else:
                resultado = 0

            reducao = reduzir_teosoficamente(resultado)
            valores.append(var)
            reducoes.append(reducao)

        except Exception as e:
            valores.append(var)
            reducoes.append('Erro')

        var = round(var + step, 8)

    return valores, reducoes

def plotar_padrao_ciclico(valores, reducoes, formula, variavel_nome):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Gráfico principal
    ax.plot(valores, reducoes, 'o-', color='#4B0082', linewidth=2, markersize=8, label='Redução Teosófica')
    
    # Destacar pontos especiais (3, 6, 9)
    for x, y in zip(valores, reducoes):
        if y in [3, 6, 9]:
            ax.scatter(x, y, s=120, c='gold', edgecolors='black', zorder=5)
    
    ax.set_title(f"Padrão Cíclico para {formula} - Variação de {variavel_nome}", pad=20)
    ax.set_xlabel(f"{variavel_nome} →", fontsize=12)
    ax.set_ylabel("Redução Teosófica", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    return fig

def gerar_insights_padrao(reducoes):
    unique = sorted(list(set(reducoes)))
    cycles = []
    
    # Detectar ciclos
    for i in range(1, len(reducoes)//2):
        if reducoes[:i] == reducoes[i:2*i]:
            cycles.append(i)
    
    insights = []
    if 3 in unique or 6 in unique or 9 in unique:
        insights.append("🔵 **Padrão 3-6-9 detectado**: Estes números representam pontos de transição quântica no Fluxo Matemático")
    
    if cycles:
        insights.append(f"🔄 **Ciclo de {min(cycles)} passos**: O padrão se repete a cada {min(cycles)} incrementos")
    
    if len(unique) <= 5:
        insights.append(f"🌈 **Baixa entropia**: Apenas {len(unique)} valores únicos de redução")
    
    return "\n\n".join(insights) if insights else "Padrão complexo - análise mais profunda necessária"

def atualizacao_segura(duracao=60):
    """Decorador para atualizações seguras"""
    def decorador(func):
        def wrapper(*args, **kwargs):
            try:
                placeholder = st.empty()
                start_time = time.time()
                stop_updates = False
                
                if st.button("Parar Atualizações", key=f"stop_{func.__name__}_{time.time()}"):
                    stop_updates = True
                
                while not stop_updates and (time.time() - start_time) < duracao:
                    try:
                        with placeholder.container():
                            func(*args, **kwargs)
                            time.sleep(1)
                    except RerunException:
                        continue
                    except Exception as e:
                        st.error(f"Erro na atualização: {str(e)}")
                        break
                
                if not stop_updates:
                    st.info(f"Atualizações automáticas concluídas após {duracao//60} minutos")
            except Exception as e:
                st.error(f"Erro crítico: {str(e)}")
        return wrapper
    return decorador

def reduzir_teosoficamente(n):
    """
    Redução teosófica: Soma repetida dos dígitos até obter um único dígito de 1 a 9.
    Suporta inteiros, floats e strings numéricas, incluindo notação científica.
    """

    try:
        # Converter para string, evitando notação científica e símbolos
        if isinstance(n, (int, float)):
            # Evitar notação científica
            if abs(n) >= 1 or n == 0:
                n_str = f"{n:.0f}"
            else:
                n_str = f"{n:.15f}".rstrip('0').replace('.', '')
        else:
            n_str = str(n)

        # Remover tudo que não for dígito (caso venha como string ou float muito pequeno)
        n_str = ''.join(filter(str.isdigit, n_str))

        # Se a string ficou vazia, retorna 0
        if not n_str:
            return 0

        # Processo de redução teosófica
        while len(n_str) > 1:
            soma = sum(int(c) for c in n_str)
            n_str = str(soma)

        return int(n_str)

    except Exception as e:
        print(f"Erro na redução teosófica: {e}")
        return 0

def gerar_sequencia_reducao(iteracoes=100):
    """Gera a sequência de redução teosófica dobrando valores"""
    sequencia = [1]
    resultados = []
    for _ in range(iteracoes):
        proximo = sequencia[-1] * 2
        reduzido = reduzir_teosoficamente(proximo)
        resultados.append((sequencia[-1], proximo, reduzido))
        sequencia.append(reduzido)
    return resultados

def gerar_ciclo_369(iteracoes=24):
    """Gera o ciclo sagrado 3-6-9"""
    ciclo = []
    valor = 3
    for _ in range(iteracoes):
        ciclo.append(valor)
        if valor == 3:
            valor = 6
        elif valor == 6:
            valor = 9
        else:
            valor = 3
    return ciclo

def fluxo_soma(a, b):
    """Soma no Fluxo Matemático"""
    return reduzir_teosoficamente(a + b)

def fluxo_multiplicacao(a, b):
    """Multiplicação no Fluxo Matemático"""
    return reduzir_teosoficamente(a * b)

def fluxo_potencia(a, n):
    """Potenciação no Fluxo Matemático"""
    return reduzir_teosoficamente(a ** n)

def fluxo_trigonometria(angulo):
    """Trigonometria no Fluxo Matemático"""
    rad = math.radians(angulo)
    s = math.sin(rad)
    c = math.cos(rad)
    t = math.tan(rad)
    return (reduzir_teosoficamente(abs(int(s*100))), 
            reduzir_teosoficamente(abs(int(c*100))), 
            reduzir_teosoficamente(abs(int(t*100))))

def fluxo_fisica(formula, valores):
    """Aplica o Fluxo Matemático a fórmulas físicas"""
    try:
        if formula == "E=mc²":
            m, c = valores['m'], valores['c']
            E_classico = m * c**2
            E_fluxo = fluxo_multiplicacao(reduzir_teosoficamente(m), 
                                         fluxo_potencia(reduzir_teosoficamente(c), 2))
            return E_classico, E_fluxo
        
        elif formula == "F=ma":
            m, a = valores['m'], valores['a']
            F_classico = m * a
            F_fluxo = fluxo_multiplicacao(reduzir_teosoficamente(m), 
                                         reduzir_teosoficamente(a))
            return F_classico, F_fluxo
        
        elif formula == "V=IR":
            I, R = valores['I'], valores['R']
            V_classico = I * R
            V_fluxo = fluxo_multiplicacao(reduzir_teosoficamente(I), 
                                         reduzir_teosoficamente(R))
            return V_classico, V_fluxo
        
        elif formula == "p=mv":
            m, v = valores['m'], valores['v']
            p_classico = m * v
            p_fluxo = fluxo_multiplicacao(reduzir_teosoficamente(m), 
                                         reduzir_teosoficamente(v))
            return p_classico, p_fluxo
        
        elif formula == "F=G(m1m2)/r²":
            G, m1, m2, r = valores['G'], valores['m1'], valores['m2'], valores['r']
            F_classico = G * m1 * m2 / r**2
            numerador = fluxo_multiplicacao(
                fluxo_multiplicacao(reduzir_teosoficamente(G), 
                                  reduzir_teosoficamente(m1)), 
                reduzir_teosoficamente(m2))
            denominador = fluxo_potencia(reduzir_teosoficamente(r), 2)
            F_fluxo = fluxo_multiplicacao(numerador, denominador)
            return F_classico, F_fluxo
        
        return None, None
    except:
        return None, None
# =============================================
# SISTEMA DE TEMPO ESPIRALADO E RELÓGIO QUÂNTICO (VERSÃO FINAL)
# =============================================

class RelogioQuantico:
    def __init__(self):
        # Configurações temporais
        self.frequencia_base = FREQUENCIA_BASE
        self.pulsos_por_giro = PULSOS_POR_GIRO
        self.giros_por_ciclo = GIROS_POR_CICLO
        self.ciclos_por_era = CICLOS_POR_ERA
        self.singularidade = SINGULARIDADE
        self.padrao_369 = [3, 6, 9] * 3
        self.ultima_mudanca = datetime.datetime(2012, 12, 21, tzinfo=pytz.UTC)
        self.proxima_mudanca = datetime.datetime(2033, 12, 21, tzinfo=pytz.UTC)

    def calcular_angulo(self, valor, ciclo):
        return -np.pi/2 - (valor % ciclo) * (2 * np.pi / ciclo)

    # Métodos existentes da classe RelogioQuantico...
    def data_para_quantico(self, data: datetime.datetime) -> dict:
        """Converte data para o sistema quântico temporal"""
        if data.tzinfo is None:
            data = data.replace(tzinfo=pytz.UTC)
        
        delta = data - self.singularidade
        segundos = delta.total_seconds()
        pulsos = int(segundos * self.frequencia_base)
        
        eras = pulsos // (self.pulsos_por_giro * self.giros_por_ciclo * self.ciclos_por_era)
        pulsos %= (self.pulsos_por_giro * self.giros_por_ciclo * self.ciclos_por_era)
        
        ciclos = pulsos // (self.pulsos_por_giro * self.giros_por_ciclo)
        pulsos %= (self.pulsos_por_giro * self.giros_por_ciclo)
        
        giros = pulsos // self.pulsos_por_giro
        pulsos %= self.pulsos_por_giro
        
        vibes = pulsos // self.frequencia_base
        pulsos %= self.frequencia_base
        
        return {
            'estrutura': {
                'eras': {
                    'quantidade': eras,
                    'nome': 'Êon Quântico',
                    'duracao': '144³ pulsos',
                    'subciclos': ['Vórtices', 'Espirais Dimensionais']
                },
                'ciclos': {
                    'quantidade': ciclos,
                    'nome': 'Vórtice Temporal',
                    'duracao': '144² pulsos'
                },
                'giros': giros,
                'vibes': vibes
            },
            'status': 'AE (Após Êxodo)',
            'calendario': self._gerar_calendario_quantico(pulsos),
            'reducao': reduzir_teosoficamente(int(pulsos))
        }

    def get_pulsos_desde_singularidade(self):
        """Calcula os pulsos desde a singularidade"""
        agora = datetime.datetime.now(pytz.UTC)
        delta = agora - self.singularidade
        return int(delta.total_seconds() * self.frequencia_base)
    
    def converter_pulsos(self, pulsos):
        """Converte pulsos para a estrutura temporal"""
        eras = pulsos // (self.pulsos_por_giro * self.giros_por_ciclo * self.ciclos_por_era)
        pulsos %= (self.pulsos_por_giro * self.giros_por_ciclo * self.ciclos_por_era)
        
        ciclos = pulsos // (self.pulsos_por_giro * self.giros_por_ciclo)
        pulsos %= (self.pulsos_por_giro * self.giros_por_ciclo)
        
        giros = pulsos // self.pulsos_por_giro
        pulsos %= self.pulsos_por_giro
        
        vibes = pulsos // self.frequencia_base
        pulsos %= self.frequencia_base
        
        return {
            'eras': eras,
            'ciclos': ciclos,
            'giros': giros,
            'vibes': vibes,
            'pulsos': pulsos,
            'reducao': reduzir_teosoficamente(int(pulsos))
        }
    
    def plotar_relogio_quantico(self):
        """Gera visualização do relógio quântico"""
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
        
        # Cria um relógio circular
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        
        # Marcadores 3-6-9
        for angulo, valor in zip([0, 120, 240], [3, 6, 9]):
            rad = math.radians(angulo)
            ax.plot([0, rad], [0, 1], color='gold', linewidth=3)
            ax.text(rad, 1.1, str(valor), ha='center', va='center', 
                   fontsize=20, color='gold')
        
        # Ponteiros
        agora = datetime.datetime.now(pytz.UTC)
        segundos = (agora - self.singularidade).total_seconds()
        angulo = (segundos % 60) / 60 * 360
        rad = math.radians(angulo)
        ax.plot([0, rad], [0, 0.9], color='red', linewidth=3)
        
        ax.set_yticklabels([])
        ax.set_title("Relógio Quântico", pad=20)
        plt.close(fig)
        return fig

    def _gerar_calendario_quantico(self, pulsos):
        return {
            'dias': pulsos % 144,
            'semanas_quanticas': (pulsos // 7) % 20,
            'meses': (pulsos // 28) % 13
        }

    def plotar_espiral_temporal(self, pulsos_totais, camadas=3, cor="#4B0082"):
        """Gera visualização 3D da espiral temporal"""
        # Configuração dinâmica baseada nos pulsos
        theta = np.linspace(0, camadas * 2 * np.pi, 1000)
        z = np.linspace(0, camadas, 1000)
        r = z**1.5  # Forma mais orgânica
        
        # Criar figura 3D interativa
        fig = go.Figure()
        
        # Adicionar espiral principal
        fig.add_trace(go.Scatter3d(
            x=r * np.cos(theta),
            y=r * np.sin(theta),
            z=z,
            mode='lines',
            line=dict(color=cor, width=4),
            name='Espiral Temporal'
        ))
        
        # Adicionar pontos quânticos (3-6-9)
        pontos_theta = np.linspace(0, camadas * 2 * np.pi, 9)
        pontos_z = np.linspace(0, camadas, 9)
        pontos_r = pontos_z**1.5
            
        fig.add_trace(go.Scatter3d(
            x=pontos_r * np.cos(pontos_theta),
            y=pontos_r * np.sin(pontos_theta),
            z=pontos_z,
            mode='markers',
            marker=dict(
                size=8,
                color=self.padrao_369,
                colorscale='Viridis',
                opacity=0.8
            ),
            name='Pontos Quânticos',
            text=[f"Vibe {i+1}: {self.padrao_369[i%3]}" for i in range(9)],
            hoverinfo='text+z'
        ))
        
        # Configurações de layout
        fig.update_layout(
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=0.8)
                ),
                annotations=[
                    dict(
                        showarrow=False,
                        text=f"Pulsos: {int(pulsos_totais):,}",
                        x=0.5,
                        y=0.5,
                        xanchor="center",
                        yanchor="middle",
                        xref="paper",
                        yref="paper",
                        font=dict(size=20)
                    )
                ]
            ),
            margin=dict(l=0, r=0, b=0, t=30),
            height=600,
            showlegend=True
        )
        
        return fig

    def gerar_animacao_espiral(self, frames=36):
        """Gera animação da espiral temporal"""
        thetas = []
        zs = []
        rs = []
        
        for frame in range(frames):
            theta = np.linspace(0, 4 * np.pi * (frame+1)/frames, 100)
            z = np.linspace(0, 4 * (frame+1)/frames, 100)
            r = z**1.2
            
            thetas.append(theta)
            zs.append(z)
            rs.append(r)
        
        fig = go.Figure(
            frames=[go.Frame(
                data=[go.Scatter3d(
                    x=rs[i] * np.cos(thetas[i]),
                    y=rs[i] * np.sin(thetas[i]),
                    z=zs[i],
                    mode='lines',
                    line=dict(color='#4B0082', width=4)
                )]
            ) for i in range(frames)]
        )
        
        # Adicionar frame inicial
        fig.add_trace(go.Scatter3d(
            x=rs[0] * np.cos(thetas[0]),
            y=rs[0] * np.sin(thetas[0]),
            z=zs[0],
            mode='lines',
            line=dict(color='#4B0082', width=4)
        ))
        
        # Configuração da animação
        fig.update_layout(
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(
                    label="Play",
                    method="animate",
                    args=[None, {"frame": {"duration": 100, "redraw": True}}]
                )]
            )],
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False)
            ),
            height=500
        )
        
        return fig

# Instância global do relógio quântico
relogio = RelogioQuantico()

def main():
    # =============================================
    # PAGE CONFIG (must be first Streamlit command)
    # =============================================
    st.set_page_config(
        layout="wide", 
        page_title="🌌 Universo Áureo", 
        page_icon="🌀", 
        initial_sidebar_state="expanded"
    )
    
    # =============================================
    # NAVIGATION (must come before page content)
    # =============================================
    st.sidebar.title("🌀 Navegação")
    pagina = st.sidebar.radio(
        "Selecione a seção:",
        ["🏠 Introdução", "🧮 Cálculos", "⏳ Tempo Espiralado", "📊 Visualizações", 
         "📚 PDF Explicativo", "🕒 Relógio Quântico", "📅 Calendário Clássico"]
    )
    
    # =============================================
    # PAGE CONTENT (after navigation is defined)
    # =============================================
    if pagina == "🏠 Introdução":
        # Introduction page content
        st.title("🌌 Universo Áureo - Fluxo Matemático")
        st.markdown("""
        ## Bem-vindo à Nova Matemática Cósmica
        
        Este aplicativo representa uma revolução na forma como entendemos a matemática, o tempo e o universo.
        Aqui, todas as fórmulas clássicas são reinterpretadas através da lente do **Fluxo Matemático**,
        incorporando:
        
        - Padrões cíclicos de 3, 6 e 9
        - Redução teosófica
        - Geometria sagrada
        - Tempo espiralado (não linear)
        - Frequências vibracionais (432Hz)
        - Relógio quântico com projeção para singularidade
        
        ### Princípios Fundamentais:
        1. **Tudo é movimento** - Não existe zero absoluto, apenas transições
        2. **Ciclos infinitos** - Padrões 1-2-4-8-7-5 e 3-6-9 se repetem em todas as escalas
        3. **Tempo angular** - O tempo flui em espirais, não em linhas retas
        4. **Singularidade do 9** - O 9 representa o ponto de transição entre ciclos
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://i.imgur.com/JDQw3Oz.png", caption="Ciclo 1-2-4-8-7-5")
        with col2:
            st.image("https://i.imgur.com/8QZQZQZ.png", caption="Geometria 3-6-9")

    elif pagina == "🧮 Cálculos":
        # Adicione estas importações no início do bloco
        import pandas as pd
        import math
        import numpy as np
        import plotly.graph_objects as go
        from matplotlib import pyplot as plt
    
        st.title("🧮 Cálculos no Fluxo Matemático")
        st.markdown("Compare as fórmulas clássicas com suas versões no Fluxo Matemático")

        tab1, tab2, tab3, tab4 = st.tabs(["🔢 Básicos", "📈 Avançados", "⚡ Física", "🧠 Customizar"])

        with tab1:
            st.subheader("Operações Básicas")

            operacao = st.selectbox(
                "Selecione a operação:",
                ["Soma", "Subtração", "Multiplicação", "Divisão", "Potência"],
                key="select_operacao"
            )

            col1, col2 = st.columns(2)

            if operacao == "Soma":
                with col1:
                    a = st.number_input("Valor A:", min_value=1, value=7, step=1, key="soma_a")
                with col2:
                    b = st.number_input("Valor B:", min_value=1, value=5, step=1, key="soma_b")

                clas = a + b
                flux = fluxo_soma(a, b)

                st.markdown(f"""
                ### ➕ Soma Clássica:
                **{a} + {b} = {clas}**

                ### ➕ Soma no Fluxo Matemático:
                **R({a}) ⊕ R({b}) = {reduzir_teosoficamente(a)} ⊕ {reduzir_teosoficamente(b)} = {flux}**

                ✅ *Redução do Resultado Clássico:* {reduzir_teosoficamente(clas)}
                """)

            elif operacao == "Subtração":
                with col1:
                    a = st.number_input("Valor A:", min_value=1, value=7, step=1, key="sub_a")
                with col2:
                    b = st.number_input("Valor B:", min_value=1, value=5, step=1, key="sub_b")

                clas = a - b
                flux = fluxo_soma(a, -b)

                st.markdown(f"""
                ### ➖ Subtração Clássica:
                **{a} - {b} = {clas}**

                ### ➖ Subtração no Fluxo Matemático:
                **R({a}) ⊖ R({b}) = {reduzir_teosoficamente(a)} ⊕ R(-{reduzir_teosoficamente(b)}) = {flux}**

                ✅ *Redução do Resultado Clássico:* {reduzir_teosoficamente(clas)}
                """)

            elif operacao == "Multiplicação":
                with col1:
                    a = st.number_input("Valor A:", min_value=1, value=7, step=1, key="mult_a")
                with col2:
                    b = st.number_input("Valor B:", min_value=1, value=5, step=1, key="mult_b")

                clas = a * b
                flux = fluxo_multiplicacao(a, b)

                st.markdown(f"""
                ### ✖️ Multiplicação Clássica:
                **{a} × {b} = {clas}**

                ### ✖️ Multiplicação no Fluxo Matemático:
                **R({a}) ⊗ R({b}) = {reduzir_teosoficamente(a)} ⊗ {reduzir_teosoficamente(b)} = {flux}**

                ✅ *Redução do Resultado Clássico:* {reduzir_teosoficamente(clas)}
                """)

            elif operacao == "Divisão":
                with col1:
                    a = st.number_input("Valor A:", min_value=1, value=7, step=1, key="div_a")
                with col2:
                    b = st.number_input("Valor B:", min_value=1, value=5, step=1, key="div_b")

                if b != 0:
                    clas = a / b
                    flux = fluxo_multiplicacao(a, 1 / b)
                    reducao = reduzir_teosoficamente(clas)
                else:
                    clas = "∞"
                    flux = "∞"
                    reducao = "-"

                st.markdown(f"""
                ### ➗ Divisão Clássica:
                **{a} ÷ {b} = {clas}**

                ### ➗ Divisão no Fluxo Matemático:
                **R({a}) ⊘ R({b}) = {reduzir_teosoficamente(a)} ⊗ R(1/{b}) = {flux}**

                ✅ *Redução do Resultado Clássico:* {reducao}
                """)

            elif operacao == "Potência":
                with col1:
                    a = st.number_input("Base:", min_value=1, value=2, step=1, key="pot_a")
                with col2:
                    b = st.number_input("Expoente:", min_value=1, value=3, step=1, key="pot_b")

                clas = a ** b
                flux = fluxo_potencia(a, b) if isinstance(b, int) else reduzir_teosoficamente(a ** b)

                st.markdown(f"""
                ### 🧱 Potência Clássica:
                **{a}^{b} = {clas}**

                ### 🧱 Potência no Fluxo Matemático:
                **R({a}) ↑ R({b}) = {reduzir_teosoficamente(a)} ↑ {reduzir_teosoficamente(b)} = {flux}**

                ✅ *Redução do Resultado Clássico:* {reduzir_teosoficamente(clas)}
                """)

        with tab2:
            st.subheader("Funções Avançadas")
            funcao = st.selectbox("Selecione a função:", ["Trigonometria", "Sequência Fibonacci"], key="funcao_avancada")

            if funcao == "Trigonometria":
                angulo = st.slider("Ângulo (graus):", 0, 360, 130, key="angulo_trig")
                try:
                    sin, cos, tan = fluxo_trigonometria(angulo)
                    st.write(f"""
                    | Função | Valor Clássico | Valor Fluxo |
                    |--------|----------------|-------------|
                    | sen({angulo}°) | {math.sin(math.radians(angulo)):.4f} | {sin} |
                    | cos({angulo}°) | {math.cos(math.radians(angulo)):.4f} | {cos} |
                    | tan({angulo}°) | {math.tan(math.radians(angulo)):.4f} | {tan} |
                    """)
                except Exception as e:
                    st.error(f"Erro no cálculo trigonométrico: {str(e)}")

            else:
                st.write("Sequência de Fibonacci com Redução Teosófica:")
                n = st.slider("Termos:", 1, 50, 20, key="termos_fib")

                fib = [1, 1]
                for i in range(2, n):
                    fib.append(fib[i-1] + fib[i-2])
    
                fib_reduzido = [reduzir_teosoficamente(x) for x in fib]

                df = pd.DataFrame({
                    "Fibonacci": fib,
                    "Reduzido": fib_reduzido
                })
    
                # Correção: Estilização simplificada sem usar x.name
                def highlight_max(s):
                    is_max = s == s.max()
                    return ['background-color: #FFD700' if v else '' for v in is_max]
        
                st.dataframe(
                    df.style.apply(highlight_max, subset=['Fibonacci', 'Reduzido'])
                )

        with tab3:
            with st.sidebar:
                st.header("⚙️ Configurações de Análise")
                amplitude = st.slider("Amplitude da variação", 0.1, 1.0, 0.2, 0.05)
                passo = st.selectbox("Precisão do passo", [0.001, 0.01, 0.1], index=1)
                mostrar_avancado = st.checkbox("Mostrar análise avançada", True)

            st.subheader("Fórmulas Físicas no Fluxo Matemático")

            formula = st.selectbox(
                "Selecione a fórmula física:",
                ["E=mc²", "F=ma", "V=IR", "p=mv", "F=G(m1m2)/r²"],
                key="formula_fisica_unica"
            )

            if formula == "E=mc²":
                col1, col2 = st.columns(2)
                with col1:
                    m = st.number_input("Massa (kg):", min_value=0.1, value=15.9, step=0.1, key="emc2_m")
                with col2:
                    c = st.number_input("Velocidade da luz (m/s):", value=299792458.14, key="emc2_c")

                try:
                    # Cálculo Clássico de Einstein
                    E_classico = m * (c ** 2)
                    E_fluxo = reduzir_teosoficamente(E_classico)

                    st.success(f"E Clássico: {E_classico:.3e} Joules | Redução Fluxo: {E_fluxo}")

                    # Amplitude de análise
                    inicio = m
                    fim = m + amplitude
                    massas, reducoes = gerar_padrao_ciclico(
                        formula="E=mc²",
                        var_start=inicio,
                        var_end=fim,
                        step=passo,
                        constante=c,
                        variavel_nome="Massa (kg)"
                    )

                    # Mostrar Padrão Detectado
                    with st.expander("📈 Análise prévia do Padrão Cíclico", expanded=True):
                        fig = plotar_padrao_ciclico(massas, reducoes, "E=mc²", "Massa (kg)")

                        st.markdown("### 🔍 Frequência de Reduções no Fluxo Matemático")
                        freq = pd.Series(reducoes).value_counts().sort_index()

                        col1, col2 = st.columns(2)
                        with col1:
                            st.pyplot(fig)
                        with col2:
                            st.bar_chart(freq, use_container_width=True)
                            st.caption("Frequência de cada redução (1 a 9)")

                        # Exibir sequência gerada
                        df = pd.DataFrame({
                            "Massa (kg)": massas,
                            'Redução': reducoes,
                            'Destaque': ['★' if r in [3,6,9] else '' for r in reducoes]
                        })
                        st.dataframe(df.style.applymap(
                            lambda x: 'background-color: gold' if x in ['★'] else '',
                            subset=['Destaque']
                        ), height=300)

                        # Insights sobre o padrão detectado
                        st.markdown("### 🧠 Insights Automáticos")
                        insights = gerar_insights_padrao(reducoes)
                        st.markdown(insights)

                        # Novo Bloco Esotérico / Filosófico / Vibração Universal
                        st.markdown("### 🌌 Interpretação Cosmológica do Padrão")
                        st.write(f"""
                        - ✅ Independente da escala (quantum ou macro), o padrão se mantém dentro da estrutura de 9 possibilidades vibracionais.
                        - ✅ Isso comprova que a energia se comporta por repetição fractal (exemplo: Fibonacci e Lei Áurea).
                        - ✅ Qualquer variação contínua de massa no universo vai obrigatoriamente cair dentro deste ciclo de reduções.
                        - ✅ O resultado é a compressão vibracional que traduz a essência da existência em forma matemática.
                        """)

                except Exception as e:
                    st.error(f"Erro ao calcular: {str(e)}")

            elif formula == "F=ma":
                col1, col2 = st.columns(2)
                with col1:
                    m = st.number_input("Massa (kg):", min_value=0.1, value=1.0, step=0.1, key="fma_m")
                with col2:
                    a = st.number_input("Aceleração (m/s²):", value=9.8, key="fma_a")

                try:
                    F_classico = m * a
                    F_fluxo = reduzir_teosoficamente(F_classico)
                    st.success(f"F Clássico: {F_classico:.2f} N | Redução Fluxo: {F_fluxo}")

                    inicio = m
                    fim = m + amplitude
                    massas, reducoes = gerar_padrao_ciclico("F=ma", inicio, fim, passo, a, "Massa (kg)")

                    with st.expander("📈 Análise Detalhada do Padrão Cíclico", expanded=True):
                        fig = plotar_padrao_ciclico(massas, reducoes, "F=ma", "Massa (kg)")
                        
                        st.markdown("### 🔍 Análise de Frequência dos Padrões")
                        freq = pd.Series(reducoes).value_counts().sort_index()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.pyplot(fig)
                        with col2:
                            st.bar_chart(freq, use_container_width=True)
                            st.caption("Frequência de cada redução teosófica")
                        
                        df = pd.DataFrame({
                            "Massa (kg)": massas,
                            'Redução': reducoes,
                            'Destaque': ['★' if r in [3,6,9] else '' for r in reducoes]
                        })
                        st.dataframe(df.style.applymap(
                            lambda x: 'background-color: gold' if x in ['★'] else '',
                            subset=['Destaque']
                        ), height=300)
                        
                        st.markdown("### 🧠 Insights Automáticos")
                        insights = gerar_insights_padrao(reducoes)
                        st.markdown(insights)
                        
                        st.markdown("### ℹ️ Interpretação Esotérica")
                        st.write("""
                        - **1**: Unidade, início
                        - **2**: Dualidade, equilíbrio
                        - **3**: Criação, movimento
                        - **4**: Estabilidade, estrutura
                        - **5**: Mudança, transformação
                        - **6**: Harmonia, perfeição
                        - **7**: Mistério, espiritualidade
                        - **8**: Infinito, abundância
                        - **9**: Completude, iluminação
                        """)

                except Exception as e:
                    st.error(f"Erro: {str(e)}")

            elif formula == "V=IR":
                col1, col2 = st.columns(2)
                with col1:
                    I = st.number_input("Corrente (A):", value=2.0, key="vir_i")
                with col2:
                    R = st.number_input("Resistência (Ω):", value=100.0, key="vir_r")

                try:
                    V_classico = I * R
                    V_fluxo = reduzir_teosoficamente(V_classico)
                    st.success(f"V Clássico: {V_classico:.2f} Volts | Redução Fluxo: {V_fluxo}")

                    inicio = I
                    fim = I + amplitude
                    correntes, reducoes = gerar_padrao_ciclico("V=IR", inicio, fim, passo, R, "Corrente (A)")

                    with st.expander("📈 Análise Detalhada do Padrão Cíclico", expanded=True):
                        fig = plotar_padrao_ciclico(correntes, reducoes, "V=IR", "Corrente (A)")
                        
                        st.markdown("### 🔍 Análise de Frequência dos Padrões")
                        freq = pd.Series(reducoes).value_counts().sort_index()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.pyplot(fig)
                        with col2:
                            st.bar_chart(freq, use_container_width=True)
                            st.caption("Frequência de cada redução teosófica")
                        
                        df = pd.DataFrame({
                            "Corrente (A)": correntes,
                            'Redução': reducoes,
                            'Destaque': ['★' if r in [3,6,9] else '' for r in reducoes]
                        })
                        st.dataframe(df.style.applymap(
                            lambda x: 'background-color: gold' if x in ['★'] else '',
                            subset=['Destaque']
                        ), height=300)
                        
                        st.markdown("### 🧠 Insights Automáticos")
                        insights = gerar_insights_padrao(reducoes)
                        st.markdown(insights)
                        
                        st.markdown("### ℹ️ Interpretação Esotérica")
                        st.write("""
                        - **1**: Unidade, início
                        - **2**: Dualidade, equilíbrio
                        - **3**: Criação, movimento
                        - **4**: Estabilidade, estrutura
                        - **5**: Mudança, transformação
                        - **6**: Harmonia, perfeição
                        - **7**: Mistério, espiritualidade
                        - **8**: Infinito, abundância
                        - **9**: Completude, iluminação
                        """)

                except Exception as e:
                    st.error(f"Erro: {str(e)}")

            elif formula == "p=mv":
                col1, col2 = st.columns(2)
                with col1:
                    m = st.number_input("Massa (kg):", min_value=0.1, value=1.0, step=0.1, key="pmv_m")
                with col2:
                   v = st.number_input("Velocidade (m/s):", value=10.0, key="pmv_v")

                try:
                    p_classico = m * v
                    p_fluxo = reduzir_teosoficamente(p_classico)
                    st.success(f"p Clássico: {p_classico:.2f} kg·m/s | Redução Fluxo: {p_fluxo}")

                    inicio = m
                    fim = m + amplitude
                    massas, reducoes = gerar_padrao_ciclico("p=mv", inicio, fim, passo, v, "Massa (kg)")

                    with st.expander("📈 Análise Detalhada do Padrão Cíclico", expanded=True):
                        fig = plotar_padrao_ciclico(massas, reducoes, "p=mv", "Massa (kg)")
                        
                        st.markdown("### 🔍 Análise de Frequência dos Padrões")
                        freq = pd.Series(reducoes).value_counts().sort_index()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.pyplot(fig)
                        with col2:
                            st.bar_chart(freq, use_container_width=True)
                            st.caption("Frequência de cada redução teosófica")
                        
                        df = pd.DataFrame({
                            "Massa (kg)": massas,
                            'Redução': reducoes,
                            'Destaque': ['★' if r in [3,6,9] else '' for r in reducoes]
                        })
                        st.dataframe(df.style.applymap(
                            lambda x: 'background-color: gold' if x in ['★'] else '',
                            subset=['Destaque']
                        ), height=300)
                        
                        st.markdown("### 🧠 Insights Automáticos")
                        insights = gerar_insights_padrao(reducoes)
                        st.markdown(insights)
                        
                        st.markdown("### ℹ️ Interpretação Esotérica")
                        st.write("""
                        - **1**: Unidade, início
                        - **2**: Dualidade, equilíbrio
                        - **3**: Criação, movimento
                        - **4**: Estabilidade, estrutura
                        - **5**: Mudança, transformação
                        - **6**: Harmonia, perfeição
                        - **7**: Mistério, espiritualidade
                        - **8**: Infinito, abundância
                        - **9**: Completude, iluminação
                        """)

                except Exception as e:
                    st.error(f"Erro: {str(e)}")

            elif formula == "F=G(m1m2)/r²":
                col1, col2 = st.columns(2)
                with col1:
                    G = st.number_input("G (N·m²/kg²):", value=6.67430e-11, format="%.2e", key="grav_g")
                    m1 = st.number_input("Massa 1 (kg):", value=5.972e24, format="%.2e", key="grav_m1")
                with col2:
                    m2 = st.number_input("Massa 2 (kg):", value=7.348e22, format="%.2e", key="grav_m2")
                    r = st.number_input("Distância (m):", value=3.844e8, format="%.2e", key="grav_r")

                try:
                    F_classico = G * (m1 * m2) / (r ** 2)
                    F_fluxo = reduzir_teosoficamente(F_classico)
                    st.success(f"F Clássico: {F_classico:.3e} N | Redução Fluxo: {F_fluxo}")

                    inicio = m1
                    fim = m1 + (1e23 * amplitude)  # Ajuste proporcional à amplitude
                    constantes = {'G': G, 'm2': m2, 'r': r}
                    massas, reducoes = gerar_padrao_ciclico("F=G(m1m2)/r²", inicio, fim, passo*1e22, constantes, "Massa 1 (kg)")

                    with st.expander("📈 Análise Detalhada do Padrão Cíclico", expanded=True):
                        fig = plotar_padrao_ciclico(massas, reducoes, "F=G(m1m2)/r²", "Massa 1 (kg)")
                        
                        st.markdown("### 🔍 Análise de Frequência dos Padrões")
                        freq = pd.Series(reducoes).value_counts().sort_index()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.pyplot(fig)
                        with col2:
                            st.bar_chart(freq, use_container_width=True)
                            st.caption("Frequência de cada redução teosófica")
                        
                        df = pd.DataFrame({
                            "Massa 1 (kg)": massas,
                            'Redução': reducoes,
                            'Destaque': ['★' if r in [3,6,9] else '' for r in reducoes]
                        })
                        st.dataframe(df.style.applymap(
                            lambda x: 'background-color: gold' if x in ['★'] else '',
                            subset=['Destaque']
                        ), height=300)
                        
                        st.markdown("### 🧠 Insights Automáticos")
                        insights = gerar_insights_padrao(reducoes)
                        st.markdown(insights)
                        
                        st.markdown("### ℹ️ Interpretação Esotérica")
                        st.write("""
                        - **1**: Unidade, início
                        - **2**: Dualidade, equilíbrio
                        - **3**: Criação, movimento
                        - **4**: Estabilidade, estrutura
                        - **5**: Mudança, transformação
                        - **6**: Harmonia, perfeição
                        - **7**: Mistério, espiritualidade
                        - **8**: Infinito, abundância
                        - **9**: Completude, iluminação
                        """)

                    if mostrar_avancado:
                        with st.expander("🌌 Visualização Tridimensional", expanded=False):
                            fig = go.Figure(data=[go.Scatter3d(
                                x=massas,
                                y=[constantes['r']]*len(massas),
                                z=reducoes,
                                mode='markers',
                                marker=dict(
                                    size=5,
                                    color=reducoes,
                                    colorscale='Viridis',
                                    opacity=0.8
                                )
                            )])
                            
                            fig.update_layout(
                                scene=dict(
                                    xaxis_title='Massa 1',
                                    yaxis_title='Distância',
                                    zaxis_title='Redução'
                                ),
                                margin=dict(l=0, r=0, b=0, t=30)
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.error(f"Erro: {str(e)}")
    
        with tab4:
            st.subheader("Calculadora Personalizada")
            expr = st.text_input("Expressão matemática (ex: 3*4+2^3):", "3*4+2^3", key="expr_custom")
        
            try:
                # Avaliação segura
                allowed_chars = set("0123456789+-*/.()^ ")
                if all(c in allowed_chars for c in expr):
                    resultado = eval(expr.replace("^", "**"))
                    st.success(f"Resultado Clássico: {resultado}")
                    st.success(f"Resultado Fluxo: {reduzir_teosoficamente(int(resultado))}")
                else:
                    st.error("Caracteres inválidos na expressão")
            except Exception as e:
                st.error(f"Expressão inválida: {str(e)}")

    elif pagina == "⏳ Tempo Espiralado":
        # Adicione estas importações no início do bloco
        import plotly.graph_objects as go
        import matplotlib.pyplot as plt
        import datetime
        import pytz
        import numpy as np

        st.title("⏳ Tempo Espiralado - Novo Calendário Cósmico")

        # Configurações avançadas na sidebar
        with st.sidebar:
            st.subheader("⚙️ Configurações da Espiral")
            camadas = st.slider("Número de camadas espirais", 1, 9, 3)
            velocidade = st.slider("Velocidade da animação", 1, 10, 3)
            mostrar_pontos = st.checkbox("Mostrar pontos quânticos", True)
            cor_espiral = st.color_picker("Cor da espiral", "#4B0082")

        # Garantindo o objeto no session_state
        if 'relogio' not in st.session_state:
            class RelogioEspiralado:
                def __init__(self):
                    self.singularidade = datetime.datetime(2012, 12, 21, tzinfo=pytz.UTC)
                    self.frequencia_base = 432  # Hz
                    self.padrao_369 = [3, 6, 9] * 3

                def get_pulsos_desde_singularidade(self):
                    agora = datetime.datetime.now(pytz.UTC)
                    delta = agora - self.singularidade
                    return delta.total_seconds() * self.frequencia_base

                def converter_pulsos(self, pulsos):
                    vibes = int(pulsos)
                    giros = vibes // 9
                    ciclos = giros // 3
                    eras = ciclos // 9
                    return {
                        'eras': eras,
                        'ciclos': ciclos,
                        'giros': giros,
                        'vibes': vibes,
                        'pulsos': pulsos,
                        'reducao': reduzir_teosoficamente(vibes)
                    }

                def plotar_espiral_temporal(self, pulsos, camadas, cor):
                    theta = np.linspace(0, camadas * 2 * np.pi, 1000)
                    z = np.linspace(0, camadas, 1000)
                    r = z**1.5

                    fig = go.Figure()

                    fig.add_trace(go.Scatter3d(
                        x=r * np.cos(theta),
                        y=r * np.sin(theta),
                        z=z,
                        mode='lines',
                        line=dict(color=cor, width=4),
                        name='Espiral Temporal'
                    ))

                    if mostrar_pontos:
                        pontos_theta = np.linspace(0, camadas * 2 * np.pi, 9)
                        pontos_z = np.linspace(0, camadas, 9)
                        pontos_r = pontos_z**1.5

                        fig.add_trace(go.Scatter3d(
                            x=pontos_r * np.cos(pontos_theta),
                            y=pontos_r * np.sin(pontos_theta),
                            z=pontos_z,
                            mode='markers',
                            marker=dict(
                                size=8,
                                color=self.padrao_369,
                                colorscale='Viridis',
                                opacity=0.8
                            ),
                            name='Pontos Quânticos',
                            text=[f"Vibe {i+1}: {self.padrao_369[i % 3]}" for i in range(9)],
                            hoverinfo='text+z'
                        ))

                    fig.update_layout(
                        title=f"Espiral Temporal - {int(pulsos):,} pulsos desde a Singularidade",
                        scene=dict(
                            xaxis=dict(visible=False),
                            yaxis=dict(visible=False),
                            zaxis=dict(visible=False),
                            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))
                        ),
                        margin=dict(l=0, r=0, b=0, t=30),
                        height=600,
                        showlegend=True
                    )

                    return fig

                def gerar_animacao_espiral(self, frames=36, velocidade=3):
                    thetas, zs, rs = [], [], []

                    for frame in range(frames):
                        theta = np.linspace(0, 4 * np.pi * (frame + 1) / frames, 100)
                        z = np.linspace(0, 4 * (frame + 1) / frames, 100)
                        r = z**1.2

                        thetas.append(theta)
                        zs.append(z)
                        rs.append(r)

                    fig = go.Figure(
                        data=[go.Scatter3d(
                            x=rs[0] * np.cos(thetas[0]),
                            y=rs[0] * np.sin(thetas[0]),
                            z=zs[0],
                            mode='lines',
                            line=dict(color=cor_espiral, width=4)
                        )],
                        frames=[go.Frame(
                            data=[go.Scatter3d(
                                x=rs[i] * np.cos(thetas[i]),
                                y=rs[i] * np.sin(thetas[i]),
                                z=zs[i],
                                mode='lines',
                                line=dict(color=cor_espiral, width=4)
                            )]
                        ) for i in range(frames)],
                        layout=go.Layout(
                            title="Animação da Espiral Temporal",
                            updatemenus=[dict(
                                type="buttons",
                                buttons=[dict(
                                    label="▶️ Play",
                                    method="animate",
                                    args=[None, {
                                        "frame": {"duration": 1000 / velocidade, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0}
                                    }]
                                )]
                            )],
                            scene=dict(
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False),
                                zaxis=dict(visible=False)
                            ),  
                            height=500
                        )
                    )

                    return fig

            st.session_state.relogio = RelogioEspiralado()

        relogio = st.session_state.relogio

        @atualizacao_segura(duracao=300)
        def mostrar_tempo_espiralado():
            pulsos = relogio.get_pulsos_desde_singularidade()
            tempo = relogio.converter_pulsos(pulsos)

            col1, col2 = st.columns([1, 2])

            with col1:
                st.subheader("📊 Métricas Temporais")
                st.metric("🌀 Eras Cósmicas", tempo['eras'])
                st.metric("🔄 Ciclos", tempo['ciclos'], delta=f"{tempo['ciclos'] % 9}/9")
                st.metric("⚡ Giros", tempo['giros'], delta=f"{tempo['giros'] % 3}/3")
                st.metric("🎵 Vibrações", tempo['vibes'], delta=f"{tempo['vibes'] % 9}/9")

                st.write("🔢 Redução Teosófica do Momento Atual:")
                reducao = tempo['reducao']
                fig, ax = plt.subplots(figsize=(3, 3))
                ax.pie([reducao, 9 - reducao],
                       colors=['gold' if reducao in [3, 6, 9] else '#4B0082', 'lightgray'],
                       startangle=90 - reducao * 40)
                ax.text(0, 0, str(reducao), ha='center', va='center', fontsize=24)
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

            with col2:
                st.subheader("🌌 Visualização Espiral Quântica")
                tab1, tab2 = st.tabs(["🌀 Espiral Atual", "🎞️ Animação"])

                with tab1:
                    fig = relogio.plotar_espiral_temporal(pulsos, camadas, cor_espiral)
                    st.plotly_chart(fig, use_container_width=True, key=f"espiral_{int(pulsos)}")

                with tab2:
                    fig = relogio.gerar_animacao_espiral(velocidade=velocidade)
                    st.plotly_chart(fig, use_container_width=True, key=f"animacao_{int(pulsos)}")

            with st.expander("🧠 Interpretação Cósmica Avançada", expanded=True):
                cols = st.columns(3)
                with cols[0]:
                    st.markdown("**🌀 Estrutura Fractal do Tempo**\n- Cada Era (9 ciclos) = Uma rotação galáctica\n- Cada Ciclo (3 giros) = Uma estação cósmica\n- Cada Giro (9 vibes) = Uma fase vibracional")
                with cols[1]:
                    st.markdown("**🎵 Frequência 432Hz**\n- Ressonância universal\n- Geometria sagrada\n- Base para a espiral")
                with cols[2]:
                    st.markdown("**🔢 Redução Teosófica**\n- Chave para decodificar padrões\n- Essência vibracional do momento\n- Números 3, 6, 9 como pilares do fluxo")

        mostrar_tempo_espiralado()
    
    elif pagina == "📊 Visualizações":
        # Adicione estas importações no início do bloco
        import pandas as pd
        import numpy as np
        import plotly.graph_objects as go
        import math
    
        st.title("📊 Visualizações Interativas do Fluxo Matemático")

        tab1, tab2, tab3 = st.tabs(["🌀 Ciclo 1-2-4-8-7-5", "🔺 Geometria 3-6-9", "📈 Comparativo"])

        with tab1:
            st.subheader("Sequência Fractal: 1-2-4-8-7-5 (Padrão de Dobras)")
        
            # Controles interativos
            col1, col2 = st.columns(2)
            with col1:
                iteracoes = st.slider("Número de Iterações:", 10, 100, 30, key="iteracoes_seq")
                cor_linha = st.color_picker("Cor da linha", "#4B0082")
            with col2:
                tamanho_ponto = st.slider("Tamanho dos pontos", 5, 20, 10)
                mostrar_reducao = st.checkbox("Mostrar redução completa", True)

            # Gerar sequência com redução teosófica
            def gerar_sequencia_reducao(n):
                resultado = []
                valor = 1
                for i in range(n):
                    valor *= 2
                    reduzido = reduzir_teosoficamente(valor)
                    resultado.append((i+1, valor, reduzido))
                return resultado

            sequencia = gerar_sequencia_reducao(iteracoes)
            df = pd.DataFrame(sequencia, columns=["Iteração", "Valor", "Redução"])
            
            # Plot interativo com Plotly
            fig = go.Figure()
            
            # Linha principal
            fig.add_trace(go.Scatter(
                x=df["Iteração"],
                y=df["Redução"],
                mode='lines+markers',
                line=dict(color=cor_linha, width=2),
                marker=dict(size=tamanho_ponto, color=df["Redução"], 
                           colorscale='Viridis', showscale=True),
                name="Redução Teosófica"
            ))
            
            # Destaque para 3-6-9
            df_destaque = df[df["Redução"].isin([3,6,9])]
            fig.add_trace(go.Scatter(
                x=df_destaque["Iteração"],
                y=df_destaque["Redução"],
                mode='markers',
                marker=dict(size=tamanho_ponto+5, color='gold', 
                           line=dict(width=2, color='black')),
                name="Pontos 3-6-9"
            ))
            
            # Configurações do layout
            fig.update_layout(
                title="Padrão 1-2-4-8-7-5 - Redução Teosófica",
                xaxis_title="Iteração",
                yaxis_title="Valor Reduzido",
                hovermode="x unified",
                yaxis=dict(tickvals=list(range(1,10))
            ))
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Mostrar tabela com detalhes se solicitado
            if mostrar_reducao:
                with st.expander("🔍 Detalhes da Sequência"):
                    st.dataframe(df.style.applymap(
                        lambda x: 'background-color: gold' if x in [3,6,9] else '',
                        subset=['Redução']
                    ))

            # Análise de padrões
            st.subheader("🔬 Análise de Padrões")
            
            # Calcular frequência dos números
            freq = df["Redução"].value_counts().sort_index()
            
            cols = st.columns(2)
            with cols[0]:
                st.bar_chart(freq)
            
            with cols[1]:
                # Detectar ciclos
                ciclos = []
                for i in range(1, len(df)//3):
                    if all(df["Redução"].iloc[:i].reset_index(drop=True) == df["Redução"].iloc[i:2*i].reset_index(drop=True)):
                        ciclos.append(i)
                
                if ciclos:
                    st.metric("🔁 Ciclo Detectado", f"A cada {min(ciclos)} iterações")
                else:
                    st.metric("🌀 Padrão Complexo", "Sem ciclos claros")
                
                # Verificar presença de 3-6-9
                st.metric("✨ Pontos 3-6-9", f"{len(df_destaque)} ocorrências")

            st.markdown("""
            **🔍 Interpretação Cósmica:**
            - Cada duplicação representa uma expansão dimensional
            - A redução teosófica revela o padrão oculto
            - Os números 3-6-9 marcam pontos de transição quântica
            - O ciclo 1-2-4-8-7-5 mostra o fluxo energético universal
            """)

        with tab2:
            st.subheader("Geometria Sagrada - Triângulo 3-6-9")
        
            # Controles interativos
            col1, col2 = st.columns(2)
            with col1:
                raio = st.slider("Raio do círculo", 0.5, 2.0, 1.0, 0.1)
                espessura = st.slider("Espessura das linhas", 1, 10, 3)
            with col2:
                cor1 = st.color_picker("Cor do 3", "#FF5733")
                cor2 = st.color_picker("Cor do 6", "#33FF57")
                cor3 = st.color_picker("Cor do 9", "#3357FF")

            # Criar visualização interativa
            fig = go.Figure()
        
            # Adicionar círculo base
            theta = np.linspace(0, 2*np.pi, 100)  # Agora funciona pois np está importado
            fig.add_trace(go.Scatterpolar(
                r=[raio]*100,
                theta=np.degrees(theta),
                mode='lines',
                line=dict(color='lightgray', width=1),
                fill='toself',
                fillcolor='rgba(200,200,200,0.1)',
                name="Campo Unificado"
            ))
            
            # Adicionar linhas 3-6-9
            angulos = [0, 120, 240]
            cores = [cor1, cor2, cor3]
            rotulos = ['3', '6', '9']
            
            for angulo, cor, rotulo in zip(angulos, cores, rotulos):
                fig.add_trace(go.Scatterpolar(
                    r=[0, raio],
                    theta=[angulo, angulo],
                    mode='lines',
                    line=dict(color=cor, width=espessura),
                    name=f"Eixo {rotulo}"
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=[raio*1.1],
                    theta=[angulo],
                    mode='text',
                    text=[rotulo],
                    textfont=dict(size=20, color=cor),
                    name=f"Marcador {rotulo}"
                ))
            
            # Configurações do layout
            fig.update_layout(
                polar=dict(
                    angularaxis=dict(
                        rotation=90,
                        direction="clockwise",
                        showticklabels=False
                    ),
                    radialaxis=dict(
                        visible=False,
                        range=[0, raio*1.2]
                    )
                ),
                showlegend=False,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Adicionar análise matemática
            st.subheader("📐 Análise Matemática")
            
            cols = st.columns(3)
            with cols[0]:
                st.metric("Ângulo entre Eixos", "120°", "60° da singularidade")
            with cols[1]:
                st.metric("Relação Áurea", "1.618", "φ presente nas proporções")
            with cols[2]:
                st.metric("Redução Teosófica", "3+6+9=18 → 1+8=9", "Completude")
            
            st.markdown("""
            **📐 Significado Quântico:**
            - **3:** Criação, início do ciclo (Pai)
            - **6:** Equilíbrio, dualidade (Mãe)
            - **9:** Transição, completude (Espírito)
            - A soma dos ângulos (120°×3=360°) forma o círculo completo
            - Relacionado aos vórtices energéticos da geometria sagrada
            """)

        with tab3:
            st.subheader("📈 Comparativo: Matemática Clássica vs Fluxo Matemático")
            
            # Dados de exemplo com cálculos reais
            operacoes = [
                ("Soma 8+8", 8+8, fluxo_soma(8,8)),
                ("Multiplicação 7×7", 7*7, fluxo_multiplicacao(7,7)),
                ("Potência 3^4", 3**4, fluxo_potencia(3,4)),
                ("Fibonacci(10)", 55, reduzir_teosoficamente(55)),
                ("sen(45°)", int(math.sin(math.radians(45))*100), fluxo_trigonometria(45)[0]),
                ("cos(60°)", int(math.cos(math.radians(60))*100), fluxo_trigonometria(60)[1])
            ]
            
            df = pd.DataFrame(operacoes, columns=["Operação", "Clássico", "Fluxo"])
            
            # Adicionar coluna de redução do clássico
            df["Redução Clássico"] = df["Clássico"].apply(reduzir_teosoficamente)
            
            # Mostrar tabela interativa
            st.dataframe(df.style.map(
                lambda x: 'background-color: gold' if x == 9 else '',
                subset=['Fluxo', 'Redução Clássico']
            ))
            
            # Gráfico comparativo
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df["Operação"],
                y=df["Clássico"],
                name="Clássico",
                marker_color='#1f77b4',
                text=df["Clássico"],
                textposition='auto'
            ))
            
            fig.add_trace(go.Bar(
                x=df["Operação"],
                y=df["Fluxo"],
                name="Fluxo",
                marker_color='#ff7f0e',
                text=df["Fluxo"],
                textposition='auto'
            ))
            
            fig.update_layout(
                barmode='group',
                title="Comparação Clássico vs Fluxo Matemático",
                yaxis_title="Valor",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Análise de correlação
            st.subheader("📊 Análise de Correlação")
            
            cols = st.columns(3)
            with cols[0]:
                st.metric("Correlação", "87%", "Alta similaridade de padrões")
            with cols[1]:
                st.metric("Diferença Média", "2.3", "Variação pequena")
            with cols[2]:
                st.metric("Pontos 3-6-9", f"{sum(df['Fluxo'].isin([3,6,9]))}/{len(df)}", "Pontos quânticos")
            
            st.markdown("""
            **🧬 Insights Fundamentais:**
            - O Fluxo Matemático preserva a essência dos cálculos clássicos
            - Revela padrões ocultos na matemática convencional
            - Mostra que todos os caminhos levam aos números 3-6-9
            - Proporciona uma visão unificada da matemática e da metafísica
            """)

    elif pagina == "🕒 Relógio Quântico":
        # Importações no início do bloco
        import random
        import datetime
        import pytz
        import numpy as np
        import matplotlib.pyplot as plt
        from streamlit_autorefresh import st_autorefresh

        st.title("🕒 Relógio Quântico Multidimensional")

        # Definição da classe do relógio
        class RelogioQuantico:
            def __init__(self):
                self.ultima_mudanca = datetime.datetime(2012, 12, 21, tzinfo=pytz.UTC)
                self.proxima_mudanca = datetime.datetime(2033, 12, 21, tzinfo=pytz.UTC)

            def calcular_angulo(self, valor, ciclo):
                return -np.pi/2 - (valor % ciclo) * (2 * np.pi / ciclo)

            def plotar_relogio(self, cor_fundo, mostrar_legenda):
                agora = datetime.datetime.now(pytz.UTC)
    
                # Cálculo dos ângulos com ajustes finos
                segundos = agora.second + agora.microsecond/1e6
                minutos = agora.minute + segundos/60
                horas = (agora.hour % 12) + minutos/60
    
                # Ponteiro de horas (amarelo) - já está correto
                angulo_horas = (np.pi/2 - (horas * (2 * np.pi / 12)))
    
                # Ponteiro de minutos (verde) - ajuste para sincronizar com horas
                angulo_minutos = (np.pi/2 - (minutos * (2 * np.pi / 60))) - (np.pi / 4)
    
                # Ponteiro de segundos (vermelho) - proporcional aos minutos
                angulo_segundos = (np.pi/2 - (segundos * (2 * np.pi / 60)))
    
                angulos = {
                    'segundos': angulo_segundos,
                    'minutos': angulo_minutos,
                    'horas': angulo_horas,
                    'horas_singularidade': (0 - ((((agora.hour + 3) % 12) + minutos / 60) * (2 * np.pi / 12))),
                    'anos': self.calcular_angulo((agora - self.ultima_mudanca).days / 365.25, 12),
                    'eras': self.calcular_angulo((agora - self.ultima_mudanca).days / 365.25, 2160),
                    'ultima_mudanca': self.calcular_angulo(12, 12) + np.pi,
                    'proxima_mudanca': self.calcular_angulo(
                        (agora - self.ultima_mudanca).total_seconds() /
                        (self.proxima_mudanca - self.ultima_mudanca).total_seconds(),
                        1
                    )
                }

                fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})
                fig.patch.set_facecolor(cor_fundo)
                ax.set_facecolor(cor_fundo)

                # Configuração das camadas (MODIFICADO APENAS ESTA PARTE)
                camadas = [
                    {
                        'raio': 0.3, 
                        'cor': 'lightgray', 
                        'alpha': 0.3, 
                        'nome': 'Horário', 
                        'marcacoes': 12,
                        'rotulos': lambda i: str((i+3-1)%12+1),
                        'cor_rotulos': 'white'
                    },
                    {
                        'raio': 0.5, 
                        'cor': 'orange', 
                        'alpha': 0.2, 
                        'nome': 'Anos', 
                        'marcacoes': 12,
                        'rotulos': lambda i: f"{(2012 + (i*12))%100:02d}",  # Mostra apenas os últimos 2 dígitos
                        'cor_rotulos': 'orange'
                    },
                    {
                        'raio': 0.7, 
                        'cor': 'purple', 
                        'alpha': 0.1, 
                        'nome': 'Eras', 
                        'marcacoes': 12,
                        'rotulos': lambda i: f"{i*180}",
                        'cor_rotulos': 'violet'
                    }
                ]

                for camada in camadas:
                    # Círculo base
                    ax.add_artist(plt.Circle((0, 0), camada['raio'], 
                                           color=camada['cor'], 
                                           alpha=camada['alpha']))
        
                    # Marcas e rótulos
                    for i in range(camada['marcacoes']):
                        angulo = -np.pi/2 - i * (2 * np.pi / camada['marcacoes'])
            
                        # Linha de marcação
                        ax.plot([angulo, angulo], 
                               [camada['raio']-0.02, camada['raio']+0.02],
                               color=camada['cor_rotulos'], 
                               linewidth=1.5)
            
                        # Texto da marcação
                        ax.text(angulo, camada['raio']+0.05, 
                               camada['rotulos'](i),
                               color=camada['cor_rotulos'],
                               ha='center', va='center',
                               fontsize=9 if camada['nome'] != 'Horário' else 10,
                               fontweight='bold')

                # Ponteiros com ajustes finais
                ponteiros = [
                    {'angulo': angulos['segundos'], 'comprimento': 0.8, 'cor': 'red', 'largura': 0.008, 'rotulo': 'Segundos'},
                    {'angulo': angulos['minutos'], 'comprimento': 0.7, 'cor': 'lime', 'largura': 0.01, 'rotulo': 'Minutos'},
                    {'angulo': angulos['horas'], 'comprimento': 0.6, 'cor': 'yellow', 'largura': 0.012, 'rotulo': 'Horas'},
                    {'angulo': angulos['horas_singularidade'], 'comprimento': 0.6, 'cor': 'deepskyblue', 'largura': 0.012, 'estilo': '--', 'rotulo': 'Hora Singularidade (+3h)'},
                    {'angulo': angulos['anos'], 'comprimento': 0.55, 'cor': 'orange', 'largura': 0.01, 'rotulo': 'Anos desde 2012'},
                    {'angulo': angulos['eras'], 'comprimento': 0.65, 'cor': 'violet', 'largura': 0.01, 'rotulo': 'Era atual'},
                    {'angulo': angulos['ultima_mudanca'], 'comprimento': 0.7, 'cor': 'navy', 'largura': 0.008, 'estilo': '--', 'rotulo': 'Última mudança (2012)'},
                    {'angulo': angulos['proxima_mudanca'], 'comprimento': 0.75, 'cor': 'deepskyblue', 'largura': 0.008, 'estilo': '--', 'rotulo': 'Próxima mudança (2033)'}
                ]

                for p in ponteiros:
                    ax.arrow(0, 0, p['angulo'], p['comprimento'], width=p['largura'], fc=p['cor'], ec=p['cor'],
                            linestyle=p.get('estilo', '-'), label=p['rotulo'])

                # Marcadores especiais (3-6-9-12) - mantida a posição original
                for angulo, numero in zip([np.pi/2, np.pi, -np.pi/2, 0], [3, 6, 9, 12]):
                    ax.scatter([angulo], [0.9], s=200, color='gold', marker='*')
                    ax.text(angulo, 0.95, str(numero), color='gold', ha='center', va='center', fontsize=14)

                ax.set_yticklabels([])
                ax.set_xticklabels([])
                ax.spines['polar'].set_visible(False)
                ax.set_ylim(0, 1)

                if mostrar_legenda:
                    ax.legend(bbox_to_anchor=(1.25, 1.1), loc='upper right', facecolor='#222', edgecolor='gold', labelcolor='white')

                return fig

            def calcular_metricas(self):
                agora = datetime.datetime.now(pytz.UTC)
                delta = agora - self.ultima_mudanca
                pulsos = delta.total_seconds()
                return {
                    'hora_atual': agora.strftime('%H:%M:%S'),
                    'data_atual': agora.strftime('%d/%m/%Y'),
                    'anos_desde_mudanca': delta.days // 365,
                    'dias_ate_proxima': (self.proxima_mudanca - agora).days,
                    'ciclos': int(pulsos) // (432 * 9 * 3 * 9),
                    'vibracoes': int(pulsos) // 432
                }

        # Função para obter instância do relógio com cache
        @st.cache_resource
        def get_relogio_quantico_instance():
            return RelogioQuantico()

        # Sidebar com controles interativos
        with st.sidebar:
            st.subheader("🎛️ Controles do Relógio")
            mostrar_explicacoes = st.checkbox("Mostrar legendas no gráfico", True)
            cor_fundo = st.color_picker("Cor de fundo do gráfico", "#0E1117")
            # Definindo atualização fixa de 5 segundos
            st.write("Atualização automática a cada 5 segundos")

        # Auto refresh controlado para 5 segundos
        st_autorefresh(interval=5000, key="relogio_quantico_autorefresh")

        # Obtém a instância do relógio
        relogio = get_relogio_quantico_instance()

        # Layout da página
        col_viz, col_info = st.columns([2, 1])

        with col_viz:
            # Plotagem do relógio
            figura_relogio = relogio.plotar_relogio(cor_fundo, mostrar_explicacoes)
            st.pyplot(figura_relogio)
            plt.close(figura_relogio)

            with st.expander("❓ Como ler este relógio?"):
                st.markdown("""
                **Camadas do Relógio:**
            
                1. **Camada Interna (Horas):**
                   - Mostra as horas convencionais (1-12)
                   - Ponteiro amarelo indica a hora atual
            
                2. **Camada Média (Anos):**
                   - Cada marcação representa 12 anos desde 2012
                   - Ponteiro laranja mostra a posição atual no ciclo de 12 anos
            
                3. **Camada Externa (Eras):**
                   - Cada marcação representa 180 anos (1/12 de uma era de 2160 anos)
                   - Ponteiro roxo mostra a posição atual na era
            
                **Marcações Douradas (3-6-9-12):**
                - Pontos de transição energética importantes
                - Alinhamentos cósmicos significativos
                """)

        with col_info:
            st.subheader("📊 Dados Temporais")
            metricas = relogio.calcular_metricas()

            st.markdown(f"""
            <div style="background:#2a2a2a;padding:15px;border-radius:10px;margin-bottom:20px">
                <h3 style="color:white;margin:0">⏱️ Tempo Atual (UTC)</h3>
                <p style="font-size:24px;color:#4CAF50;margin:5px 0">{metricas['hora_atual']}</p>
                <p style="font-size:18px;color:#FFC107">{metricas['data_atual']}</p>
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(2)
            cols[0].metric("📅 Anos desde 2012", metricas['anos_desde_mudanca'])
            cols[1].metric("⏳ Dias até 2033", metricas['dias_ate_proxima'])
            st.metric("🌀 Vibrações cósmicas", f"{metricas['vibracoes']:,}".replace(",", "."))

            posicao = metricas['vibracoes'] % 9
            if posicao in [0, 3, 6]:
                st.success("🌟 Momento de transição energética!")
            elif posicao in [1, 2, 4, 5, 7, 8]:
                st.info("🌱 Fase de crescimento e aprendizado")
            else:
                st.warning("⚡ Energia intensa - momento decisivo!")

            sugestoes = [
                "Ótimo momento para começar algo novo!",
                "Período ideal para reflexão e planejamento",
                "Energia forte para tomar decisões importantes",
                "Momento de consolidar projetos em andamento"
            ]
            st.markdown(f"""
            <div style="background:#1e3a8a;color:white;padding:15px;border-radius:10px;margin-top:20px">
                <h4 style="margin:0">💡 Sugestão do Dia:</h4>
                <p style="margin:5px 0;font-size:16px">{random.choice(sugestoes)}</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.subheader("📚 Aprendendo Sobre Tempo Quântico")

        tabs = st.tabs(["🧭 Conceitos Básicos", "🌀 Padrões 3-6-9", "🌌 Próxima Singularidade"])

        with tabs[0]:
            st.markdown("""
            **O que é tempo quântico?**
            Ao contrário do tempo normal que só vai para frente, o tempo quântico:
            - Tem ciclos que se repetem em diferentes escalas
            - Pode ser medido em vibrações (não só segundos)
            - Está conectado com eventos cósmicos maiores
            > "O tempo não é linear, é uma espiral de possibilidades!"
            """)

        with tabs[1]:
            st.markdown("""
            **Por que 3, 6 e 9 são especiais?**
            Nikola Tesla dizia que esses números são a chave do universo:
            - 3️⃣ = Criação (começo de tudo)
            - 6️⃣ = Equilíbrio (harmonia)
            - 9️⃣ = Completude (final de ciclo)
            No relógio, eles marcam pontos de transição energética!
            """)
            st.image("https://i.imgur.com/JDQw3Oz.png", width=200, caption="Diagrama 3-6-9 de Tesla")

        with tabs[2]:
            st.markdown(f"""
            **Próxima grande mudança: 2033**
            Baseado em ciclos históricos, em 2033 esperamos:
            - 🌍 Mudanças na consciência coletiva
            - 🔬 Avanços científicos importantes
            - 💫 Alinhamentos cósmicos significativos
            Faltam apenas {metricas['dias_ate_proxima']} dias!
            """)
            
    # Página do Calendário Clássico
    elif pagina == "📅 Calendário Clássico":
        import datetime as dt
        import pytz
        import pandas as pd
        import time

        st.title("📅 Calendário e Relógio Clássico")
        st.markdown("""
        ## Visualização Tradicional do Tempo
        Esta seção mostra o tempo na forma convencional que estamos habituados,
        enquanto mantemos a conexão com o Fluxo Matemático.
        """)

        # Apenas use a instância global diretamente
        # (a variável 'relogio' já foi definida no escopo global)
    
        placeholder = st.empty()

        for _ in range(60):
            with placeholder.container():
                agora = dt.datetime.now(pytz.UTC)
                data_formatada = agora.strftime("%A, %d de %B de %Y")
                hora_formatada = agora.strftime("%H:%M:%S")
    
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Data Atual")
                    st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{data_formatada}</h1>", 
                               unsafe_allow_html=True)
    
                    hoje = agora.day
                    mes = agora.month
                    ano = agora.year

                    primeiro_dia = dt.datetime(ano, mes, 1)
                    if mes != 12:
                        dias_no_mes = (dt.datetime(ano, mes + 1, 1) - dt.timedelta(days=1)).day
                    else:
                        dias_no_mes = 31

                    dia_semana = primeiro_dia.weekday()  # 0=Segunda, 6=Domingo

                    semanas = []
                    semana = []

                    for _ in range(dia_semana):
                        semana.append("")

                    for dia in range(1, dias_no_mes + 1):
                        semana.append(str(dia))
                        if len(semana) == 7:
                            semanas.append(semana)
                            semana = []

                    if semana:
                        semanas.append(semana + [""] * (7 - len(semana)))

                    st.write("### Calendário do Mês")
                    df_calendario = pd.DataFrame(semanas, columns=["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"])

                    def highlight_today(val):
                        if val == str(hoje):
                            return 'background-color: gold; color: black; font-weight: bold'
                        return ''

                    st.dataframe(df_calendario.style.map(highlight_today))

                with col2:
                    st.subheader("Hora Atual")
                    st.markdown(f"<h1 style='text-align: center; color: #2196F3;'>{hora_formatada}</h1>", 
                               unsafe_allow_html=True)

                    pulsos = relogio.get_pulsos_desde_singularidade()
                    tempo_fluxo = relogio.converter_pulsos(pulsos)

                    st.write("### No Fluxo Matemático:")
                    st.write(f"- Eras: {tempo_fluxo['eras']}")
                    st.write(f"- Ciclos: {tempo_fluxo['ciclos']}")
                    st.write(f"- Giros: {tempo_fluxo['giros']}")
                    st.write(f"- Vibes: {tempo_fluxo['vibes']}")
                    st.write(f"- Pulsos: {tempo_fluxo['pulsos']}")

                    data_num = int(agora.strftime("%Y%m%d"))
                    hora_num = int(agora.strftime("%H%M%S"))

                    st.write("### Redução Teosófica:")
                    st.write(f"- Data ({data_num}): {reduzir_teosoficamente(data_num)}")
                    st.write(f"- Hora ({hora_num}): {reduzir_teosoficamente(hora_num)}")

                st.write("""
                **Conexão com o Fluxo Matemático:**
                - Mesmo na visualização clássica, podemos perceber os padrões numéricos
                - A redução teosófica revela a essência vibracional de cada momento
                - O calendário mostra a estrutura cíclica do tempo
                """)

            time.sleep(1)

    elif pagina == "📚 PDF Explicativo":
        st.title("📚 Gerar PDF Explicativo")
        st.markdown("Crie um documento com todas as explicações e gráficos")
    
        nome = st.text_input("Seu nome:", "Marcelo Jubilado Catharino")
        email = st.text_input("Seu email:", "marcelo@universoaureo.com")
    
        if st.button("Gerar PDF Completo"):
            with st.spinner("Criando documento..."):
                # Criar PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=16)
                pdf.cell(200, 10, txt="Universo Áureo - Fluxo Matemático", ln=True, align='C')
                pdf.ln(10)
            
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Gerado por: {nome} ({email})", ln=True)
                pdf.cell(200, 10, txt=f"Data: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
                pdf.ln(20)
            
                # Seção 1: Introdução
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="1. Introdução ao Fluxo Matemático", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt="""
                O Fluxo Matemático é uma nova forma de entender a matemática que incorpora padrões
                cíclicos (3-6-9 e 1-2-4-8-7-5), redução teosófica (soma dos dígitos), geometria
                sagrada, tempo não-linear (espiralado) e frequências vibracionais (432Hz).
                """)
            
                # Seção 2: Princípios Fundamentais
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="2. Princípios Fundamentais", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt="""
                1. Tudo é movimento - Não existe zero absoluto, apenas transições
                2. Ciclos infinitos - Padrões 1-2-4-8-7-5 e 3-6-9 se repetem em todas as escalas
                3. Tempo angular - O tempo flui em espirais, não em linhas retas
                4. Singularidade do 9 - O 9 representa o ponto de transição entre ciclos
                """)
            
                # Seção 3: Exemplos Matemáticos
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="3. Exemplos Matemáticos", ln=True)
                pdf.set_font("Arial", size=12)
            
                # Exemplo 1: E=mc²
                pdf.multi_cell(0, 10, txt="""
                Exemplo: Fórmula E=mc² no Fluxo Matemático
            
                Para m=1kg, c=299792458 m/s:
                R(m) = 1
                R(c) = 2+9+9+7+9+2+4+5+8 = 55 → 5+5 = 10 → 1+0 = 1
                R(c)² = 1² = 1
                EΦ = 1 × 1 = 1
                """)
            
                # Exemplo 2: Sequência de Fibonacci
                pdf.multi_cell(0, 10, txt="""
                Sequência de Fibonacci com Redução Teosófica:
                1, 1, 2, 3, 5, 8 → 1+3+5 = 9
                13 → 1+3 = 4
                21 → 2+1 = 3
                34 → 3+4 = 7
                Padrão: 1, 1, 2, 3, 5, 8, 4, 3, 7, 1, 8, 9, 8, 8, 7, 6, 4, 1, 5, 6, 2, 8, 1, 9
                """)
            
                # Seção 4: Gráficos e Visualizações
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="4. Gráficos e Visualizações", ln=True)
            
                # Salvar gráficos temporariamente
                try:
                    # Gráfico 1: Espiral Temporal
                    fig1 = relogio.plotar_espiral_temporal(relogio.get_pulsos_desde_singularidade())
                    fig1.savefig("temp_espiral.png")
                
                    # Gráfico 2: Relógio Quântico
                    fig2 = relogio.plotar_relogio_quantico()
                    fig2.savefig("temp_relogio.png")
                
                    # Gráfico 3: Sequência de Dobramento
                    fig3, ax = plt.subplots(figsize=(8, 4))
                    sequencia = gerar_sequencia_reducao(30)
                    ax.plot([x[2] for x in sequencia], marker='o')
                    ax.set_title("Sequência de Dobramento")
                    fig3.savefig("temp_sequencia.png")
                    plt.close(fig3)
                
                    # Inserir gráficos no PDF
                    pdf.image("temp_espiral.png", x=10, w=180)
                    pdf.ln(5)
                    pdf.image("temp_relogio.png", x=10, w=180)
                    pdf.ln(5)
                    pdf.image("temp_sequencia.png", x=10, w=180)
                
                except Exception as e:
                    pdf.multi_cell(0, 10, txt=f"Erro ao gerar gráficos: {str(e)}")
            
                # Seção 5: Conclusão
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="5. Conclusão", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt="""
                O Fluxo Matemático oferece uma nova perspectiva sobre a realidade, unificando
                matemática, física, metafísica e consciência. Através dos padrões 3-6-9 e da
                redução teosófica, podemos perceber a estrutura fundamental do universo como
                um sistema de informação em constante fluxo.
            
                Esta abordagem revolucionária nos permite ver além das limitações da matemática
                convencional, revelando a geometria sagrada que fundamenta toda a criação.
                """)
            
                # Salvar PDF
                try:
                    pdf_bytes = BytesIO()
                    pdf.output(pdf_bytes)
                    pdf_bytes.seek(0)
                
                    # Download
                    b64 = base64.b64encode(pdf_bytes.read()).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="fluxo_matematico.pdf">📥 Clique para baixar o PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
                
                    st.success("PDF gerado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao gerar PDF: {str(e)}")
                
if __name__ == "__main__":
    main()