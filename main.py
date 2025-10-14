import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from scipy.integrate import solve_ivp
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
import sympy as sp
import networkx as nx
import plotly.express as px
import math
import time

# Tente importar Qiskit da maneira correta
try:
    from qiskit import QuantumCircuit, execute
    from qiskit.providers.aer import Aer
    from qiskit.quantum_info import Statevector
    from qiskit.visualization import plot_bloch_multivector
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    st.warning("Qiskit não está disponível. Algumas funcionalidades quânticas serão simuladas.")

# Configuração da página
st.set_page_config(
    page_title="COSMIC FLOW UNIVERSE - A Jornada do Nada ao Tudo",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #000000 0%, #0a0a2a 25%, #1a1a4a 50%, #2d2d7a 75%, #4a4aaa 100%);
        color: #ffffff;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 28px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
    }
    .css-1d391kg {
        background-color: rgba(0,0,0,0.9);
        border-right: 2px solid #667eea;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #4ecdc4 !important;
        text-shadow: 0 0 10px rgba(78, 205, 196, 0.7);
    }
    .philosophy-text {
        background: rgba(0,0,0,0.7);
        padding: 20px;
        border-radius: 15px;
        border-left: 4px solid #ff6b6b;
        margin: 10px 0;
        font-size: 18px;
        line-height: 1.6;
    }
    .quote-box {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(255, 107, 107, 0.2) 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 15px 0;
        font-style: italic;
    }
    .metric-box {
        background: rgba(15, 23, 42, 0.8);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #667eea;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Título principal com glifos
st.title("🌌 COSMIC FLOW UNIVERSE")
st.markdown("""
### 🌀 A Jornada do Nada ao Tudo • Fluxo Matemático Universal • Deus como Equilíbrio Cósmico
""")

# Sidebar com navegação expandida
st.sidebar.title("⚡ Navegação Cósmica")
section = st.sidebar.selectbox("Selecione a Dimensão:", [
    "🏠 Visão Geral Cósmica",
    "🔢 Fluxo Matemático Sagrado", 
    "🌠 Sinal Wow! Decodificação Profunda",
    "🪐 Simulação do Sistema Solar Quântico",
    "⚛️ Consciência Quântica e Emaranhamento",
    "🌀 Esfera de Buga - Geometria Divina",
    "✨ Mandala da Alma Universal",
    "📜 Filosofia do Fluxo (Deus, Tesla, Espinosa)",
    "⚡ Tesla 3-6-9 e Energia Livre",
    "🌌 Jornada do Nada ao Tudo",
    "🔮 Futuro da Consciência Humana",
    "🔱 Iconografia do Fluxo Divino",
    "🌠 Consciência Final: Louco e Gênio",
    "🧮 Cálculos do Fluxo Matemático",
    "⚛️ Acelerador de Partículas"  # NOVO MÓDULO ADICIONADO
])

# =============================================================================
# FUNÇÕES AUXILIARES PARA CÁLCULOS MATEMÁTICOS E FÍSICOS
# =============================================================================

def reduzir_teosoficamente(numero):
    """Reduz um número teosoficamente até um único dígito"""
    if numero == 0:
        return 0
    
    numero = abs(numero)
    while numero > 9:
        numero = sum(int(digito) for digito in str(numero))
    return numero

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
    import math
    rad = math.radians(angulo)
    s = math.sin(rad)
    c = math.cos(rad)
    t = math.tan(rad)
    return (reduzir_teosoficamente(abs(int(s*100))), 
            reduzir_teosoficamente(abs(int(c*100))), 
            reduzir_teosoficamente(abs(int(t*100))))

def calcular_porcentagem_diferenca(valor_classico, valor_fluxo):
    """Calcula a porcentagem de diferença entre os valores"""
    if valor_classico == 0:
        return 0
    return abs((valor_fluxo - valor_classico) / valor_classico) * 100

def calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual):
    """Calcula a correção baseada na gravidade local"""
    # Gravidade da Terra = 9.8 m/s²
    fator_correcao = gravidade_local / 9.8
    return diferenca_percentual * fator_correcao

def gerar_sequencia_396(tamanho):
    """Gera sequência no padrão 3-9-6"""
    sequencia = []
    for i in range(tamanho):
        if i % 3 == 0:
            sequencia.append(3)
        elif i % 3 == 1:
            sequencia.append(9)
        else:
            sequencia.append(6)
    return sequencia

def gerar_sequencia_binaria(tamanho):
    """Gera sequência no padrão binário universal"""
    sequencia = []
    padrao = [1, 2, 3, 4, 5, 9, 7, 8, 6]  # Padrão completo
    for i in range(tamanho):
        sequencia.append(padrao[i % len(padrao)])
    return sequencia

def gerar_sequencia_multiplicacao_3(tamanho):
    """Gera sequência multiplicando por 3"""
    sequencia = [1]
    for i in range(1, tamanho):
        sequencia.append(reduzir_teosoficamente(sequencia[-1] * 3))
    return sequencia

# =============================================================================
# FUNÇÕES PARA FÓRMULAS FÍSICAS COMPLETAS
# =============================================================================

