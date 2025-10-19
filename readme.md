# 🚀 EXPLORANDO DADOS DO IDEB: ANÁLISE COMPUTACIONAL SOBRE OS EFEITOS DA PANDEMIA

## Contexto e Visão Geral do Projeto

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-success)
![Linguagem Principal](https://img.shields.io/badge/Python-3.9+-blue)
![Stack de Dados](https://img.shields.io/badge/Stack-Pandas%2C%20Plotly%2C%20ETL-orange)
![Design/IHC](https://img.shields.io/badge/Design-Figma%2FHTML%2FCSS-informational)
![Tipo de Projeto](https://img.shields.io/badge/Tipo-PCG%20Interdisciplinar-red)

Este projeto faz parte da **Pesquisa Curricularizado de Graduação (PCG)** uma pesquisa interdisciplinar presente na grade do curso de **Bacharelado em Sistemas de Informação**. Ele evoluiu de uma análise acadêmica para o presente projeto de portfólio completo, demonstrando competências em Engenharia de Dados, Análise Exploratória e Desenvolvimento Front-end (IHC).

### 🎯 Objetivo da Análise

O projeto visa realizar uma **análise exploratória** dos impactos da pandemia da COVID-19 no desempenho escolar com recorte geográfico na **Baixada Santista (SP)**. Realizando o processo de extração, transformação e carregamento (ETL), além de Visualização dos dados, com o foco em comparar a **Taxa de Aprovação** do Ensino Fundamental (Anos Finais) nos anos **pré-pandemia (2017, 2019)** com o ano de **impacto (2021)**, usando dados públicos e abertos do IDEB - Índice de Desenvolvimento da Educação Básica. Os gráficos gerados são salvos como HTML interativo para serem consumidos pela interface web para melhor visualização dos resultados do projeto.

---

## 💻 Acesse a Análise Interativa

Clique no link abaixo para acessar o dashboard web e interagir com os gráficos gerados pelo pipeline Python:

### [✨ ACESSE A INTERFACE WEB AQUI](interface_web/index.html)

---

## ⚙️ Arquitetura e Metodologia (Pipeline ETL)

O projeto é estruturado em um pipeline de **ETL (Extract, Transform, Load)** implementado no script **`src/analysis.py`**, garantindo modularidade e rastreabilidade:

### I. Extração (Extract)

* **Fonte:** Arquivo Excel (`.xlsx`) oficial do IDEB/INEP (mantido com o nome original por fidelidade à fonte governamental).
* **Tecnologia:** `pd.read_excel` (com `openpyxl`) e `pathlib` para manipulação robusta do caminho.

### II. Transformação (Transform)

* **Engenharia de Dados:** Implementação do **`pd.melt()`** para converter o formato *wide* (anos em colunas) para *long* (série temporal).
* **Limpeza Crítica:** Mapeamento de colunas para corrigir a inconsistência de nomes no arquivo fonte (ex: mapeando a coluna `'Taxa de Aprovação - 20212'` para o nome técnico `VL_APROVACAO_2021_SI_4`).
* **Filtros:** Isolamento dos 9 municípios da Baixada Santista e das redes de ensino.

### III. Carga (Load)

* **Visualização:** Geração de gráficos de **barras agrupadas** interativos usando **Plotly Express**.
* **Output:** Exportação dos resultados para arquivos `.html` estáticos consumidos pela interface web.

## 📈 Resultados (Insights)

* **Disparidade de Redes:** Comparação direta da Taxa de Aprovação Média entre a Rede Pública e a Rede Privada na região, destacando a diferença de resiliência ao impacto da pandemia.
* **Interface e Design (IHC):** O layout e o estilo da interface web (HTML/CSS) foram implementados a partir de um protótipo (criado pela plataforma Figma), demonstrando a aplicação prática dos princípios de Interação Homem-Computador.

## 🤝 Destaque Interdisciplinar

Este projeto demonstra a aplicação de múltiplos pilares de Sistemas de Informação:

* **Programação Orientada a Objetos (POO):** Estrutura modular do pipeline (`extract`, `transform`, `load`).
* **Interação Humano-Computador (IHC):** Design e implementação do dashboard (`/interface_web`).
* **Redes de Computadores:** Versionamento do projeto e colaboração via Git/GitHub.
* **Estrutura de Dados:** Manipulação e transposição de grandes DataFrames (`pandas/numpy`).
* **Linguagens de Programação:** Uso avançado de Python e seus ecossistemas.
* **Segurança da Informação:** Boas práticas de versionamento (uso do .gitignore) e anonimização de dados (ao focar apenas em médias e municípios, sem dados pessoais).

---

## 💡 Tecnologias Utilizadas

* **Linguagem:** Python
* **Análise de Dados:** Pandas, NumPy
* **Visualização:** Plotly Express (Gráficos interativos)
* **Web/IHC:** HTML5, CSS3 (Design baseado em Figma)
* **Versionamento:** Git/GitHub

---

## 🔮 Próximos Passos e Escopo Futuro

Este projeto está pronto para ser expandido para atender a futuros requisitos de análise e a fim de expandir meus conhecimentos na área de dados:

* **Expansão do Escopo:** Incluir a análise dos ciclos Anos Iniciais (1º ao 5º ano) e Ensino Médio.
* **Análise Preditiva:** Utilizar modelos de regressão para tentar prever a recuperação do IDEB nos anos subsequentes (2023 em diante).
* **Integração Web:** Refatorar a interface para um framework web (como Dash ou Flask) para permitir consultas dinâmicas.

---

## 🛠️ Como Executar a Análise Localmente

Para replicar o ambiente e gerar os resultados:

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/M1llyz/ideb-data-analysis.git](https://github.com/M1llyz/ideb-data-analysis.git)
    cd ideb-data-analysis
    ```
2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    python -m venv venv
    call venv\Scripts\activate  # No Windows (CMD/PowerShell)
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o Script de Análise:**
    ```bash
    python src/analysis.py
    ```
    *Este comando irá gerar (ou atualizar) os arquivos HTML dos gráficos na pasta `interface_web/`.*
5.  **Visualize:** Abra o arquivo `interface_web/index.html` em seu navegador para ver o dashboard final.

---

<p align="center">
  <img src="https://img.shields.io/badge/Feito%20com%20%E2%9D%A4%20por-Millyz%20%20-blue" alt="Feito por Millyz">
  <br>
</p>