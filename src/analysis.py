# ==============================================================================
# PCG - EXPLORANDO DADOS DO IDEB: UMA ABORDAGEM COMPUTACIONAL EM PYTHON SOBRE OS EFEITOS DA PANDEMIA NA BAIXADA SANTISTA
#
# Projeto interdisciplinar da grade do curso Bacharelado em Sistemas 
# de Informação da UNISANTOS, integrando conhecimentos das disciplinas
# de Programação Orientada a Objetos, Redes de Computadores, Interação
# Homem-Computador, Estrutura de Dados, Segurança da Informação e 
# Linguagens de Programação.
#            
# Descrição: Script de Extração, Transformação e Carga (ETL) e Visualização
#            de dados do IDEB - Índice de Desenvolvimento da Educação Básica 
#            para analisar a Taxa de Aprovação nos Anos Finais (6º ao 9º ano)
#            na Baixada Santista, com foco nos impactos do período pandêmico.
#
# Objetivo: Comparar o desempenho escolar nos anos pré-pandemia (2017, 2019)
#           com o ano de impacto (2021). Os gráficos gerados são salvos como HTML
#           interativo para serem consumidos pela interface web do projeto.
# ==============================================================================

import pandas as pd
import plotly.express as px
import os
from pathlib import Path 

# ------------------------------------------------------------------------------
# 1. VARIÁVEIS DE CONFIGURAÇÃO E ESCOPO DA ANÁLISE
# ------------------------------------------------------------------------------

# Nome de arquivo mantido por fidelidade à fonte oficial (INEP/gov.br)
DATA_FILENAME = 'divulgacao_anos_finais_municipios_2023 (1).xlsx'
DATA_PATH = Path('data') / DATA_FILENAME

OUTPUT_DIR = 'interface_web/'

# Definição do escopo geográfico e temporal da análise
MUNICIPALITIES_BAIXADA = [
    'Cubatão', 'Praia Grande', 'Santos', 'São Vicente', 'Guarujá', 
    'Bertioga', 'Itanhaém', 'Mongaguá', 'Peruíbe'
]
RELEVANT_YEARS = [2017, 2019, 2021] 

# ------------------------------------------------------------------------------
# 2. FUNÇÃO DE EXTRAÇÃO (EXTRACT)
# ------------------------------------------------------------------------------

def extract_data(file_path: Path) -> pd.DataFrame:
    """
    Carrega o dataset do IDEB (INEP) a partir do arquivo Excel (.xlsx).
    Trata o cabeçalho específico do arquivo (header=6).
    """
    print(f"Tentando carregar dados de: {file_path}") 
    
    if not file_path.exists():
        raise FileNotFoundError(f"Erro: Arquivo não encontrado em {file_path}. Verifique o caminho e o nome.")

    try:
        df = pd.read_excel(
            file_path,
            sheet_name=0, 
            header=6  
        )
        print(f"Arquivo Excel lido com sucesso! Total de linhas carregadas: {len(df)}")
        return df
    except Exception as e:
        print(f"\n[ERRO AO LER EXCEL] Verifique se o arquivo está fechado. Detalhe: {e}")
        raise 

# ------------------------------------------------------------------------------
# 3. FUNÇÃO DE TRANSFORMAÇÃO (TRANSFORM) - CORREÇÃO FINAL COM DIAGNÓSTICO
# ------------------------------------------------------------------------------

