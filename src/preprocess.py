import pandas as pd

COLUNAS_AVALIACAO = [
    'Financeira',
    'Engenharia',
    'Planejamento',
    'Ambiental'
]

def carregar_dados(caminho):

    df = pd.read_excel(caminho)

    # Renomeia colunas para padronizar
    df = df.rename(columns={
        'ID do Projeto': 'projeto_id',
        'Planejamento.1': 'Nota_Planejamento'
    })

    # Verificações
    colunas_obrigatorias = ['projeto_id'] + COLUNAS_AVALIACAO

    faltantes = [
        col for col in colunas_obrigatorias
        if col not in df.columns
    ]

    if faltantes:
        raise ValueError(
            f'Colunas não encontradas: {faltantes}'
        )

    return df