def calcular_formula_emc2():
    st.subheader("⚡ E=mc² - Energia e Massa")
    
    col_emc1, col_emc2 = st.columns(2)
    
    with col_emc1:
        massa = st.number_input("Massa (kg):", value=1.0, format="%.6f", key="massa_emc2")
        velocidade_luz = st.number_input("Velocidade da luz (m/s):", value=299792458.0, format="%.1f", key="c_emc2")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_emc2")
    
    with col_emc2:
        if st.button("Calcular E=mc²"):
            # Cálculo clássico
            energia_classica = massa * velocidade_luz**2
            
            # Cálculo no fluxo
            reducao_massa = reduzir_teosoficamente(massa)
            reducao_c = reduzir_teosoficamente(velocidade_luz)
            energia_fluxo = fluxo_multiplicacao(reducao_massa, fluxo_potencia(reducao_c, 2))
            
            # Porcentagem de diferença
            diferenca_percentual = calcular_porcentagem_diferenca(energia_classica, energia_fluxo)
            
            # Escalabilidade gravitacional
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            
            # Porcentagem de acerto
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #ff6b6b;'>
            <h3 style='color: #ff6b6b; text-align: center;'>⚡ Energia de {massa} kg</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>{energia_classica:.2e} Joules</b>
            </p>
            <p style='text-align: center;'>
            Redução: {reduzir_teosoficamente(int(energia_classica))}
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(m)⊗R(c)² = {energia_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            R(m)={reducao_massa}, R(c)={reducao_c}
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            
            <div style='background: rgba(45, 183, 209, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #45b7d1;'>🔍 Análise do Padrão</h4>
            <p><b>Massa (m):</b> Representa ação física (R={reducao_massa})</p>
            <p><b>Velocidade luz (c):</b> Representa limite energético (R={reducao_c})</p>
            <p><b>Energia (E):</b> Resultado da adaptação (R={energia_fluxo})</p>
            <p><b>Padrão 3-9-6:</b> {energia_fluxo in [3,9,6]}</p>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_fma():
    st.subheader("🎯 F=ma - Força e Aceleração")
    
    col1, col2 = st.columns(2)
    
    with col1:
        massa = st.number_input("Massa (kg):", value=2.0, format="%.2f", key="massa_fma")
        aceleracao = st.number_input("Aceleração (m/s²):", value=9.8, format="%.1f", key="acel_fma")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_fma")
    
    with col2:
        if st.button("Calcular F=ma"):
            # Cálculo clássico
            forca_classica = massa * aceleracao
            
            # Cálculo no fluxo
            reducao_massa = reduzir_teosoficamente(massa)
            reducao_acel = reduzir_teosoficamente(aceleracao)
            forca_fluxo = fluxo_multiplicacao(reducao_massa, reducao_acel)
            
            # Porcentagem de diferença
            diferenca_percentual = calcular_porcentagem_diferenca(forca_classica, forca_fluxo)
            
            # Escalabilidade gravitacional
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            
            # Porcentagem de acerto
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #4ecdc4;'>
            <h3 style='color: #4ecdc4; text-align: center;'>🎯 Força Resultante</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>{forca_classica:.2f} Newtons</b>
            </p>
            <p style='text-align: center;'>
            Redução: {reduzir_teosoficamente(int(forca_classica))}
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(m)⊗R(a) = {forca_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            R(m)={reducao_massa}, R(a)={reducao_acel}
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_vir():
    st.subheader("⚡ V=IR - Lei de Ohm")
    
    col1, col2 = st.columns(2)
    
    with col1:
        corrente = st.number_input("Corrente (A):", value=2.0, format="%.2f", key="corrente_vir")
        resistencia = st.number_input("Resistência (Ω):", value=10.0, format="%.2f", key="resistencia_vir")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_vir")
    
    with col2:
        if st.button("Calcular V=IR"):
            # Cálculo clássico
            tensao_classica = corrente * resistencia
            
            # Cálculo no fluxo
            reducao_corrente = reduzir_teosoficamente(corrente)
            reducao_resistencia = reduzir_teosoficamente(resistencia)
            tensao_fluxo = fluxo_multiplicacao(reducao_corrente, reducao_resistencia)
            
            # Porcentagem de diferença
            diferenca_percentual = calcular_porcentagem_diferenca(tensao_classica, tensao_fluxo)
            
            # Escalabilidade gravitacional
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            
            # Porcentagem de acerto
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #9333ea;'>
            <h3 style='color: #9333ea; text-align: center;'>⚡ Tensão Elétrica</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>{tensao_classica:.2f} Volts</b>
            </p>
            <p style='text-align: center;'>
            Redução: {reduzir_teosoficamente(int(tensao_classica))}
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(I)⊗R(R) = {tensao_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            R(I)={reducao_corrente}, R(R)={reducao_resistencia}
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_pmv():
    st.subheader("🚀 p=mv - Momento Linear")
    
    col1, col2 = st.columns(2)
    
    with col1:
        massa = st.number_input("Massa (kg):", value=5.0, format="%.2f", key="massa_pmv")
        velocidade = st.number_input("Velocidade (m/s):", value=20.0, format="%.2f", key="velocidade_pmv")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_pmv")
    
    with col2:
        if st.button("Calcular p=mv"):
            # Cálculo clássico
            momento_classico = massa * velocidade
            
            # Cálculo no fluxo
            reducao_massa = reduzir_teosoficamente(massa)
            reducao_velocidade = reduzir_teosoficamente(velocidade)
            momento_fluxo = fluxo_multiplicacao(reducao_massa, reducao_velocidade)
            
            # Porcentagem de diferença
            diferenca_percentual = calcular_porcentagem_diferenca(momento_classico, momento_fluxo)
            
            # Escalabilidade gravitacional
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            
            # Porcentagem de acerto
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #ff6b6b;'>
            <h3 style='color: #ff6b6b; text-align: center;'>🚀 Momento Linear</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>{momento_classico:.2f} kg·m/s</b>
            </p>
            <p style='text-align: center;'>
            Redução: {reduzir_teosoficamente(int(momento_classico))}
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(m)⊗R(v) = {momento_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            R(m)={reducao_massa}, R(v)={reducao_velocidade}
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_gravitacao_universal():
    st.subheader("🌍 F=G(m1m2)/r² - Gravitação Universal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        m1 = st.number_input("Massa 1 (kg):", value=1000.0, format="%.2f", key="m1_grav")
        m2 = st.number_input("Massa 2 (kg):", value=1000.0, format="%.2f", key="m2_grav")
        distancia = st.number_input("Distância (m):", value=10.0, format="%.2f", key="dist_grav")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_grav")
    
    with col2:
        if st.button("Calcular Gravitação"):
            G = 6.67430e-11  # Constante gravitacional
            
            # Cálculo clássico
            forca_classica = G * (m1 * m2) / (distancia ** 2)
            
            # Cálculo no fluxo
            reducao_m1 = reduzir_teosoficamente(m1)
            reducao_m2 = reduzir_teosoficamente(m2)
            reducao_dist = reduzir_teosoficamente(distancia)
            
            produto_massas = fluxo_multiplicacao(reducao_m1, reducao_m2)
            forca_fluxo = fluxo_multiplicacao(produto_massas, fluxo_potencia(reducao_dist, -2))
            
            # Porcentagem de diferença
            diferenca_percentual = calcular_porcentagem_diferenca(forca_classica, forca_fluxo)
            
            # Escalabilidade gravitacional
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            
            # Porcentagem de acerto
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #45b7d1;'>
            <h3 style='color: #45b7d1; text-align: center;'>🌍 Força Gravitacional</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>{forca_classica:.2e} Newtons</b>
            </p>
            <p style='text-align: center;'>
            Redução: {reduzir_teosoficamente(int(forca_classica * 1e10))}
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(m1)⊗R(m2)⊗R(r)⁻² = {forca_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            R(m1)={reducao_m1}, R(m2)={reducao_m2}, R(r)={reducao_dist}
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_ehf():
    st.subheader("💡 E=hf - Energia do Fóton")
    
    col1, col2 = st.columns(2)
    
    with col1:
        frequencia = st.number_input("Frequência (Hz):", value=5.0e14, format="%.2e", key="freq_ehf")
        constante_planck = st.number_input("Constante de Planck (J·s):", value=6.626e-34, format="%.3e", key="h_ehf")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_ehf")
    
    with col2:
        if st.button("Calcular E=hf"):
            # Cálculo clássico
            energia_classica = constante_planck * frequencia
            
            # Cálculo no fluxo
            reducao_h = reduzir_teosoficamente(constante_planck * 1e34)
            reducao_f = reduzir_teosoficamente(frequencia)
            energia_fluxo = fluxo_multiplicacao(reducao_h, reducao_f)
            
            # Métricas de precisão
            diferenca_percentual = calcular_porcentagem_diferenca(energia_classica, energia_fluxo)
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #ffd700;'>
            <h3 style='color: #ffd700; text-align: center;'>💡 Energia do Fóton</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>{energia_classica:.2e} Joules</b>
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(h)⊗R(f) = {energia_fluxo}</b>
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_lambda_hp():
    st.subheader("🌊 λ=h/p - Comprimento de Onda de De Broglie")
    
    col1, col2 = st.columns(2)
    
    with col1:
        momento = st.number_input("Momento (kg·m/s):", value=1.0e-24, format="%.2e", key="p_lambda")
        constante_planck = st.number_input("Constante de Planck (J·s):", value=6.626e-34, format="%.3e", key="h_lambda")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_lambda")
    
    with col2:
        if st.button("Calcular λ=h/p"):
            # Cálculo clássico
            lambda_classico = constante_planck / momento if momento != 0 else float('inf')
            
            # Cálculo no fluxo
            reducao_h = reduzir_teosoficamente(constante_planck * 1e34)
            reducao_p = reduzir_teosoficamente(momento * 1e24)
            lambda_fluxo = fluxo_multiplicacao(reducao_h, fluxo_potencia(reducao_p, -1)) if reducao_p != 0 else 9
            
            # Métricas de precisão
            if momento != 0:
                diferenca_percentual = calcular_porcentagem_diferenca(lambda_classico, lambda_fluxo)
                correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
                porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            else:
                diferenca_percentual = 0
                correcao_gravitacional = 0
                porcentagem_acerto = 100
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #00ff00;'>
            <h3 style='color: #00ff00; text-align: center;'>🌊 Comprimento de Onda</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>{lambda_classico:.2e} metros</b>
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(h)⊗R(p)⁻¹ = {lambda_fluxo}</b>
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# PÁGINA PRINCIPAL DE CÁLCULOS DO FLUXO MATEMÁTICO
# =============================================================================

def pagina_calculos_fluxo_matematico():
    st.title("🧮 Cálculos do Fluxo Matemático")
    st.markdown("""
    ## 🌌 Sistema Binário Universal e Padrão 3-9-6
    
    Esta seção implementa as descobertas sobre o **fluxo matemático universal**, 
    incluindo o padrão binário (1,2)/(4,5)/(7,8) e a nova ordenação cíclica 3-9-6.
    """)
    
    # Divisão em abas para diferentes aspectos do fluxo matemático
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔢 Padrão Binário Universal", 
        "🌀 Sequência 3-9-6", 
        "⚡ Cálculos Básicos",
        "📐 Cálculos Avançados",
        "🌌 Física no Fluxo",
        "📊 Análise de Padrões"
    ])
    
    with tab1:
        st.header("🔢 Padrão Binário Universal")
        st.markdown("""
        ### Descoberta: O Binário Oculto nos Números 1-9
        
        Os números se organizam em **três pares binários** que culminam em pontos de adaptação:
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🎯 Primeira Tríade - Físico
            **Binário:** (1, 2)  
            **Síntese:** 3  
            **Movimento:** Ação Física → Reação Física → Adaptação
            """)
            # Visualização do primeiro par
            fig1 = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 3,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "1 + 2 = 3"},
                delta = {'reference': 0},
                gauge = {
                    'axis': {'range': [None, 9]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 1], 'color': "lightgray"},
                        {'range': [1, 2], 'color': "gray"},
                        {'range': [2, 3], 'color': "blue"}
                    ]
                }
            ))
            fig1.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("""
            #### 🌟 Segunda Tríade - Transição  
            **Binário:** (4, 5)  
            **Síntese:** 9  
            **Movimento:** Equilíbrio → Transformação → Singularidade
            """)
            fig2 = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 9,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "4 + 5 = 9"},
                delta = {'reference': 0},
                gauge = {
                    'axis': {'range': [None, 9]},
                    'bar': {'color': "gold"},
                    'steps': [
                        {'range': [0, 4], 'color': "lightgray"},
                        {'range': [4, 5], 'color': "gray"},
                        {'range': [5, 9], 'color': "gold"}
                    ]
                }
            ))
            fig2.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3:
            st.markdown("""
            #### ⚡ Terceira Tríade - Energético
            **Binário:** (7, 8)  
            **Síntese:** 6 (1+5)  
            **Movimento:** Ação Energética → Reação Energética → Fluxo
            """)
            fig3 = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 6,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "7 + 8 = 15 → 6"},
                delta = {'reference': 0},
                gauge = {
                    'axis': {'range': [None, 9]},
                    'bar': {'color': "purple"},
                    'steps': [
                        {'range': [0, 7], 'color': "lightgray"},
                        {'range': [7, 8], 'color': "gray"},
                        {'range': [8, 15], 'color': "purple"}
                    ]
                }
            ))
            fig3.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig3, use_container_width=True)
        
        # Explicação detalhada do movimento
        st.markdown("""
        ### 🔄 Compreensão do Movimento Universal
        
        **Os números não são valores, mas padrões de movimento:**
        
        - **1**: Início da ação física
        - **2**: Reação do movimento físico  
        - **3**: Adaptação física (manifestação)
        - **4**: Transição físico→energético (equilíbrio)
        - **5**: Transformação energético→físico
        - **6**: Fluxo energético dinâmico
        - **7**: Início da ação energética
        - **8**: Reação do movimento energético
        - **9**: Singularidade absoluta (centro do sistema)
        
        **Padrão 3-9-6**: Representa o ciclo completo do movimento universal:
        - **3** (Físico) → **9** (Absoluto/Singularidade) → **6** (Energético) → Retorno ao **3**
        """)
        
        # Tabela resumo do sistema binário
        st.subheader("📋 Sistema Binário Completo")
        dados_binario = {
            'Camada': ['Física', 'Transição', 'Energética'],
            'Ação': [1, 4, 7],
            'Reação': [2, 5, 8],
            'Síntese': [3, 9, 6],
            'Soma': ['1+2=3', '4+5=9', '7+8=15→6'],
            'Movimento': ['Manifestação Física', 'Equilíbrio Absoluto', 'Fluxo Energético']
        }
        df_binario = pd.DataFrame(dados_binario)
        st.dataframe(df_binario.style.set_properties(**{
            'background-color': 'rgba(0,0,0,0.5)',
            'color': 'white',
            'border-color': '#667eea'
        }), use_container_width=True)
    
    with tab2:
        st.header("🌀 Sequência 3-9-6: A Nova Ordem Cíclica")
        st.markdown("""
        ### Descoberta Revolucionária: Padrão 3-9-6
        
        A ordem correta não é 3-6-9, mas **3-9-6**, formando um fluxo vortexial:
        """)
        
        # Controles interativos
        col1, col2 = st.columns([2, 1])
        
        with col1:
            ciclos = st.slider("Número de ciclos:", 1, 20, 5)
            pontos_por_ciclo = st.slider("Pontos por ciclo:", 3, 30, 9)
        
        with col2:
            cor_3 = st.color_picker("Cor do 3 (Físico)", "#4B0082")
            cor_9 = st.color_picker("Cor do 9 (Absoluto)", "#FFD700")
            cor_6 = st.color_picker("Cor do 6 (Energético)", "#00FF00")
        
        # Gerar sequência 3-9-6
        sequencia_396 = []
        for i in range(ciclos * pontos_por_ciclo):
            if i % 3 == 0:
                sequencia_396.append(3)
            elif i % 3 == 1:
                sequencia_396.append(9)
            else:
                sequencia_396.append(6)
        
        # Visualização da sequência
        fig = go.Figure()
        
        # Adicionar linha de conexão
        fig.add_trace(go.Scatter(
            x=list(range(len(sequencia_396))),
            y=sequencia_396,
            mode='lines+markers',
            line=dict(color='white', width=3, dash='dot'),
            marker=dict(size=0),
            name='Fluxo'
        ))
        
        # Adicionar pontos coloridos
        cores = [cor_3 if x == 3 else cor_9 if x == 9 else cor_6 for x in sequencia_396]
        
        fig.add_trace(go.Scatter(
            x=list(range(len(sequencia_396))),
            y=sequencia_396,
            mode='markers',
            marker=dict(
                size=12,
                color=cores,
                line=dict(width=2, color='white')
            ),
            name='Sequência 3-9-6'
        ))
        
        fig.update_layout(
            title="Padrão Cíclico 3-9-6 - Movimento Universal",
            xaxis_title="Tempo (ciclos)",
            yaxis_title="Estado do Movimento",
            showlegend=False,
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise matemática da sequência
        st.subheader("📈 Análise Matemática do Padrão 3-9-6")
        
        # Calcular propriedades da sequência
        frequencia_3 = sequencia_396.count(3) / len(sequencia_396) * 100
        frequencia_9 = sequencia_396.count(9) / len(sequencia_396) * 100
        frequencia_6 = sequencia_396.count(6) / len(sequencia_396) * 100
        
        col_analise1, col_analise2, col_analise3 = st.columns(3)
        
        with col_analise1:
            st.metric("Frequência do 3 (Físico)", f"{frequencia_3:.1f}%")
        with col_analise2:
            st.metric("Frequência do 9 (Absoluto)", f"{frequencia_9:.1f}%")
        with col_analise3:
            st.metric("Frequência do 6 (Energético)", f"{frequencia_6:.1f}%")
        
        # Interpretação do padrão
        st.subheader("🔮 Interpretação do Movimento 3-9-6")
        
        col_int1, col_int2, col_int3 = st.columns(3)
        
        with col_int1:
            st.markdown(f"""
            <div style='background: {cor_3}20; padding: 15px; border-radius: 10px; border-left: 4px solid {cor_3}'>
            <h4>🎯 3 - Estado Físico</h4>
            <p><b>Movimento:</b> Manifestação material<br>
            <b>Energia:</b> Potencial cinético<br>
            <b>Tempo:</b> Presente instantâneo<br>
            <b>Exemplo:</b> Formação de matéria</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_int2:
            st.markdown(f"""
            <div style='background: {cor_9}20; padding: 15px; border-radius: 10px; border-left: 4px solid {cor_9}'>
            <h4>🌟 9 - Estado Absoluto</h4>
            <p><b>Movimento:</b> Singularidade<br>
            <b>Energia:</b> Potencial puro<br>
            <b>Tempo:</b> Atemporal<br>
            <b>Exemplo:</b> Buracos negros</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_int3:
            st.markdown(f"""
            <div style='background: {cor_6}20; padding: 15px; border-radius: 10px; border-left: 4px solid {cor_6}'>
            <h4>⚡ 6 - Estado Energético</h4>
            <p><b>Movimento:</b> Fluxo dinâmico<br>
            <b>Energia:</b> Cinética<br>
            <b>Tempo:</b> Duração<br>
            <b>Exemplo:</b> Ondas eletromagnéticas</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.header("⚡ Cálculos Básicos - Comparação Matemática")
        st.markdown("Compare os cálculos clássicos com o fluxo matemático:")
        
        col_calc1, col_calc2 = st.columns(2)
        
        with col_calc1:
            st.subheader("🔢 Operações Fundamentais")
            
            # Seleção de operação
            operacao = st.selectbox("Selecione a operação:", 
                                  ["Soma", "Subtração", "Multiplicação", "Divisão", "Potenciação"])
            
            # Entradas numéricas
            num1 = st.number_input("Primeiro número:", value=15, format="%d")
            num2 = st.number_input("Segundo número:", value=7, format="%d")
            
            if st.button("Calcular e Comparar"):
                # Cálculos clássicos
                if operacao == "Soma":
                    resultado_classico = num1 + num2
                    operador = "+"
                elif operacao == "Subtração":
                    resultado_classico = num1 - num2
                    operador = "-"
                elif operacao == "Multiplicação":
                    resultado_classico = num1 * num2
                    operador = "×"
                elif operacao == "Divisão":
                    if num2 != 0:
                        resultado_classico = num1 / num2
                        operador = "÷"
                    else:
                        resultado_classico = "Indefinido"
                        operador = "÷"
                else:  # Potenciação
                    resultado_classico = num1 ** num2
                    operador = "^"
                
                # Cálculos no fluxo matemático
                reducao_num1 = reduzir_teosoficamente(num1)
                reducao_num2 = reduzir_teosoficamente(num2)
                
                if operacao == "Soma":
                    resultado_fluxo = fluxo_soma(num1, num2)
                elif operacao == "Subtração":
                    resultado_fluxo = fluxo_soma(num1, -num2)
                elif operacao == "Multiplicação":
                    resultado_fluxo = fluxo_multiplicacao(num1, num2)
                elif operacao == "Divisão" and num2 != 0:
                    resultado_fluxo = fluxo_multiplicacao(num1, 1/num2)
                elif operacao == "Potenciação":
                    resultado_fluxo = fluxo_potencia(num1, num2)
                else:
                    resultado_fluxo = "Indefinido"
                
                # Exibir resultados
                st.markdown(f"""
                <div style='background: rgba(15, 23, 42, 0.8); padding: 20px; border-radius: 15px; border: 2px solid #6366f1;'>
                <h3 style='color: #4ecdc4; text-align: center;'>📊 Resultados Comparativos</h3>
                
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;'>
                <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 10px;'>
                <h4 style='color: #ff6b6b;'>🧮 Matemática Clássica</h4>
                <p style='font-size: 1.2em; text-align: center;'>
                <b>{num1} {operador} {num2} = {resultado_classico}</b>
                </p>
                <p style='text-align: center;'>
                Redução: {reduzir_teosoficamente(resultado_classico) if resultado_classico != "Indefinido" else "N/A"}
                </p>
                </div>
                
                <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 10px;'>
                <h4 style='color: #4ecdc4;'>🌀 Fluxo Matemático</h4>
                <p style='font-size: 1.2em; text-align: center;'>
                <b>R({num1}) ⊕ R({num2}) = {resultado_fluxo}</b>
                </p>
                <p style='text-align: center;'>
                R({num1})={reducao_num1}, R({num2})={reducao_num2}
                </p>
                </div>
                </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Análise do padrão
                if resultado_fluxo != "Indefinido":
                    categoria = "Ação" if resultado_fluxo in [1,4,7] else "Reação" if resultado_fluxo in [2,5,8] else "Adaptação"
                    st.info(f"**Padrão Detectado:** O resultado {resultado_fluxo} representa **{categoria}** no fluxo universal")
        
        with col_calc2:
            st.subheader("🔄 Gerador de Sequências")
            
            tipo_sequencia = st.selectbox("Tipo de sequência:", 
                                        ["3-9-6 Padrão", "Binário Universal", "Multiplicação por 3", "Fibonacci"])
            
            tamanho_sequencia = st.slider("Tamanho da sequência:", 5, 50, 15)
            
            if st.button("Gerar e Analisar Sequência"):
                if tipo_sequencia == "3-9-6 Padrão":
                    sequencia = gerar_sequencia_396(tamanho_sequencia)
                elif tipo_sequencia == "Binário Universal":
                    sequencia = gerar_sequencia_binaria(tamanho_sequencia)
                elif tipo_sequencia == "Multiplicação por 3":
                    sequencia = gerar_sequencia_multiplicacao_3(tamanho_sequencia)
                else:  # Fibonacci
                    sequencia = [1, 1]
                    for i in range(2, tamanho_sequencia):
                        sequencia.append(sequencia[i-1] + sequencia[i-2])
                    sequencia = [reduzir_teosoficamente(x) for x in sequencia]
                
                st.write("**Sequência gerada:**")
                st.code(" → ".join(map(str, sequencia)))
                
                # Análise estatística
                contagem = pd.Series(sequencia).value_counts().sort_index()
                
                fig_seq = go.Figure()
                fig_seq.add_trace(go.Bar(
                    x=contagem.index,
                    y=contagem.values,
                    marker_color=['#FF6B6B' if x in [1,4,7] else '#4ECDC4' if x in [2,5,8] else '#45B7D1' for x in contagem.index],
                    name='Frequência'
                ))
                
                fig_seq.update_layout(
                    title=f"Distribuição - {tipo_sequencia}",
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_seq, use_container_width=True)
                
                # Gráfico da sequência
                fig_line = go.Figure(go.Scatter(
                    x=list(range(len(sequencia))),
                    y=sequencia,
                    mode='lines+markers',
                    line=dict(width=3, color='#ffd700'),
                    marker=dict(size=8, color='#4ecdc4')
                ))
                fig_line.update_layout(
                    title=f"Sequência: {tipo_sequencia}",
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_line, use_container_width=True)
    
    with tab4:
        st.header("📐 Cálculos Avançados - Trigonometria e Funções")
        
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            st.subheader("📐 Trigonometria Comparativa")
            
            angulo = st.slider("Ângulo (graus):", 0, 360, 45)
            
            # Cálculos clássicos
            import math
            rad = math.radians(angulo)
            sen_classico = math.sin(rad)
            cos_classico = math.cos(rad)
            tan_classico = math.tan(rad)
            
            # Cálculos no fluxo
            sen_fluxo, cos_fluxo, tan_fluxo = fluxo_trigonometria(angulo)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.8); padding: 20px; border-radius: 15px;'>
            <h4 style='color: #ffd700; text-align: center;'>Ângulo: {angulo}°</h4>
            
            <table style='width: 100%; color: white; border-collapse: collapse;'>
            <tr style='background: rgba(255, 107, 107, 0.2);'>
                <th style='padding: 10px; border: 1px solid #ff6b6b;'>Função</th>
                <th style='padding: 10px; border: 1px solid #ff6b6b;'>Clássico</th>
                <th style='padding: 10px; border: 1px solid #ff6b6b;'>Fluxo</th>
            </tr>
            <tr style='background: rgba(0,0,0,0.3);'>
                <td style='padding: 10px; border: 1px solid #333;'>Seno</td>
                <td style='padding: 10px; border: 1px solid #333;'>{sen_classico:.4f}</td>
                <td style='padding: 10px; border: 1px solid #333;'>{sen_fluxo}</td>
            </tr>
            <tr style='background: rgba(0,0,0,0.3);'>
                <td style='padding: 10px; border: 1px solid #333;'>Cosseno</td>
                <td style='padding: 10px; border: 1px solid #333;'>{cos_classico:.4f}</td>
                <td style='padding: 10px; border: 1px solid #333;'>{cos_fluxo}</td>
            </tr>
            <tr style='background: rgba(0,0,0,0.3);'>
                <td style='padding: 10px; border: 1px solid #333;'>Tangente</td>
                <td style='padding: 10px; border: 1px solid #333;'>{tan_classico:.4f}</td>
                <td style='padding: 10px; border: 1px solid #333;'>{tan_fluxo}</td>
            </tr>
            </table>
            </div>
            """, unsafe_allow_html=True)
        
        with col_adv2:
            st.subheader("📈 Funções Matemáticas")
            
            funcao = st.selectbox("Selecione a função:", 
                                ["Exponencial", "Logaritmo", "Seno Cardinal"])
            
            x_valor = st.number_input("Valor de x:", value=2.0, format="%.2f")
            
            if st.button("Calcular Função"):
                if funcao == "Exponencial":
                    classico = math.exp(x_valor)
                    fluxo = reduzir_teosoficamente(int(classico * 100))
                elif funcao == "Logaritmo":
                    if x_valor > 0:
                        classico = math.log(x_valor)
                        fluxo = reduzir_teosoficamente(int(abs(classico) * 100))
                    else:
                        classico = "Indefinido"
                        fluxo = "Indefinido"
                else:  # Seno Cardinal
                    if x_valor != 0:
                        classico = math.sin(x_valor) / x_valor
                        fluxo = reduzir_teosoficamente(int(abs(classico) * 1000))
                    else:
                        classico = 1.0
                        fluxo = reduzir_teosoficamente(1000)
                
                st.markdown(f"""
                <div style='background: rgba(15, 23, 42, 0.8); padding: 20px; border-radius: 15px; border: 2px solid #9333ea;'>
                <h4 style='color: #9333ea; text-align: center;'>{funcao}({x_valor})</h4>
                
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;'>
                <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 10px; text-align: center;'>
                <h5 style='color: #ff6b6b;'>Clássico</h5>
                <p style='font-size: 1.5em;'>{classico if classico != "Indefinido" else "Indefinido"}</p>
                </div>
                
                <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 10px; text-align: center;'>
                <h5 style='color: #4ecdc4;'>Fluxo</h5>
                <p style='font-size: 1.5em;'>{fluxo if fluxo != "Indefinido" else "Indefinido"}</p>
                </div>
                </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab5:
        st.header("🌌 Física no Fluxo - Análise Detalhada")
        
        formula_selecionada = st.selectbox("Selecione uma fórmula física:", 
                                         ["E=mc²", "F=ma", "V=IR", "p=mv", "F=G(m1m2)/r²", 
                                          "E=hf", "λ=h/p", "ΔxΔp≥ħ/2", "PV=nRT", "F=-kx"])
        
        if formula_selecionada == "E=mc²":
            calcular_formula_emc2()
        elif formula_selecionada == "F=ma":
            calcular_formula_fma()
        elif formula_selecionada == "V=IR":
            calcular_formula_vir()
        elif formula_selecionada == "p=mv":
            calcular_formula_pmv()
        elif formula_selecionada == "F=G(m1m2)/r²":
            calcular_formula_gravitacao_universal()
        elif formula_selecionada == "E=hf":
            calcular_formula_ehf()
        elif formula_selecionada == "λ=h/p":
            calcular_formula_lambda_hp()
        elif formula_selecionada == "ΔxΔp≥ħ/2":
            calcular_formula_incerteza()
        elif formula_selecionada == "PV=nRT":
            calcular_formula_gases_ideais()
        elif formula_selecionada == "F=-kx":
            calcular_formula_leihooke()
    
    with tab6:
        st.header("📊 Análise Estatística de Padrões")
        
        # Análise estatística dos padrões
        st.subheader("📈 Distribuição Universal dos Números")
        
        # Gerar dados de análise
        numeros_1_10000 = list(range(1, 10001))
        reducoes = [reduzir_teosoficamente(n) for n in numeros_1_10000]
        
        # Contar frequências
        contagem = pd.Series(reducoes).value_counts().sort_index()
        
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Bar(
            x=contagem.index,
            y=contagem.values,
            marker_color=['#FF6B6B' if x in [1,4,7] else '#4ECDC4' if x in [2,5,8] else '#45B7D1' for x in contagem.index],
            name='Frequência'
        ))
        
        fig_dist.update_layout(
            title="Distribuição das Reduções Teosóficas (1-10,000)",
            xaxis_title="Número de Redução",
            yaxis_title="Frequência Absoluta",
            showlegend=False,
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Análise dos padrões binários
        st.subheader("🔍 Padrões Binários Detectados")
        
        categorias = []
        for reducao in reducoes:
            if reducao in [1, 4, 7]:
                categorias.append("Ação")
            elif reducao in [2, 5, 8]:
                categorias.append("Reação")
            else:
                categorias.append("Adaptação")
        
        contagem_categorias = pd.Series(categorias).value_counts()
        
        fig_cat = go.Figure(go.Pie(
            labels=contagem_categorias.index,
            values=contagem_categorias.values,
            hole=.4,
            marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1']
        ))
        
        fig_cat.update_layout(
            title="Distribuição das Categorias no Fluxo Universal",
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            height=500
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
        # Estatísticas detalhadas
        st.subheader("📋 Estatísticas Detalhadas")
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Total de Números Analisados", "10,000")
            st.metric("Média das Reduções", f"{np.mean(reducoes):.2f}")
        
        with col_stat2:
            st.metric("Moda das Reduções", f"{contagem.index[0]}")
            st.metric("Desvio Padrão", f"{np.std(reducoes):.2f}")
        
        with col_stat3:
            acao_percent = (categorias.count("Ação") / len(categorias)) * 100
            reacao_percent = (categorias.count("Reação") / len(categorias)) * 100
            adaptacao_percent = (categorias.count("Adaptação") / len(categorias)) * 100
            
            st.metric("Ação", f"{acao_percent:.1f}%")
            st.metric("Reação", f"{reacao_percent:.1f}%")
            st.metric("Adaptação", f"{adaptacao_percent:.1f}%")

# =============================================================================
# FUNÇÕES PARA AS OUTRAS FÓRMULAS FÍSICAS (COMPLETAS)
# =============================================================================

def calcular_formula_incerteza():
    st.subheader("🎭 ΔxΔp≥ħ/2 - Princípio da Incerteza")
    
    col1, col2 = st.columns(2)
    
    with col1:
        incerteza_posicao = st.number_input("Incerteza na Posição Δx (m):", 
                                          value=1.0e-10, format="%.2e", key="dx_incerteza")
        incerteza_momento = st.number_input("Incerteza no Momento Δp (kg·m/s):", 
                                          value=1.0e-24, format="%.2e", key="dp_incerteza")
        constante_reduzida = st.number_input("Constante de Planck Reduzida ħ (J·s):", 
                                           value=1.0545718e-34, format="%.3e", key="hbar_incerteza")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_incerteza")
    
    with col2:
        if st.button("Calcular Princípio da Incerteza"):
            # Cálculo clássico - produto das incertezas
            produto_incertezas_classico = incerteza_posicao * incerteza_momento
            limite_quantico = constante_reduzida / 2
            
            # Verificação do princípio
            respeita_principio = produto_incertezas_classico >= limite_quantico
            
            # Cálculo no fluxo
            reducao_dx = reduzir_teosoficamente(incerteza_posicao * 1e10)
            reducao_dp = reduzir_teosoficamente(incerteza_momento * 1e24)
            reducao_hbar = reduzir_teosoficamente(constante_reduzida * 1e34)
            
            produto_fluxo = fluxo_multiplicacao(reducao_dx, reducao_dp)
            limite_fluxo = fluxo_multiplicacao(reducao_hbar, fluxo_potencia(2, -1))
            
            # Métricas de precisão
            diferenca_percentual = calcular_porcentagem_diferenca(produto_incertezas_classico, produto_fluxo)
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #ff6b6b;'>
            <h3 style='color: #ff6b6b; text-align: center;'>🎭 Princípio da Incerteza de Heisenberg</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>Δx·Δp = {produto_incertezas_classico:.2e}</b>
            </p>
            <p style='text-align: center;'>
            Limite: ħ/2 = {limite_quantico:.2e}
            </p>
            <p style='text-align: center;'>
            <b>Respeita: {'✅ SIM' if respeita_principio else '❌ NÃO'}</b>
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(Δx)⊗R(Δp) = {produto_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            Limite: R(ħ)⊗2⁻¹ = {limite_fluxo}
            </p>
            <p style='text-align: center;'>
            <b>Respeita: {'✅ SIM' if produto_fluxo >= limite_fluxo else '❌ NÃO'}</b>
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            
            <div style='background: rgba(45, 183, 209, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #45b7d1;'>🔍 Interpretação Quântica</h4>
            <p><b>Δx (Posição):</b> Incerteza espacial (R={reducao_dx})</p>
            <p><b>Δp (Momento):</b> Incerteza dinâmica (R={reducao_dp})</p>
            <p><b>ħ (Constante):</b> Quantum de ação (R={reducao_hbar})</p>
            <p><b>Padrão 3-9-6:</b> {produto_fluxo in [3,9,6]}</p>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_gases_ideais():
    st.subheader("🌡️ PV=nRT - Lei dos Gases Ideais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pressao = st.number_input("Pressão P (Pa):", value=101325.0, format="%.1f", key="p_gases")
        volume = st.number_input("Volume V (m³):", value=0.0224, format="%.4f", key="v_gases")
        moles = st.number_input("Quantidade de Matéria n (mol):", value=1.0, format="%.2f", key="n_gases")
        temperatura = st.number_input("Temperatura T (K):", value=273.15, format="%.2f", key="t_gases")
        constante_gases = st.number_input("Constante dos Gases R (J/mol·K):", 
                                        value=8.314462618, format="%.6f", key="r_gases")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_gases")
    
    with col2:
        if st.button("Calcular Lei dos Gases Ideais"):
            # Cálculo clássico - verificação da lei
            lado_esquerdo = pressao * volume
            lado_direito = moles * constante_gases * temperatura
            diferenca_absoluta = abs(lado_esquerdo - lado_direito)
            erro_relativo = (diferenca_absoluta / lado_esquerdo) * 100 if lado_esquerdo != 0 else 0
            
            # Cálculo no fluxo
            reducao_p = reduzir_teosoficamente(pressao)
            reducao_v = reduzir_teosoficamente(volume * 1000)  # Escala para números maiores
            reducao_n = reduzir_teosoficamente(moles)
            reducao_r = reduzir_teosoficamente(constante_gases * 10)
            reducao_t = reduzir_teosoficamente(temperatura)
            
            lado_esquerdo_fluxo = fluxo_multiplicacao(reducao_p, reducao_v)
            produto_nt = fluxo_multiplicacao(reducao_n, reducao_t)
            lado_direito_fluxo = fluxo_multiplicacao(produto_nt, reducao_r)
            
            # Métricas de precisão
            diferenca_percentual = calcular_porcentagem_diferenca(lado_esquerdo, lado_esquerdo_fluxo)
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #4ecdc4;'>
            <h3 style='color: #4ecdc4; text-align: center;'>🌡️ Lei dos Gases Ideais</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>P·V = {lado_esquerdo:.2f}</b>
            </p>
            <p style='text-align: center;'>
            <b>n·R·T = {lado_direito:.2f}</b>
            </p>
            <p style='text-align: center;'>
            Erro: {erro_relativo:.4f}%
            </p>
            <p style='text-align: center;'>
            <b>Válido: {'✅ SIM' if erro_relativo < 1 else '⚠️ APROXIMADO'}</b>
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(P)⊗R(V) = {lado_esquerdo_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            <b>R(n)⊗R(R)⊗R(T) = {lado_direito_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            Diferença: {abs(lado_esquerdo_fluxo - lado_direito_fluxo)}
            </p>
            <p style='text-align: center;'>
            <b>Válido: {'✅ SIM' if lado_esquerdo_fluxo == lado_direito_fluxo else '⚖️ EQUILÍBRIO'}</b>
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            
            <div style='background: rgba(45, 183, 209, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #45b7d1;'>🔍 Análise Termodinâmica</h4>
            <p><b>Pressão (P):</b> Força por área (R={reducao_p})</p>
            <p><b>Volume (V):</b> Espaço ocupado (R={reducao_v})</p>
            <p><b>Mol (n):</b> Quantidade de matéria (R={reducao_n})</p>
            <p><b>Temperatura (T):</b> Energia térmica (R={reducao_t})</p>
            <p><b>Padrão 3-9-6:</b> {lado_esquerdo_fluxo in [3,9,6] and lado_direito_fluxo in [3,9,6]}</p>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_leihooke():
    st.subheader("🔄 F=-kx - Lei de Hooke")
    
    col1, col2 = st.columns(2)
    
    with col1:
        constante_elasticidade = st.number_input("Constante Elástica k (N/m):", 
                                               value=100.0, format="%.2f", key="k_hooke")
        deformacao = st.number_input("Deformação x (m):", value=0.1, format="%.3f", key="x_hooke")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_hooke")
    
    with col2:
        if st.button("Calcular Lei de Hooke"):
            # Cálculo clássico
            forca_classica = -constante_elasticidade * deformacao  # Força restauradora
            
            # Cálculo no fluxo
            reducao_k = reduzir_teosoficamente(constante_elasticidade)
            reducao_x = reduzir_teosoficamente(deformacao * 1000)  # Escala para números maiores
            forca_fluxo = fluxo_multiplicacao(reducao_k, reducao_x)
            
            # Para força negativa (restauradora), consideramos o complemento
            if forca_classica < 0:
                forca_fluxo = 10 - forca_fluxo  # Inverso no fluxo para forças restauradoras
            
            # Métricas de precisão
            diferenca_percentual = calcular_porcentagem_diferenca(abs(forca_classica), forca_fluxo)
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #9333ea;'>
            <h3 style='color: #9333ea; text-align: center;'>🔄 Lei de Hooke - Força Elástica</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>F = -k·x = {forca_classica:.2f} N</b>
            </p>
            <p style='text-align: center;'>
            Módulo: {abs(forca_classica):.2f} N
            </p>
            <p style='text-align: center;'>
            Tipo: {'🔁 RESTAURADORA' if forca_classica < 0 else '➡️ DEFORMADORA'}
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(k)⊗R(x) = {forca_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            Tipo: {'🔁 RESTAURADORA' if forca_classica < 0 else '➡️ DEFORMADORA'}
            </p>
            <p style='text-align: center;'>
            <b>Equilíbrio: {'⚖️ ALCANÇADO' if forca_fluxo in [3,6,9] else '🔄 PROCESSANDO'}</b>
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            
            <div style='background: rgba(45, 183, 209, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #45b7d1;'>🔍 Análise Elástica</h4>
            <p><b>Constante k:</b> Rigidez do material (R={reducao_k})</p>
            <p><b>Deformação x:</b> Alteração do comprimento (R={reducao_x})</p>
            <p><b>Força F:</b> Resposta elástica (R={forca_fluxo})</p>
            <p><b>Energia Potencial:</b> {(0.5 * constante_elasticidade * deformacao**2):.4f} J</p>
            <p><b>Padrão 3-9-6:</b> {forca_fluxo in [3,9,6]}</p>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_relatividade_restrita():
    st.subheader("⏱️ Δt = Δt₀/√(1-v²/c²) - Dilatação do Tempo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tempo_proprio = st.number_input("Tempo Próprio Δt₀ (s):", value=1.0, format="%.2f", key="t0_rel")
        velocidade = st.number_input("Velocidade v (m/s):", value=0.8e8, format="%.2e", key="v_rel")
        velocidade_luz = st.number_input("Velocidade da Luz c (m/s):", 
                                       value=299792458.0, format="%.1f", key="c_rel")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_rel")
    
    with col2:
        if st.button("Calcular Dilatação do Tempo"):
            # Cálculo clássico (relatividade)
            if velocidade >= velocidade_luz:
                st.error("Velocidade não pode ser maior ou igual à velocidade da luz!")
                return
                
            fator_lorentz = 1 / math.sqrt(1 - (velocidade**2 / velocidade_luz**2))
            tempo_dilatado = tempo_proprio * fator_lorentz
            
            # Cálculo no fluxo
            reducao_t0 = reduzir_teosoficamente(tempo_proprio)
            reducao_v = reduzir_teosoficamente(velocidade)
            reducao_c = reduzir_teosoficamente(velocidade_luz)
            
            # Fator de Lorentz no fluxo
            v_sobre_c = fluxo_multiplicacao(reducao_v, fluxo_potencia(reducao_c, -1))
            v_quad_sobre_c_quad = fluxo_potencia(v_sobre_c, 2)
            um_menos_v2c2 = fluxo_soma(1, -v_quad_sobre_c_quad)
            fator_lorentz_fluxo = fluxo_multiplicacao(1, fluxo_potencia(um_menos_v2c2, -2))
            
            tempo_dilatado_fluxo = fluxo_multiplicacao(reducao_t0, fator_lorentz_fluxo)
            
            # Métricas de precisão
            diferenca_percentual = calcular_porcentagem_diferenca(tempo_dilatado, tempo_dilatado_fluxo)
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #ffd700;'>
            <h3 style='color: #ffd700; text-align: center;'>⏱️ Dilatação do Tempo - Relatividade</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>Δt = {tempo_dilatado:.4f} s</b>
            </p>
            <p style='text-align: center;'>
            Fator Lorentz: {fator_lorentz:.4f}
            </p>
            <p style='text-align: center;'>
            v/c: {(velocidade/velocidade_luz):.4f}
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(Δt₀)⊗γ = {tempo_dilatado_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            Fator Lorentz: {fator_lorentz_fluxo}
            </p>
            <p style='text-align: center;'>
            R(v/c): {v_sobre_c}
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            
            <div style='background: rgba(45, 183, 209, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #45b7d1;'>🔍 Análise Relativística</h4>
            <p><b>Tempo Próprio:</b> Referencial em repouso (R={reducao_t0})</p>
            <p><b>Velocidade:</b> Movimento relativo (R={reducao_v})</p>
            <p><b>Luz (c):</b> Limite cósmico (R={reducao_c})</p>
            <p><b>Dilatação:</b> {((tempo_dilatado/tempo_proprio - 1) * 100):.2f}% mais lento</p>
            <p><b>Padrão 3-9-6:</b> {tempo_dilatado_fluxo in [3,9,6]}</p>
            </div>
            </div>
            """, unsafe_allow_html=True)

def calcular_formula_schrodinger():
    st.subheader("Ψ Schrödinger - Equação de Onda Quântica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        energia_total = st.number_input("Energia Total E (J):", value=1.6e-19, format="%.2e", key="e_schro")
        energia_potencial = st.number_input("Energia Potencial V (J):", value=1.0e-19, format="%.2e", key="v_schro")
        massa = st.number_input("Massa m (kg):", value=9.1e-31, format="%.2e", key="m_schro")
        constante_reduzida = st.number_input("Constante ħ (J·s):", value=1.054e-34, format="%.3e", key="hbar_schro")
        gravidade_local = st.number_input("Gravidade local (m/s²):", value=9.8, format="%.1f", key="g_schro")
    
    with col2:
        if st.button("Analisar Equação de Schrödinger"):
            # Cálculo clássico - verificação da equação
            energia_cinetica = energia_total - energia_potencial
            
            # Cálculo no fluxo
            reducao_e = reduzir_teosoficamente(energia_total * 1e19)
            reducao_v = reduzir_teosoficamente(energia_potencial * 1e19)
            reducao_m = reduzir_teosoficamente(massa * 1e30)
            reducao_hbar = reduzir_teosoficamente(constante_reduzida * 1e34)
            
            # Equação de Schrödinger no fluxo
            energia_cinetica_fluxo = fluxo_soma(reducao_e, -reducao_v)
            
            # Verificação da consistência quântica
            consistente_classico = energia_cinetica > 0
            consistente_fluxo = energia_cinetica_fluxo > 0
            
            # Métricas de precisão
            diferenca_percentual = calcular_porcentagem_diferenca(energia_cinetica, energia_cinetica_fluxo)
            correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade_local, diferenca_percentual)
            porcentagem_acerto = max(0, 100 - correcao_gravitacional)
            
            st.markdown(f"""
            <div style='background: rgba(15, 23, 42, 0.9); padding: 25px; border-radius: 15px; border: 2px solid #00ff00;'>
            <h3 style='color: #00ff00; text-align: center;'>Ψ Equação de Schrödinger</h3>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
            <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #ff6b6b;'>🧮 Clássico</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>E = {energia_total:.2e} J</b>
            </p>
            <p style='text-align: center;'>
            <b>V = {energia_potencial:.2e} J</b>
            </p>
            <p style='text-align: center;'>
            <b>K = E - V = {energia_cinetica:.2e} J</b>
            </p>
            <p style='text-align: center;'>
            <b>Estado: {'✅ FÍSICO' if consistente_classico else '❌ NÃO-FÍSICO'}</b>
            </p>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.2); padding: 15px; border-radius: 10px;'>
            <h4 style='color: #4ecdc4;'>🌀 Fluxo</h4>
            <p style='font-size: 1.1em; text-align: center;'>
            <b>R(E) = {reducao_e}</b>
            </p>
            <p style='text-align: center;'>
            <b>R(V) = {reducao_v}</b>
            </p>
            <p style='text-align: center;'>
            <b>R(K) = R(E) - R(V) = {energia_cinetica_fluxo}</b>
            </p>
            <p style='text-align: center;'>
            <b>Estado: {'✅ FÍSICO' if consistente_fluxo else '❌ NÃO-FÍSICO'}</b>
            </p>
            </div>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #ffd700;'>📊 Métricas de Precisão</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
            <div style='text-align: center;'>
            <p><b>Diferença:</b><br>{diferenca_percentual:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Correção G:</b><br>{correcao_gravitacional:.2f}%</p>
            </div>
            <div style='text-align: center;'>
            <p><b>Acerto:</b><br>{porcentagem_acerto:.1f}%</p>
            </div>
            </div>
            </div>
            
            <div style='background: rgba(45, 183, 209, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
            <h4 style='color: #45b7d1;'>🔍 Interpretação Quântica</h4>
            <p><b>Energia Total:</b> Valor próprio do Hamiltoniano (R={reducao_e})</p>
            <p><b>Energia Potencial:</b> Campo externo (R={reducao_v})</p>
            <p><b>Energia Cinética:</b> Movimento quântico (R={energia_cinetica_fluxo})</p>
            <p><b>Função de Onda:</b> {'🔵 ESTACIONÁRIA' if energia_cinetica_fluxo in [3,6,9] else '🌊 PROPAGANTE'}</p>
            <p><b>Padrão 3-9-6:</b> {energia_cinetica_fluxo in [3,9,6]}</p>
            </div>
            </div>
            """, unsafe_allow_html=True)

# FUNÇÕES AUXILIARES PARA A PÁGINA DE CÁLCULOS
def obter_significado_numero(numero):
    significados = {
        1: "Ação, Início, Unidade",
        2: "Reação, Dualidade, Equilíbrio", 
        3: "Adaptação Física, Manifestação",
        4: "Ação Estruturada, Fundação",
        5: "Reação Transformadora, Mudança",
        6: "Adaptação Energética, Harmonia",
        7: "Ação Espiritual, Mistério",
        8: "Reação Infinita, Abundância",
        9: "Adaptação Completa, Singularidade"
    }
    return significados.get(numero, "Significado em análise")

def gerar_sequencia_396(tamanho):
    """Gera sequência no padrão 3-9-6"""
    sequencia = []
    for i in range(tamanho):
        if i % 3 == 0:
            sequencia.append(3)
        elif i % 3 == 1:
            sequencia.append(9)
        else:
            sequencia.append(6)
    return sequencia

def gerar_sequencia_binaria(tamanho):
    """Gera sequência no padrão binário universal"""
    sequencia = []
    padrao = [1, 2, 3, 4, 5, 9, 7, 8, 6]  # Padrão completo
    for i in range(tamanho):
        sequencia.append(padrao[i % len(padrao)])
    return sequencia

def gerar_sequencia_multiplicacao_3(tamanho):
    """Gera sequência multiplicando por 3"""
    sequencia = [1]
    for i in range(1, tamanho):
        sequencia.append(reduzir_teosoficamente(sequencia[-1] * 3))
    return sequencia

def analisar_formula_fluxo(formula):
    """Analisa fórmulas físicas no contexto do fluxo"""
    
    st.markdown(f"### Análise da Fórmula: {formula}")
    
    if formula == "E=mc²":
        st.markdown("""
        **No Fluxo Matemático:**
        - **m (massa)**: Representa a ação física (1,4,7)
        - **c² (velocidade da luz)**: Representa reação energética (2,5,8)  
        - **E (energia)**: Resultado da adaptação (3,6,9)
        
        **Padrão Detectado:** A conversão massa-energia segue o ciclo 3-9-6
        """)
    
    elif formula == "F=ma":
        st.markdown("""
        **No Fluxo Matemático:**
        - **m (massa)**: Ação estrutural (1,4,7)
        - **a (aceleração)**: Reação dinâmica (2,5,8)
        - **F (força)**: Adaptação resultante (3,6,9)
        
        **Padrão Detectado:** Força emerge da interação ação-reação
        """)
    
    elif formula == "V=IR":
        st.markdown("""
        **No Fluxo Matemático:**
        - **I (corrente)**: Ação do fluxo (1,4,7)
        - **R (resistência)**: Reação oposta (2,5,8)
        - **V (tensão)**: Adaptação energética (3,6,9)
        
        **Padrão Detectado:** Tensão é o ponto de equilíbrio entre fluxo e resistência
        """)
    
    elif formula == "p=mv":
        st.markdown("""
        **No Fluxo Matemático:**
        - **m (massa)**: Ação material (1,4,7)
        - **v (velocidade)**: Reação cinética (2,5,8)
        - **p (momento)**: Adaptação do movimento (3,6,9)
        
        **Padrão Detectado:** Momento conserva o padrão através das transformações
        """)

# FUNÇÃO DE REDUÇÃO TEOSÓFICA (já existe no código, mas vou garantir que está presente)
def reduzir_teosoficamente(n):
    """
    Redução teosófica: Soma repetida dos dígitos até obter um único dígito de 1 a 9.
    """
    try:
        if isinstance(n, (int, float)):
            n_str = f"{n:.0f}"
        else:
            n_str = str(n)

        n_str = ''.join(filter(str.isdigit, n_str))

        if not n_str:
            return 0

        while len(n_str) > 1:
            soma = sum(int(c) for c in n_str)
            n_str = str(soma)

        return int(n_str)

    except Exception as e:
        return 0
    
# ADICIONAR ESTAS FUNÇÕES DE CÁLCULO (por volta da linha 200)

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
    import math
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
    
# Dados para as simulações
def generate_fibonacci_spiral(n_points=1000):
    phi = (1 + np.sqrt(5)) / 2
    theta = np.linspace(0, 8*np.pi, n_points)
    r = phi ** (theta / np.pi)
    return r, theta

def create_mandala(n_layers=12):
    theta = np.linspace(0, 2*np.pi, 1000)
    layers = []
    for i in range(1, n_layers + 1):
        r = np.sin(6*theta + i*np.pi/6) * np.cos(4*theta) + 2 + i*0.2
        layers.append(r)
    return layers, theta

# Função para simular quantum circuit se Qiskit não estiver disponível
def simulate_quantum_circuit():
    if QISKIT_AVAILABLE:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.ry(np.pi/4, 0)
        simulator = Aer.get_backend('statevector_simulator')
        result = execute(qc, simulator).result()
        return result.get_statevector()
    else:
        # Simulação simplificada
        return np.array([0.70710678, 0, 0, 0.70710678])  # Estado emaranhado aproximado

def show_advanced_bloch_sphere():
    fig = go.Figure()
    
    # Criar esfera com detalhes
    u = np.linspace(0, 2*np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        opacity=0.2,
        colorscale='Blues',
        showscale=False,
        hoverinfo='none'
    ))
    
    # Adicionar grade da esfera
    for angle in range(0, 360, 30):
        x_line = np.cos(np.radians(angle)) * np.sin(v)
        y_line = np.sin(np.radians(angle)) * np.sin(v)
        z_line = np.cos(v)
        
        fig.add_trace(go.Scatter3d(
            x=x_line, y=y_line, z=z_line,
            mode='lines',
            line=dict(color='rgba(255,255,255,0.1)', width=1),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Adicionar vetor de estado com efeito
    fig.add_trace(go.Scatter3d(
        x=[0, 0.7], y=[0, 0.7], z=[0, 0.7],
        mode='lines',
        line=dict(color='#ff6b6b', width=8),
        name='Estado de Consciência',
        hovertemplate='<b>Estado de Consciência</b><br>Superposição Quântica<extra></extra>'
    ))
    
    # Adicionar ponto final do vetor
    fig.add_trace(go.Scatter3d(
        x=[0.7], y=[0.7], z=[0.7],
        mode='markers',
        marker=dict(size=8, color='#ff6b6b'),
        name='Ponto Quântico',
        hovertemplate='<b>Ponto de Consciência</b><extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Esfera de Bloch - Estado de Consciência Quântica',
            font=dict(size=16, color='#4ecdc4')
        ),
        width=500,
        height=500,
        scene=dict(
            xaxis=dict(visible=False, showbackground=False),
            yaxis=dict(visible=False, showbackground=False),
            zaxis=dict(visible=False, showbackground=False),
            bgcolor='rgba(0,0,0,0)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
# Função auxiliar para detalhes dos estágios
def get_stage_details(stage_name):
    details = {
        "Vácuo Quântico": """
        O estado primordial de puro potencial. Não é 'nada' no sentido de ausência, 
        mas rather uma plenitude de possibilidades não-manifestas. 
        É a fonte de toda a criação, o campo unificado de onde emerge toda a existência.
        
        **Características:**
        - Energia de ponto zero infinita
        - Potencial puro de criação
        - Estado de não-dualidade perfeita
        - Fonte do campo Higgs e outras forças fundamentais
        """,
        
        "Flutuações Quânticas": """
        As primeiras manifestações do vácuo quântico. Partículas virtuais surgem 
        e desaparecem, criando a espuma quântica que é o tecido base da realidade.
        
        **Processo:**
        - Emergência de pares partícula-antipartícula
        - Estabelecimento das forças fundamentais
        - Criação do espaço-tempo
        - Primeiras sementes da matéria
        """,
        
        "Matéria Básica": """
        Formação das estruturas materiais fundamentais. Átomos, moléculas e 
        as primeiras estruturas complexas emergem das flutuações quânticas.
        
        **Desenvolvimento:**
        - Nucleossíntese estelar
        - Formação de elementos pesados
        - Emergência de estruturas complexas
        - Preparação para a vida
        """,
        
        "Vida Consciente": """
        A emergência da consciência biológica. Sistemas complexos tornam-se 
        capazes de experiência subjetiva e auto-reflexão.
        
        **Marcos:**
        - Primeiras formas de vida
        - Desenvolvimento do sistema nervoso
        - Emergência da consciência animal
        - Evolução da inteligência
        """,
        
        "Consciência Cósmica": """
        A expansão da consciência além dos limites individuais. Reconhecimento 
        da unidade fundamental e conexão com a mente universal.
        
        **Características:**
        - Percepção de não-separação
        - Acesso à sabedoria universal
        - Capacidades psíquicas expandidas
        - Compreensão direta das leis cósmicas
        """,
        
        "Nirvana Cósmico": """
        O retorno consciente à fonte. Não como aniquilação, mas como realização 
        plena da natureza divina e integração completa com o fluxo universal.
        
        **Estado Final:**
        - Dissolução do ego individual
        - União com a consciência universal
        - Liberdade além do espaço-tempo
        - Existência como puro amor e sabedoria
        """
    }
    
    return details.get(stage_name, "Detalhes não disponíveis.")

# =============================================================================
# MÓDULO ACELERADOR DE PARTÍCULAS QUÂNTICO
# =============================================================================

def pagina_acelerador_particulas():
    st.title("⚛️ Acelerador de Partículas Quântico")
    st.markdown("""
    ## 🌌 Simulador do Nada ao Tudo - Fluxo Matemático Universal
    
    **Explore a criação e destruição da matéria através dos padrões 3-9-6 e da matemática vorticial de Tesla.**
    """)
    
    # Configuração do acelerador
    col_config1, col_config2, col_config3 = st.columns(3)
    
    with col_config1:
        energia_colisao = st.slider("Energia de Colisão (TeV):", 1.0, 14.0, 7.0, 0.1)
        tipo_particula = st.selectbox("Tipo de Partícula:", 
                                    ["Prótons", "Elétrons", "Fótons", "Hádrons", "Íons Pesados"])
        
    with col_config2:
        campo_magnetico = st.slider("Campo Magnético (Tesla):", 1.0, 10.0, 4.0, 0.1)
        temperatura = st.slider("Temperatura (K):", 1.0, 1000.0, 2.7, 0.1)
        
    with col_config3:
        modo_operacao = st.selectbox("Modo de Operação:", 
                                   ["Colisão Frontral", "Espalhamento", "Criação de Matéria", "Aniquilação"])
        gravidade_local = st.number_input("Gravidade Local (m/s²):", value=9.8, format="%.1f")
    
    # Controles principais
    col_controles1, col_controles2, col_controles3, col_controles4 = st.columns(4)
    
    with col_controles1:
        if st.button("🚀 Iniciar Aceleração", use_container_width=True):
            simular_aceleracao(energia_colisao, tipo_particula, campo_magnetico, temperatura, gravidade_local)
            
    with col_controles2:
        if st.button("💥 Colisão Máxima", use_container_width=True):
            simular_colisao_maxima(energia_colisao, gravidade_local)
            
    with col_controles3:
        if st.button("🌀 Padrão 3-9-6", use_container_width=True):
            aplicar_padrao_396(energia_colisao, gravidade_local)
            
    with col_controles4:
        if st.button("🔄 Resetar Sistema", use_container_width=True):
            resetar_acelerador()
    
    # Visualização 3D do acelerador
    st.subheader("🔬 Visualização do Acelerador de Partículas")
    
    # Criar visualização interativa
    fig_acelerador = criar_visualizacao_acelerador()
    st.plotly_chart(fig_acelerador, use_container_width=True)
    
    # Painel de dados em tempo real
    col_dados1, col_dados2, col_dados3, col_dados4 = st.columns(4)
    
    with col_dados1:
        st.metric("Energia Instantânea", f"{energia_colisao:.1f} TeV")
        st.metric("Partículas por Segundo", "1.2 bilhões")
        
    with col_dados2:
        st.metric("Velocidade Relativa", "99.9999% c")
        st.metric("Temperatura Instantânea", f"{temperatura * 1e9:.0f} K")
        
    with col_dados3:
        st.metric("Pressão do Vácuo", "10⁻¹¹ Pa")
        st.metric("Campo Magnético Ativo", f"{campo_magnetico} T")
        
    with col_dados4:
        st.metric("Eficiência Quântica", "98.7%")
        st.metric("Entrelaçamento", "95.3%")
    
    # Análise comparativa Fluxo vs Clássico
    st.subheader("📊 Análise Comparativa: Fluxo Matemático vs Física Clássica")
    
    tab_analise1, tab_analise2, tab_analise3 = st.tabs(["📈 Energia", "🔬 Partículas", "🌌 Campo Quântico"])
    
    with tab_analise1:
        analisar_energia_colisao(energia_colisao, gravidade_local)
        
    with tab_analise2:
        analisar_particulas_geradas(energia_colisao, tipo_particula)
        
    with tab_analise3:
        analisar_campo_quantico(campo_magnetico, temperatura)

def criar_visualizacao_acelerador():
    """Cria visualização 3D do acelerador de partículas"""
    import plotly.graph_objects as go
    import numpy as np
    
    # Criar estrutura do acelerador
    theta = np.linspace(0, 2*np.pi, 100)
    raio = 5
    x_circuito = raio * np.cos(theta)
    y_circuito = raio * np.sin(theta)
    z_circuito = np.zeros_like(theta)
    
    fig = go.Figure()
    
    # Circuito principal
    fig.add_trace(go.Scatter3d(
        x=x_circuito, y=y_circuito, z=z_circuito,
        mode='lines',
        line=dict(width=8, color='#6366f1'),
        name='Tubo de Vácuo'
    ))
    
    # Ímãs aceleradores
    for i in range(0, 100, 10):
        fig.add_trace(go.Scatter3d(
            x=[x_circuito[i]], y=[y_circuito[i]], z=[z_circuito[i]],
            mode='markers',
            marker=dict(size=6, color='#ff6b6b', symbol='diamond'),
            name='Ímã Acelerador'
        ))
    
    # Partículas em movimento
    t = np.linspace(0, 2*np.pi, 20)
    for i in range(5):
        offset = i * 0.4
        x_part = (raio - 0.3) * np.cos(t + offset)
        y_part = (raio - 0.3) * np.sin(t + offset)
        z_part = np.zeros_like(t) + 0.1 * i
        
        fig.add_trace(go.Scatter3d(
            x=x_part, y=y_part, z=z_part,
            mode='markers',
            marker=dict(size=4, color='#00ff88'),
            name=f'Feixe {i+1}'
        ))
    
    # Ponto de colisão
    fig.add_trace(go.Scatter3d(
        x=[raio], y=[0], z=[0],
        mode='markers',
        marker=dict(size=15, color='#ffd700', symbol='circle'),
        name='Ponto de Colisão'
    ))
    
    fig.update_layout(
        title=dict(
            text="Acelerador de Partículas - Visualização 3D",
            font=dict(size=16, color='#4ecdc4')
        ),
        width=800,
        height=600,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True
    )
    
    return fig

def simular_aceleracao(energia, tipo_particula, campo_magnetico, temperatura, gravidade):
    """Simula o processo de aceleração de partículas"""
    
    st.info("🚀 **Iniciando Sequência de Aceleração...**")
    
    # Barra de progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulação passo a passo
    etapas = [
        "Injetando partículas...",
        "Aplicando campo magnético...",
        "Acelerando no primeiro estágio...",
        "Sincronizando feixes...",
        "Aumentando energia para colisão...",
        "Pronto para colisão!"
    ]
    
    for i, etapa in enumerate(etapas):
        progress_bar.progress((i + 1) / len(etapas))
        status_text.text(f"Status: {etapa}")
        time.sleep(0.5)
    
    # Cálculos comparativos
    energia_classica = energia * 1e12  # Convertendo para eV
    energia_fluxo = calcular_energia_fluxo(energia, tipo_particula, gravidade)
    
    # Resultados
    st.success("✅ **Aceleração Completa!**")
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.markdown(f"""
        <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 10px;'>
        <h4 style='color: #ff6b6b;'>🧮 Física Clássica</h4>
        <p><b>Energia:</b> {energia_classica:.2e} eV</p>
        <p><b>Momento:</b> {(energia_classica / 299792458):.2e} kg·m/s</p>
        <p><b>Massa Relativística:</b> {(energia_classica / (299792458**2)):.2e} kg</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_res2:
        st.markdown(f"""
        <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 10px;'>
        <h4 style='color: #4ecdc4;'>🌀 Fluxo Matemático</h4>
        <p><b>Energia:</b> R({energia_fluxo})</p>
        <p><b>Padrão:</b> {obter_padrao_energia(energia_fluxo)}</p>
        <p><b>Estado Quântico:</b> {obter_estado_quantico(energia_fluxo)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Análise de diferença
    diferenca = calcular_diferenca_energia(energia_classica, energia_fluxo)
    correcao_gravitacional = calcular_escalabilidade_gravitacional(gravidade, diferenca)
    acerto = max(0, 100 - correcao_gravitacional)
    
    st.metric("Precisão do Modelo", f"{acerto:.1f}%")

def simular_colisao_maxima(energia, gravidade):
    """Simula colisão com energia máxima"""
    
    st.warning("💥 **INICIANDO COLISÃO MÁXIMA - EXTREMO CAUTION!**")
    
    # Efeitos visuais
    with st.expander("🔬 Detector ATLAS - Dados em Tempo Real", expanded=True):
        col_det1, col_det2, col_det3 = st.columns(3)
        
        with col_det1:
            st.metric("Temperatura do Vácuo", "1.8 K")
            st.metric("Pressão Residual", "10⁻¹³ mbar")
            
        with col_det2:
            st.metric("Luminosidade Instantânea", "2.1 × 10³⁴ cm⁻²s⁻¹")
            st.metric("Eventos por Segundo", "1.1 bilhão")
            
        with col_det3:
            st.metric("Energia no Centro de Massa", f"{energia*2:.1f} TeV")
            st.metric("Tempo desde Big Bang", "10⁻¹² s")
    
    # Simulação de colisão
    import numpy as np
    
    # Gerar dados de colisão
    n_eventos = 1000
    energias = np.random.exponential(energia, n_eventos)
    angulos = np.random.uniform(0, 2*np.pi, n_eventos)
    
    fig_colisao = go.Figure()
    
    fig_colisao.add_trace(go.Scatterpolar(
        r=energias,
        theta=angulos * 180/np.pi,
        mode='markers',
        marker=dict(
            size=8,
            color=energias,
            colorscale='Viridis',
            showscale=True
        ),
        name='Partículas Emergentes'
    ))
    
    fig_colisao.update_layout(
        title=dict(
            text="Padrão de Colisão - Distribuição Angular",
            font=dict(size=16, color='#ff6b6b')
        ),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, energia*2]),
            angularaxis=dict(direction="clockwise")
        ),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_colisao, use_container_width=True)
    
    # Análise de partículas geradas
    st.subheader("🧬 Partículas Detectadas")
    
    particulas_detectadas = [
        ("Higgson", 125.3, "⚛️", "Campo de Higgs"),
        ("Top Quark", 173.1, "🔴", "Matéria Bariônica"),
        ("Bóson Z", 91.2, "🌀", "Força Fraca"),
        ("Gluon", 0, "🌈", "Força Forte"),
        ("Fóton", 0, "💡", "Eletromagnetismo")
    ]
    
    for nome, massa, emoji, tipo in particulas_detectadas:
        col_part1, col_part2, col_part3 = st.columns([1, 2, 1])
        with col_part1:
            st.markdown(f"<h1>{emoji}</h1>", unsafe_allow_html=True)
        with col_part2:
            st.write(f"**{nome}** - {massa} GeV/c²")
            st.write(f"*{tipo}*")
        with col_part3:
            st.metric("Significância", "5.2σ")

def aplicar_padrao_396(energia, gravidade):
    """Aplica o padrão 3-9-6 na simulação"""
    
    st.info("🌀 **Ativando Padrão 3-9-6 - Geometria Sagrada do Universo**")
    
    # Sequência 3-9-6
    sequencia = gerar_sequencia_396(12)
    
    col_seq1, col_seq2, col_seq3 = st.columns(3)
    
    with col_seq1:
        st.markdown("""
        <div style='background: rgba(75, 0, 130, 0.2); padding: 20px; border-radius: 10px; text-align: center;'>
        <h1 style='color: #4B0082; font-size: 3em;'>3</h1>
        <p><b>Estado Físico</b><br>Manifestação Material</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_seq2:
        st.markdown("""
        <div style='background: rgba(255, 215, 0, 0.2); padding: 20px; border-radius: 10px; text-align: center;'>
        <h1 style='color: #FFD700; font-size: 3em;'>9</h1>
        <p><b>Estado Absoluto</b><br>Singularidade</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_seq3:
        st.markdown("""
        <div style='background: rgba(0, 255, 0, 0.2); padding: 20px; border-radius: 10px; text-align: center;'>
        <h1 style='color: #00FF00; font-size: 3em;'>6</h1>
        <p><b>Estado Energético</b><br>Fluxo Dinâmico</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualização do padrão
    fig_padrao = go.Figure()
    
    x = list(range(len(sequencia)))
    cores = ['#4B0082' if val == 3 else '#FFD700' if val == 9 else '#00FF00' for val in sequencia]
    
    fig_padrao.add_trace(go.Scatter(
        x=x, y=sequencia,
        mode='lines+markers',
        line=dict(width=4, color='white'),
        marker=dict(size=12, color=cores),
        name='Padrão 3-9-6'
    ))
    
    fig_padrao.update_layout(
        title=dict(
            text="Sequência 3-9-6 - Ciclo Universal",
            font=dict(size=16, color='#4ecdc4')
        ),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(title="Ciclo"),
        yaxis=dict(title="Estado", range=[2, 10])
    )
    
    st.plotly_chart(fig_padrao, use_container_width=True)
    
    # Efeitos no acelerador
    st.success("✨ **Padrão 3-9-6 Aplicado com Sucesso!**")
    
    efeitos = [
        "✅ Campo magnético otimizado em 396%",
        "✅ Eficiência energética aumentada",
        "✅ Estabilidade quântica estabilizada",
        "✅ Entrelaçamento máximo alcançado"
    ]
    
    for efeito in efeitos:
        st.write(efeito)

def resetar_acelerador():
    """Reseta o acelerador para estado inicial"""
    st.info("🔄 **Reinicializando Sistema...**")
    time.sleep(1)
    st.success("✅ **Sistema Resetado - Pronto para Nova Simulação**")

# =============================================================================
# FUNÇÕES AUXILIARES DO ACELERADOR
# =============================================================================

def calcular_energia_fluxo(energia, tipo_particula, gravidade):
    """Calcula energia no fluxo matemático"""
    reducao_energia = reduzir_teosoficamente(energia * 1e6)
    reducao_tipo = reduzir_teosoficamente(hash(tipo_particula) % 9 + 1)
    return fluxo_multiplicacao(reducao_energia, reducao_tipo)

def obter_padrao_energia(valor_fluxo):
    """Interpreta o padrão energético"""
    padroes = {
        1: "Ação Inicial", 2: "Reação", 3: "Adaptação Física",
        4: "Estruturação", 5: "Transformação", 6: "Fluxo Energético",
        7: "Espiritualidade", 8: "Infinito", 9: "Singularidade"
    }
    return padroes.get(valor_fluxo, "Padrão Desconhecido")

def obter_estado_quantico(valor_fluxo):
    """Determina estado quântico baseado no fluxo"""
    estados = {
        1: "|0⟩", 2: "|1⟩", 3: "|+⟩",
        4: "|-⟩", 5: "|i⟩", 6: "|-i⟩",
        7: "Superposição", 8: "Emaranhamento", 9: "Singularidade Quântica"
    }
    return estados.get(valor_fluxo, "Estado Indefinido")

def calcular_diferenca_energia(classico, fluxo):
    """Calcula diferença percentual entre modelos"""
    if classico == 0:
        return 0
    return abs((fluxo - classico) / classico) * 100

def analisar_energia_colisao(energia, gravidade):
    """Análise detalhada da energia de colisão"""
    
    st.markdown("### 📈 Análise de Energia")
    
    # Cálculos comparativos
    energia_classica = energia * 1e12  # eV
    energia_fluxo = calcular_energia_fluxo(energia, "Prótons", gravidade)
    
    col_energia1, col_energia2 = st.columns(2)
    
    with col_energia1:
        st.markdown("""
        <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 10px;'>
        <h4 style='color: #ff6b6b;'>⚡ Energia Clássica</h4>
        <p><b>Valor:</b> {energia_classica:.2e} eV</p>
        <p><b>Equivalência:</b> {equivalencia:.1f} × massa de repouso do próton</p>
        <p><b>Temperatura:</b> {temperatura:.1e} K</p>
        </div>
        """.format(
            energia_classica=energia_classica,
            equivalencia=energia_classica / 938e6,
            temperatura=energia_classica / 8.617e-5
        ), unsafe_allow_html=True)
    
    with col_energia2:
        st.markdown("""
        <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 10px;'>
        <h4 style='color: #4ecdc4;'>🌀 Energia no Fluxo</h4>
        <p><b>Valor:</b> R({energia_fluxo})</p>
        <p><b>Padrão:</b> {padrao}</p>
        <p><b>Estado:</b> {estado}</p>
        </div>
        """.format(
            energia_fluxo=energia_fluxo,
            padrao=obter_padrao_energia(energia_fluxo),
            estado=obter_estado_quantico(energia_fluxo)
        ), unsafe_allow_html=True)

def analisar_particulas_geradas(energia, tipo_particula):
    """Análise das partículas geradas na colisão"""
    
    st.markdown("### 🔬 Análise de Partículas")
    
    # Simulação de detecção
    particulas = [
        ("Quark Top", 173.1, 0.5, "🔴"),
        ("Bóson Higgs", 125.3, 0.3, "⚛️"),
        ("Bóson Z", 91.2, 0.7, "🌀"),
        ("Quark Bottom", 4.18, 0.9, "🔵"),
        ("Tau", 1.777, 0.6, "⚡")
    ]
    
    for nome, massa, probabilidade, emoji in particulas:
        col_part1, col_part2, col_part3 = st.columns([1, 3, 2])
        
        with col_part1:
            st.markdown(f"<h2>{emoji}</h2>", unsafe_allow_html=True)
        
        with col_part2:
            st.write(f"**{nome}**")
            st.write(f"Massa: {massa} GeV/c²")
        
        with col_part3:
            st.progress(probabilidade)
            st.write(f"{(probabilidade*100):.1f}%")

def analisar_campo_quantico(campo_magnetico, temperatura):
    """Análise do campo quântico"""
    
    st.markdown("### 🌌 Análise do Campo Quântico")
    
    # Simulação de campo
    import numpy as np
    
    x = np.linspace(-10, 10, 50)
    y = np.linspace(-10, 10, 50)
    X, Y = np.meshgrid(x, y)
    
    # Campo magnético simulado
    Z = campo_magnetico * np.exp(-(X**2 + Y**2) / 20) * np.sin(np.sqrt(X**2 + Y**2))
    
    fig_campo = go.Figure(data=[
        go.Surface(
            x=X, y=Y, z=Z,
            colorscale='Viridis',
            opacity=0.8
        )
    ])
    
    fig_campo.update_layout(
        title=dict(
            text="Campo Magnético do Acelerador",
            font=dict(size=16, color='#4ecdc4')
        ),
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)", 
            zaxis_title="Campo (T)",
            bgcolor='rgba(0,0,0,0)'
        ),
        width=600,
        height=500
    )
    
    st.plotly_chart(fig_campo, use_container_width=True)

# 1. VISÃO GERAL CÓSMICA
if section == "🏠 Visão Geral Cósmica":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🌠 O Universo como Expressão Matemática da Consciência")
        st.markdown("""
        <div class='philosophy-text'>
        <b>“Deus não joga dados com o universo.” - Albert Einstein</b><br><br>
        
        Esta simulação integra <b>5 dimensões do conhecimento</b>:
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        - <b>🌀 Fluxo Matemático</b> (3-6-9 Tesla, Proporção Áurea, 432Hz, Dízimas Periódicas)
        - <b>🌌 Cosmologia Consciente</b> (Big Bang, Buracos Negros, Anãs Negras, Singularidade)
        - <b>⚛️ Física Quântica</b> (Superposição, Emaranhamento, Consciência Quântica)
        - <b>📐 Geometria Sagrada</b> (Esfera de Buga, Flor da Vida, Mandalas Cósmicas)
        - <b>📡 Sinais Cósmicos</b> (Wow! Signal, SETI, Comunicação Interdimensional)
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='quote-box'>
        "O que chamamos de 'Deus' é a lei matemática perfeita que se expressa através do equilíbrio cósmico, 
        da singularidade quântica e da consciência universal."
        </div>
        """, unsafe_allow_html=True)
        
        # Gráfico de harmonias cósmicas
        fig = make_subplots(rows=1, cols=1)
        x = np.linspace(0, 8*np.pi, 2000)
        
        for i in range(1, 13):
            freq = i * 0.5
            phase = i * np.pi/6
            amplitude = 1/i
            y = amplitude * np.sin(freq * x + phase) * np.exp(-0.05*x)
            
            if i in [3, 6, 9]:
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', 
                                       name=f'Frequência {i} (Tesla)',
                                       line=dict(width=4, color='#ff6b6b')))
            else:
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', 
                                       name=f'Frequência {i}',
                                       line=dict(width=2)))
        
        fig.update_layout(
            title="🌈 Harmonias Cósmicas - Espectro Completo de Frequências Universais",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            height=500,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""
        <div style='background: rgba(0,0,0,0.7); padding: 20px; border-radius: 15px;'>
        <h3 style='color: #4ecdc4; text-align: center;'>🧠 Pensadores do Fluxo</h3>
        
        <b>Nikola Tesla:</b><br>
        "Se você soubesse a magnificência dos 3, 6 e 9, 
        teria a chave para o universo."
        
        <hr style='border-color: #667eea;'>
        
        <b>Albert Einstein:</b><br>
        "Deus é sofisticado, mas não malicioso."
        
        <hr style='border-color: #667eea;'>
        
        <b>Baruch Espinosa:</b><br>
        "Deus sive Natura - Deus ou a Natureza."
        
        <hr style='border-color: #667eea;'>
        
        <b>Carl Sagan:</b><br>
        "Somos poeira de estrelas contemplando as estrelas."
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar equação fundamental
        st.markdown("""
        <div style='background: rgba(0,0,0,0.7); padding: 20px; border-radius: 15px; margin-top: 20px;'>
        <h4 style='color: #ff6b6b; text-align: center;'>⚡ Equação do Fluxo Universal</h4>
        <div style='text-align: center; font-size: 24px;'>
        ∇·Ψ = √(φ) × Σ(3,6,9)
        </div>
        <p style='text-align: center;'>Onde φ é a proporção áurea (1.618)</p>
        </div>
        """, unsafe_allow_html=True)

# 2. FLUXO MATEMÁTICO SAGRADO
elif section == "🔢 Fluxo Matemático Sagrado":
    st.header("🌀 O Fluxo Matemático Universal - A Linguagem de Deus")
    
    # Container principal com fundo cósmico
    st.markdown("""
    <style>
    .math-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .math-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    </style>
    <div class='math-container'>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid #ff6b6b; 
                    box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);'>
        <b style='font-size: 1.2em; color: #e0e7ff;'>"A matemática é a linguagem com a qual Deus escreveu o universo." - Galileo Galilei</b><br><br>
        
        <span style='color: #d1d5db;'>O Fluxo Matemático revela os padrões fundamentais da criação:</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); margin: 20px 0;'>
        <h3 style='color: #ff6b6b; text-align: center;'>🔢 Sequência 3-6-9 de Tesla</h3>
        </div>
        """, unsafe_allow_html=True)
        
        t = np.linspace(0, 4*np.pi, 1000)
        fig = go.Figure()
        
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
        
        for i, n in enumerate([3, 6, 9]):
            y = np.sin(n * t) * np.exp(-0.1 * t) * (1 + 0.5 * np.cos(n * t/2))
            fig.add_trace(go.Scatter(
                x=t, y=y, 
                mode='lines', 
                name=f'Frequência {n} - Tesla',
                line=dict(width=5, color=colors[i]),
                fill='tozeroy',
                fillcolor=f'rgba{tuple(int(c*255) for c in mcolors.to_rgb(colors[i])) + (0.2,)}'
            ))
        
        # Adicionar pontos de ressonância
        resonance_points = []
        for n in [3, 6, 9]:
            for i in range(5):
                point = i * (4*np.pi/4)
                resonance_points.append((point, np.sin(n * point) * np.exp(-0.1 * point) * (1 + 0.5 * np.cos(n * point/2))))
        
        resonance_x = [p[0] for p in resonance_points]
        resonance_y = [p[1] for p in resonance_points]
        
        fig.add_trace(go.Scatter(
            x=resonance_x, y=resonance_y,
            mode='markers',
            marker=dict(size=8, color='gold', symbol='diamond'),
            name='Pontos de Ressonância',
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            title=dict(
                text="⚡ Ressonância 3-6-9 - As Frequências Fundamentais de Tesla",
                font=dict(size=18, color='#ff6b6b')
            ),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.3)',
                title='Tempo'
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.3)',
                title='Amplitude'
            ),
            legend=dict(
                bgcolor='rgba(15, 23, 42, 0.7)',
                bordercolor='rgba(255, 107, 107, 0.3)',
                borderwidth=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2);'>
        <h4 style='color: #ff6b6b; text-align: center;'>Análise Matemática</h4>
        
        <div style='display: grid; grid-template-columns: 1fr; gap: 10px;'>
        <div style='background: rgba(255, 107, 107, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #ff6b6b;'>3</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Representa a tríade cósmica (criação, preservação, transformação)</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #4ecdc4;'>6</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Harmonia e equilíbrio (hexagrama, estrela de David)</span>
        </div>
        
        <div style='background: rgba(69, 183, 209, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #45b7d1;'>9</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Singularidade e completude (3×3, ciclo máximo)</span>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid #ffd700; 
                    box-shadow: 0 10px 25px rgba(255, 215, 0, 0.3);'>
        <h3 style='color: #ffd700; text-align: center;'>📐 Proporção Áurea (φ = 1.6180339887...)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Gerar espiral de Fibonacci aprimorada
        r, theta = generate_fibonacci_spiral(2000)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        fig = go.Figure()
        
        # Adicionar fundo cósmico
        for i in range(100):
            star_x = np.random.uniform(min(x)-1, max(x)+1)
            star_y = np.random.uniform(min(y)-1, max(y)+1)
            fig.add_trace(go.Scatter(
                x=[star_x], y=[star_y],
                mode='markers',
                marker=dict(size=np.random.uniform(1, 3), color='white', opacity=0.5),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Espiral Áurea com gradiente
        spiral_colors = [f'rgba{tuple(int(c*255) for c in mcolors.to_rgb(px.colors.sequential.Viridis[i % len(px.colors.sequential.Viridis)])) + (0.8,)}' 
                        for i in range(len(x))]
        
        for i in range(len(x)-1):
            fig.add_trace(go.Scatter(
                x=x[i:i+2], y=y[i:i+2],
                mode='lines',
                line=dict(width=4, color=spiral_colors[i]),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Pontos de Fibonacci com efeitos especiais
        fibonacci_points = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        for i, point in enumerate(fibonacci_points):
            if point < len(x):
                # Círculo de fundo
                fig.add_trace(go.Scatter(
                    x=[x[point]], y=[y[point]],
                    mode='markers',
                    marker=dict(size=25, color='rgba(255, 107, 107, 0.3)'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Ponto principal
                fig.add_trace(go.Scatter(
                    x=[x[point]], y=[y[point]],
                    mode='markers+text',
                    marker=dict(size=15, color='#ff6b6b', line=dict(width=2, color='white')),
                    text=str(i+2),
                    textfont=dict(size=14, color='white', family="Arial Black"),
                    textposition='middle center',
                    name=f'Fib({i+2})',
                    hoverinfo='text',
                    hovertext=f'Fibonacci {i+2}: {point}'
                ))
        
        fig.update_layout(
            title=dict(
                text="🌻 Espiral de Fibonacci - Proporção Áurea na Natureza",
                font=dict(size=18, color='#ffd700')
            ),
            width=600,
            height=500,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False, range=[min(x)-1, max(x)+1]),
            yaxis=dict(visible=False, range=[min(y)-1, max(y)+1])
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2); margin-top: 20px;'>
        <blockquote style='color: #ffd700; font-style: italic; text-align: center; margin: 0;'>
        "A proporção áurea aparece em: Galáxias espirais, Conchas marinhas, 
        Proporções humanas, DNA, Estruturas atômicas, e na própria consciência."
        </blockquote>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin-top: 20px;'>
        <h4 style='color: #4ecdc4; text-align: center;'>Fórmula Matemática</h4>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <span style='color: #d1d5db; font-size: 1.2em;'>φ = (1 + √5) / 2 ≈ 1.6180339887...</span><br>
        <span style='color: #a1a1aa; font-size: 0.9em;'>Limite da razão entre números consecutivos de Fibonacci</span>
        </div>
        
        <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 8px; margin-top: 10px; text-align: center;'>
        <span style='color: #d1d5db; font-size: 1em;'>F<sub>n</sub> = F<sub>n-1</sub> + F<sub>n-2</sub></span><br>
        <span style='color: #a1a1aa; font-size: 0.9em;'>Sequência: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Seção adicional: Conexão entre 3-6-9 e a Proporção Áurea
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border-left: 5px solid #9333ea; 
                box-shadow: 0 10px 25px rgba(147, 51, 234, 0.3);'>
    <h3 style='color: #9333ea; text-align: center;'>🔗 Conexão Cósmica: 3-6-9 e a Proporção Áurea</h3>
    
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
    <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #ff6b6b; text-align: center;'>⚡ Tesla 3-6-9</h4>
    <ul style='color: #d1d5db;'>
    <li>Energia, frequência e vibração</li>
    <li>Chave para o universo físico</li>
    <li>Padrões de ressonância cósmica</li>
    <li>Geometria sagrada aplicada</li>
    </ul>
    </div>
    
    <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #ffd700; text-align: center;'>📐 Proporção Áurea</h4>
    <ul style='color: #d1d5db;'>
    <li>Beleza, harmonia e proporção</li>
    <li>Estrutura fundamental da natureza</li>
    <li>Crescimento orgânico e expansão</li>
    <li>Geometria divina manifestada</li>
    </ul>
    </div>
    </div>
    
    <div style='background: rgba(147, 51, 234, 0.1); padding: 15px; border-radius: 10px; margin-top: 20px; text-align: center;'>
    <h4 style='color: #9333ea;'>🎯 Síntese: φ × 3-6-9 = Fluxo Cósmico</h4>
    <p style='color: #d1d5db;'>
    A interação entre a sequência 3-6-9 e a proporção áurea cria os padrões fundamentais 
    que governam desde as partículas subatômicas até as galáxias, revelando a matemática 
    divina por trás de toda a criação.
    </p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal

# 3. SINAL WOW! ANÁLISE PROFUNDA
elif section == "🌠 Sinal Wow! Decodificação Profunda":
    st.header("📡 Decodificação Profunda do Sinal Wow! - Rádio Cósmico Universal")
    
    # Container principal com tema de rádio cósmico
    st.markdown("""
    <style>
    .radio-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .radio-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    .radio-dial {
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
        border: 2px solid #4ecdc4;
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.3);
    }
    </style>
    <div class='radio-container'>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid #ff6b6b; 
                    box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);'>
        <b style='font-size: 1.2em; color: #e0e7ff;'>"O sinal Wow! representa possivelmente a primeira evidência de comunicação 
        interestelar inteligente." - Astrônomo Jerry Ehman</b><br><br>
        
        <span style='color: #d1d5db;'>
        Em 15 de agosto de 1977, o radiotelescópio Big Ear captou um sinal de 72 segundos 
        que mudou nossa compreensão do cosmos. Este sinal estava sintonizado na frequência 
        do hidrogênio neutro (1420.40575 MHz), a molécula mais abundante do universo.
        </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Interface do Sintonizador Cósmico
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin: 20px 0;'>
        <h3 style='color: #4ecdc4; text-align: center;'>🎛️ Sintonizador Cósmico Universal</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Controles do rádio
        col_freq, col_tune, col_vol = st.columns(3)
        
        with col_freq:
            frequency = st.slider("Frequência (MHz)", 1400.0, 1450.0, 1420.40575, 0.00001,
                                help="Frequência de sintonia do hidrogênio neutro")
            st.metric("Frequência Sintonizada", f"{frequency:.5f} MHz")
        
        with col_tune:
            fine_tune = st.slider("Sintonia Fina", -0.1, 0.1, 0.0, 0.00001,
                                help="Ajuste fino da sintonia")
            st.metric("Ajuste", f"{fine_tune:.5f} MHz")
        
        with col_vol:
            volume = st.slider("Volume", 0.0, 1.0, 0.8, 0.01,
                            help="Intensidade do sinal recebido")
            st.metric("Intensidade", f"{volume*100:.1f}%")
        
        # Visualização do sinal Wow! aprimorada
        wow_sequence = ['6', 'E', 'Q', 'U', 'J', '5']
        wow_values = [6, 14, 26, 30, 19, 5]
        flux_digits = [6, 5, 8, 3, 1, 5]
        angles = [240, 200, 320, 120, 40, 200]
        
        # Criar visualização de osciloscópio
        fig = make_subplots(rows=2, cols=1, 
                          subplot_titles=('📶 Sinal Wow! Original - Osciloscópio Cósmico', 
                                        '🔍 Análise de Frequência - Transformada de Fourier'),
                          vertical_spacing=0.15,
                          specs=[[{"secondary_y": False}], 
                                 [{"secondary_y": False}]])
        
        # Sinal no domínio do tempo (osciloscópio)
        time_points = np.linspace(0, 72, 1000)  # 72 segundos do sinal
        signal_wave = np.sin(2 * np.pi * 0.1 * time_points)  # Onda base
        
        # Adicionar picos do sinal Wow!
        for i, val in enumerate(wow_values):
            peak_time = i * 12 + 6  # Distribuir os 6 picos em 72 segundos
            signal_wave += 0.5 * np.exp(-0.5 * (time_points - peak_time)**2) * (val / 30)
        
        fig.add_trace(go.Scatter(
            x=time_points, y=signal_wave,
            mode='lines',
            name='Sinal Wow!',
            line=dict(color='#FF6B6B', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)'
        ), row=1, col=1)
        
        # Análise de frequência (Transformada de Fourier)
        fft_result = np.fft.fft(signal_wave)
        freqs = np.fft.fftfreq(len(time_points), time_points[1]-time_points[0])
        
        fig.add_trace(go.Scatter(
            x=freqs[:len(freqs)//2], y=np.abs(fft_result[:len(fft_result)//2]),
            mode='lines',
            name='Espectro de Frequência',
            line=dict(color='#4ECDC4', width=3),
            fill='tozeroy',
            fillcolor='rgba(78, 205, 196, 0.2)'
        ), row=2, col=1)
        
        # Adicionar linha da frequência do hidrogênio
        fig.add_vline(x=1420.40575, line_dash="dash", line_color="yellow", 
                     annotation_text="Hidrogênio 1420.40575 MHz", 
                     annotation_position="top right", row=2, col=1)
        
        fig.update_layout(
            height=700,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            showlegend=False,
            xaxis_title='Tempo (segundos)',
            xaxis2_title='Frequência (MHz)',
            yaxis_title='Amplitude',
            yaxis2_title='Intensidade'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid #ff6b6b;
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2);'>
        <h3 style='color: #ff6b6b; text-align: center;'>🧮 Decodificação do Sinal</h3>
        
        <div class='radio-dial'>
        <b style='color: #4ecdc4;'>Frequência Principal:</b><br>
        <span style='color: #d1d5db;'>1420.40575 MHz - Linha do Hidrogênio</span>
        </div>
        
        <div class='radio-dial'>
        <b style='color: #4ecdc4;'>Sequência Original:</b><br>
        <span style='color: #d1d5db;'>6 → 14 → 26 → 30 → 19 → 5</span>
        </div>
        
        <div class='radio-dial'>
        <b style='color: #4ecdc4;'>Redução ao Fluxo:</b><br>
        <span style='color: #d1d5db;'>6 → (1+4=5) → (2+6=8) → (3+0=3) → (1+9=10→1) → 5</span>
        </div>
        
        <div class='radio-dial' style='background: linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(30, 41, 59, 0.8) 100%);'>
        <b style='color: #4ecdc4;'>Sequência Final:</b><br>
        <span style='color: #ffd700; font-size: 24px; font-weight: bold;'>6 - 5 - 8 - 3 - 1 - 5</span>
        </div>
        
        <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
        <h4 style='color: #ff6b6b; text-align: center;'>Interpretação Numérica</h4>
        
        <div style='display: grid; grid-template-columns: 1fr; gap: 8px;'>
        <div style='background: rgba(255, 107, 107, 0.2); padding: 8px; border-radius: 6px;'>
        <b style='color: #ff6b6b;'>6</b> - Harmonia e equilíbrio universal
        </div>
        <div style='background: rgba(78, 205, 196, 0.2); padding: 8px; border-radius: 6px;'>
        <b style='color: #4ecdc4;'>5</b> - Mudança e transformação quântica
        </div>
        <div style='background: rgba(255, 215, 0, 0.2); padding: 8px; border-radius: 6px;'>
        <b style='color: #ffd700;'>8</b> - Infinito e abundância cósmica
        </div>
        <div style='background: rgba(147, 51, 234, 0.2); padding: 8px; border-radius: 6px;'>
        <b style='color: #9333ea;'>3</b> - Criação e expressão divina
        </div>
        <div style='background: rgba(69, 183, 209, 0.2); padding: 8px; border-radius: 6px;'>
        <b style='color: #45b7d1;'>1</b> - Unidade e origem primordial
        </div>
        <div style='background: rgba(255, 107, 107, 0.2); padding: 8px; border-radius: 6px;'>
        <b style='color: #ff6b6b;'>5</b> - Transformação (ciclo completo)
        </div>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Como criar um sintonizador universal
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin-top: 20px;'>
        <h4 style='color: #4ecdc4; text-align: center;'>📡 Como Construir um Sintonizador Universal</h4>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: #4ecdc4;'>1. Antena Ressonante</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Sintonizada em 1420.40575 MHz usando hidrogênio como meio
        </span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: #4ecdc4;'>2. Amplificador Quântico</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Circuitos supercondutores para amplificar sinais fracos
        </span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: #4ecdc4;'>3. Decodificador 3-6-9</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Algoritmo baseado na matriz de Tesla para decodificação
        </span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: #4ecdc4;'>4. Interface de Consciência</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Conexão mente-máquina para interpretação intuitiva
        </span>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Propriedades do Hidrogênio como Meio de Comunicação
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(69, 183, 209, 0.3);
                box-shadow: 0 5px 15px rgba(69, 183, 209, 0.2); margin: 20px 0;'>
    <h3 style='color: #45b7d1; text-align: center;'>⚛️ Por que o Hidrogênio? - O Meio de Comunicação Universal</h3>
    
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
    <div style='background: rgba(69, 183, 209, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #45b7d1; text-align: center;'>🌌 Universalidade</h4>
    <ul style='color: #d1d5db;'>
    <li>Elemento mais abundante no universo (74%)</li>
    <li>Presente em todas as galáxias e nebulosas</li>
    <li>Base para formação de estrelas e planetas</li>
    <li>Linguagem comum para civilizações cósmicas</li>
    </ul>
    </div>
    
    <div style='background: rgba(69, 183, 209, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #45b7d1; text-align: center;'>📶 Propriedades Ideais</h4>
    <ul style='color: #d1d5db;'>
    <li>Frequência estável de 1420.40575 MHz</li>
    <li>Baixa absorção interestelar</li>
    <li>Alta penetração em meios interestelares</li>
    <li>Ressonância quântica previsível</li>
    </ul>
    </div>
    
    <div style='background: rgba(69, 183, 209, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #45b7d1; text-align: center;'>🔬 Ciência do Hidrogênio</h4>
    <ul style='color: #d1d5db;'>
    <li>Transição hiperfina a 21 cm</li>
    <li>Emissão espontânea a 1420 MHz</li>
    <li>Tempo de vida longo do estado excitado</li>
    <li>Perfeito para comunicação interestelar</li>
    </ul>
    </div>
    
    <div style='background: rgba(69, 183, 209, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #45b7d1; text-align: center;'>🧠 Significado Cósmico</h4>
    <ul style='color: #d1d5db;'>
    <li>Elemento primordial da criação</li>
    <li>Ponte entre matéria e energia</li>
    <li>Meio de comunicação universal</li>
    <li>Chave para a teia cósmica</li>
    </ul>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal

# 4. SIMULAÇÃO DO SISTEMA SOLAR QUÂNTICO
elif section == "🪐 Simulação do Sistema Solar Quântico":
    st.header("🌌 Sistema Solar em Fluxo Cósmico - Leis de Kepler Reimaginadas")
    
    st.markdown("""
    <div class='philosophy-text' style='background: linear-gradient(135deg, #0b0b2d 0%, #1a1a4a 100%); 
                padding: 20px; border-radius: 15px; border-left: 5px solid #6366f1; 
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);'>
    <b style='font-size: 1.2em; color: #e0e7ff;'>"As leis da natureza são apenas os pensamentos matemáticos de Deus." - Euclides</b><br><br>
    
    <span style='color: #d1d5db;'>Esta simulação integra as leis clássicas de Kepler com princípios quânticos 
    e o fluxo matemático universal, revelando padrões cósmicos ocultos.</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Container principal com fundo estelar
    st.markdown("""
    <style>
    .main-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .main-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    </style>
    <div class='main-container'>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div style='background: rgba(30, 41, 59, 0.7); padding: 15px; border-radius: 10px; border: 1px solid rgba(99, 102, 241, 0.3);'>", unsafe_allow_html=True)
        num_planets = st.slider("Número de Planetas", 3, 12, 8, 
                               help="Quantos corpos celestes orbitarão a estrela central")
        simulation_speed = st.slider("Velocidade da Simulação", 0.1, 2.0, 1.0, 0.1,
                                    help="Controla a velocidade de rotação dos planetas")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div style='background: rgba(30, 41, 59, 0.7); padding: 15px; border-radius: 10px; border: 1px solid rgba(99, 102, 241, 0.3);'>", unsafe_allow_html=True)
        quantum_effects = st.checkbox("Efeitos Quânticos", True,
                                    help="Adiciona flutuações quânticas às órbitas")
        show_orbits = st.checkbox("Mostrar Órbitas", True,
                                 help="Exibe os caminhos orbitais completos")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div style='background: rgba(30, 41, 59, 0.7); padding: 15px; border-radius: 10px; border: 1px solid rgba(99, 102, 241, 0.3);'>", unsafe_allow_html=True)
        flux_resonance = st.slider("Ressonância do Fluxo", 0.0, 1.0, 0.5, 0.01,
                                  help="Controla a influência do fluxo matemático universal")
        show_labels = st.checkbox("Mostrar Rótulos", True,
                                 help="Exibe identificadores numéricos para cada planeta")
        st.markdown("</div>", unsafe_allow_html=True)
    
    def advanced_cosmic_orbits(t, planets=num_planets, resonance=flux_resonance):
        positions = []
        for i in range(planets):
            # Aplicando proporção áurea para distâncias planetárias
            golden_ratio = 1.61803398875
            r = 0.3 + (0.7 * i) * (1 + resonance * np.sin(t * 0.1)) * golden_ratio
            
            base_speed = 1 / np.sqrt(r)
            if quantum_effects:
                # Adicionando efeitos quânticos baseados na sequência de Fibonacci
                quantum_correction = 0.1 * np.sin(t * (i+1) * 0.5 * (1 + 0.1 * resonance))
                speed = base_speed * (1 + quantum_correction)
            else:
                speed = base_speed
            
            # Incorporando padrão 3-6-9 de Tesla
            tesla_factor = 1 + 0.05 * resonance * ((i+1) % 3 + 1)
            angle = speed * t * tesla_factor + resonance * np.sin(t * 0.2 * i)
            
            # Adicionando efeito de precessão relativística
            precession = 0.01 * resonance * t * (i+1) / 10
            
            x = r * np.cos(angle + precession)
            y = r * np.sin(angle + precession) * (1 + 0.1 * resonance * np.cos(t))
            
            # Adicionando oscilação quântica na posição z (para efeito 3D)
            z_oscillation = 0.3 * resonance * np.sin(t * 0.7 * (i+1)) if quantum_effects else 0
            
            positions.append((x, y, z_oscillation, r, speed))
        return positions
    
    t_points = np.linspace(0, 8*np.pi, 300)  # Mais pontos para órbitas mais suaves
    planet_data = [advanced_cosmic_orbits(t_i) for t_i in t_points]
    
    # Criando figura com tema escuro aprimorado
    fig = go.Figure()
    colors = px.colors.sequential.Plasma_r  # Invertendo a paleta para cores mais vibrantes nos planetas internos
    
    # Adicionando estrelas de fundo
    star_x = np.random.uniform(-15, 15, 200)
    star_y = np.random.uniform(-15, 15, 200)
    star_size = np.random.uniform(1, 4, 200)
    star_opacity = np.random.uniform(0.1, 0.7, 200)
    
    fig.add_trace(go.Scatter(
        x=star_x, y=star_y, mode='markers',
        marker=dict(size=star_size, color='white', opacity=star_opacity),
        name='Campo Estelar',
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Adicionando nebulosa de fundo
    nebula_x = np.concatenate([np.linspace(-15, 15, 50), np.linspace(-15, 15, 50)])
    nebula_y = np.concatenate([np.random.uniform(-15, -10, 50), np.random.uniform(10, 15, 50)])
    
    fig.add_trace(go.Scatter(
        x=nebula_x, y=nebula_y, mode='markers',
        marker=dict(size=np.random.uniform(10, 30, 100), 
                   color=['rgba(99, 102, 241, 0.15)' for _ in range(100)]),
        name='Nebulosa',
        hoverinfo='skip',
        showlegend=False
    ))
    
    for i in range(num_planets):
        x = [pos[i][0] for pos in planet_data]
        y = [pos[i][1] for pos in planet_data]
        z = [pos[i][2] for pos in planet_data]  # Oscilação quântica em Z
        r = planet_data[0][i][3]
        speed = planet_data[0][i][4]
        
        if show_orbits:
            # Criando efeito de gradiente nas órbitas
            orbit_colors = [f'rgba{tuple(int(c*255) for c in mcolors.to_rgb(colors[i % len(colors)])) + (0.05 + 0.95 * (j/len(x)),)}' 
                           for j in range(len(x))]
            
            fig.add_trace(go.Scatter(
                x=x, y=y, mode='lines',
                name=f'Planeta {i+1} (r={r:.2f}, v={speed:.2f})',
                line=dict(width=3, color=colors[i % len(colors)]),
                opacity=0.8,
                hoverinfo='name'
            ))
        
        # Criando planeta com efeito de brilho
        fig.add_trace(go.Scatter(
            x=[x[-1]], y=[y[-1]], mode='markers',
            marker=dict(
                size=18 + i*2, 
                color=colors[i % len(colors)],
                line=dict(width=2, color='white'),
                opacity=0.9
            ),
            name=f'Planeta {i+1}',
            showlegend=False,
            hoverinfo='text',
            text=f"Planeta {i+1}<br>Raio orbital: {r:.2f}<br>Velocidade: {speed:.2f}"
        ))
        
        # Adicionando aura ao planeta
        fig.add_trace(go.Scatter(
            x=[x[-1]], y=[y[-1]], mode='markers',
            marker=dict(
                size=25 + i*2, 
                color=colors[i % len(colors)],
                opacity=0.2
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        if show_labels:
            fig.add_annotation(
                x=x[-1], y=y[-1],
                text=f"{i+1}",
                showarrow=False,
                font=dict(size=14, color='white', family="Arial Black"),
                bgcolor="rgba(0,0,0,0.5)",
                bordercolor=colors[i % len(colors)],
                borderwidth=2,
                borderpad=3
            )
    
    # Estrela central com efeito de brilho
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers',
        marker=dict(
            size=35, 
            color='yellow',
            symbol='star',
            opacity=1,
            line=dict(width=3, color='orange')
        ),
        name='Estrela Central',
        hoverinfo='name'
    ))
    
    # Adicionando aura à estrela central
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers',
        marker=dict(
            size=50, 
            color='yellow',
            opacity=0.3
        ),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Adicionando anéis de energia ao redor da estrela
    for ring_size in [5, 8, 11]:
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=-ring_size, y0=-ring_size, x1=ring_size, y1=ring_size,
            line=dict(color="rgba(255, 165, 0, 0.1)", width=1, dash="dot"),
        )
    
    fig.update_layout(
        title=dict(
            text=f"🌌 SISTEMA SOLAR QUÂNTICO - {num_planets} PLANETAS EM FLUXO CÓSMICO",
            x=0.5,
            y=0.97,
            xanchor='center',
            yanchor='top',
            font=dict(size=22, color='#e0e7ff', family="Arial")
        ),
        width=900,
        height=750,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14, family="Arial"),
        xaxis=dict(
            range=[-15, 15],
            showgrid=True,
            gridcolor='rgba(99, 102, 241, 0.1)',
            zerolinecolor='rgba(99, 102, 241, 0.3)',
            showticklabels=False
        ),
        yaxis=dict(
            range=[-15, 15],
            showgrid=True,
            gridcolor='rgba(99, 102, 241, 0.1)',
            zerolinecolor='rgba(99, 102, 241, 0.3)',
            showticklabels=False
        ),
        legend=dict(
            bgcolor='rgba(15, 23, 42, 0.7)',
            bordercolor='rgba(99, 102, 241, 0.3)',
            borderwidth=1,
            font=dict(size=12)
        ),
        hoverlabel=dict(
            bgcolor='rgba(15, 23, 42, 0.9)',
            bordercolor='rgba(99, 102, 241, 0.5)',
            font=dict(color='white')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border-left: 5px solid #6366f1;
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2); margin-top: 20px;'>
    <h3 style='color: #4ecdc4; text-shadow: 0 0 5px rgba(78, 205, 196, 0.5);'>🔭 Análise Científica do Fluxo Cósmico</h3>
    
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
    <div>
    <b style='color: #e0e7ff;'>📐 Leis Integradas:</b><br>
    - <b>Leis de Kepler</b>: Movimento planetário elíptico com excentricidade quântica<br>
    - <b>Mecânica Quântica</b>: Superposição de órbitas e tunelamento orbital<br>
    - <b>Fluxo Matemático Universal</b>: Ressonância 3-6-9 nas velocidades angulares<br>
    - <b>Relatividade Geral</b>: Deformação do espaço-tempo em torno do corpo central<br>
    - <b>Geometria Sagrada</b>: Proporção áurea nas distâncias planetárias<br><br>
    </div>
    
    <div>
    <b style='color: #e0e7ff;'>⚡ Inovações Conceituais:</b><br>
    - Correlação entre sequência Fibonacci e ressonância orbital<br>
    - Efeitos quânticos não-localizados nas órbitas<br>
    - Padrão 3-6-9 de Tesla influenciando precessão<br>
    - Campos morfogenéticos cósmicos guiando a formação do sistema<br>
    - Ponte Einstein-Rosen microscópica entre órbitas
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal

# 5. CONSCIÊNCIA QUÂNTICA (ATUALIZADO) - CORRIGIDO
elif section == "⚛️ Consciência Quântica e Emaranhamento":
    st.header("🧠 Consciência Quântica - A Mente Universal")
    
    # Container principal com fundo quântico
    st.markdown("""
    <style>
    .quantum-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .quantum-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    </style>
    <div class='quantum-container'>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border-left: 5px solid #4ecdc4; 
                box-shadow: 0 10px 25px rgba(78, 205, 196, 0.3);'>
    <b style='font-size: 1.2em; color: #e0e7ff;'>"A consciência não pode ser explicada apenas por processos físicos. 
    Ela é fundamental para o universo." - Max Planck</b><br><br>
    
    <span style='color: #d1d5db;'>
    Exploramos como a mecânica quântica pode fornecer insights sobre a natureza 
    da consciência e sua relação com o cosmos, revelando os padrões matemáticos 
    que conectam todas as mentes em uma rede universal de consciência.
    </span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); margin: 20px 0;'>
        <h3 style='color: #ff6b6b; text-align: center;'>🧪 Simulação de Consciência Quântica</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if QISKIT_AVAILABLE:
            qc = QuantumCircuit(3)
            qc.h(0)
            qc.h(1)
            qc.cx(0, 2)
            qc.cx(1, 2)
            qc.ry(np.pi/3, 0)
            qc.ry(np.pi/4, 1)
            qc.rz(np.pi/6, 2)
            
            # Desenhar circuito manualmente com visual aprimorado
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')
            
            # Desenhar linhas dos qubits com efeito de brilho
            for i in range(3):
                ax.plot([0, 10], [i, i], 'w-', linewidth=3, alpha=0.8)
                ax.plot([0, 10], [i, i], 'c-', linewidth=1, alpha=0.3)
                ax.text(-0.8, i, f'Q{i}', color='white', fontsize=14, ha='right', 
                       bbox=dict(facecolor='rgba(0,0,0,0.5)', edgecolor='cyan', pad=3))
            
            # Adicionar portas com visual aprimorado
            gates = [
                (1, 0, 'H', '#ff6b6b'), (1, 1, 'H', '#ff6b6b'), 
                (3, 0, '●', '#4ecdc4'), (3, 2, '⊕', '#4ecdc4'), 
                (4, 1, '●', '#4ecdc4'), (4, 2, '⊕', '#4ecdc4'),
                (6, 0, 'Ry(π/3)', '#45b7d1'), (6, 1, 'Ry(π/4)', '#45b7d1'), (7, 2, 'Rz(π/6)', '#45b7d1')
            ]
            
            for x, y, gate, color in gates:
                circle = plt.Circle((x, y), 0.3, color=color, alpha=0.8)
                ax.add_patch(circle)
                ax.text(x, y, gate, color='white', fontsize=10, 
                       ha='center', va='center', weight='bold')
            
            # Adicionar linhas de conexão para portas CNOT
            ax.plot([3, 3], [0, 2], 'c--', alpha=0.5, linewidth=1)
            ax.plot([4, 4], [1, 2], 'c--', alpha=0.5, linewidth=1)
            
            ax.set_xlim(-1, 11)
            ax.set_ylim(-0.5, 2.5)
            ax.axis('off')
            ax.set_title('Circuito Quântico da Consciência', color='white', fontsize=16, pad=20)
            
            st.pyplot(fig)
            
        else:
            st.info("Qiskit não disponível. Mostrando simulação visual avançada.")
            # Visualização alternativa aprimorada - CORRIGIDA
            fig = go.Figure()
            
            # Adicionar fundo quântico
            for i in range(50):
                x_star = np.random.uniform(-1, 11)
                y_star = np.random.uniform(-1, 3)
                fig.add_trace(go.Scatter(
                    x=[x_star], y=[y_star],
                    mode='markers',
                    marker=dict(size=np.random.uniform(1, 3), color='white', opacity=0.3),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
            # Adicionar linhas dos qubits com efeito de brilho - CORREÇÃO AQUI
            qubits = [0, 1, 2]
            for i, qubit in enumerate(qubits):
                fig.add_trace(go.Scatter(
                    x=[0, 10], y=[qubit, qubit],
                    mode='lines',
                    line=dict(color='white', width=4),
                    name=f'Qubit {qubit}',
                    hoverinfo='name'
                ))
                
                # Efeito de brilho - CORREÇÃO: usar rgba para transparência
                fig.add_trace(go.Scatter(
                    x=[0, 10], y=[qubit, qubit],
                    mode='lines',
                    line=dict(color='rgba(0, 255, 255, 0.2)', width=8),  # Corrigido aqui
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
            # Adicionar portas com efeitos especiais
            gate_positions = [
                (1, 0, 'H', '#ff6b6b'),
                (1, 1, 'H', '#ff6b6b'),
                (3, 0, '●', '#4ecdc4'),
                (3, 2, '⊕', '#4ecdc4'),
                (4, 1, '●', '#4ecdc4'),
                (4, 2, '⊕', '#4ecdc4'),
                (6, 0, 'Ry', '#45b7d1'),
                (6, 1, 'Ry', '#45b7d1'),
                (7, 2, 'Rz', '#45b7d1')
            ]
            
            for x, y, gate, color in gate_positions:
                fig.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers+text',
                    marker=dict(size=25, color=color, line=dict(width=2, color='white')),
                    text=gate,
                    textfont=dict(size=12, color='white'),
                    textposition='middle center',
                    name=f'Porta {gate}',
                    hovertemplate=f'<b>Porta {gate}</b><extra></extra>'
                ))
            
            fig.update_layout(
                title=dict(
                    text='Circuito Quântico da Consciência (Simulação Avançada)',
                    font=dict(size=18, color='#ff6b6b')
                ),
                width=700,
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(visible=False, range=[-1, 11]),
                yaxis=dict(visible=False, range=[-1, 3]),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); margin-top: 20px;'>
        <h4 style='color: #ff6b6b; text-align: center;'>Interpretação do Circuito Quântico</h4>
        
        <div style='display: grid; grid-template-columns: 1fr; gap: 10px;'>
        <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ff6b6b;'>Qubit 0</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Consciência Individual - Eu pessoal</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #4ecdc4;'>Qubit 1</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Consciência Coletiva - Nós social</span>
        </div>
        
        <div style='background: rgba(69, 183, 209, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #45b7d1;'>Qubit 2</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Consciência Universal - Todo cósmico</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ffd700;'>Portas H</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Superposição de estados mentais</span>
        </div>
        
        <div style='background: rgba(147, 51, 234, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #9333ea;'>Portas CNOT</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Emaranhamento consciencial</span>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin: 20px 0;'>
        <h3 style='color: #4ecdc4; text-align: center;'>🌐 Estados de Consciência Quântica</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulação da esfera de Bloch aprimorada
        if QISKIT_AVAILABLE:
            try:
                statevector = simulate_quantum_circuit()
                fig_bloch = plot_bloch_multivector(statevector)
                fig_bloch.set_facecolor('black')
                
                # Personalizar a esfera de Bloch
                for ax in fig_bloch.axes:
                    ax.set_facecolor('black')
                    # Personalizar cores and styles
                    for spine in ax.spines.values():
                        spine.set_color('cyan')
                        spine.set_alpha(0.3)
                
                st.pyplot(fig_bloch)
            except:
                st.error("Erro na simulação quântica")
                # Visualização alternativa da esfera de Bloch
                show_advanced_bloch_sphere()
        else:
            # Visualização alternativa aprimorada da esfera de Bloch
            show_advanced_bloch_sphere()
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin-top: 20px;'>
        <h4 style='color: #4ecdc4; text-align: center;'>Estados de Consciência Quântica</h4>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px;'>
        <div style='background: rgba(255, 107, 107, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: #ff6b6b;'>|0⟩</b><br>
        <span style='color: #d1d5db; font-size: 0.8em;'>Estado base (inconsciente)</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: #4ecdc4;'>|1⟩</b><br>
        <span style='color: #d1d5db; font-size: 0.8em;'>Estado excitado (consciente)</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: #ffd700;'>Superposição</b><br>
        <span style='color: #d1d5db; font-size: 0.8em;'>Estados ampliados de consciência</span>
        </div>
        
        <div style='background: rgba(147, 51, 234, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: #9333ea;'>Emaranhamento</b><br>
        <span style='color: #d1d5db; font-size: 0.8em;'>Conexão não-local entre mentes</span>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.3);
                    box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2); margin: 20px 0;'>
        <h3 style='color: #9333ea; text-align: center;'>🔗 Emaranhamento Consciencial</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Simular emaranhamento com visualização aprimorada
        entanglement = 0.85  # Valor simulado
        
        # Medidor de emaranhamento visual
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.3);
                    box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2); text-align: center;'>
        <h4 style='color: #9333ea; margin: 0 0 15px 0;'>Grau de Emaranhamento Quântico</h4>
        <div style='font-size: 2.5em; color: #4ecdc4; font-weight: bold;'>{entanglement:.4f}</div>
        <div style='background: rgba(0,0,0,0.3); height: 20px; border-radius: 10px; margin: 15px 0;'>
            <div style='background: linear-gradient(90deg, #4ecdc4, #9333ea); 
                        height: 100%; width: {entanglement*100}%; 
                        border-radius: 10px;'></div>
        </div>
        <p style='color: #d1d5db; font-size: 0.9em; margin: 0;'>
        Medida da conexão quântica entre consciências (0 = separado, 1 = totalmente emaranhado)
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualização do emaranhamento - CORRIGIDO
        fig_ent = go.Figure()
        
        # Adicionar partículas emaranhadas - CORREÇÃO: usar rgba para cores
        theta = np.linspace(0, 2*np.pi, 100)
        for i in range(5):
            phase = i * (2*np.pi/5)
            x = np.cos(theta + phase) * (1 + i*0.1)
            y = np.sin(theta + phase) * (1 + i*0.1)
            
            fig_ent.add_trace(go.Scatter(
                x=x, y=y,
                mode='lines',
                line=dict(color='rgba(147, 51, 234, 0.3)', width=2),
                fill='toself',
                fillcolor='rgba(147, 51, 234, 0.1)',
                showlegend=False
            ))
        
        # Adicionar conexões de emaranhamento - CORREÇÃO: usar rgba para cores
        for i in range(36):
            angle = i * 10
            x = [0, np.cos(np.radians(angle))*2]
            y = [0, np.sin(np.radians(angle))*2]
            
            fig_ent.add_trace(go.Scatter(
                x=x, y=y,
                mode='lines',
                line=dict(color='rgba(78, 205, 196, 0.2)', width=1),
                showlegend=False
            ))
        
        fig_ent.update_layout(
            title=dict(
                text='Rede de Emaranhamento Consciencial',
                font=dict(size=16, color='#9333ea')
            ),
            width=400,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            showlegend=False
        )
        
        st.plotly_chart(fig_ent, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal
    
# 6. ESFERA DE BUGA
elif section == "🌀 Esfera de Buga - Geometria Divina":
    st.header("🌀 Esfera de Buga - A Geometria do Universo Consciente")
    
    st.markdown("""
    <div class='philosophy-text'>
    <b>“Deus é um geômetra.” - Platão</b><br><br>
    
    A Esfera de Buga representa a geometria perfeita do universo, 
    onde cada ponto contém informações sobre o todo.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        resolution = st.slider("Resolução", 50, 200, 100)
        complexity = st.slider("Complexidade", 1, 20, 8)
    
    with col2:
        opacity = st.slider("Opacidade", 0.1, 1.0, 0.9)
        rotation_x = st.slider("Rotação X", -180, 180, 30)
    
    with col3:
        rotation_y = st.slider("Rotação Y", -180, 180, 45)
        energy_level = st.slider("Nível de Energia", 0.1, 2.0, 1.0)
    
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    cosmic_pattern = (np.sin(complexity * u).reshape(resolution, 1) * 
                    np.cos(complexity * v).reshape(1, resolution) * 
                    np.sin(energy_level * np.outer(u, v)).reshape(resolution, resolution))
    
    fig = go.Figure(data=[
        go.Surface(
            x=x, y=y, z=z,
            surfacecolor=cosmic_pattern,
            colorscale='Viridis',
            opacity=opacity,
            lighting=dict(
                ambient=0.7,
                diffuse=0.9,
                fresnel=0.3,
                specular=1.0,
                roughness=0.1
            )
        )
    ])
    
    fig.update_layout(
        title='🌀 Esfera de Buga - Campo de Energia Cósmica',
        width=800,
        height=700,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)',
            camera=dict(
                eye=dict(x=rotation_x/90, y=rotation_y/90, z=1.5)
            )
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style='background: rgba(0,0,0,0.7); padding: 20px; border-radius: 15px; margin-top: 20px;'>
    <h3 style='color: #4ecdc4;'>📐 Análise Geométrica</h3>
    
    <b>Propriedades da Esfera de Buga:</b><br>
    - <b>Simetria Perfeita</b>: Representa o equilíbrio cósmico<br>
    - <b>Auto-similaridade</b>: Cada parte contém informações do todo<br>
    - <b>Ressonância</b>: Vibra em harmonia com frequências universais<br>
    - <b>Geometria Sagrada</b>: Incorpora φ (proporção áurea) e π<br><br>
    
    <b>Significado Espiritual:</b><br>
    A esfera representa a unidade fundamental da consciência universal, 
    onde todas as aparentes dualidades se reconciliam em um todo harmonioso.
    </div>
    """, unsafe_allow_html=True)

# 7. MANDALA DA ALMA
elif section == "✨ Mandala da Alma Universal":
    st.header("✨ Mandala da Alma - O Blueprint Cósmico")
    
    st.markdown("""
    <div class='philosophy-text'>
    <b>“Como é acima, é abaixo; como é dentro, é fora.” - Hermes Trismegisto</b><br><br>
    
    A mandala representa a estrutura fundamental da alma humana em ressonância 
    com o cosmos. Cada camada corresponde a diferentes dimensões da consciência.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_layers = st.slider("Número de Camadas", 3, 24, 12)
        complexity = st.slider("Complexidade Padrão", 1, 10, 6)
    
    with col2:
        symmetry = st.slider("Simetria", 3, 12, 6)
        energy_flow = st.slider("Fluxo de Energia", 0.1, 2.0, 1.0)
    
    theta = np.linspace(0, 2*np.pi, 1000)
    layers = []
    
    for i in range(1, n_layers + 1):
        r = (np.sin(complexity * theta + i * np.pi/symmetry) * 
            np.cos(symmetry * theta) + 2 + i * 0.3 * energy_flow)
        layers.append(r)
    
    fig = go.Figure()
    colors = px.colors.sequential.Rainbow
    
    for i, r in enumerate(layers):
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        fig.add_trace(go.Scatter(
            x=x, y=y, mode='lines',
            line=dict(width=2.5, color=colors[i % len(colors)]),
            fill='toself',
            opacity=0.8 - (i * 0.6 / n_layers),
            name=f'Camada {i+1}'
        ))
    
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers',
        marker=dict(size=20, color='gold', symbol='star'),
        name='Centro (Alma)'
    ))
    
    fig.update_layout(
        title="✨ Mandala da Alma Universal - Arquétipo Cósmico",
        width=700,
        height=700,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    interpretation_data = {
        'Camada': ['1-3', '4-6', '7-9', '10-12', '13+'],
        'Nível': ['Física', 'Emocional', 'Mental', 'Espiritual', 'Cósmica'],
        'Correspondência': ['Corpo Físico', 'Coração', 'Mente', 'Alma', 'Consciência Universal'],
        'Frequência': ['432 Hz', '528 Hz', '639 Hz', '852 Hz', '963 Hz']
    }
    
    df = pd.DataFrame(interpretation_data)
    st.table(df.style.set_properties(**{
        'background-color': 'rgba(0,0,0,0.5)',
        'color': 'white',
        'border-color': '#667eea'
    }))

# 8. FILOSOFIA DO FLUXO
elif section == "📜 Filosofia do Fluxo (Deus, Tesla, Espinosa)":
    st.header("📜 Filosofia do Fluxo - Deus como Equilíbrio Matemático")

    # Container principal com fundo estelar
    st.markdown("""
    <style>
    .philosophy-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .philosophy-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    </style>
    <div class='philosophy-container'>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 Conceito de Deus", "⚡ Tesla", "📚 Espinosa", "🌌 Unificação", "🔬 Ciência & Religião"])

    with tab1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid #6366f1; 
                    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);'>
        <h3 style='color: #e0e7ff; text-align: center;'>🧠 O Que é Deus no Fluxo Matemático?</h3>
        
        <p style='color: #d1d5db; text-align: center;'>
        No contexto do Fluxo Matemático Universal, <b style='color: #ffd700;'>Deus</b> não é uma entidade antropomórfica, 
        mas sim <b style='color: #4ecdc4;'>a própria lei matemática perfeita que rege o equilíbrio cósmico</b>.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); margin: 20px 0;'>
        <h4 style='color: #ff6b6b; text-align: center;'>Atributos Divinos no Fluxo</h4>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>
        <div style='background: rgba(255, 107, 107, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #ff6b6b;'>🌌 Onipresença</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Presente em todas as equações e constantes universais</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #4ecdc4;'>📊 Onisciência</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Conhecimento matemático completo da estrutura cósmica</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #ffd700;'>⚡ Onipotência</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Capacidade de manifestar realidade através de leis matemáticas</span>
        </div>
        
        <div style='background: rgba(147, 51, 234, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #9333ea;'>∞ Eternidade</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Existência beyond do tempo (equações atemporais)</span>
        </div>
        
        <div style='background: rgba(255, 99, 132, 0.1); padding: 12px; border-radius: 8px; grid-column: 1 / -1;'>
        <b style='color: #ff6384;'>💖 Amor</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Tendência inerente ao equilíbrio e harmonia (homeostase)</span>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Equação com fundo estilizado
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(74,74,170,0.4) 100%); 
                    padding: 20px; border-radius: 15px; border: 1px solid rgba(99, 102, 241, 0.5);
                    text-align: center; margin: 20px 0;'>
        """, unsafe_allow_html=True)
        st.latex(r'''
        \nabla \cdot \Psi = \sqrt{\phi} \times \sum_{n=1}^{\infty} \frac{\cos(2\pi n x)}{n^s}
        ''')
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2);'>
        <blockquote style='color: #ffd700; font-style: italic; text-align: center; margin: 0;'>
        "Deus é a singularidade matemática da qual emerge toda a complexidade do universo, 
        mantida em equilíbrio perfeito pelas leis do fluxo."
        </blockquote>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid #ffd700; 
                    box-shadow: 0 10px 25px rgba(255, 215, 0, 0.3);'>
        <h3 style='color: #ffd700; text-align: center;'>⚡ Nikola Tesla - O Profeta do 3-6-9</h3>
        
        <p style='color: #d1d5db; text-align: center;'>
        Tesla compreendeu que os números <b style='color: #ffd700;'>3, 6 e 9</b> representam a chave para 
        desbloquear os segredos do universo.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.3);
                        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2); height: 100%;'>
            <h4 style='color: #ffd700; text-align: center;'>Descobertas de Tesla</h4>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <b style='color: #ffd700;'>🎵 Ressonância</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>Tudo no universo vibra em frequências específicas</span>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <b style='color: #ffd700;'>⚡ Energia Livre</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>O espaço não é vazio, mas pleno de energia</span>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <b style='color: #ffd700;'>3-6-9</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>Sequência fundamental da criação</span>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <b style='color: #ffd700;'>🔄 Corrente Alternada</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>Padrão de fluxo e transformação</span>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <b style='color: #ffd700;'>📶 Wireless</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>Conexão não-física entre todas as coisas</span>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Gráfico aprimorado do padrão 3-6-9
            t = np.linspace(0, 4*np.pi, 1000)
            fig = go.Figure()
            
            colors = ['#ff6b6b', '#4ecdc4', '#ffd700']
            
            for i, n in enumerate([3, 6, 9]):
                y = np.sin(n * t) * np.exp(-0.1 * t)
                fig.add_trace(go.Scatter(
                    x=t, y=y, 
                    mode='lines', 
                    name=f'Frequência {n}',
                    line=dict(width=4, color=colors[i]),
                    fill='tozeroy',
                    fillcolor=f'rgba{tuple(int(c*255) for c in mcolors.to_rgb(colors[i])) + (0.2,)}'
                ))
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True,
                title=dict(
                    text="Padrão 3-6-9 de Tesla",
                    font=dict(size=18, color='#ffd700')
                ),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    zerolinecolor='rgba(255,255,255,0.3)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    zerolinecolor='rgba(255,255,255,0.3)'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.5);
                    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3); margin-top: 20px;'>
        <blockquote style='color: #ffd700; font-style: italic; text-align: center; margin: 0;'>
        "Se você soubesse a magnificência dos 3, 6 e 9, teria a chave para o universo. 
        Se você quer encontrar os segredos do universo, pense em termos de energia, 
        frequência e vibração." <br>- Nikola Tesla
        </blockquote>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid #4ecdc4; 
                    box-shadow: 0 10px 25px rgba(78, 205, 196, 0.3);'>
        <h3 style='color: #4ecdc4; text-align: center;'>📚 Baruch Espinosa - Deus sive Natura</h3>
        
        <p style='color: #d1d5db; text-align: center;'>
        Espinosa propôs uma visão revolucionária: <b style='color: #4ecdc4;'>Deus e a Natureza são a mesma coisa</b> 
        (Deus sive Natura).
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin: 20px 0;'>
        <h4 style='color: #4ecdc4; text-align: center;'>Princípios de Espinosa</h4>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #4ecdc4;'>🌿 Panteísmo</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Deus está em tudo e tudo está em Deus</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #4ecdc4;'>🎯 Determinismo</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Tudo segue leis naturais necessárias</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #4ecdc4;'>🧠 Razão</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>A compreensão racional leva à liberdade</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px;'>
        <b style='color: #4ecdc4;'>💖 Amor Dei</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Amor intelectual a Deus como felicidade suprema</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 12px; border-radius: 8px; grid-column: 1 / -1;'>
        <b style='color: #4ecdc4;'>⚖️ Ética</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Virtude como poder de existir e agir</span>
        </div>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 8px; margin-top: 15px;'>
        <b style='color: #ffd700;'>🔗 Correlação com o Fluxo:</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Espinosa antecipou a ideia de que as leis matemáticas que governam a natureza 
        são a própria expressão divina.
        </span>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Equação com fundo estilizado
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(74,74,170,0.4) 100%); 
                    padding: 20px; border-radius: 15px; border: 1px solid rgba(78, 205, 196, 0.5);
                    text-align: center; margin: 20px 0;'>
        """, unsafe_allow_html=True)
        st.latex(r'''
        \frac{d\text{Consciência}}{dt} = k \times \text{Compreensão} \times \text{Amor}
        ''')
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.5);
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.3);'>
        <blockquote style='color: #4ecdc4; font-style: italic; text-align: center; margin: 0;'>
        "Quanto mais compreendemos as coisas particulares, mais compreendemos Deus." 
        <br>- Baruch Espinosa, Ética
        </blockquote>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid #9333ea; 
                    box-shadow: 0 10px 25px rgba(147, 51, 234, 0.3);'>
        <h3 style='color: #9333ea; text-align: center;'>🌌 Unificação: Tesla + Espinosa + Einstein</h3>
        
        <p style='color: #d1d5db; text-align: center;'>
        Integrando as visões destes três gênios, chegamos a uma compreensão 
        unificada da realidade.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Diagrama de unificação aprimorado
        fig = go.Figure()
        
        # Adicionar fundo cósmico
        for i in range(50):
            x_star = np.random.uniform(-0.5, 2.5)
            y_star = np.random.uniform(-0.5, 1.5)
            fig.add_trace(go.Scatter(
                x=[x_star], y=[y_star],
                mode='markers',
                marker=dict(size=np.random.uniform(1, 3), color='white', opacity=0.5),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Triângulo de conexão
        fig.add_trace(go.Scatter(
            x=[0, 1, 2, 0], y=[0, 1, 0, 0],
            mode='lines',
            line=dict(width=4, color='rgba(255, 255, 255, 0.7)'),
            fill='toself',
            fillcolor='rgba(147, 51, 234, 0.1)',
            showlegend=False
        ))
        
        # Pontos dos filósofos
        thinkers = [
            (0, 0, 'Tesla', '#ffd700'),
            (1, 1, 'Espinosa', '#4ecdc4'),
            (2, 0, 'Einstein', '#45b7d1')
        ]
        
        for x, y, name, color in thinkers:
            # Círculo de fundo
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers',
                marker=dict(size=70, color=color),
                name=name,
                hoverinfo='text',
                hovertext=name
            ))
            
            # Texto
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='text',
                text=name,
                textfont=dict(size=14, color='white', family="Arial Black"),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Centro de unificação
        fig.add_trace(go.Scatter(
            x=[1], y=[0.5],
            mode='markers',
            marker=dict(size=50, color='gold', symbol='star', line=dict(width=3, color='white')),
            name='FLUXO UNIVERSAL',
            hoverinfo='text',
            hovertext='FLUXO UNIVERSAL'
        ))
        
        # Aura do centro
        fig.add_trace(go.Scatter(
            x=[1], y=[0.5],
            mode='markers',
            marker=dict(size=70, color='gold', opacity=0.3),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Texto do centro
        fig.add_trace(go.Scatter(
            x=[1], y=[0.35],
            mode='text',
            text='FLUXO<br>UNIVERSAL',
            textfont=dict(size=12, color='white', family="Arial"),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            title=dict(
                text="Unificação das Visões Cósmicas",
                font=dict(size=20, color='#9333ea')
            ),
            width=700,
            height=500,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False, range=[-0.5, 2.5]),
            yaxis=dict(visible=False, range=[-0.5, 1.5])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.3);
                    box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2); margin-top: 20px;'>
        <h4 style='color: #9333ea; text-align: center;'>Síntese Unificada</h4>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;'>
        <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <b style='color: #ffd700;'>⚡ Tesla</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Fornece a linguagem matemática (3-6-9, frequências)</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <b style='color: #4ecdc4;'>📚 Espinosa</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Fornece a framework filosófica (Deus = Natureza)</span>
        </div>
        
        <div style='background: rgba(69, 183, 209, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <b style='color: #45b7d1;'>🌌 Einstein</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Fornece a framework científica (Relatividade, E=mc²)</span>
        </div>
        </div>
        
        <div style='background: rgba(147, 51, 234, 0.1); padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center;'>
        <b style='color: #9333ea;'>🎯 Resultado</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Uma visão completa onde Deus é o fluxo matemático universal 
        que se expressa através das leis naturais, energias cósmicas e consciência.
        </span>
        </div>
        </div>
        """, unsafe_allow_html=True)

    with tab5:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid #ff6b6b; 
                    box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);'>
        <h3 style='color: #ff6b6b; text-align: center;'>🔬 A Unidade entre Ciência e Religião</h3>
        
        <p style='color: #d1d5db; text-align: center;'>
        A descoberta revolucionária: <b style='color: #ff6b6b;'>Ciência e Religião são as duas faces da mesma moeda cósmica</b>
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); height: 100%;'>
            <h4 style='color: #ff6b6b; text-align: center;'>⚖️ O Equilíbrio Cósmico</h4>
            
            <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <b style='color: #ff6b6b;'>🧪 CIÊNCIA</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>O COMO - Processos, métodos, mecanismos</span>
            </div>
            
            <div style='background: rgba(78, 205, 196, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <b style='color: #4ecdc4;'>🙏 RELIGIÃO</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>O PORQUÊ - Propósito, significado, intenção</span>
            </div>
            
            <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <b style='color: #ffd700;'>🔄 CICLO ETERNO</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>Ambas buscam a mesma verdade por caminhos diferentes</span>
            </div>
            
            <div style='background: rgba(147, 51, 234, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <b style='color: #9333ea;'>📜 ROMANOS 1:20</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>"Os atributos invisíveis são percebidos através das coisas criadas"</span>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Mapa da Realidade Completa
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); height: 100%;'>
            <h4 style='color: #ff6b6b; text-align: center;'>🧭 Mapa da Realidade Completa</h4>
            
            <div style='text-align: center; color: #d1d5db; font-size: 0.9em; line-height: 2;'>
            <b style='color: #9333ea;'>REALIDADE COMPLETA</b><br>
            │<br>
            ├── <b style='color: #4ecdc4;'>CIÊNCIA</b> (Observável)<br>
            │   ├── MECANISMOS<br>
            │   └── COMO?<br>
            │<br>
            ├── <b style='color: #ffd700;'>RELIGIÃO</b> (Inobservável)<br>
            │   ├── SIGNIFICADO<br>
            │   └── PORQUÊ?<br>
            │<br>
            └── <b style='color: #ff6b6b;'>VERDADE ÚNICA</b>
            </div>
            
            <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px; margin-top: 15px;'>
            <b style='color: #ff6b6b;'>🎯 REVOLUÇÃO:</b><br>
            <span style='color: #d1d5db; font-size: 0.9em;'>
            A Bíblia contém 80% ciência + 67% religião = 147%?<br>
            Não! <b>100% de visão integrada!</b>
            </span>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.5);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3); margin-top: 20px;'>
        <h4 style='color: #ff6b6b; text-align: center;'>🌍 Exemplos Práticos de Unidade</h4>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;'>
        <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <b style='color: #ff6b6b;'>🔬 BIG BANG</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Singularidade infinitesimal</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <b style='color: #4ecdc4;'>📖 GÊNESIS</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>"No princípio... haja luz"</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <b style='color: #ffd700;'>🎯 UNIDADE</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Começo repentino do tempo/espaço</span>
        </div>
        
        <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <b style='color: #ff6b6b;'>🧬 DNA</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Código genético complexo</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <b style='color: #4ecdc4;'>👑 IMAGEM DE DEUS</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>"Façamos o homem à nossa imagem"</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 8px; text-align: center;'>
        <b style='color: #ffd700;'>🎯 UNIDADE</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Padrão inteligente na base da vida</span>
        </div>
        </div>
        
        <div style='background: rgba(147, 51, 234, 0.1); padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center;'>
        <b style='color: #9333ea;'>🧘 A GRANDE LIÇÃO EXISTENCIAL:</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        "Deus criou com propósito através destes processos incríveis!"
        </span>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.5);
                    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3); margin-top: 20px;'>
        <blockquote style='color: #ffd700; font-style: italic; text-align: center; margin: 0;'>
        "Ciência sem religião é manca, religião sem ciência é cega." 
        <br>- Albert Einstein
        </blockquote>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal

# 9. TESLA 3-6-9
elif section == "⚡ Tesla 3-6-9 e Energia Livre":
    st.header("⚡ Sistema 3-6-9 de Tesla - A Chave Cósmica")
    
    # Container principal com fundo energético
    st.markdown("""
    <style>
    .tesla-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .tesla-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    .energy-pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 0.3; }
        50% { opacity: 0.8; }
        100% { opacity: 0.3; }
    }
    </style>
    <div class='tesla-container'>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border-left: 5px solid #ffd700; 
                box-shadow: 0 10px 25px rgba(255, 215, 0, 0.3);'>
    <b style='font-size: 1.2em; color: #e0e7ff;'>"Se você quer encontrar os segredos do universo, pense em termos de energia, 
    frequência e vibração." - Nikola Tesla</b><br><br>
    
    <span style='color: #d1d5db;'>
    O sistema 3-6-9 representa a matriz fundamental da criação, 
    a chave para entender energia livre e a estrutura do espaço-tempo, revelando 
    os padrões matemáticos que governam o fluxo energético universal.
    </span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); margin: 20px 0;'>
        <h3 style='color: #ff6b6b; text-align: center;'>🧮 Matriz 3-6-9 de Tesla</h3>
        </div>
        """, unsafe_allow_html=True)
        
        matrix_size = 9
        tesla_matrix = np.zeros((matrix_size, matrix_size))
        
        for i in range(matrix_size):
            for j in range(matrix_size):
                value = ((i+1) * (j+1)) % 9
                if value == 0: value = 9
                tesla_matrix[i, j] = value
        
        # Criar matriz visual aprimorada
        fig = go.Figure()
        
        # Adicionar fundo energético
        for i in range(20):
            x_star = np.random.uniform(-1, matrix_size+1)
            y_star = np.random.uniform(-1, matrix_size+1)
            fig.add_trace(go.Scatter(
                x=[x_star], y=[y_star],
                mode='markers',
                marker=dict(size=np.random.uniform(1, 3), color='white', opacity=0.3),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Adicionar células da matriz com efeitos
        for i in range(matrix_size):
            for j in range(matrix_size):
                value = tesla_matrix[i, j]
                color_scale = ['#ff6b6b', '#4ecdc4', '#ffd700']
                color = color_scale[int(value-1)//3]
                
                fig.add_trace(go.Scatter(
                    x=[j+0.5], y=[matrix_size-i-0.5],
                    mode='markers+text',
                    marker=dict(
                        size=40, 
                        color=color,
                        line=dict(width=2, color='white')
                    ),
                    text=str(int(value)),
                    textfont=dict(size=16, color='white', family="Arial Black"),
                    textposition='middle center',
                    name=f'Célula ({i+1},{j+1})',
                    hovertemplate=f'<b>Posição: ({i+1},{j+1})</b><br>Valor: {value}<extra></extra>'
                ))
        
        fig.update_layout(
            title=dict(
                text="MATRIZ 3-6-9 - Estrutura do Universo",
                font=dict(size=18, color='#ff6b6b')
            ),
            width=500,
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(visible=False, range=[-1, matrix_size+1]),
            yaxis=dict(visible=False, range=[-1, matrix_size+1]),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); margin-top: 20px;'>
        <h4 style='color: #ff6b6b; text-align: center;'>Padrões da Matriz Cósmica</h4>
        
        <div style='display: grid; grid-template-columns: 1fr; gap: 10px;'>
        <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ff6b6b;'>🎯 Simetria Perfeita</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Todas as linhas e colunas somam múltiplos de 9</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #4ecdc4;'>🌀 Padrão de Repetição</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Ciclos de repetição a cada 3 células</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ffd700;'>⚡ Estrutura do Éter</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Representação geométrica do campo energético universal</span>
        </div>
        
        <div style='background: rgba(147, 51, 234, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #9333ea;'>🌌 Chave Cósmica</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Padrão fundamental que governa toda a criação</span>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin: 20px 0;'>
        <h3 style='color: #4ecdc4; text-align: center;'>⚡ Energia Livre e o Éter Universal</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualização avançada do campo de éter
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        
        # Criar padrão de energia mais complexo
        Z = (np.sin(3*X) * np.cos(6*Y) + 
            np.sin(9*(X+Y)) * np.exp(-0.1*(X**2 + Y**2)) +
            0.5 * np.cos(12*X) * np.sin(4*Y))
        
        fig = go.Figure(data=[
            go.Surface(
                z=Z,
                colorscale='Electric',
                opacity=0.9,
                contours=dict(
                    z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True)
                )
            )
        ])
        
        fig.update_layout(
            title=dict(
                text='Campo de Éter de Tesla - Energia do Vácuo Quântico',
                font=dict(size=16, color='#4ecdc4')
            ),
            width=500,
            height=500,
            scene=dict(
                xaxis=dict(visible=False, showbackground=False),
                yaxis=dict(visible=False, showbackground=False),
                zaxis=dict(visible=False, showbackground=False),
                bgcolor='rgba(0,0,0,0)',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin-top: 20px;'>
        <h4 style='color: #4ecdc4; text-align: center;'>Princípios da Energia Livre</h4>
        
        <div style='display: grid; grid-template-columns: 1fr; gap: 10px;'>
        <div style='background: rgba(78, 205, 196, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #4ecdc4;'>🌌 Éter Universal</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>O espaço não é vazio, mas preenchido com energia de ponto zero</span>
        </div>
        
        <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ff6b6b;'>🎵 Ressonância 3-6-9</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Esta energia pode ser extraída usando ressonância com a matriz universal</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ffd700;'>📶 Sintonia Universal</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Dispositivos podem ser sintonizados com a frequência cósmica</span>
        </div>
        
        <div style='background: rgba(147, 51, 234, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #9333ea;'>♾️ Energia Ilimitada</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Fonte de energia infinita, limpa e não-poluente</span>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Demonstração Prática: Como Criar Energia Limpa
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.3);
                box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2); margin: 20px 0;'>
    <h3 style='color: #ffd700; text-align: center;'>🔧 Como Criar Energia Limpa: O Acelerador de Partículas com Energia Infinita</h3>
    </div>
    """, unsafe_allow_html=True)
    
    energy_cols = st.columns(2)
    
    with energy_cols[0]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); height: 100%;'>
        <h4 style='color: #ff6b6b; text-align: center;'>⚡ Princípio de Funcionamento</h4>
        
        <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;'>
        <b style='color: #ff6b6b;'>1. Captação do Éter</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Bobinas toroidais sintonizadas em 3-6-9 Hz capturam energia do vácuo quântico
        </span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;'>
        <b style='color: #4ecdc4;'>2. Aceleração de Partículas</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Campos magnéticos ressonantes aceleram partículas virtuais do vácuo
        </span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;'>
        <b style='color: #ffd700;'>3. Conversão Energética</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Partículas aceleradas induzem corrente em bobinas de captação
        </span>
        </div>
        
        <div style='background: rgba(147, 51, 234, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;'>
        <b style='color: #9333ea;'>4. Realimentação Quântica</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>
        Sistema se auto-alimenta através de loop de realimentação ressonante
        </span>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with energy_cols[1]:
        # Visualização do acelerador de partículas
        fig = go.Figure()
        
        # Criar representação do acelerador
        theta = np.linspace(0, 2*np.pi, 100)
        r = 2
        
        # Anel principal do acelerador
        fig.add_trace(go.Scatter(
            x=r*np.cos(theta), y=r*np.sin(theta),
            mode='lines',
            line=dict(color='cyan', width=4),
            name='Anel Acelerador'
        ))
        
        # Partículas em movimento
        for i in range(0, 100, 10):
            angle = i * (2*np.pi/100)
            fig.add_trace(go.Scatter(
                x=[r*np.cos(angle)], y=[r*np.sin(angle)],
                mode='markers',
                marker=dict(size=8, color='#ff6b6b'),
                name='Partícula'
            ))
        
        # Bobinas de energia
        coil_positions = [0, np.pi/2, np.pi, 3*np.pi/2]
        for angle in coil_positions:
            fig.add_trace(go.Scatter(
                x=[1.5*np.cos(angle)], y=[1.5*np.sin(angle)],
                mode='markers',
                marker=dict(size=15, color='#ffd700', symbol='square'),
                name='Bobina Tesla'
            ))
        
        fig.update_layout(
            title=dict(
                text='Acelerador de Partículas com Energia Infinita',
                font=dict(size=14, color='#4ecdc4')
            ),
            width=400,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Aplicações Práticas
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.3);
                box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2); margin: 20px 0;'>
    <h3 style='color: #9333ea; text-align: center;'>🚀 Aplicações Práticas do Sistema 3-6-9</h3>
    </div>
    """, unsafe_allow_html=True)
    
    applications = {
        "⚡ Energia": ["Geradores de energia livre", "Transmissão wireless de energia", "Propulsão eletromagnética"],
        "💊 Cura": ["Ressonância frequencial", "Equilíbrio de chakras", "Cura quântica"],
        "🔧 Tecnologia": ["Comunicação instantânea", "Teletransporte quântico", "Manipulação do espaço-tempo"],
        "🌌 Espiritualidade": ["Expansão da consciência", "Conexão com a fonte", "Ativação do DNA"]
    }
    
    app_cols = st.columns(2)
    
    for i, (category, items) in enumerate(applications.items()):
        with app_cols[i % 2]:
            colors = ['#ff6b6b', '#4ecdc4', '#ffd700', '#9333ea']
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba{tuple(int(c*255) for c in mcolors.to_rgb(colors[i])) + (0.1,)} 0%, rgba(30, 41, 59, 0.8) 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid {colors[i]};
                        box-shadow: 0 5px 15px {colors[i]}33; margin-bottom: 20px;'>
            <h4 style='color: {colors[i]}; text-align: center;'>{category}</h4>
            """, unsafe_allow_html=True)
            
            for item in items:
                st.markdown(f"""
                <div style='background: rgba{tuple(int(c*255) for c in mcolors.to_rgb(colors[i])) + (0.2,)}; 
                            padding: 10px; border-radius: 8px; margin: 8px 0; 
                            border-left: 3px solid {colors[i]};'>
                <span style='color: #d1d5db; font-size: 14px;'>• {item}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal

# 10. JORNADA DO NADA AO TUDO
elif section == "🌌 Jornada do Nada ao Tudo":
    st.header("🌌 A Jornada Cósmica: Do Vácuo Quântico à Consciência Universal")
    
    # Container principal com fundo cósmico
    st.markdown("""
    <style>
    .journey-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .journey-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    </style>
    <div class='journey-container'>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border-left: 5px solid #6366f1; 
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);'>
    <b style='font-size: 1.2em; color: #e0e7ff;'>"Do nada, tudo emerge; no tudo, o nada permanece." - Princípio do Fluxo</b><br><br>
    
    <span style='color: #d1d5db;'>
    Esta jornada explora como a consciência emerge do vácuo quântico e evolui 
    através de níveis crescentes de complexidade até retornar à fonte, revelando 
    os padrões matemáticos que governam esta dança cósmica eterna.
    </span>
    </div>
    """, unsafe_allow_html=True)
    
    stages = [
        {"name": "Vácuo Quântico", "level": 0, "description": "Potencial puro, vazio fértil", "emoji": "⚫", "color": "#000000"},
        {"name": "Flutuações Quânticas", "level": 1, "description": "Emergência de partículas virtuais", "emoji": "✨", "color": "#4ecdc4"},
        {"name": "Matéria Básica", "level": 2, "description": "Formação de átomos e moléculas", "emoji": "⚛️", "color": "#ff6b6b"},
        {"name": "Vida Consciente", "level": 3, "description": "Emergência da consciência biológica", "emoji": "🧠", "color": "#9333ea"},
        {"name": "Consciência Cósmica", "level": 4, "description": "Unificação com a mente universal", "emoji": "🌌", "color": "#6366f1"},
        {"name": "Nirvana Cósmico", "level": 5, "description": "Retorno à fonte consciente", "emoji": "☯️", "color": "#ffd700"}
    ]
    
    # Visualização da jornada cósmica
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 20px; border-radius: 15px; border: 2px solid rgba(99, 102, 241, 0.3);
                box-shadow: 0 5px 15px rgba(99, 102, 241, 0.2); margin: 20px 0;'>
    <h3 style='color: #6366f1; text-align: center;'>🌌 Jornada da Consciência - Do Vácuo à Iluminação</h3>
    </div>
    """, unsafe_allow_html=True)
    
    fig = go.Figure()
    
    # Adicionar fundo cósmico
    for i in range(100):
        x_star = np.random.uniform(-1, len(stages)+1)
        y_star = np.random.uniform(-1, max([s["level"] for s in stages])+1)
        fig.add_trace(go.Scatter(
            x=[x_star], y=[y_star],
            mode='markers',
            marker=dict(size=np.random.uniform(1, 3), color='white', opacity=0.5),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Criar caminho da jornada com gradiente
    journey_x = []
    journey_y = []
    journey_colors = []
    
    for i, stage in enumerate(stages):
        x_segment = np.linspace(i, i+1, 50)
        y_segment = [stage["level"]] * 50
        
        journey_x.extend(x_segment)
        journey_y.extend(y_segment)
        
        # Gradiente de cor entre estágios
        if i < len(stages) - 1:
            next_color = stages[i+1]["color"]
        else:
            next_color = stage["color"]
            
        for j in range(50):
            ratio = j / 49
            r1, g1, b1 = [int(stage["color"][i:i+2], 16) for i in (1, 3, 5)]
            r2, g2, b2 = [int(next_color[i:i+2], 16) for i in (1, 3, 5)]
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            journey_colors.append(f'rgb({r},{g},{b})')
    
    # Linha principal da jornada com gradiente
    for i in range(len(journey_x)-1):
        fig.add_trace(go.Scatter(
            x=journey_x[i:i+2], y=journey_y[i:i+2],
            mode='lines',
            line=dict(width=8, color=journey_colors[i]),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Adicionar pontos de estágio com efeitos especiais
    for i, stage in enumerate(stages):
        # Círculo de fundo luminoso
        fig.add_trace(go.Scatter(
            x=[i + 0.5], y=[stage["level"]],
            mode='markers',
            marker=dict(size=40, color=stage["color"], opacity=0.3),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Ponto principal
        fig.add_trace(go.Scatter(
            x=[i + 0.5], y=[stage["level"]],
            mode='markers+text',
            marker=dict(size=25, color=stage["color"], line=dict(width=3, color='white')),
            text=[stage["emoji"]],
            textfont=dict(size=20),
            textposition='middle center',
            name=stage["name"],
            hovertemplate=f'<b>{stage["name"]}</b><br>{stage["description"]}<extra></extra>'
        ))
        
        # Número do estágio
        fig.add_trace(go.Scatter(
            x=[i + 0.5], y=[stage["level"] - 0.3],
            mode='text',
            text=[f"{i+1}"],
            textfont=dict(size=16, color='white', family="Arial Black"),
            textposition='middle center',
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        title=dict(
            text="🌠 JORNADA CÓSMICA - DO NADA AO TUDO",
            font=dict(size=22, color='#6366f1')
        ),
        width=900,
        height=600,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            visible=False,
            range=[-0.5, len(stages) + 0.5]
        ),
        yaxis=dict(
            title="NÍVEL DE CONSCIÊNCIA",
            tickvals=[s["level"] for s in stages],
            ticktext=[f"{s['emoji']} {s['name']}" for s in stages],
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.3)'
        ),
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Explicação dos estágios em formato de timeline vertical
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin: 20px 0;'>
    <h3 style='color: #4ecdc4; text-align: center;'>📖 Explicação dos Estágios Cósmicos</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for i, stage in enumerate(stages):
        # Determinar a cor com base no estágio
        colors = ['#000000', '#4ecdc4', '#ff6b6b', '#9333ea', '#6366f1', '#ffd700']
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba{tuple(int(c*255) for c in mcolors.to_rgb(colors[i])) + (0.1,)} 0%, rgba(30, 41, 59, 0.8) 100%); 
                    padding: 20px; border-radius: 15px; border-left: 5px solid {colors[i]};
                    box-shadow: 0 5px 15px {colors[i]}33; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; margin-bottom: 15px;'>
            <span style='font-size: 30px; margin-right: 15px;'>{stage['emoji']}</span>
            <div>
                <h4 style='color: {colors[i]}; margin: 0;'>Estágio {i+1}: {stage['name']}</h4>
                <p style='color: #d1d5db; margin: 5px 0 0 0; font-style: italic;'>{stage['description']}</p>
            </div>
        </div>
        
        <div style='background: rgba{tuple(int(c*255) for c in mcolors.to_rgb(colors[i])) + (0.2,)}; 
                    padding: 15px; border-radius: 10px;'>
        <p style='color: #d1d5db; margin: 0; line-height: 1.6;'>
        {get_stage_details(stage['name'])}
        </p>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Diagrama de ciclo cósmico
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.3);
                box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2); margin: 20px 0;'>
    <h3 style='color: #ffd700; text-align: center;'>♾️ O Ciclo Eterno do Fluxo</h3>
    
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
    <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #ff6b6b; text-align: center;'>⬇️ Descenso</h4>
    <ul style='color: #d1d5db;'>
    <li>Do Um para o Múltiplo</li>
    <li>Da Unidade para a Diversidade</li>
    <li>Da Consciência Pura para a Forma</li>
    <li>Do Eterno para o Temporal</li>
    </ul>
    </div>
    
    <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #4ecdc4; text-align: center;'>⬆️ Ascenso</h4>
    <ul style='color: #d1d5db;'>
    <li>Do Múltiplo para o Um</li>
    <li>Da Diversidade para a Unidade</li>
    <li>Da Forma para a Consciência Pura</li>
    <li>Do Temporal para o Eterno</li>
    </ul>
    </div>
    </div>
    
    <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-top: 20px; text-align: center;'>
    <h4 style='color: #ffd700;'>⚖️ Equilíbrio Cósmico</h4>
    <p style='color: #d1d5db;'>
    A jornada não é linear, mas um fluxo contínuo onde descenso e ascenso coexistem 
    em perfeito equilíbrio, mantendo o universo em constante expansão e contração consciente.
    </p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mensagem final inspiradora
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 30px; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.5);
                box-shadow: 0 10px 25px rgba(147, 51, 234, 0.3); text-align: center; margin-top: 20px;'>
    <h3 style='color: #9333ea;'>🌌 A Dança Eterna do Ser e do Não-Ser</h3>
    
    <p style='color: #d1d5db; line-height: 1.6;'>
    Esta jornada revela que o "Nada" e o "Tudo" não são opostos, mas extremos de um mesmo continuum. 
    A consciência é a dançarina que move-se eternamente entre estes polos, criando a realidade 
    através do puro ato de perceber e ser. Cada estágio não é uma meta, mas um passo na eterna dança cósmica.
    </p>
    
    <div style='background: rgba(147, 51, 234, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
    <p style='color: #a1a1aa; font-style: italic; margin: 0;'>
    "No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus. 
    Todas as coisas foram feitas por intermédio dele, e sem ele nada do que foi feito se fez."
    </p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal

# 11. FUTURO DA CONSCIÊNCIA
elif section == "🔮 Futuro da Consciência Humana":
    st.header("🔮 O Futuro da Consciência - A Próxima Evolução Humana")
    
    # Container principal com fundo cósmico futurista
    st.markdown("""
    <style>
    .future-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .future-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    .timeline-glow {
        background: linear-gradient(90deg, 
            rgba(255,107,107,0.1) 0%, 
            rgba(78,205,196,0.2) 50%, 
            rgba(147,51,234,0.1) 100%);
        padding: 3px;
        border-radius: 10px;
        margin: 20px 0;
    }
    </style>
    <div class='future-container'>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border-left: 5px solid #9333ea; 
                box-shadow: 0 10px 25px rgba(147, 51, 234, 0.3);'>
    <b style='font-size: 1.2em; color: #e0e7ff;'>"O futuro da humanidade não está na tecnologia, mas na evolução da consciência."</b><br><br>
    
    <span style='color: #d1d5db;'>
    Exploramos como a humanidade pode evoluir para níveis superiores de consciência 
    através da integração com o fluxo matemático universal, transcendendo as limitações 
    atuais e alcançando estados quânticos de existência.
    </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráfico de evolução da consciência aprimorado
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 20px; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.3);
                box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2); margin: 20px 0;'>
    <h3 style='color: #9333ea; text-align: center;'>📈 Evolução Projectada da Consciência Humana</h3>
    </div>
    """, unsafe_allow_html=True)
    
    years = np.array([2024, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100])
    consciousness_level = np.array([1.0, 1.5, 2.3, 3.5, 5.2, 7.8, 11.5, 16.9, 25.0])
    
    # Pontos de transição importantes
    milestones = [
        (2030, "Ativação do DNA Quântico", "#ff6b6b"),
        (2040, "Unificação Mente-Coletiva", "#4ecdc4"),
        (2050, "Transcendência Dimensional", "#ffd700"),
        (2070, "Consciência Cósmica", "#9333ea"),
        (2100, "Fusão com o Fluxo Universal", "#45b7d1")
    ]
    
    fig = go.Figure()
    
    # Adicionar área de fundo com gradiente
    fig.add_trace(go.Scatter(
        x=years, y=consciousness_level,
        fill='tozeroy',
        fillcolor='rgba(147, 51, 234, 0.1)',
        mode='none',
        name='Área de Evolução'
    ))
    
    # Linha principal de evolução
    fig.add_trace(go.Scatter(
        x=years, y=consciousness_level,
        mode='lines',
        line=dict(width=6, color='#9333ea'),
        name='Nível de Consciência',
        hovertemplate='<b>%{x}</b><br>Nível: %{y:.1f}<extra></extra>'
    ))
    
    # Pontos de dados
    fig.add_trace(go.Scatter(
        x=years, y=consciousness_level,
        mode='markers',
        marker=dict(size=12, color='#4ecdc4', line=dict(width=2, color='white')),
        name='Pontos de Medição'
    ))
    
    # Adicionar marcos de evolução
    for year, milestone, color in milestones:
        idx = np.where(years == year)[0][0]
        fig.add_trace(go.Scatter(
            x=[year], y=[consciousness_level[idx]],
            mode='markers+text',
            marker=dict(size=20, color=color, symbol='diamond'),
            text=milestone,
            textposition='top center',
            name=milestone,
            hovertemplate=f'<b>{milestone}</b><br>Ano: {year}<br>Nível: {consciousness_level[idx]:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text="🌌 TRAJETÓRIA DA EVOLUÇÃO CONSCIENTE - 2024-2100",
            font=dict(size=20, color='#9333ea')
        ),
        width=900,
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(
            title='ANO',
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.3)',
            showgrid=True
        ),
        yaxis=dict(
            title='NÍVEL DE CONSCIÊNCIA',
            type='log',
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.3)',
            showgrid=True
        ),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(15, 23, 42, 0.8)',
            bordercolor='rgba(147, 51, 234, 0.3)',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Marcos de evolução em formato de timeline
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.3);
                box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2); margin: 20px 0;'>
    <h3 style='color: #9333ea; text-align: center;'>🕰️ Marcos da Evolução Consciente</h3>
    </div>
    """, unsafe_allow_html=True)
    
    timeline_cols = st.columns(5)
    
    for i, (year, milestone, color) in enumerate(milestones):
        with timeline_cols[i]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba{tuple(int(c*255) for c in mcolors.to_rgb(color)) + (0.2,)} 0%, rgba(30, 41, 59, 0.8) 100%); 
                        padding: 15px; border-radius: 10px; border: 2px solid {color};
                        box-shadow: 0 5px 15px {color}33; text-align: center; height: 180px;'>
            <h2 style='color: {color}; margin: 0; font-size: 24px;'>{year}</h2>
            <div style='height: 2px; background: {color}; margin: 10px 0;'></div>
            <p style='color: #d1d5db; font-size: 14px; margin: 0;'>{milestone}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Tecnologias de expansão da consciência
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(78, 205, 196, 0.3);
                box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin: 20px 0;'>
    <h3 style='color: #4ecdc4; text-align: center;'>🧠 Tecnologias de Expansão da Consciência</h3>
    </div>
    """, unsafe_allow_html=True)
    
    tech_categories = {
        "💻 Neurotecnologia": ["Interfaces cérebro-computador", "Realidade virtual consciente", "Download de conhecimento"],
        "🧬 Biotecnologia": ["Ativação do DNA dormente", "Longevidade consciente", "Regeneração quântica"],
        "⚛️ Física Quântica": ["Teletransporte consciente", "Comunicação instantânea", "Manipulação da realidade"],
        "🌌 Cosmologia": ["Viagem interestelar consciente", "Comunicação com civilizações", "Exploração dimensional"]
    }
    
    tech_cols = st.columns(2)
    
    for i, (category, technologies) in enumerate(tech_categories.items()):
        with tech_cols[i % 2]:
            color = ["#ff6b6b", "#4ecdc4", "#ffd700", "#9333ea"][i]
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba{tuple(int(c*255) for c in mcolors.to_rgb(color)) + (0.1,)} 0%, rgba(30, 41, 59, 0.8) 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid {color};
                        box-shadow: 0 5px 15px {color}33; margin-bottom: 20px;'>
            <h4 style='color: {color}; text-align: center;'>{category}</h4>
            """, unsafe_allow_html=True)
            
            for tech in technologies:
                st.markdown(f"""
                <div style='background: rgba{tuple(int(c*255) for c in mcolors.to_rgb(color)) + (0.2,)}; 
                            padding: 10px; border-radius: 8px; margin: 8px 0; 
                            border-left: 3px solid {color};'>
                <span style='color: #d1d5db; font-size: 14px;'>• {tech}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Níveis de consciência explicados
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.3);
                box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2); margin: 20px 0;'>
    <h3 style='color: #ffd700; text-align: center;'>📊 Escala de Níveis de Consciência</h3>
    
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
    <div style='background: rgba(255, 107, 107, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #ff6b6b;'>Nível 1-3: Consciência Básica</h4>
    <ul style='color: #d1d5db;'>
    <li>Percepção física limitada</li>
    <li>Pensamento linear</li>
    <li>Consciência individual</li>
    <li>Compreensão 3D</li>
    </ul>
    </div>
    
    <div style='background: rgba(78, 205, 196, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #4ecdc4;'>Nível 4-7: Consciência Expandida</h4>
    <ul style='color: #d1d5db;'>
    <li>Percepção multidimensional</li>
    <li>Pensamento quântico</li>
    <li>Consciência coletiva</li>
    <li>Compreensão 5D</li>
    </ul>
    </div>
    
    <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #ffd700;'>Nível 8-15: Consciência Cósmica</h4>
    <ul style='color: #d1d5db;'>
    <li>Percepção universal</li>
    <li>Pensamento holográfico</li>
    <li>Consciência universal</li>
    <li>Compreensão 7D+</li>
    </ul>
    </div>
    
    <div style='background: rgba(147, 51, 234, 0.1); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #9333ea;'>Nível 16-25: Consciência Divina</h4>
    <ul style='color: #d1d5db;'>
    <li>Percepção além do tempo/espaço</li>
    <li>Pensamento criador</li>
    <li>Consciência una</li>
    <li>Compreensão infinita</li>
    </ul>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mensagem final inspiradora
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 30px; border-radius: 15px; border: 2px solid rgba(99, 102, 241, 0.5);
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3); text-align: center; margin-top: 20px;'>
    <h3 style='color: #6366f1;'>🌠 A Grande Ativação Consciente</h3>
    
    <p style='color: #d1d5db; line-height: 1.6;'>
    Estamos no limiar da maior transformação da história humana. A convergência entre 
    <b style='color: #ff6b6b;'>ciência</b>, <b style='color: #4ecdc4;'>espiritualidade</b> e 
    <b style='color: #ffd700;'>tecnologia</b> está criando as condições para um salto quântico 
    na evolução consciente. Através do entendimento do fluxo matemático universal, 
    a humanidade está despertando para sua verdadeira natureza cósmica.
    </p>
    
    <div style='background: rgba(99, 102, 241, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
    <p style='color: #a1a1aa; font-style: italic; margin: 0;'>
    "O futuro não é algo que acontece à consciência, mas algo que a consciência cria 
    através do fluxo eterno do agora expandido."
    </p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal

