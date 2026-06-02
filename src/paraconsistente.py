import numpy as np
import pandas as pd

NOTAS_COLS = [
    'Financeira',
    'Engenharia',
    'Nota_Planejamento',
    'Ambiental'
]


def calcular_mu_lambda(row):

    favoraveis = []
    contrarias = []

    for col in NOTAS_COLS:

        nota = float(row[col])

        if nota >= 6:
            favoraveis.append(nota / 10)

        elif nota <= 4:
            contrarias.append((10 - nota) / 10)

    mu = np.mean(favoraveis) if favoraveis else 0
    lamb = np.mean(contrarias) if contrarias else 0

    return pd.Series([mu, lamb])


def aplicar_paraconsistente(df):

    df[['mu', 'lambda']] = df.apply(
        calcular_mu_lambda,
        axis=1
    )

    # Grau de certeza
    df['G'] = df['mu'] - df['lambda']

    # Grau de contradição
    df['C'] = df['mu'] + df['lambda'] - 1

    # Amplitude entre avaliações
    df['A'] = (
        df[NOTAS_COLS].max(axis=1)
        - df[NOTAS_COLS].min(axis=1)
    )

    return df


def classificar_projeto(row):

    if row['G'] < 0:
        return 'Baixa Prioridade'

    elif row['C'] > 0.25:
        return 'Divergente'

    elif abs(row['G']) <= 0.10:
        return 'Indeterminado'

    elif row['G'] >= 0.70:
        return 'Prioridade Muito Alta'

    elif row['G'] >= 0.40:
        return 'Prioridade Alta'

    else:
        return 'Prioridade Média'


def classificar_media(media):

    if media >= 7:
        return "Prioridade Muito Alta"

    elif media >= 6:
        return "Prioridade Alta"

    elif media >= 5:
        return "Prioridade Média"

    else:
        return "Baixa Prioridade"


def classificar(df):

    # Classificação Paraconsistente
    df['classificacao'] = df.apply(
        classificar_projeto,
        axis=1
    )

    # Classificação por Média Simples
    if 'Média Simples' in df.columns:
        df['classificacao_media'] = (
            df['Média Simples']
            .apply(classificar_media)
        )

    return df