def transform_data(df_original: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os dados brutos: mapeamento de nomes, unpivoting (melt) e tratamento de tipos.
    Usa o mapeamento de colunas exato encontrado no arquivo (incluindo 'Taxa de Aprovação - 20212').
    """
    print("2. Limpando e transformando o DataFrame (ETL)...")
    
    # PASSO CRÍTICO 1: Limpeza de nomes de colunas
    # Remove espaços em branco (leading/trailing whitespace) nos nomes das colunas lidas.
    df_original.columns = df_original.columns.str.strip()
    
    # Mapeamento de Colunas: Usa os nomes EXATOS do Excel para renomear para os nomes técnicos do projeto.
    COLUMNS_MAPPING = {
        # Colunas de identificação
        'Nome do Município': 'NO_MUNICIPIO',
        'Rede': 'REDE',
        
        # Colunas de Taxa de Aprovação: Usando o nome EXATO 'Taxa de Aprovação - 20212'
        'Taxa de Aprovação - 2017': 'VL_APROVACAO_2017_SI_4', 
        'Taxa de Aprovação - 2019': 'VL_APROVACAO_2019_SI_4', 
        'Taxa de Aprovação - 20212': 'VL_APROVACAO_2021_SI_4', # CHAVE CORRIGIDA DEFINITIVAMENTE
    }
    
    # 3.1. Seleção e Renomeação
    # Seleciona apenas as colunas que realmente existem no DataFrame original.
    cols_to_select = [col for col in COLUMNS_MAPPING.keys() if col in df_original.columns]
    
    # Cria o DataFrame de trabalho, renomeando as colunas e criando uma cópia limpa.
    df_work = df_original[cols_to_select].rename(columns=COLUMNS_MAPPING).copy()

    # 3.2. Transposição (Melt): Converte de formato 'wide' para 'long'
    # Mapeia os nomes técnicos para os ANOS de análise (2017, 2019, 2021)
    df_work = df_work.rename(columns={
        'VL_APROVACAO_2017_SI_4': 2017,
        'VL_APROVACAO_2019_SI_4': 2019,
        'VL_APROVACAO_2021_SI_4': 2021
    })

    df_long = pd.melt(
        df_work,
        id_vars=['NO_MUNICIPIO', 'REDE'],
        value_vars=RELEVANT_YEARS, 
        var_name='Ano',
        value_name='Taxa_Aprovacao'
    )
    df_long['Ano'] = df_long['Ano'].astype(int)

    # 3.3. Tratamento da Coluna de Medida
    # Substitui a vírgula decimal (padrão Brasil) por ponto para conversão em float
    df_long['Taxa_Aprovacao'] = df_long['Taxa_Aprovacao'].replace({',': '.'}, regex=True)
    df_long['Taxa_Aprovacao'] = pd.to_numeric(df_long['Taxa_Aprovacao'], errors='coerce')

    return df_long

# NO SEU ARQUIVO src/analysis.py, SUBSTITUA O BLOCO 4 INTEIRO POR ESTE:

# ------------------------------------------------------------------------------
# 4. FUNÇÕES DE VISUALIZAÇÃO E CARGA (LOAD TO WEB INTERFACE) - AJUSTES ESTÉTICOS
# ------------------------------------------------------------------------------

def filter_and_plot_municipalities(df_long: pd.DataFrame):
    """
    Filtra os dados para Rede Pública na Baixada Santista e gera um gráfico de barras.
    """
    print("3.1. Gerando visualização 1: Evolução por Município (Rede Pública)...")

    df_filtered = df_long[
        (df_long['NO_MUNICIPIO'].isin(MUNICIPALITIES_BAIXADA)) &
        (df_long['REDE'] == 'Pública')
    ].copy()
    df_filtered.dropna(subset=['Taxa_Aprovacao'], inplace=True)

    # Gráfico de Barras com layout elegante
    fig = px.bar(
        df_filtered,
        x='Ano',
        y='Taxa_Aprovacao',
        color='NO_MUNICIPIO',
        barmode='group',
        text_auto='.1f',  # Exibe 1 casa decimal
        title='Taxa de Aprovação por Município (2017–2021) - Rede Pública'
    )

    # Configurações estéticas: remove linhas de grade, alinha ao centro
    fig.update_layout(
        template='simple_white',
        title_font_size=18,
        title_x=0.5,
        xaxis_title=None,
        yaxis_title='Taxa de Aprovação (%)',
        xaxis=dict(tickmode='array', tickvals=RELEVANT_YEARS),
        yaxis=dict(showgrid=False), # Remove linhas horizontais
        legend_title_text='Município'
    )
    
    # Exporta o gráfico interativo
    output_path = os.path.join(OUTPUT_DIR, 'grafico_municipios.html')
    fig.write_html(output_path, include_plotlyjs='cdn')
    print(f"   -> Gráfico interativo exportado para: {output_path}")


def plot_mean_comparison(df_long: pd.DataFrame):
    """
    Calcula e plota a média regional (Pública vs. Privada) em barras.
    """
    print("3.2. Gerando visualização 2: Comparação de Média por Rede...")

    df_all_networks = df_long[
        (df_long['NO_MUNICIPIO'].isin(MUNICIPALITIES_BAIXADA))
    ].copy()
    df_all_networks.dropna(subset=['Taxa_Aprovacao'], inplace=True)
    
    df_media = df_all_networks.groupby(['Ano', 'REDE'])['Taxa_Aprovacao'].mean().reset_index()

    # Gráfico de Barras com layout elegante
    fig2 = px.bar(
        df_media,
        x='Ano',
        y='Taxa_Aprovacao',
        color='REDE',
        barmode='group',
        text_auto='.1f', # Exibe 1 casa decimal
        title='Evolução da Taxa de Aprovação por Rede de Ensino (2017–2021)'
    )

    # Configurações estéticas: remove linhas de grade, alinha ao centro
    fig2.update_layout(
        template='simple_white',
        title_font_size=18,
        title_x=0.5,
        xaxis_title=None,
        yaxis_title='Taxa de Aprovação Média (%)',
        xaxis=dict(tickmode='array', tickvals=RELEVANT_YEARS),
        yaxis=dict(showgrid=False), # Remove linhas horizontais
        legend_title_text='Rede'
    )

    # Exporta o gráfico interativo
    output_path = os.path.join(OUTPUT_DIR, 'grafico_media.html')
    fig2.write_html(output_path, include_plotlyjs='cdn')
    print(f" -> Gráfico interativo exportado para: {output_path}")

# ------------------------------------------------------------------------------
# 5. ENTRY POINT PRINCIPAL (MAIN)
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        # EXECUÇÃO DO FLUXO DE TRABALHO (ETL + ANÁLISE)
        print("Iniciando o Processo de Análise IDEB...")
        
        # 1. Extração
        df_original = extract_data(DATA_PATH)
        
        # 2. Transformação
        df_long = transform_data(df_original)
        
        # 3. Visualização e Carga dos Resultados
        filter_and_plot_municipalities(df_long)
        plot_mean_comparison(df_long)
        
        print("\nProcesso de análise e exportação concluído com sucesso!")

    except FileNotFoundError as e:
        print(f"\n[ERRO DE ARQUIVO] Falha ao encontrar ou carregar o arquivo. Detalhe: {e}")
    except Exception as e:
        print(f"\n[ERRO DE EXECUÇÃO] Ocorreu um erro no pipeline de análise: {e}")
        # Verificar se as dependências (requirements.txt) estão instaladas.
        print("Verifique se todas as dependências estão instaladas conforme requirements.txt.")