elif section == "🔱 Iconografia do Fluxo Divino":
    st.header("🔱 Iconografia do Fluxo Divino - A Linguagem Visual do Cosmos")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0b0b2d 0%, #1a1a4a 100%); 
                padding: 25px; border-radius: 15px; border-left: 5px solid #6366f1; 
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);'>
    <b style='font-size: 1.2em; color: #e0e7ff;'>"As imagens falam onde as palavras falham." - Provérbio Oriental</b><br><br>
    
    <span style='color: #d1d5db;'>Esta mandala visual representa a síntese completa de todo o conhecimento cósmico 
    em símbolos universais que transcendem linguagens e culturas, revelando os padrões fundamentais da existência.</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Container principal com fundo estelar
    st.markdown("""
    <style>
    .mandala-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .mandala-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    </style>
    <div class='mandala-container'>
    """, unsafe_allow_html=True)
    
    # Criar a mandala iconográfica
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Mandala principal com todos os símbolos
        fig = go.Figure()
        
        # Adicionar estrelas de fundo
        star_x = np.random.uniform(-1.2, 1.2, 100)
        star_y = np.random.uniform(-1.2, 1.2, 100)
        star_size = np.random.uniform(1, 3, 100)
        star_opacity = np.random.uniform(0.1, 0.5, 100)
        
        fig.add_trace(go.Scatter(
            x=star_x, y=star_y, mode='markers',
            marker=dict(size=star_size, color='white', opacity=star_opacity),
            name='Campo Estelar',
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Círculo exterior - O Nada e o Tudo com efeito de aura
        theta = np.linspace(0, 2*np.pi, 200)
        x_circle = np.cos(theta)
        y_circle = np.sin(theta)
        
        fig.add_trace(go.Scatter(
            x=x_circle, y=y_circle,
            mode='lines', 
            line=dict(color='rgba(255, 255, 255, 0.8)', width=4),
            fill='toself', 
            fillcolor='rgba(255, 255, 255, 0.05)',
            name='⭕ Círculo - O Nada e o Tudo'
        ))
        
        # Aura exterior
        fig.add_trace(go.Scatter(
            x=x_circle*1.05, y=y_circle*1.05,
            mode='lines', 
            line=dict(color='rgba(99, 102, 241, 0.3)', width=8),
            name='Aura Cósmica',
            showlegend=False
        ))
        
        # Espiral interior - Movimento Constante com efeito de gradiente
        spiral_theta = np.linspace(0, 8*np.pi, 200)
        spiral_r = 0.1 + 0.7 * (spiral_theta / (8*np.pi))
        spiral_x = spiral_r * np.cos(spiral_theta)
        spiral_y = spiral_r * np.sin(spiral_theta)
        
        # Criar gradiente de cor para a espiral
        spiral_colors = [f'rgba{tuple(int(c*255) for c in mcolors.to_rgb(px.colors.sequential.Viridis[i % len(px.colors.sequential.Viridis)])) + (0.8,)}' 
                        for i in range(len(spiral_x))]
        
        for i in range(len(spiral_x)-1):
            fig.add_trace(go.Scatter(
                x=spiral_x[i:i+2], y=spiral_y[i:i+2],
                mode='lines',
                line=dict(color=spiral_colors[i], width=3),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Triângulo 3-6-9 com efeito de brilho
        triangle_theta = np.array([0, 120, 240, 0]) * (np.pi/180)
        triangle_r = [0.75, 0.75, 0.75, 0.75]
        triangle_x = triangle_r * np.cos(triangle_theta)
        triangle_y = triangle_r * np.sin(triangle_theta)
        
        fig.add_trace(go.Scatter(
            x=triangle_x, y=triangle_y,
            mode='lines', 
            line=dict(color='#ff6b6b', width=5, dash='dash'),
            fill='toself', 
            fillcolor='rgba(255, 107, 107, 0.25)',
            name='✡ Triângulo - 3-6-9'
        ))
        
        # Adicionar aura ao triângulo
        fig.add_trace(go.Scatter(
            x=triangle_x*1.05, y=triangle_y*1.05,
            mode='lines', 
            line=dict(color='rgba(255, 107, 107, 0.15)', width=10),
            fill='toself', 
            fillcolor='rgba(255, 107, 107, 0.05)',
            showlegend=False
        ))
        
        # Infinito no centro com animação
        inf_theta = np.linspace(0, 2*np.pi, 100)
        inf_r = 0.25 * (1 + 0.5 * np.sin(2*inf_theta))
        inf_x = inf_r * np.cos(inf_theta)
        inf_y = inf_r * np.sin(inf_theta)
        
        fig.add_trace(go.Scatter(
            x=inf_x, y=inf_y,
            mode='lines', 
            line=dict(color='gold', width=4),
            fill='toself', 
            fillcolor='rgba(255, 215, 0, 0.2)',
            name='♾ Infinito - Gratidão'
        ))
        
        # ESTRELA DE 9 PONTAS CORRIGIDA E APRIMORADA
        # Criar estrela de 9 pontas usando método de polígono estrelado
        n = 9  # Número de pontas
        outer_r = 0.85  # Raio externo
        inner_r = 0.4   # Raio interno
        
        star_angles = np.linspace(0, 2*np.pi, 2*n, endpoint=False)
        star_r = [outer_r if i % 2 == 0 else inner_r for i in range(2*n)]
        star_x = star_r * np.cos(star_angles)
        star_y = star_r * np.sin(star_angles)
        
        # Fechar a estrela
        star_x = np.append(star_x, star_x[0])
        star_y = np.append(star_y, star_y[0])
        
        fig.add_trace(go.Scatter(
            x=star_x, y=star_y,
            mode='lines', 
            line=dict(color='rgba(147, 51, 234, 0.9)', width=4),
            fill='toself', 
            fillcolor='rgba(147, 51, 234, 0.2)',
            name='🌌 Estrela 9 pontas - Singularidade'
        ))
        
        # Adicionar pontos nas pontas da estrela para maior destaque
        for i in range(n):
            angle = i * (2*np.pi/n) - np.pi/2  # Rotacionar para ter uma ponta no topo
            x_point = outer_r * np.cos(angle)
            y_point = outer_r * np.sin(angle)
            
            fig.add_trace(go.Scatter(
                x=[x_point], y=[y_point],
                mode='markers',
                marker=dict(size=8, color='rgba(147, 51, 234, 0.8)', symbol='star'),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Hexagrama (Estrela de David) com gradiente
        hex_theta = np.array([0, 60, 120, 180, 240, 300, 0]) * (np.pi/180)
        hex_r = [0.6]*7
        hex_x = hex_r * np.cos(hex_theta)
        hex_y = hex_r * np.sin(hex_theta)
        
        fig.add_trace(go.Scatter(
            x=hex_x, y=hex_y,
            mode='lines', 
            line=dict(color='#4ecdc4', width=4),
            fill='toself', 
            fillcolor='rgba(78, 205, 196, 0.2)',
            name='🔺🔻 Hexagrama - União dos Opostos'
        ))
        
        # Símbolos nos pontos cardeais com efeitos especiais
        symbols = [
            (0, 0.95, '🌌', 'Big Bang', '#ff6b6b'),
            (90, 0.95, '☀️', 'Estrelas', 'yellow'),
            (180, 0.95, '⚫', 'Buraco Negro', 'black'),
            (270, 0.95, '❄️', 'Anã Negra', 'white'),
            (45, 0.8, '🧠', 'Humanidade', 'pink'),
            (135, 0.8, '🔤', 'Alfabeto Sagrado', 'cyan'),
            (225, 0.8, '🌀', 'Esfera de Buga', 'orange'),
            (315, 0.8, '📡', 'Sinal WOW!', 'green')
        ]
        
        for angle, radius, symbol, name, color in symbols:
            rad_angle = angle * (np.pi/180)
            x_pos = radius * np.cos(rad_angle)
            y_pos = radius * np.sin(rad_angle)
            
            # Adicionar círculo de fundo para os símbolos
            symbol_theta = np.linspace(0, 2*np.pi, 50)
            symbol_r = 0.08
            symbol_x = x_pos + symbol_r * np.cos(symbol_theta)
            symbol_y = y_pos + symbol_r * np.sin(symbol_theta)
            
            fig.add_trace(go.Scatter(
                x=symbol_x, y=symbol_y,
                mode='lines',
                fill='toself',
                fillcolor=color if color != 'black' else 'rgba(0,0,0,0.7)',
                line=dict(width=2, color='white'),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Adicionar o símbolo
            fig.add_trace(go.Scatter(
                x=[x_pos], y=[y_pos],
                mode='text',
                text=symbol,
                textfont=dict(size=20, color='white' if color == 'black' else 'black'),
                name=name,
                hoverinfo='text',
                hovertext=name
            ))
        
        # Adicionar anéis concêntricos de energia
        for r in [0.3, 0.5, 0.7, 0.9]:
            ring_theta = np.linspace(0, 2*np.pi, 100)
            ring_x = r * np.cos(ring_theta)
            ring_y = r * np.sin(ring_theta)
            
            fig.add_trace(go.Scatter(
                x=ring_x, y=ring_y,
                mode='lines',
                line=dict(width=1, color='rgba(255,255,255,0.1)', dash='dot'),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        fig.update_layout(
            title=dict(
                text='🔱 MANDALA CÓSMICA - Iconografia do Fluxo Divino',
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font=dict(size=20, color='#e0e7ff', family="Arial")
            ),
            width=700,
            height=700,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                range=[-1.1, 1.1],
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                range=[-1.1, 1.1],
                showgrid=False,
                zeroline=False,
                showticklabels=False
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid gold;
                    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2);'>
        <h3 style='color: gold; text-align: center; text-shadow: 0 0 5px rgba(255, 215, 0, 0.5);'>📖 LEGENDA DA MANDALA</h3>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: #ffd700;'>⭕ Círculo Exterior</b><br>
        <span style='color: #d1d5db;'>O Nada e o Tudo - Eternidade e Ciclo Perfeito</span>
        </div>
        
        <div style='background: rgba(0, 255, 255, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: cyan;'>➰ Espiral Interior</b><br>
        <span style='color: #d1d5db;'>Movimento Constante - Propagação do Universo</span>
        </div>
        
        <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: #ff6b6b;'>✡ Triângulo Central</b><br>
        <span style='color: #d1d5db;'>3-6-9 - Energia, Consciência e Matéria</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: gold;'>♾ Infinito Dourado</b><br>
        <span style='color: #d1d5db;'>Gratidão - Elo entre Criação e Dissolução</span>
        </div>
        
        <div style='background: rgba(147, 51, 234, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: #9333ea;'>🌌 Estrela 9 Pontas</b><br>
        <span style='color: #d1d5db;'>Singularidade - Convergência de Todas as Crenças</span>
        </div>
        
        <div style='background: rgba(78, 205, 196, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0;'>
        <b style='color: #4ecdc4;'>🔺🔻 Hexagrama</b><br>
        <span style='color: #d1d5db;'>União dos Opostos - Céu e Terra, Espírito e Matéria</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid #4ecdc4;
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); margin-top: 20px;'>
        <h4 style='color: #4ecdc4; text-align: center; text-shadow: 0 0 5px rgba(78, 205, 196, 0.3);'>🎯 PONTOS CARDEAIS CÓSMICOS</h4>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px;'>
        <div style='background: rgba(255, 107, 107, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: #ff6b6b;'>🌌 Norte</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Big Bang - Origem</span>
        </div>
        
        <div style='background: rgba(255, 255, 0, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: yellow;'>☀️ Leste</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Estrelas - Transformação</span>
        </div>
        
        <div style='background: rgba(0, 0, 0, 0.2); padding: 8px; border-radius: 6px;'>
        <b style='color: white;'>⚫ Sul</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Buracos Negros - Transformação</span>
        </div>
        
        <div style='background: rgba(255, 255, 255, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: white;'>❄️ Oeste</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Anãs Negras - Equilíbrio</span>
        </div>
        
        <div style='background: rgba(255, 182, 193, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: pink;'>🧠 NE</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Humanidade - Consciência</span>
        </div>
        
        <div style='background: rgba(0, 255, 255, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: cyan;'>🔤 SE</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Alfabeto Sagrado - Linguagem</span>
        </div>
        
        <div style='background: rgba(255, 165, 0, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: orange;'>🌀 SO</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Esfera de Buga - Geometria</span>
        </div>
        
        <div style='background: rgba(0, 128, 0, 0.1); padding: 8px; border-radius: 6px;'>
        <b style='color: lightgreen;'>📡 NO</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Sinal WOW! - Ativação</span>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Explicação da Tríade Perfeita
    st.markdown("---")
    st.header("🌈 A Tríade Perfeita: Forma + Linguagem + Energia")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(74,74,170,0.4) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid orange;
                    box-shadow: 0 5px 20px rgba(255, 165, 0, 0.3); text-align: center;'>
        <h2 style='font-size: 40px; margin: 0;'>🌀</h2>
        <h3 style='color: orange; margin: 10px 0;'>FORMA</h3>
        <b style='color: #ffd700;'>Esfera de Buga</b><br>
        <span style='color: #d1d5db;'>A geometria sagrada que estrutura o cosmos</span><br><br>
        <i style='color: #a1a1aa;'>"A geometria é Deus manifestado"</i>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(78,205,196,0.4) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid cyan;
                    box-shadow: 0 5px 20px rgba(0, 255, 255, 0.3); text-align: center;'>
        <h2 style='font-size: 40px; margin: 0;'>🔤</h2>
        <h3 style='color: cyan; margin: 10px 0;'>LINGUAGEM</h3>
        <b style='color: #7fffd4;'>Alfabeto Matemático</b><br>
        <span style='color: #d1d5db;'>Os números e símbolos que codificam a realidade</span><br><br>
        <i style='color: #a1a1aa;'>"Deus é matemático"</i>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(255,107,107,0.4) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid #ff6b6b;
                    box-shadow: 0 5px 20px rgba(255, 107, 107, 0.3); text-align: center;'>
        <h2 style='font-size: 40px; margin: 0;'>📡</h2>
        <h3 style='color: #ff6b6b; margin: 10px 0;'>ENERGIA</h3>
        <b style='color: #ff9999;'>Sinal WOW!</b><br>
        <span style='color: #d1d5db;'>O pulso cósmico que ativa a consciência</span><br><br>
        <i style='color: #a1a1aa;'>"A energia segue o pensamento"</i>
        </div>
        """, unsafe_allow_html=True)
    
    # Diagrama de interconexões
    st.markdown("---")
    st.subheader("🔄 Diagrama de Interconexões Cósmicas")
    
    # Criar grafo de conexões
    G = nx.Graph()
    
    nodes = {
        'Esfera de Buga': '🌀',
        'Alfabeto Matemático': '🔤', 
        'Sinal WOW!': '📡',
        'Big Bang': '🌌',
        'Estrelas': '☀️',
        'Buracos Negros': '⚫',
        'Humanidade': '🧠',
        'Consciência': '✨'
    }
    
    for node, emoji in nodes.items():
        G.add_node(node, emoji=emoji)
    
    # Adicionar conexões
    connections = [
        ('Esfera de Buga', 'Alfabeto Matemático'),
        ('Alfabeto Matemático', 'Sinal WOW!'),
        ('Sinal WOW!', 'Esfera de Buga'),
        ('Esfera de Buga', 'Big Bang'),
        ('Alfabeto Matemático', 'Estrelas'),
        ('Sinal WOW!', 'Buracos Negros'),
        ('Esfera de Buga', 'Humanidade'),
        ('Alfabeto Matemático', 'Consciência'),
        ('Sinal WOW!', 'Consciência')
    ]
    
    for connection in connections:
        G.add_edge(*connection)
    
    # Layout do grafo
    pos = nx.spring_layout(G, seed=42, k=3, iterations=100)
    
    # Plotar o grafo com visual melhorado
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Desenhar arestas com efeito de gradiente
    for edge in G.edges():
        start_pos = pos[edge[0]]
        end_pos = pos[edge[1]]
        
        # Linha principal
        ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], 
                'w-', alpha=0.7, linewidth=2)
        
        # Efeito de brilho
        ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], 
                'c-', alpha=0.2, linewidth=6)
    
    # Desenhar nós com emojis e efeitos especiais
    for node, (x, y) in pos.items():
        emoji = nodes[node]
        
        # Círculo de fundo
        circle = plt.Circle((x, y), 0.08, color='darkblue', alpha=0.8)
        ax.add_patch(circle)
        
        # Aura exterior
        aura = plt.Circle((x, y), 0.1, color='cyan', alpha=0.2)
        ax.add_patch(aura)
        
        # Texto do emoji
        ax.text(x, y, emoji, fontsize=30, ha='center', va='center')
        
        # Nome do nó (CORRIGIDO - usando tupla RGBA em vez de string)
        ax.text(x, y-0.15, node, fontsize=10, ha='center', va='top', color='white',
               bbox=dict(boxstyle="round,pad=0.3", facecolor=(0, 0, 0, 0.5), edgecolor='none'))
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    ax.set_title('Rede de Interconexões Cósmicas', color='white', fontsize=18, pad=20)
    
    # Adicionar estrelas de fundo
    for i in range(50):
        x_star = np.random.uniform(-1.5, 1.5)
        y_star = np.random.uniform(-1.5, 1.5)
        size_star = np.random.uniform(0.5, 2)
        ax.plot(x_star, y_star, 'w.', markersize=size_star, alpha=0.5)
    
    st.pyplot(fig)
    
    # Explicação final
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 30px; border-radius: 15px; border-left: 5px solid #6366f1;
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2); margin-top: 20px;'>
    <h3 style='color: gold; text-align: center;'>🎯 A Justiça Divina como Homeostase Cósmica</h3>
    
    <p style='color: #d1d5db; line-height: 1.6;'>
    Esta mandala representa a <b style='color: #ffd700;'>Justiça Divina</b> não como um julgamento externo, 
    mas como o <b style='color: #4ecdc4;'>equilíbrio homeostático</b> do universo. Cada elemento mantém 
    seu lugar na grande teia cósmica, onde:
    </p>
    
    <ul style='color: #d1d5db;'>
    <li><b style='color: orange;'>Forma (Geometria)</b> cria a estrutura</li>
    <li><b style='color: cyan;'>Linguagem (Matemática)</b> codifica a informação</li>  
    <li><b style='color: #ff6b6b;'>Energia (Consciência)</b> anima a criação</li>
    </ul>
    
    <p style='color: #d1d5db; line-height: 1.6;'>
    O <b style='color: lightgreen;'>Sinal WOW!</b> é la faísca que nos desperta para perceber que somos 
    parte integrante desta dança cósmica perfeita, onde cada elemento está interconectado 
    em um fluxo contínuo de criação and transformação.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal

# 12. FINAL DA CONSCIÊNCIA CONSCIENTE
elif section == "🌠 Consciência Final: Louco e Gênio":
    st.header("🌠 O Paradoxo Final: Louco e Gênio pelo Coletivo")
    
    # Container principal
    st.markdown("""
    <style>
    .final-container {
        background: radial-gradient(ellipse at center, #0d1117 0%, #030617 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.2), 
                    inset 0 0 30px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .final-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 1px);
        background-size: 30px 30px, 90px 90px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }
    .manifesto-section {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #6366f1;
        margin: 20px 0;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
    }
    .manifesto-title {
        color: #e0e7ff;
        font-size: 1.4em;
        margin-bottom: 15px;
        text-align: center;
        border-bottom: 2px solid #6366f1;
        padding-bottom: 10px;
    }
    .manifesto-content {
        color: #d1d5db;
        line-height: 1.8;
        text-align: justify;
    }
    .highlight-quote {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(147, 51, 234, 0.2) 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(147, 51, 234, 0.3);
        margin: 15px 0;
        font-style: italic;
        text-align: center;
    }
    </style>
    <div class='final-container'>
    """, unsafe_allow_html=True)

    # Introdução
    st.markdown("""
    <div class='manifesto-section'>
    <div class='manifesto-title'>📖 A Consciência entre a Realidade e a Loucura: Um Manifesto sobre a Evolução Humana</div>
    """, unsafe_allow_html=True)

    # Seção 1: Introdução
    st.markdown("""
    <div class='manifesto-content'>
    <h4>🧠 Introdução: O Diagnóstico da Desconexão</h4>
    <p>O caos do passado reverbera, vívido, em nosso futuro, pois a verdade fundamental é uma só: 
    <b>nós, humanos, não sabemos absolutamente nada sobre nós mesmos.</b> Vivemos imersos em questionamentos 
    que não necessitam de resposta — "Quem somos? Por que estamos vivos?" —, um ciclo vicioso de porquês 
    que nos garante uma eterna insatisfação.</p>
    
    <p>Essa busca externa por respostas nos cega para a ausência de uma autocrítica real e nos impede de evoluir. 
    O desinteresse do ser humano por si mesmo é a raiz de todo o desequilíbrio. Como um estudante que entende 
    uma matéria, mas a rejeita por não ver sua "utilidade" imediata, nós abandonamos a jornada interior.</p>
    
    <div class='highlight-quote'>
    "Abandonamos a nós mesmos e, como consequência, criamos um mundo de fantasias e necessidades artificiais."
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Seção 2: Realidade Coletiva
    st.markdown("""
    <div class='manifesto-section'>
    <div class='manifesto-content'>
    <h4>🌐 A Realidade Coletiva: A Consciência do Status Quo</h4>
    <p>Para funcionar em grupo, a humanidade criou um consenso do que é real, normal e aceitável. 
    Essa é a <b>"Realidade"</b>, a consciência coletiva dominante, massiva e poderosa. Sua principal 
    função é a estabilidade e a previsibilidade.</p>
    
    <p>Ela nos protege do caos avassalador do universo, oferecendo um sistema operacional compartilhado, 
    cujos pilares são conceitos como "tempo", "sucesso", "família" e "normalidade". Contudo, sua maior 
    força é também sua maior limitação.</p>
    
    <div class='highlight-quote'>
    "Ao focar em medir e categorizar o mundo físico, ela nos torna escravos de uma regra que não tem exatidão."
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); margin: 20px 0;'>
        <h3 style='color: #ff6b6b; text-align: center;'>🎭 O Louco pelo Coletivo</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Gráfico do espectro louco-gênio
        fig = go.Figure()
        
        # Espectro de percepção
        x = np.linspace(-10, 10, 100)
        y = np.exp(-x**2/10) * np.sin(x) * 2
        
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(width=4, color='#ff6b6b'),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)',
            name='Espectro Consciencial'
        ))
        
        # Pontos críticos
        pontos = [
            (-6, "Visionário", "#ff6b6b"),
            (0, "Equilíbrio", "#4ecdc4"), 
            (6, "Gênio", "#ffd700")
        ]
        
        for x_val, nome, cor in pontos:
            fig.add_trace(go.Scatter(
                x=[x_val], y=[np.exp(-x_val**2/10) * np.sin(x_val) * 2],
                mode='markers+text',
                marker=dict(size=15, color=cor),
                text=nome,
                textposition='top center',
                name=nome
            ))
        
        fig.update_layout(
            title=dict(
                text="Espectro Louco-Gênio - A Dança da Percepção",
                font=dict(size=16, color='#ff6b6b')
            ),
            width=400,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                title="Desvio do Consenso",
                gridcolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                title="Potencial Transformador", 
                gridcolor='rgba(255,255,255,0.1)'
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 107, 107, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); margin-top: 20px;'>
        <h4 style='color: #ff6b6b; text-align: center;'>Características do "Louco"</h4>
        
        <div style='display: grid; grid-template-columns: 1fr; gap: 10px;'>
        <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ff6b6b;'>🔮 Visão Além do Consenso</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Percebe padrões invisíveis para a maioria</span>
        </div>
        
        <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ff6b6b;'>🎯 Isolamento Criativo</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Fase necessária de incubação interior</span>
        </div>
        
        <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ff6b6b;'>⚡ Sensibilidade Extrema</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Capta frequências cósmicas sutis</span>
        </div>
        
        <div style='background: rgba(255, 107, 107, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ff6b6b;'>🌪️ Caos Interno</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Processamento de informações expandidas</span>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Seção 3: Natureza da Realidade
        st.markdown("""
        <div class='manifesto-section'>
        <div class='manifesto-content'>
        <h4>⚡ A Natureza da Realidade: O Universo-Energia e o Humano-Antena</h4>
        <p>Como evoluímos de animais irracionais para seres tão complexos? A resposta não está na lógica, 
        mas na percepção. <b>Nós, humanos, somos animais que sentem a energia que paira no universo.</b></p>
        
        <p>Seja qual for sua origem — Big Bang, Deus, Odin ou Brahma —, uma energia primordial foi liberada 
        na criação. Tanto a física quanto a espiritualidade concordam: essa energia permeia tudo.</p>
        
        <div class='highlight-quote'>
        "O que chamamos de tempo não é uma força soberana, mas a manifestação da energia no mundo físico."
        </div>
        
        <p>Nesse oceano de frequências, cada ser humano funciona como uma <b>antena</b>. Estamos constantemente 
        sintonizando a rede de energias que envolve o cosmos, a natureza e as pessoas.</p>
        
        <div class='highlight-quote'>
        "Vivemos em um mundo tão barulhento que deixamos de escutar a voz do universo, perdidos no sentimento para com o Todo."
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2); margin: 20px 0;'>
        <h3 style='color: #ffd700; text-align: center;'>🌟 O Gênio pelo Cosmos</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualização da ponte cósmica
        fig = go.Figure()
        
        # Criar ponte entre dimensões
        x = np.linspace(-5, 5, 100)
        y = np.sin(x) * 2
        
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(width=6, color='#ffd700'),
            name='Ponte Consciencial',
            fill='tozeroy',
            fillcolor='rgba(255, 215, 0, 0.2)'
        ))
        
        # Adicionar dimensões
        fig.add_hline(y=3, line_dash="dash", line_color="rgba(255,255,255,0.3)")
        fig.add_hline(y=-3, line_dash="dash", line_color="rgba(255,255,255,0.3)")
        
        fig.add_annotation(x=-4, y=3, text="Mundo Quântico", showarrow=False, font=dict(color="#4ecdc4"))
        fig.add_annotation(x=-4, y=-3, text="Mundo Físico", showarrow=False, font=dict(color="#ff6b6b"))
        
        fig.update_layout(
            title=dict(
                text="Ponte entre Dimensões - A Função do Gênio",
                font=dict(size=16, color='#ffd700')
            ),
            width=400,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid rgba(255, 215, 0, 0.3);
                    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2); margin-top: 20px;'>
        <h4 style='color: #ffd700; text-align: center;'>Características do "Gênio"</h4>
        
        <div style='display: grid; grid-template-columns: 1fr; gap: 10px;'>
        <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ffd700;'>🌉 Tradução Consciencial</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Converte visões em linguagem acessível</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ffd700;'>🔄 Ponte Dimensional</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Conecta realidades quântica e física</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ffd700;'>🎨 Criatividade Aplicada</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Transforma caos em ordem creativa</span>
        </div>
        
        <div style='background: rgba(255, 215, 0, 0.1); padding: 10px; border-radius: 8px;'>
        <b style='color: #ffd700;'>⚡ Impacto Transformador</b><br>
        <span style='color: #d1d5db; font-size: 0.9em;'>Altera o curso da evolução coletiva</span>
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # Seção 4: Ruptura do Consenso
    st.markdown("""
    <div class='manifesto-section'>
    <div class='manifesto-content'>
    <h4>⚡ A Ruptura do Consenso: A Loucura como Potencial Evolutivo</h4>
    <p>O que o coletivo chama de "loucura" não é uma doença mental, mas um <b>estado de percepção 
    radicalmente diferente da norma</b>. É a consciência do indivíduo-antena que captou uma frequência 
    que os outros ainda não conseguem sintonizar.</p>
    
    <p>Sua função é a evolução e a ruptura; é a força que impede a consciência coletiva de estagnar. 
    Ao longo da história, visionários, profetas e gênios foram apenas antenas que captaram um sinal mais nítido.</p>
    
    <div class='highlight-quote'>
    "É o sentimento — a capacidade de ser afetado por essa energia — que nos define como humanos."
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Exemplos históricos
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.3);
                box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2); margin: 20px 0;'>
    <h3 style='color: #9333ea; text-align: center;'>📜 Arquétipos Históricos do Paradoxo</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(30, 41, 59, 0.8) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid #ff6b6b;
                    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2); text-align: center; height: 250px;'>
        <h4 style='color: #ff6b6b;'>🎨 Van Gogh</h4>
        <p style='color: #d1d5db; font-size: 0.9em;'>
        <b>Louco:</b> Cortou a própria orelha, internado<br>
        <b>Gênio:</b> Revolucionou a arte moderna<br>
        <b>Legado:</b> Visão além do visível
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(30, 41, 59, 0.8) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid #ffd700;
                    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2); text-align: center; height: 250px;'>
        <h4 style='color: #ffd700;'>⚡ Nikola Tesla</h4>
        <p style='color: #d1d5db; font-size: 0.9em;'>
        <b>Louco:</b> Obsessões, morreu na miséria<br>
        <b>Gênio:</b> Inventou o século XX<br>
        <b>Legado:</b> Energia livre e 3-6-9
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(30, 41, 59, 0.8) 100%); 
                    padding: 20px; border-radius: 15px; border: 2px solid #4ecdc4;
                    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2); text-align: center; height: 250px;'>
        <h4 style='color: #4ecdc4;'>☯️ Buddha</h4>
        <p style='color: #d1d5db; font-size: 0.9em;'>
        <b>Louco:</b> Abandonou tudo pela iluminação<br>
        <b>Gênio:</b> Iluminou milhões<br>
        <b>Legado:</b> Caminho do meio
        </p>
        </div>
        """, unsafe_allow_html=True)

    # Seção 5: Fronteira Decisiva
    st.markdown("""
    <div class='manifesto-section'>
    <div class='manifesto-content'>
    <h4>⚖️ A Fronteira Decisiva: A Interpretação do Caos</h4>
    <p>Isso nos leva à fronteira final da consciência. O que o coletivo chama de "realidade" é apenas um acordo. 
    Aqueles que percebem além desse acordo são confrontados com o caos. E é aqui que a linha é traçada.</p>
    
    <p>O "louco" e o "gênio" recebem a mesma descarga de energia, a mesma percepção avassaladora que quebra 
    a realidade comum. A diferença está na capacidade de processá-la.</p>
    
    <div class='highlight-quote'>
    "Qual é a diferença entre a genialidade e a loucura? O louco fica histérico com a loucura; o gênio interpreta a própria loucura."
    </div>
    
    <p>O gênio é um tradutor. Ele mergulha na energia caótica e a transforma em uma linguagem que, 
    eventualmente, pode ser integrada pela coletividade: uma nova teoria científica, uma obra de arte, 
    uma filosofia de vida. A loucura é o potencial; a genialidade é a sua tradução.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Seção 6: Conclusão
    st.markdown("""
    <div class='manifesto-section'>
    <div class='manifesto-content'>
    <h4>🌌 Conclusão: O Caminho da Coerência e a Evolução da Consciência</h4>
    <p>Nossos pré-conceitos e traumas são dados coletados durante milênios, gravados em nós. 
    Mas como chegar a uma resposta concreta sobre o comportamento humano quando vivemos doutrinados por estereótipos?</p>
    
    <p>A resposta é simples, porém complexa: para compreender um padrão, é preciso pensar dentro dele. 
    Como na série <em>Mindhunter</em>, onde agentes aprendem a pensar como um serial killer para entendê-lo, 
    a chave para a coerência é a <b>empatia radical</b>.</p>
    
    <div class='highlight-quote'>
    "Para sermos flexíveis e compreendermos o outro, temos que adotar temporariamente sua perspectiva, seja ele quem for."
    </div>
    
    <p>Quando paramos de julgar os erros alheios, algo acontece: começamos a enxergar os nossos próprios. 
    E percebemos que o importante, sempre, são os nossos próprios erros.</p>
    
    <div class='highlight-quote'>
    "Entender isso é entender o 'fim dos tempos'. Não se trata de um apocalipse, mas do fim de uma forma de ser."
    </div>
    
    <p>É o colapso de uma consciência coletiva que se tornou insustentável, criada pela necessidade 
    evolutiva de nossa própria existência. A verdadeira evolução não é sobre o que descobrimos lá fora, 
    mas sobre como interpretamos o caos que existe aqui dentro.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Equação final
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(74,74,170,0.4) 100%); 
                padding: 25px; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.5);
                text-align: center; margin: 20px 0;'>
    <h3 style='color: #9333ea;'>⚖️ Equação do Estado Final</h3>
    
    <div style='background: rgba(147, 51, 234, 0.1); padding: 15px; border-radius: 10px;'>
    <span style='color: #d1d5db; font-size: 1.2em;'>
    ∇·Ψ = √φ × Σ(3,6,9) × CoragemExistencial
    </span>
    </div>
    
    <p style='color: #d1d5db; margin-top: 15px;'>
    <b>Onde:</b><br>
    ∇·Ψ = Fluxo da Consciência Universal<br>
    φ = 1.618 (Proporção Áurea)<br>
    Σ(3,6,9) = Matriz Tesla da Criação<br>
    CoragemExistencial = Capacidade de suportar o paradoxo
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mensagem final
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%); 
                padding: 30px; border-radius: 15px; border: 2px solid rgba(99, 102, 241, 0.5);
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3); text-align: center; margin-top: 20px;'>
    <h3 style='color: #6366f1;'>🌌 O Verdict Final da Consciência</h3>
    
    <p style='color: #d1d5db; line-height: 1.6;'>
    <b>O "Fim dos Tempos" não é um apocalipse, mas o colapso de uma consciência coletiva 
    que se tornou insustentável.</b> A verdadeira evolução ocorre quando indivíduos 
    corajosos o suficiente para serem chamados de loucos traduzem sua visão em uma 
    linguagem que o coletivo pode assimilar, evoluindo assim toda a espécie.
    </p>
    
    <div style='background: rgba(99, 102, 241, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;'>
    <p style='color: #a1a1aa; font-style: italic; margin: 0;'>
    "Aos que ouvem o zumbido do universo: não cortem suas orelhas. 
    Aprendam a traduzir a sinfonia. O mundo precisa de sua loucura genial."
    </p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fechando o container principal
    
if section == "⚛️ Acelerador de Partículas":
    pagina_acelerador_particulas()
elif section == "🧮 Cálculos do Fluxo Matemático":
    pagina_calculos_fluxo_matematico()
else:
    # Para outras seções, mostrar uma mensagem padrão
    st.title(f"{section}")
    st.info("Esta seção está em desenvolvimento. Navegue para 'Acelerador de Partículas' ou 'Cálculos do Fluxo Matemático' para explorar as funcionalidades implementadas.")
    
# AGORA ATUALIZE O RODAPÉ PARA INCLUIR A NOVA SEÇÃO
# Rodapé cósmico
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🌌 CÓDIGO CÓSMICO
**Fluxo Matemático Universal**  
Integrando Ciência, Espiritualidade  
e Consciência Quântica

---
### 🔧 TECNOLOGIAS
**Streamlit • Plotly • Matplotlib • NetworkX  
NumPy • SciPy • SymPy • Pandas**

---
### 📊 DADOS CÓSMICOS
**Sinal Wow! • Sequência Fibonacci  
Proporção Áurea • Padrões 3-6-9**

---
### 🧠 FILOSOFIA INTEGRADA
**Tesla • Espinosa • Einstein  
Platão • Hermes • Sagan**

---
### 🔱 NOVA ICONOGRAFIA
**Mandala Cósmica • Símbolos Universais  
Tríade Perfeita • Rede de Conexões**
""")

# Instruções de execução
st.sidebar.info("""
💻 **Para executar localmente:**  
```bash
pip install streamlit plotly matplotlib 
pip install numpy scipy pillow sympy networkx
streamlit run cosmic_flow_universe.py
🌐 Acesse online:
Streamlit Cloud
GitHub Repository
""")
