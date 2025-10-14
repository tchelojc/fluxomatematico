import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import IsolationForest
import folium
from streamlit_folium import st_folium

# ==================================================
# Constantes Físicas
# ==================================================
c = 3e8  # Velocidade da luz em m/s
G = 6.67430e-11  # Constante gravitacional em m^3 kg^-1 s^-2
ano_luz = 9.461e15  # Distância que a luz percorre em um ano (em metros)
h = 6.626e-34  # Constante de Planck (J·s)
e = 1.602e-19  # Carga do elétron (C)
phi = 1.61803398875  # Proporção áurea

# ==================================================
# Funções de Cálculo
# ==================================================
def calcular_frequencias(frequencia_alvo, harmonico_aureo):
    """Calcula frequências harmônicas áureas."""
    return [frequencia_alvo * (1 + 0.61803398875)**i for i in range(harmonico_aureo)]

def detectar_anomalias_isolation_forest(dados):
    """Detecta anomalias usando Isolation Forest."""
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    anomalias = iso_forest.fit_predict(dados)
    return anomalias == -1  # Retorna True para anomalias

def distorcao_espaco_tempo(massa, distancia, modelo):
    """Calcula a distorção do espaço-tempo com base no modelo escolhido."""
    if modelo == "Clássico":
        return (2 * G * massa) / (c**2 * distancia)
    elif modelo == "Fluxo Matemático":
        return (2 * G * massa) / (c**2 * distancia) * np.exp(-distancia / (1e9 * ano_luz))
    else:
        return 0

def calcular_orbita(massa_bn, massa_planeta, perturbacao, num_passos=1000, dt=0.05):
    """Simula a órbita de um planeta em torno de um buraco negro."""
    posicao = np.array([1.0, 0.0])
    velocidade = np.array([0.0, 1.0])
    trajetoria = []
    energia_orbita = []
    
    for _ in range(num_passos):
        r = np.linalg.norm(posicao)
        aceleracao = -G * massa_bn / r**3 * posicao + perturbacao * np.random.normal(0, 1, 2)
        velocidade += aceleracao * dt
        posicao += velocidade * dt
        trajetoria.append(posicao.copy())
        energia_orbita.append(0.5 * massa_planeta * np.linalg.norm(velocidade)**2 - G * massa_bn * massa_planeta / r)
    
    return np.array(trajetoria), np.array(energia_orbita)

def calcular_colisao_asteroide(distancias_planetas, rotacoes_planetas, tamanhos_planetas):
    """Simula a possibilidade de colisão de asteroides com os planetas."""
    colisoes = []
    for i in range(len(distancias_planetas)):
        # Simulação simples: colisão se o asteroide estiver dentro do raio do planeta
        raio_planeta = tamanhos_planetas[i] * ano_luz
        colisoes.append(np.random.random() < 0.1)  # 10% de chance de colisão (exemplo)
    return colisoes

def aplicar_distorcao_espaco_tempo(probabilidades, tempo_decorrido, eventos, tempo_total=90):
    """Ajusta as probabilidades com base no tempo decorrido e nos eventos."""
    probabilidades_ajustadas = {}
    for evento, (prob_min, prob_max) in probabilidades.items():
        fator_correcao = 1 + (tempo_decorrido / tempo_total) * (np.mean([prob_min, prob_max]) / prob_min)
        fator_evento = 1 + (eventos * 0.05)  # Cada evento influencia a probabilidade em 5%
        probabilidades_ajustadas[evento] = (prob_min * fator_correcao * fator_evento, prob_max * fator_correcao * fator_evento)
    return probabilidades_ajustadas

def plotar_campo_magnetico(distancias_planetas, campo_magnetico):
    import plotly.graph_objects as go
    import streamlit as st

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=distancias_planetas,
        y=campo_magnetico,
        mode='lines+markers',
        name='Oscilação do Campo Magnético',
        line=dict(color='royalblue', width=2)
    ))

    fig.update_layout(
        title='Oscilações do Campo Magnético vs Distância dos Planetas',
        xaxis_title='Distância ao Astro Central (anos-luz)',
        yaxis_title='Intensidade do Campo Magnético (unidades arbitrárias)',
        template='plotly_dark'
    )

    st.plotly_chart(fig, use_container_width=True)

def energia_quantica_fluxo(frequencia):
    """Calcula a energia quântica de um fóton: E = h * f."""
    return h * frequencia

def tensao_fluxo(energia):
    """Calcula a tensão equivalente: V = E / e."""
    return energia / e

def calcular_campo_magnetico(distancias_planetas, massas_planetas):
    """Calcula as oscilações do campo magnético."""
    campo_magnetico = []
    for i in range(len(distancias_planetas)):
        # Simulação simples: campo magnético proporcional à massa e inversamente proporcional à distância
        campo_magnetico.append(massas_planetas[i] / distancias_planetas[i])
    return campo_magnetico

def grafico_escala_galaxia(df_resultados):
    """Gráfico 3D para representar eventos em escala galáctica."""
    # Adiciona uma coluna de probabilidade ajustada ao DataFrame
    df_resultados["Probabilidade Ajustada"] = df_resultados["Valor de Aplicação"] * 0.1  # Exemplo de cálculo

    fig = px.scatter_3d(
        df_resultados,
        x="Evento",
        y="Valor de Aplicação",
        z="Probabilidade Ajustada",
        size="Valor de Aplicação",
        color="Evento",
        title="Eventos Cósmicos em Escala Galáctica",
        labels={"Valor de Aplicação": "Impacto", "Probabilidade Ajustada": "Probabilidade"}
    )
    st.plotly_chart(fig)

# ==================================================
# Funções de Visualização
# ==================================================
def plotar_orbita(trajetoria):
    """Plota a trajetória da órbita em 2D."""
    fig, ax = plt.subplots()
    ax.plot(trajetoria[:, 0], trajetoria[:, 1], label="Órbita")
    ax.set_xlabel("X (anos-luz)")
    ax.set_ylabel("Y (anos-luz)")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

