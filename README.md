# 🐧 Palmer Penguins: Data Science Pipeline Dashboard

> **Status:** ![Em Desenvolvimento](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=flat-square)
> **Stack:** ![Python](https://img.shields.io/badge/Python-3.x-bd93f9?style=flat-square) ![Flask](https://img.shields.io/badge/Framework-Flask-ff79c6?style=flat-square)
> **UI:** ![Dracula Theme](https://img.shields.io/badge/Theme-Dracula_Glass-8be9fd?style=flat-square)

Este projeto é um dashboard interativo focado no processamento e análise do dataset **Palmer Penguins**. A aplicação utiliza uma estética de ambiente de desenvolvimento (IDE) para guiar o usuário através de um pipeline completo de Ciência de Dados, desde a ingestão bruta até a predição baseada em heurísticas morfológicas.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Framework Web:** Flask
* **Processamento de Dados:** Pandas & NumPy
* **Visualização:** Seaborn & Matplotlib
* **Frontend:** HTML5, CSS3 (Glassmorphism) e JavaScript

## 🚀 Estrutura do Pipeline (Slides 0-9)

A apresentação técnica está dividida em etapas modulares que simulam o fluxo de trabalho de um Engenheiro de Dados:

1.  **Ingestão & Auditoria:** Carregamento do dataset e verificação de integridade inicial.
2.  **Análise Descritiva:** Extração de tendências centrais e dispersão das variáveis quantitativas.
3.  **Qualidade de Dados:** Identificação sistemática de *missing values* (NaN) no arquivo bruto.
4.  **Sanitização:** Aplicação de limpeza via *Listwise Deletion* para garantir um dataset "Zero Nulls".
5.  **Análise Exploratória (EDA):** Visualização de distribuições de classes e correlações bivariadas entre bico e nadadeira.
6.  **Engenharia de Atributos:** Demonstração de pipelines de codificação (Label & One-Hot Encoding).
7.  **Multicolinearidade:** Mapeamento de redundâncias utilizando a Matriz de Correlação de Pearson.

## 💻 Como Rodar o Projeto

1.  **Instale as dependências necessárias:**
    ```bash
    pip install flask pandas seaborn matplotlib scikit-learn
    ```

2.  **Inicie o servidor Flask:**
    ```bash
    python app.py
    ```

3.  **Acesse no navegador:** `http://127.0.0.1:5000`

## 🧠 Insights de Engenharia
O projeto destaca a importância da preparação dos dados, evidenciando que atributos como o **Comprimento da Nadadeira** possuem alto ganho de informação (correlação de 0.85) para a classificação das espécies. A interface foi projetada para manter o contraste máximo no modo claro e imersão total no modo escuro.

---
**Desenvolvido por Kaíque Nunes**
