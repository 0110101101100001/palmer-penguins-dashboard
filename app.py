from flask import Flask, render_template, send_file, request, jsonify
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from sklearn.preprocessing import LabelEncoder
import io
import matplotlib
import os

# Garante que o Matplotlib rode corretamente no servidor sem interface gráfica
matplotlib.use('Agg')

app = Flask(__name__)

# Configurações de Design Dracula
FOREGROUND = '#f8f8f2'
PURPLE = '#bd93f9'
PINK = '#ff79c6'
GREEN = '#50fa7b'
GRAFICO_SIZE = (7.5, 4.5) 
DPI_PADRAO = 100

def carregar_dados():
    try:
        # Pega o caminho absoluto para evitar erros de diretório
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'penguins.csv')
        return pd.read_csv(file_path).dropna()
    except:
        return pd.DataFrame()

def config_layout_adaptativo(fig, ax, tema):
    cor_texto = '#282a36' if tema == 'light' else '#f8f8f2'
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    ax.tick_params(colors=cor_texto)
    ax.xaxis.label.set_color(cor_texto)
    ax.yaxis.label.set_color(cor_texto)
    ax.title.set_color(cor_texto)
    for spine in ax.spines.values(): 
        spine.set_edgecolor('#44475a' if tema == 'dark' else '#d1d1d1')

@app.route('/')
def index():
    df_limpo = carregar_dados()
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'penguins.csv')
    
    # 1. Tabela de Amostra (Preview)
    preview_html = df_limpo.head(8).to_html(classes='table-data', index=False)
    
    # 2. Panorama Estatístico
    stats_html = df_limpo.describe(include='all').T.reset_index().to_html(classes='table-data', index=False)
    
    # 3. Diagnóstico de Nulos: ANTES (Arquivo Bruto)
    df_raw = pd.read_csv(file_path)
    null_before_html = df_raw.isnull().sum().to_frame().reset_index().rename(
        columns={'index': 'Variável', 0: 'Nulos'}
    ).to_html(classes='table-data', index=False)
    
    # 4. Diagnóstico de Nulos: DEPOIS (Dataset Limpo)
    null_after_html = df_limpo.isnull().sum().to_frame().reset_index().rename(
        columns={'index': 'Variável', 0: 'Nulos'}
    ).to_html(classes='table-data', index=False)
    
    return render_template('index.html', 
                           preview_table=preview_html,
                           stats_table=stats_html, 
                           null_before=null_before_html,
                           null_after=null_after_html)

@app.route('/download')
def download_data():
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'penguins.csv')
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)   

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        f = float(data.get('flipper'))
        b = float(data.get('bill_len'))
        # Lógica Simples de IA (Substitua por modelo treinado se desejar)
        if f >= 206: res, exp = "Gentoo", "Nadadeira longa detectada."
        elif b >= 43: res, exp = "Chinstrap", "Bico alongado detectado."
        else: res, exp = "Adélie", "Porte compacto detectado."
        return jsonify({"especie": res, "explica": exp})
    except: return jsonify({'error': 'Erro'}), 400

@app.route('/limpar-dataset', methods=['POST'])
def limpar_dataset():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado", 400
    
    file = request.files['file']
    if file.filename == '':
        return "Nome de arquivo inválido", 400

    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        # Aplica a limpeza (remove nulos)
        df_limpo = df.dropna()
        
        output = io.BytesIO()
        df_limpo.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype="text/csv",
            as_attachment=True,
            download_name="dataset_limpo.csv"
        )
    return "Formato inválido", 400

@app.route('/chart/barras')
def chart_barras():
    tema = request.args.get('tema', 'dark')
    df = carregar_dados()
    fig = Figure(figsize=GRAFICO_SIZE, dpi=DPI_PADRAO)
    ax = fig.subplots()
    sns.countplot(data=df, x='species', hue='species', palette=[PURPLE, PINK, GREEN], legend=False, ax=ax)
    ax.set_title('Volume Amostral por Espécie', fontweight='bold', pad=20)
    config_layout_adaptativo(fig, ax, tema)
    return fig_to_img(fig)