def plotar_orbita_3d(trajetoria):
    """Plota a trajetória da órbita em 3D."""
    z = np.linspace(0, 10, len(trajetoria))  # Simulação de altura ao longo do tempo
    fig = go.Figure(data=[go.Scatter3d(
        x=trajetoria[:, 0], y=trajetoria[:, 1], z=z,
        mode='lines',
        line=dict(color='blue', width=2),
    )])
    fig.update_layout(
        title="Trajetória da Órbita em 3D",
        scene=dict(
            xaxis_title="X (anos-luz)",
            yaxis_title="Y (anos-luz)",
            zaxis_title="Z (altura simulada)"
        ),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    st.plotly_chart(fig)

def plotar_energia(energia_orbita):
    """Plota a energia ao longo da órbita."""
    fig, ax = plt.subplots()
    ax.plot(energia_orbita, label="Energia Orbital")
    ax.set_xlabel("Passo de Tempo")
    ax.set_ylabel("Energia (J)")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

def plotar_energia_tempo(tempo, energia, titulo="Energia Armazenada"):
    """Plota a energia ao longo do tempo."""
    fig, ax = plt.subplots()
    ax.plot(tempo, energia, label=titulo, color='green')
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Energia (J)")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

def plotar_fluxo_3d(X, Y, Z, titulo="Fluxo de Energia no Espaço-Tempo"):
    """Plota o fluxo de energia em 3D."""
    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale="Viridis", opacity=0.7)])
    fig.update_layout(
        title=titulo,
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Energia (J)"
        ),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    st.plotly_chart(fig)
    
def plotar_colisoes_asteroides(distancias_planetas, colisoes):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.set_title("Colisões de Asteroides vs Distância dos Planetas")
    ax.set_xlabel("Planetas")
    ax.set_ylabel("Distância / Colisões")

    ax.plot(distancias_planetas, label="Distância dos Planetas (em AU)")
    ax.plot(colisoes, label="Número de Colisões de Asteroides")

    ax.legend()
    st.pyplot(fig)


