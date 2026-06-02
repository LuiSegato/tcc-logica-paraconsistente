import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(__file__))

from src.preprocess import carregar_dados
from src.paraconsistente import (
    aplicar_paraconsistente,
    classificar
)

st.set_page_config(layout="wide")

st.title("Priorização de Projetos com Lógica Paraconsistente")


def classificar_media(media):

    if media >= 7:
        return "Prioridade Muito Alta"

    elif media >= 6:
        return "Prioridade Alta"

    elif media >= 5:
        return "Prioridade Média"

    else:
        return "Baixa Prioridade"


arquivo = st.file_uploader(
    "Selecione a planilha Excel",
    type=["xlsx"]
)

if arquivo:

    try:

        df = carregar_dados(arquivo)

        st.subheader("Dados Carregados")

        st.dataframe(
            df[
                [
                    'projeto_id',
                    'Financeira',
                    'Engenharia',
                    'Nota_Planejamento',
                    'Ambiental'
                ]
            ]
        )

        if st.button(
            "Aplicar Lógica Paraconsistente",
            use_container_width=True
        ):

            # ==========================
            # PROCESSAMENTO
            # ==========================

            df = aplicar_paraconsistente(df)

            df = classificar(df)

            df['classificacao_media'] = (
                df['Média Simples']
                .apply(classificar_media)
            )

            st.success(
                "Processamento concluído!"
            )

            # ==========================
            # DASHBOARD
            # ==========================

            total = len(df)

            muito_alta = len(
                df[
                    df['classificacao']
                    == 'Prioridade Muito Alta'
                ]
            )

            alta = len(
                df[
                    df['classificacao']
                    == 'Prioridade Alta'
                ]
            )

            media = len(
                df[
                    df['classificacao']
                    == 'Prioridade Média'
                ]
            )

            divergente = len(
                df[
                    df['classificacao']
                    == 'Divergente'
                ]
            )

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric("Projetos", total)
            col2.metric("Muito Alta", muito_alta)
            col3.metric("Alta", alta)
            col4.metric("Média", media)
            col5.metric("Divergentes", divergente)

            # ==========================
            # RESULTADO FINAL
            # ==========================

            st.subheader("Resultado Final")

            st.dataframe(
                df[
                    [
                        'projeto_id',
                        'mu',
                        'lambda',
                        'G',
                        'C',
                        'A',
                        'classificacao'
                    ]
                ]
            )

            # ==========================
            # COMPARAÇÃO DE MÉTODOS
            # ==========================

            st.subheader(
                "Comparação: Média Simples x Paraconsistente"
            )

            comparacao = df[
                [
                    'projeto_id',
                    'Média Simples',
                    'classificacao_media',
                    'classificacao',
                    'G',
                    'C'
                ]
            ]

            st.dataframe(comparacao)

            # ==========================
            # DECISÕES DIFERENTES
            # ==========================

            diferentes = df[
                df['classificacao_media']
                != df['classificacao']
            ]

            st.subheader(
                "Projetos com Decisões Diferentes"
            )

            st.write(
                f"Total: {len(diferentes)}"
            )

            if len(diferentes) > 0:

                st.dataframe(
                    diferentes[
                        [
                            'projeto_id',
                            'Média Simples',
                            'classificacao_media',
                            'classificacao',
                            'G',
                            'C'
                        ]
                    ]
                )

            # ==========================
            # RANKING
            # ==========================

            ranking = (
                df[
                    [
                        'projeto_id',
                        'G',
                        'classificacao'
                    ]
                ]
                .sort_values(
                    'G',
                    ascending=False
                )
                .reset_index(drop=True)
            )

            ranking.index += 1

            st.subheader(
                "Ranking por Grau de Certeza"
            )

            st.dataframe(ranking)

            # ==========================
            # CONTRADIÇÃO
            # ==========================

            st.subheader(
                "Projetos por Contradição"
            )

            st.dataframe(
                df[
                    [
                        'projeto_id',
                        'C',
                        'G',
                        'Financeira',
                        'Engenharia',
                        'Nota_Planejamento',
                        'Ambiental'
                    ]
                ]
                .sort_values(
                    'C',
                    ascending=False
                )
            )

            # ==========================
            # PROJETOS DE INTERESSE
            # ==========================

            st.subheader(
                "Projetos de Interesse"
            )

            projetos_interesse = df[
                (
                    (df['C'] > 0)
                    |
                    (df['G'] < 0)
                )
            ]

            st.dataframe(
                projetos_interesse[
                    [
                        'projeto_id',
                        'Financeira',
                        'Engenharia',
                        'Nota_Planejamento',
                        'Ambiental',
                        'G',
                        'C',
                        'classificacao'
                    ]
                ]
            )

            # ==========================
            # DISTRIBUIÇÃO
            # ==========================

            st.subheader(
                "Distribuição das Classificações"
            )

            stats = (
                df['classificacao']
                .value_counts()
            )

            st.bar_chart(stats)

            # ==========================
            # GRÁFICO G X C
            # ==========================

            st.subheader(
                "Plano Cartesiano Paraconsistente (G x C)"
            )

            fig, ax = plt.subplots(
                figsize=(10, 8)
            )

            ax.scatter(
                df['G'],
                df['C'],
                s=80
            )

            ax.axhline(
                y=0,
                linestyle='--'
            )

            ax.axvline(
                x=0,
                linestyle='--'
            )

            ax.set_xlabel(
                "Grau de Certeza (G)"
            )

            ax.set_ylabel(
                "Grau de Contradição (C)"
            )

            ax.set_title(
                "Distribuição dos Projetos"
            )

            st.pyplot(fig)

            st.subheader(
                "Análise das Divergências"
            )

            st.dataframe(
                diferentes[
                    [
                        'projeto_id',
                        'Financeira',
                        'Engenharia',
                        'Nota_Planejamento',
                        'Ambiental',
                        'Média Simples',
                        'classificacao_media',
                        'classificacao',
                        'G',
                        'C'
                    ]
                ]
            )

    except Exception as e:

        st.error(
            f"Erro ao processar: {str(e)}"
        )

else:

    st.info(
        "Faça upload da planilha para iniciar."
    )