@app.route('/chart/dispersao')
def chart_dispersao():
    tema = request.args.get('tema', 'dark')
    df = carregar_dados()
    # Configuração para evitar fundo branco no Seaborn
    sns.set_style("whitegrid", {'axes.facecolor': 'none', 'figure.facecolor': 'none'})
    
    # Criação do Pairplot
    g = sns.pairplot(df, hue='species', palette=[PURPLE, PINK, GREEN], height=1.5, aspect=1.3)
    g.fig.set_size_inches(GRAFICO_SIZE[0], GRAFICO_SIZE[1])
    
    cor_texto = '#282a36' if tema == 'light' else '#f8f8f2'
    for ax in g.axes.flatten():
        if ax:
            ax.tick_params(colors=cor_texto, labelsize=8)
            ax.xaxis.label.set_color(cor_texto)
            ax.yaxis.label.set_color(cor_texto)
            ax.patch.set_alpha(0)
    
    img = io.BytesIO()
    g.savefig(img, format='png', bbox_inches='tight', transparent=True, dpi=DPI_PADRAO)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/chart/dinamico')
def chart_dinamico():
    tema = request.args.get('tema', 'dark')
    ilha = request.args.get('ilha', 'Todas')
    sexo = request.args.get('sexo', 'Todos')
    metrica = request.args.get('metrica', 'body_mass_g')
    
    # 1. Carga e Limpeza idêntica ao Heatmap
    df = carregar_dados() # Já executa o dropna()
    
    # 2. Filtro de Integridade: Garante que a métrica existe antes de processar
    if df.empty or metrica not in df.columns:
        fig = Figure(figsize=GRAFICO_SIZE, dpi=DPI_PADRAO)
        ax = fig.subplots()
        ax.text(0.5, 0.5, "Coluna não encontrada\nou Dataset vazio", ha='center', va='center')
        return fig_to_img(fig)

    # 3. Aplicação dos Filtros (Ilha e Sexo)
    if ilha != 'Todas':
        df = df[df['island'] == ilha]
    if sexo != 'Todos':
        df = df[df['sex'] == sexo.upper()]

    fig = Figure(figsize=GRAFICO_SIZE, dpi=DPI_PADRAO)
    ax = fig.subplots()
    
    # 4. Renderização do Gráfico com Dados Sanitizados
    if not df.empty:
        # Usamos o boxplot para visualizar a distribuição da métrica limpa por espécie
        sns.boxplot(data=df, x='species', y=metrica, palette=[PURPLE, PINK, GREEN], ax=ax, hue='species', legend=False)
    
    titulos = {
        'body_mass_g': 'Massa Corporal (g)',
        'flipper_length_mm': 'Comprimento da Nadadeira (mm)',
        'bill_length_mm': 'Comprimento do Bico (mm)',
        'bill_depth_mm': 'Profundidade do Bico (mm)'
    }
    
    ax.set_title(f"{titulos.get(metrica, 'Análise')}: {ilha} | {sexo}", fontweight='bold', pad=20)
    config_layout_adaptativo(fig, ax, tema)
    return fig_to_img(fig)

@app.route('/chart/heatmap')
def chart_heatmap():
    tema = request.args.get('tema', 'dark')
    df = carregar_dados()
    le = LabelEncoder()
    # Pré-processamento rápido para o Heatmap
    df_encoded = df.copy()
    df_encoded['species'] = le.fit_transform(df_encoded['species'])
    df_corr = pd.get_dummies(df_encoded, columns=['island', 'sex'], drop_first=True).astype(float)
    
    fig = Figure(figsize=GRAFICO_SIZE, dpi=DPI_PADRAO)
    ax = fig.subplots()
    sns.heatmap(df_corr.corr(), annot=True, cmap='magma' if tema == 'dark' else 'coolwarm', 
                fmt=".2f", ax=ax, annot_kws={"color": "white" if tema == 'dark' else "black"})
    ax.set_title('Matriz de Correlação das Features', fontweight='bold', pad=20)
    config_layout_adaptativo(fig, ax, tema)
    return fig_to_img(fig)

def fig_to_img(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', transparent=True)
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)