def plotar_distorcao_espaco_tempo(X, Y, Z, astro_central, planetas, modelo):
    """Plota a distorção do espaço-tempo em 3D."""
    fig = go.Figure()
    
    # Malha do espaço-tempo
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale="Blues", opacity=0.7, name="Distorção do Espaço-Tempo"))
    
    # Astro Central
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[-distorcao_espaco_tempo(astro_central["massa"], astro_central["tamanho"] * ano_luz, modelo)],
        mode="markers",
        marker=dict(size=20, color="black", opacity=0.8),
        name="Astro Central"
    ))
    
    # Planetas
    for i, planeta in enumerate(planetas):
        fig.add_trace(go.Scatter3d(
            x=[planeta["distancia"]], y=[0], z=[-distorcao_espaco_tempo(planeta["massa"], planeta["tamanho"] * ano_luz, modelo)],
            mode="markers",
            marker=dict(size=10, color="red", opacity=0.8),
            name=f"Planeta {i+1}"
        ))
    
    # Configurações do gráfico
    fig.update_layout(
        title="Distorção do Espaço-Tempo e Interações Gravitacionais",
        scene=dict(
            xaxis_title="Distância (anos-luz)",
            yaxis_title="Y (anos-luz)",
            zaxis_title="Distorção do Espaço-Tempo"
        ),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    return fig

# ==================================================
# Módulo de Buracos Negros e Anomalias
# ==================================================
def modulo_buracos_negros():
    """Módulo principal para simulação de buracos negros e anomalias."""
    st.header("Buracos Negros e Anomalias")
    
    # Sidebar para entrada de dados
    st.sidebar.subheader("Entrada de Dados")
    modelo = st.sidebar.radio(
        "Escolha o Modelo", 
        ["Clássico", "Fluxo Matemático"], 
        key="modelo_radio_buracos_negros"
    )
    
    # Buraco Negro
    st.sidebar.subheader("Buraco Negro")
    massa_bn = st.sidebar.number_input(
        "Massa do Buraco Negro (kg)", 
        value=1e31, 
        format="%.2e", 
        min_value=0.0, 
        key="massa_bn"
    )
    tamanho_bn = st.sidebar.number_input(
        "Tamanho do Buraco Negro (anos-luz)", 
        value=0.01, 
        min_value=0.0, 
        key="tamanho_bn"
    )
    
    # Astros
    st.sidebar.subheader("Astros")
    num_astros = st.sidebar.number_input(
        "Número de Astros", 
        min_value=1, 
        max_value=5, 
        value=1, 
        key="num_astros"
    )
    massas_astros = []
    distancias_astros = []
    
    for i in range(num_astros):
        st.sidebar.write(f"Astro {i+1}")
        massa_astro = st.sidebar.number_input(
            f"Massa do Astro {i+1} (kg)", 
            value=1e30, 
            format="%.2e", 
            min_value=0.0, 
            key=f"massa_astro_{i}"
        )
        distancia_astro = st.sidebar.number_input(
            f"Distância do Astro {i+1} ao Buraco Negro (anos-luz)", 
            value=1000.0, 
            min_value=0.0, 
            key=f"distancia_astro_{i}"
        )
        massas_astros.append(massa_astro)
        distancias_astros.append(distancia_astro)
    
    # Planetas
    st.sidebar.subheader("Planetas")
    num_planetas = st.sidebar.number_input(
        "Número de Planetas", 
        min_value=1, 
        max_value=5, 
        value=1, 
        key="num_planetas"
    )
    massas_planetas = []
    
    for i in range(num_planetas):
        st.sidebar.write(f"Planeta {i+1}")
        massa_planeta = st.sidebar.number_input(
            f"Massa do Planeta {i+1} (kg)", 
            value=1e24, 
            format="%.2e", 
            min_value=0.0, 
            key=f"massa_planeta_{i}"
        )
        massas_planetas.append(massa_planeta)
    
    # Simulação de órbitas e energia
    st.subheader("Simulação de Órbitas e Energia")
    perturbacao = st.slider(
        "Intensidade da Perturbação (Matéria Escura)", 
        0.0, 0.1, 0.02, 
        key="perturbacao"
    )
    num_passos = st.sidebar.number_input(
        "Número de Passos na Simulação de Órbita", 
        min_value=100, 
        max_value=10000, 
        value=1000, 
        step=100,
        key="num_passos"
    )

    if st.button("Simular Órbita", key="simular_orbita"):
        trajetoria, energia_orbita = calcular_orbita(massa_bn, massas_planetas[0], perturbacao, num_passos=num_passos, dt=0.05)
        
        # Exibir gráficos
        st.subheader("Trajetória da Órbita 2D")
        plotar_orbita(trajetoria)
        
        st.subheader("Trajetória da Órbita 3D")
        plotar_orbita_3d(trajetoria)
        
        st.subheader("Energia ao Longo da Órbita")
        plotar_energia(energia_orbita)

        # Exportação de Resultados de Energia
        resultados_energia = pd.DataFrame({
            "Passo de Tempo": np.arange(num_passos),
            "Energia Orbital (J)": energia_orbita
        })
        csv_energia = resultados_energia.to_csv(index=False)
        st.download_button(
            "Baixar Resultados de Energia (CSV)", 
            csv_energia, 
            file_name="resultados_energia.csv", 
            key="download_energia"
        )
    else:
        st.warning("Nenhuma simulação de órbita foi executada. Clique em 'Simular Órbita' para gerar resultados.")

# ==================================================
# Módulo 2: Captação e Transformação de Energia
# ==================================================
def corrente_fluxo(P, V_F, theta_F):
    """Calcula a corrente em fluxo: I = P / (V_F * cos(theta_F))."""
    return P / (V_F * np.cos(np.radians(theta_F)))

def energia_perdida(E_F, alpha, R_l):
    """Calcula a energia perdida: E_p = E_F * alpha * R_l."""
    return E_F * alpha * R_l

def energia_singularidade(E_F, alpha, R_l):
    """Calcula a energia em singularidade: E_singularidade = E_F * (1 + alpha) / R_l."""
    return E_F * (1 + alpha) / R_l

def bobina_aurea(f_F, R_l):
    """Calcula a energia captada pela bobina áurea."""
    return (0.5 * 1e-3 * (f_F / R_l)**2)

def modulo_captacao_energia():
    """Módulo principal para captação e transformação de energia."""
    st.header("Captação e Transformação de Energia")
    
    # Sidebar para entrada de dados
    st.sidebar.subheader("Entrada de Dados")
    modelo = st.sidebar.radio(
        "Escolha o Modelo", 
        ["Clássico", "Fluxo Matemático"], 
        key="modelo_radio_captacao_energia"
    )

    # Parâmetros de energia
    st.sidebar.subheader("Parâmetros de Energia")
    P = st.sidebar.number_input("Potência Fornecida (W)", value=200.0, min_value=0.0, key="potencia_fornecida")
    f_F = st.sidebar.number_input("Frequência do Fluxo (Hz)", value=50.0, min_value=0.0, key="frequencia_fluxo")
    theta_F = st.sidebar.number_input("Ângulo do Fluxo (graus)", value=130.0, min_value=0.0, key="angulo_fluxo")
    R_l = st.sidebar.number_input("Resistência da Linha (Ω)", value=3.0, min_value=0.0, key="resistencia_linha")
    alpha = st.sidebar.number_input("Fator de Ajuste (α)", value=-23.8, min_value=-100.0, max_value=100.0, key="fator_ajuste")
    
    # Cálculos de energia
    E_F = energia_quantica_fluxo(f_F)
    V_F = tensao_fluxo(E_F)
    I_F = corrente_fluxo(P, V_F, theta_F)
    E_p = energia_perdida(E_F, alpha, R_l)
    E_singularidade = energia_singularidade(E_F, alpha, R_l)
    
    # Exibição dos resultados
    st.write(f"**Energia Quântica no Fluxo (E_F):** {E_F:.5e} J")
    st.write(f"**Tensão em Fluxo (V_F):** {V_F:.5e} V")
    st.write(f"**Corrente em Fluxo (I_F):** {I_F:.5e} A")
    st.write(f"**Energia Perdida (E_p):** {E_p:.5e} J")
    st.write(f"**Energia em Singularidade (E_singularidade):** {E_singularidade:.5e} J")
    
    # Gráfico de energia ao longo do tempo
    tempo = np.linspace(0, 0.1, 1000)
    energia_armazenada = (0.5 * 1e-3 * I_F**2) * (1 + alpha) * np.sin(2 * np.pi * f_F * tempo)
    plotar_energia_tempo(tempo, energia_armazenada, "Energia Armazenada (J)")
    
    # Visualização 3D do fluxo de energia
    st.subheader("Visualização 3D do Fluxo de Energia")
    x = np.linspace(-10, 10, 20)
    y = np.linspace(-10, 10, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * I_F  # Simulação de um campo de energia
    plotar_fluxo_3d(X, Y, Z, "Fluxo de Energia no Espaço-Tempo")
    
    # Bobina Áurea
    st.subheader("Bobina Áurea")
    energia_bobina = bobina_aurea(f_F, R_l)
    st.write(f"**Energia Captada pela Bobina Áurea:** {energia_bobina:.5e} J")
    
    # Exportação de Resultados
    resultados = {
        "Energia Quântica no Fluxo (E_F)": [E_F],
        "Tensão em Fluxo (V_F)": [V_F],
        "Corrente em Fluxo (I_F)": [I_F],
        "Energia Perdida (E_p)": [E_p],
        "Energia em Singularidade (E_singularidade)": [E_singularidade],
        "Energia Captada pela Bobina Áurea": [energia_bobina]
    }
    df = pd.DataFrame(resultados)
    
    # Botão para baixar CSV
    st.download_button(
        label="Baixar Resultados em CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="resultados_energia.csv",
        mime="text/csv",
        key="download_resultados_energia"
    )

def simular_translacao_planetas(massa_astro_central, massas_planetas, distancias_planetas, tamanhos_planetas, modelo, num_passos=1000, dt=0.05):
    """Simula o movimento de translação dos planetas ao redor do astro central."""
    trajetorias = []
    colisoes = []  # Armazenar informações sobre colisões
    
    for i in range(len(massas_planetas)):
        # Posição inicial do planeta (distância no eixo X)
        posicao = np.array([distancias_planetas[i], 0.0])
        velocidade = np.array([0.0, np.sqrt(G * massa_astro_central / distancias_planetas[i])])  # Velocidade orbital inicial
        trajetoria = []
        
        for _ in range(num_passos):
            r = np.linalg.norm(posicao)
            aceleracao = -G * massa_astro_central / r**3 * posicao  # Aceleração gravitacional
            
            # Aplicar perturbação no modelo de fluxo matemático
            if modelo == "Fluxo Matemático":
                aceleracao += np.random.normal(0, 1e-6, 2)  # Perturbação aleatória
            
            velocidade += aceleracao * dt
            posicao += velocidade * dt
            trajetoria.append(posicao.copy())
        
        trajetorias.append(np.array(trajetoria))
    
    # Verificar colisões entre planetas
    for i in range(len(trajetorias)):
        for j in range(i + 1, len(trajetorias)):
            distancias = np.linalg.norm(trajetorias[i] - trajetorias[j], axis=1)
            raio_total = tamanhos_planetas[i] + tamanhos_planetas[j]
            if np.any(distancias < raio_total):
                colisoes.append((i, j, np.where(distancias < raio_total)[0]))
    
    return trajetorias, colisoes

def plotar_translacao_planetas(trajetorias, colisoes, tamanhos_planetas):
    """Plota as trajetórias dos planetas ao redor do astro central e destaca colisões."""
    fig, ax = plt.subplots()
    for i, trajetoria in enumerate(trajetorias):
        ax.plot(trajetoria[:, 0], trajetoria[:, 1], label=f"Planeta {i+1}")
    
    # Destacar colisões
    for colisao in colisoes:
        i, j, passos = colisao
        for passo in passos:
            ax.scatter(trajetorias[i][passo, 0], trajetorias[i][passo, 1], color='red', s=100, label="Colisão" if passo == passos[0] else "")
    
    # Astro central
    ax.scatter([0], [0], color='yellow', s=200, label="Astro Central")
    
    ax.set_xlabel("X (anos-luz)")
    ax.set_ylabel("Y (anos-luz)")
    ax.legend()
    ax.grid()
    ax.set_title("Movimento de Translação dos Planetas")
    st.pyplot(fig)

def modulo_sistema_planetario():
    st.header("Sistema Planetário e Espaço-Tempo")
    
    # Sidebar para entrada de dados
    st.sidebar.subheader("Entrada de Dados")
    modelo = st.sidebar.radio("Escolha o Modelo", ["Clássico", "Fluxo Matemático"], key="modelo_radio_sistema_planetario")
    
    # Astro Central
    st.sidebar.subheader("Astro Central")
    massa_astro_central = st.sidebar.number_input("Massa do Astro Central (kg)", value=1e30, format="%.2e", min_value=0.0, key="massa_astro_central")
    tamanho_astro_central = st.sidebar.number_input("Tamanho do Astro Central (anos-luz)", value=0.01, min_value=0.0, key="tamanho_astro_central")
    
    # Planetas
    st.sidebar.subheader("Planetas")
    num_planetas = st.sidebar.number_input("Número de Planetas", min_value=1, max_value=5, value=1, key="num_planetas")
    massas_planetas = []
    tamanhos_planetas = []
    distancias_planetas = []
    rotacoes_planetas = []
    translacoes_planetas = []
    
    for i in range(num_planetas):
        st.sidebar.write(f"Planeta {i+1}")
        massa_planeta = st.sidebar.number_input(f"Massa do Planeta {i+1} (kg)", value=1e24, format="%.2e", min_value=0.0, key=f"massa_planeta_{i}")
        tamanho_planeta = st.sidebar.number_input(f"Tamanho do Planeta {i+1} (anos-luz)", value=0.0001, min_value=0.0, key=f"tamanho_planeta_{i}")
        distancia_planeta = st.sidebar.number_input(f"Distância do Planeta {i+1} ao Astro Central (anos-luz)", value=1.0, min_value=0.0, key=f"distancia_planeta_{i}")
        rotacao_planeta = st.sidebar.number_input(f"Rotação do Planeta {i+1} (horas)", value=24.0, min_value=0.0, key=f"rotacao_planeta_{i}")
        translacao_planeta = st.sidebar.number_input(f"Translação do Planeta {i+1} (dias)", value=365.0, min_value=0.0, key=f"translacao_planeta_{i}")
        
        massas_planetas.append(massa_planeta)
        tamanhos_planetas.append(tamanho_planeta)
        distancias_planetas.append(distancia_planeta)
        rotacoes_planetas.append(rotacao_planeta)
        translacoes_planetas.append(translacao_planeta)
    
    # Criando a malha do tecido espaço-tempo
    x = np.linspace(-2000, 2000, 20)
    y = np.linspace(-2000, 2000, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    # Aplicando a distorção gravitacional
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            r_astro_central = np.sqrt(X[i, j]**2 + Y[i, j]**2)
            Z[i, j] -= distorcao_espaco_tempo(massa_astro_central, r_astro_central * ano_luz, modelo)
            for k in range(num_planetas):
                r_planeta = np.sqrt((X[i, j] - distancias_planetas[k])**2 + Y[i, j]**2)
                Z[i, j] -= distorcao_espaco_tempo(massas_planetas[k], r_planeta * ano_luz, modelo)
    
    # Exibindo o gráfico 3D da distorção do espaço-tempo
    st.subheader("Distorção do Espaço-Tempo")
    fig_distorcao = plotar_distorcao_espaco_tempo(X, Y, Z, {"massa": massa_astro_central, "tamanho": tamanho_astro_central}, 
                                                 [{"massa": massas_planetas[i], "tamanho": tamanhos_planetas[i], "distancia": distancias_planetas[i]} for i in range(num_planetas)], modelo)
    st.plotly_chart(fig_distorcao)
    
    # Simulação de colisão de asteroides
    st.subheader("Possibilidade de Colisão de Asteroides")
    colisoes = calcular_colisao_asteroide(distancias_planetas, rotacoes_planetas, tamanhos_planetas)
    plotar_colisoes_asteroides(distancias_planetas, colisoes)
    
    # Oscilações do campo magnético
    st.subheader("Oscilações do Campo Magnético")
    campo_magnetico = calcular_campo_magnetico(distancias_planetas, massas_planetas)
    plotar_campo_magnetico(distancias_planetas, campo_magnetico)
    
    # Simulação do movimento de translação
    st.subheader("Movimento de Translação dos Planetas")
    if st.button("Simular Translação", key="simular_translacao"):
        trajetorias, colisoes = simular_translacao_planetas(massa_astro_central, massas_planetas, distancias_planetas, tamanhos_planetas, modelo)
        plotar_translacao_planetas(trajetorias, colisoes, tamanhos_planetas)
        
        # Exibir alerta de colisão
        if colisoes:
            st.warning("Colisão detectada entre planetas!")
        else:
            st.success("Nenhuma colisão detectada.")
    
    # Exportação de Resultados
    resultados = pd.DataFrame({
        "Corpo Celeste": ["Astro Central"] + [f"Planeta {i+1}" for i in range(num_planetas)],
        "Massa (kg)": [massa_astro_central] + massas_planetas,
        "Distorção do Espaço-Tempo": [distorcao_espaco_tempo(massa_astro_central, tamanho_astro_central * ano_luz, modelo)] + \
                                     [distorcao_espaco_tempo(massas_planetas[i], tamanhos_planetas[i] * ano_luz, modelo) for i in range(num_planetas)]
    })
    csv = resultados.to_csv(index=False)
    st.download_button("Baixar Resultados (CSV)", csv, file_name="resultados_sistema_planetario.csv", key="download_resultados_sistema_planetario")
    
# ==================================================
# Módulo 4: Frequências Áureas e Territórios
# ==================================================
def modulo_frequencias_aureas():
    st.header("Frequências Áureas e Territórios")
    st.markdown("""
        Este módulo analisa as frequências harmônicas áureas em territórios, identificando desequilíbrios térmicos, energéticos e gravitacionais.
        Use os controles na barra lateral para ajustar os parâmetros e explore as visualizações interativas.
    """)
    
    # Sidebar para entrada de dados
    st.sidebar.subheader("⚙️ Configurações do Simulador")
    frequencia_alvo = st.sidebar.slider("Frequência Alvo (Hz)", 100, 1000, 432, 10, key="frequencia_alvo")
    alpha = st.sidebar.slider("Fator de Gratidão Quântica (α)", 0.0, 1.0, 0.5, 0.1, key="fator_gratidao_quantica")
    harmonico_aureo = st.sidebar.slider("Número de Harmônicos Áureos", 1, 10, 3, 1, key="harmonico_aureo")
    
    latitude = st.sidebar.number_input("Latitude", -90.0, 90.0, -23.5505, key="latitude")
    longitude = st.sidebar.number_input("Longitude", -180.0, 180.0, -46.6333, key="longitude")
    raio = st.sidebar.slider("Raio de Busca (km)", 1, 100, 10, key="raio_busca")
    num_pontos = st.sidebar.slider("Número de Pontos Térmicos", 10, 500, 100, key="num_pontos")
    
    # Simulação de dados térmicos
    np.random.seed(42)
    latitudes = latitude + np.random.uniform(-0.1, 0.1, num_pontos)
    longitudes = longitude + np.random.uniform(-0.1, 0.1, num_pontos)
    temperaturas = np.random.uniform(20, 40, num_pontos)
    desequilibrios = np.abs(temperaturas - np.mean(temperaturas))
    
    # Cálculo de frequências harmônicas áureas
    frequencias = calcular_frequencias(frequencia_alvo, harmonico_aureo)
    
    # Simulação de sinal detectado
    tempo = np.linspace(0, 0.1, num_pontos)
    sinal_detectado = np.sum([np.sin(2 * np.pi * f * tempo) * np.exp(-0.1 * tempo) for f in frequencias], axis=0)
    sinal_detectado /= np.max(np.abs(sinal_detectado))
    
    # Cálculo de energia e radiação
    energia_armazenada = (0.5 * 1e-3 * sinal_detectado**2) * (1 + alpha)
    radiacao_termica = 5.67e-8 * (temperaturas + 273.15)**4
    
    # Simulação da distorção da gravidade
    M_equivalente = energia_armazenada / (c**2)
    distorcao_gravidade = (2 * G * M_equivalente) / (c**2 * 1e-9)
    
    # Detectar anomalias com Isolation Forest
    dados_anomalias = np.column_stack((desequilibrios, distorcao_gravidade, radiacao_termica, energia_armazenada))
    anomalias = detectar_anomalias_isolation_forest(dados_anomalias)
    
    # Criando abas
    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        "Frequências e Desequilíbrios", "Energia e Radiação", "Mapa Interativo", "Distorção Gravitacional", "Desequilíbrios por Zona"
    ])
    
    # Aba 1: Frequências e Desequilíbrios
    with aba1:
        st.subheader("Relação entre Frequências Harmônicas e Desequilíbrios Térmicos")
        ressonancia = np.array(frequencias) * alpha
        desequilibrios_ressonancia = desequilibrios[:len(ressonancia)]
        
        fig, ax = plt.subplots()
        ax.scatter(ressonancia, desequilibrios_ressonancia, c='purple', label="Ressonância Magnética")
        ax.plot(ressonancia, desequilibrios_ressonancia, color='orange', linestyle='--', label="Tendência")
        ax.set_xlabel("Frequência Harmônica (Hz)")
        ax.set_ylabel("Desequilíbrio Térmico (°C)")
        ax.legend()
        ax.grid()
        st.pyplot(fig)
    
    # Aba 2: Energia e Radiação
    with aba2:
        st.subheader("Energia e Radiação Térmica")
        
        # Gráfico de energia armazenada
        fig, ax = plt.subplots()
        ax.plot(tempo, energia_armazenada, label="Energia Armazenada (J)", color='green')
        ax.set_xlabel("Tempo (s)")
        ax.set_ylabel("Energia (J)")
        ax.legend()
        ax.grid()
        st.pyplot(fig)
        
        # Gráfico de radiação térmica
        fig, ax = plt.subplots()
        ax.plot(temperaturas, radiacao_termica, label="Radiação Térmica (W/m²)", color='red')
        ax.set_xlabel("Temperatura (°C)")
        ax.set_ylabel("Radiação (W/m²)")
        ax.legend()
        ax.grid()
        st.pyplot(fig)
    
    # Aba 3: Mapa Interativo
    with aba3:
        st.subheader("Mapa de Desequilíbrios e Anomalias")
        mapa = folium.Map(location=[latitude, longitude], zoom_start=12)
        
        # Adicionar marcadores para desequilíbrios térmicos
        for lat, lon, temp, deseq, energia, radiacao, distorcao, anomalia in zip(latitudes, longitudes, temperaturas, desequilibrios, energia_armazenada, radiacao_termica, distorcao_gravidade, anomalias):
            cor = "red" if anomalia else "blue"
            popup = f"Temperatura: {temp:.1f}°C<br>Desequilíbrio: {deseq:.1f}°C<br>Energia: {energia:.2f} J<br>Radiação: {radiacao:.2f} W/m²<br>Distorção: {distorcao:.2e} m/s²"
            folium.CircleMarker(location=[lat, lon], radius=6, color=cor, fill=True, fill_color=cor, fill_opacity=0.7, popup=popup).add_to(mapa)
        
        st_folium(mapa)
    
    # Aba 4: Distorção Gravitacional
    with aba4:
        st.subheader("Simulação de Distorção Gravitacional e Anomalias")
        
        # Visualização 3D da distorção gravitacional
        fig = go.Figure(data=[go.Surface(z=np.random.rand(20, 20), colorscale='inferno')])
        fig.update_layout(title="Distorção Gravitacional 3D", scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Intensidade Gravitacional"))
        st.plotly_chart(fig)
        
        # Explicação dos valores críticos
        st.markdown("""
            **Valores Críticos para Distorção Espaço-Temporal:**
            - **Distorção Gravitacional > 1e-5 m/s²**: Indica uma curvatura significativa no espaço-tempo.
            - **Energia Armazenada > 1 J**: Pode criar uma distorção localizada.
            - **Radiação Térmica > 500 W/m²**: Associada a eventos extremos.
        """)
    
    # Aba 5: Desequilíbrios por Zona
    with aba5:
        st.subheader("Desequilíbrios por Zona e Catástrofes")
        st.markdown("""
            Esta aba mostra os desequilíbrios por zona, destacando áreas críticas onde podem ocorrer catástrofes como terremotos, furacões ou outros eventos.
            As cores indicam a intensidade dos desequilíbrios:
            - **Vermelho**: Áreas críticas (alto risco de catástrofes).
            - **Amarelo**: Áreas moderadas (risco médio).
            - **Verde**: Áreas estáveis (baixo risco).
        """)
        
        # Mapa de desequilíbrios por zona
        mapa_desequilibrios = folium.Map(location=[latitude, longitude], zoom_start=12)
        
        # Adicionar marcadores para desequilíbrios por zona
        for lat, lon, deseq in zip(latitudes, longitudes, desequilibrios):
            if deseq > 10:  # Área crítica
                cor = "red"
            elif deseq > 5:  # Área moderada
                cor = "yellow"
            else:  # Área estável
                cor = "green"
            
            popup = f"Desequilíbrio: {deseq:.1f}°C"
            folium.CircleMarker(location=[lat, lon], radius=6, color=cor, fill=True, fill_color=cor, fill_opacity=0.7, popup=popup).add_to(mapa_desequilibrios)
        
        st_folium(mapa_desequilibrios)
    
    # Exportação de Resultados
    resultados = pd.DataFrame({
        "Latitude": latitudes,
        "Longitude": longitudes,
        "Temperatura (°C)": temperaturas,
        "Desequilíbrio Térmico (°C)": desequilibrios,
        "Energia Armazenada (J)": energia_armazenada,
        "Radiação Térmica (W/m²)": radiacao_termica,
        "Distorção Gravitacional (m/s²)": distorcao_gravidade,
        "Anomalia": anomalias
    })
    csv = resultados.to_csv(index=False)
    st.download_button("Baixar Resultados (CSV)", csv, file_name="resultados_frequencias_aureas.csv", key="download_resultados_frequencias_aureas")
    
# ==================================================
# Módulo 5: Aplicações e Cálculo Infinito
# ==================================================
def calcular_aplicacoes(probabilidades_ajustadas, valor_esperado):
    """Calcula as aplicações com base nas probabilidades ajustadas e no valor esperado."""
    aplicacoes = {}
    for evento, (prob_min, prob_max) in probabilidades_ajustadas.items():
        aplicacoes[evento] = valor_esperado * (prob_min + prob_max) / 2
    return aplicacoes

def grafico_escala_sistema_solar(df_resultados):
    """Gráfico 3D para representar eventos em escala do sistema solar."""
    fig = px.scatter_3d(
        df_resultados,
        x="Evento",
        y="Valor de Aplicação",
        z="Probabilidade Ajustada",
        size="Valor de Aplicação",
        color="Evento",
        title="Eventos Cósmicos em Escala do Sistema Solar",
        labels={"Valor de Aplicação": "Impacto", "Probabilidade Ajustada": "Probabilidade"}
    )
    st.plotly_chart(fig)

def simular_distorcao_espaco_tempo(probabilidades_ajustadas):
    """Simula a distorção do tecido espaço-tempo."""
    eventos = list(probabilidades_ajustadas.keys())
    distorcao = [np.random.normal(0, 1) for _ in eventos]
    
    fig, ax = plt.subplots()
    ax.bar(eventos, distorcao, color='purple', label="Distorção do Espaço-Tempo")
    ax.set_xlabel("Evento")
    ax.set_ylabel("Intensidade da Distorção")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

def modulo_aplicacoes_infinitas():
    st.header("Aplicações e Cálculo Infinito")
    st.markdown("""
        Este módulo projeta dinamicamente as **ODDS (probabilidades)** de eventos cósmicos,
        ajustando-as com base no tempo decorrido e em eventos significativos. Use os controles abaixo para definir
        as ODDS, o valor esperado de energia ou impacto, e simular a influência do tempo e eventos.
    """)
    
    # Sidebar com instruções e feedback
    st.sidebar.header("⚙️ Como Usar")
    st.sidebar.markdown("""
        1. **Defina as ODDS**: Ajuste as probabilidades para cada tipo de evento cósmico com base em dados reais e cálculos matemáticos.
        2. **Insira o Valor Esperado**: Defina o valor esperado de energia ou impacto para cada evento cósmico.
        3. **Informe o Tempo e Eventos**: Insira o tempo decorrido e os eventos significativos para calcular projeções futuras.
        4. **Calcule a Projeção**: Clique em "Calcular Projeção de ODDS" para ver os resultados e análises.
    """)
    
    # Entrada das probabilidades com intervalos
    st.header("Defina as Probabilidades dos Eventos Cósmicos")
    probabilidades = {
        "Colisão de Asteroides": st.slider("Colisão de Asteroides", min_value=1.01, max_value=10.0, value=(1.75, 1.75), key="colisao_asteroides"),
        "Explosão de Supernova": st.slider("Explosão de Supernova", min_value=1.01, max_value=10.0, value=(3.0, 4.5), key="explosao_supernova"),
        "Formação de Buraco Negro": st.slider("Formação de Buraco Negro", min_value=1.01, max_value=10.0, value=(3.2, 3.2), key="formacao_buraco_negro"),
        "Passagem de Cometa": st.slider("Passagem de Cometa", min_value=1.01, max_value=10.0, value=(2.0, 3.5), key="passagem_cometa"),
        "Erupção Solar": st.slider("Erupção Solar", min_value=1.01, max_value=10.0, value=(2.5, 6.5), key="erupcao_solar"),
        "Alinhamento Planetário": st.slider("Alinhamento Planetário", min_value=1.01, max_value=10.0, value=(1.5, 2.5), key="alinhamento_planetario"),
        "Choque de Galáxias": st.slider("Choque de Galáxias", min_value=1.01, max_value=25.0, value=(5.5, 23.0), key="choque_galaxias"),
        "Formação de Estrela": st.slider("Formação de Estrela", min_value=1.01, max_value=20.0, value=(4.5, 13.5), key="formacao_estrela")
    }
    
    # Entrada do valor esperado, tempo decorrido e eventos
    valor_esperado = st.number_input("Valor Esperado de Energia ou Impacto", min_value=1.0, step=0.1, value=3.0, key="valor_esperado")
    tempo_decorrido = st.number_input("Tempo decorrido (minutos)", min_value=0, max_value=90, value=0, key="tempo_decorrido")
    eventos = st.number_input("Eventos significativos (colisões, explosões, etc.)", min_value=0, max_value=10, value=0, key="eventos_significativos")
    
    # Aplicar distorção espaço-tempo às probabilidades
    probabilidades_ajustadas = aplicar_distorcao_espaco_tempo(probabilidades, tempo_decorrido, eventos)
    
    # Calcular aplicações iniciais
    if st.button("Calcular Projeção de Probabilidades", key="calcular_projecao"):
        aplicacoes = calcular_aplicacoes(probabilidades_ajustadas, valor_esperado)
        st.session_state["aplicacoes"] = aplicacoes

        # Exibir resultados em uma tabela
        st.write("Projeção de Probabilidades com base no tempo e eventos:")
        df_resultados = pd.DataFrame(aplicacoes.items(), columns=["Evento", "Valor de Aplicação"])
        st.dataframe(df_resultados)

        # Gráficos interativos
        grafico_escala_galaxia(df_resultados)
        grafico_escala_sistema_solar(df_resultados)

        # Simulação da distorção do tecido espaço-tempo
        simular_distorcao_espaco_tempo(probabilidades_ajustadas)

        # Gráfico de comparação de probabilidades (antes e depois do ajuste)
        eventos_keys = list(probabilidades_ajustadas.keys())
        prob_min_antes = [probabilidades[evento][0] for evento in eventos_keys]
        prob_max_antes = [probabilidades[evento][1] for evento in eventos_keys]
        prob_min_depois = [probabilidades_ajustadas[evento][0] for evento in eventos_keys]
        prob_max_depois = [probabilidades_ajustadas[evento][1] for evento in eventos_keys]

        fig, ax = plt.subplots()
        ax.plot(eventos_keys, prob_min_antes, label="Probabilidade Mínima (Antes)", marker="o")
        ax.plot(eventos_keys, prob_max_antes, label="Probabilidade Máxima (Antes)", marker="o")
        ax.plot(eventos_keys, prob_min_depois, label="Probabilidade Mínima (Depois)", marker="x")
        ax.plot(eventos_keys, prob_max_depois, label="Probabilidade Máxima (Depois)", marker="x")
        ax.set_xlabel("Evento Cósmico")
        ax.set_ylabel("Valor da Probabilidade")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

# ==================================================
# Módulo 6: Ajuda e Orientação
# ==================================================
def modulo_ajuda_orientacao():
    st.header("Ajuda e Orientação")
    st.markdown("""
        Bem-vindo à aba de **Ajuda e Orientação**! Aqui você encontrará exemplos práticos, comparações com dados reais e orientações para utilizar os módulos do Universo Áureo de forma eficiente.
    """)
    
    st.subheader("📊 Exemplos Práticos e Comparações")
    st.markdown("""
        - **Colisões Reais**: Compare colisões de asteroides, explosões de supernovas e outros eventos cósmicos com dados reais.
            - [Dados de Colisões de Asteroides (NASA)](https://cneos.jpl.nasa.gov/)
            - [Explosões de Supernovas (ESA)](https://www.esa.int/)
        - **Gravidades Comparadas**: Analise a gravidade de planetas, estrelas e buracos negros conhecidos.
            - [Gravidade de Planetas (NASA)](https://solarsystem.nasa.gov/)
            - [Buracos Negros (Event Horizon Telescope)](https://eventhorizontelescope.org/)
        - **Planetas Habitáveis**: Explore dados de exoplanetas potencialmente habitáveis e compare suas características.
            - [Exoplanetas Habitáveis (NASA Exoplanet Archive)](https://exoplanetarchive.ipac.caltech.edu/)
        - **Distorções Gravitacionais**: Identifique anomalias gravitacionais e portais dimensionais com base em cálculos precisos.
            - [Anomalias Gravitacionais (LIGO)](https://www.ligo.org/)
    """)
    
    st.subheader("🔧 Como Fazer")
    st.markdown("""
        - **Bobina Áurea**: Aprenda a criar e ajustar uma bobina áurea para captação e transformação de energia.
            - **Passo a Passo**:
                1. Defina os parâmetros de frequência e harmônicos áureos.
                2. Utilize os cálculos de energia quântica para otimizar a bobina.
                3. Aplique a correção de valores proporcionais para equilibrar o sistema.
        - **Correção de Valores Proporcionais**: Utilize o diferencial de valores para corrigir desequilíbrios em sistemas cósmicos.
            - **Exemplo**: Calcule a diferença de gravidade entre dois corpos celestes e ajuste os valores para equilibrar o sistema.
        - **Mapa de Anomalias**: Saiba como identificar e mapear distorções gravitacionais e portais dimensionais.
            - **Exemplo**: Utilize dados de telescópios e satélites para localizar anomalias gravitacionais.
    """)
    
    st.subheader("📈 Cálculos e Projeções")
    st.markdown("""
        - **Diferencial Gravitacional**: Calcule a diferença de gravidade entre corpos celestes e seu impacto no espaço-tempo.
            - **Fórmula**: `Δg = g1 - g2`, onde `g1` e `g2` são as gravidades dos corpos celestes.
        - **Sobreposições de Indicações**: Analise como as anomalias afetam ou sobrepõem outros corpos celestes.
            - **Exemplo**: Sobreponha mapas de gravidade e temperatura para identificar regiões críticas.
        - **Projeções de Eventos**: Utilize dados reais para projetar eventos cósmicos futuros e suas consequências.
            - **Exemplo**: Projete a trajetória de um asteroide e calcule o impacto na Terra.
    """)
    
    st.subheader("❓ Dúvidas Frequentes")
    st.markdown("""
        - **O que são ODDS?**: ODDS são probabilidades ajustadas com base em eventos cósmicos e cálculos matemáticos.
        - **Como calcular eventos futuros?**: Utilize os dados atuais e as leis da física para projetar eventos cósmicos.
        - **Onde encontrar dados reais?**: Consulte bancos de dados astronômicos, como a NASA ou a ESA, para obter informações precisas.
    """)
    
    st.subheader("🌌 Gráficos de Anomalias")
    st.markdown("""
        Aqui está um exemplo de gráfico de anomalias gravitacionais:
    """)
    
    # Exemplo de gráfico de anomalias
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Dados de exemplo
    x = np.linspace(-10, 10, 100)
    y = np.sin(x) + np.random.normal(0, 0.1, 100)
    
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Anomalia Gravitacional")
    ax.set_xlabel("Posição (anos-luz)")
    ax.set_ylabel("Intensidade Gravitacional")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

# ==================================================
# Aplicativo Principal
# ==================================================
def main():
    st.sidebar.title("Universo Áureo")
    modulo = st.sidebar.radio(
        "Escolha o Módulo",
        [
            "Buracos Negros e Anomalias",
            "Captação e Transformação de Energia",
            "Sistema Planetário e Espaço-Tempo",
            "Frequências Áureas e Territórios",
            "Aplicações e Cálculo Infinito",
            "Ajuda e Orientação"
        ],
        key="modulo_principal"  # Chave única para o menu principal
    )

    if modulo == "Buracos Negros e Anomalias":
        modulo_buracos_negros()
    elif modulo == "Captação e Transformação de Energia":
        modulo_captacao_energia()
    elif modulo == "Sistema Planetário e Espaço-Tempo":
        modulo_sistema_planetario()
    elif modulo == "Frequências Áureas e Territórios":
        modulo_frequencias_aureas()
    elif modulo == "Aplicações e Cálculo Infinito":
        modulo_aplicacoes_infinitas()
    elif modulo == "Ajuda e Orientação":
        modulo_ajuda_orientacao()

# Executar o aplicativo
if __name__ == "__main__":
    main()
