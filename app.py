from os import PathLike
from typing import Union

import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

from figures import create_bubble_chart, create_hist
from utils import format_numerical_value

DATA_PATH = "https://entropeak-public-data.s3.eu-west-3.amazonaws.com/enthic/indicateurs_2020_full_20220412.csv"
CODES_APE = {
    "Supermarchés et Hypermarchés": ["^47\.11D", "^47\.11F"],
    "Cultures permanentes": ["^01\.2"],
    "Restauration": ["^56"],
    "Activités liées au sport": ["^93.1"],
    "Industrie automobile": ["^29"],
    "Construction aéronautique et spatiale": ["^30.3"],
}
FEATURES_NAME_MAPPING = {
    "exploitation_share": "Part du résultat d'exploitation distribuée en participation et impôts",
    "overall_wages_weight": "Part de la masse salariale dans le total des charges d'exploitation",
    "wage_quality": "Ratio entre les cotisations sociales et les salaires",
    "average_wage": "Salaire moyen",
    "profit_sharing": "Part des 3 résultats (exploitation, financier et exceptionnel) distribuée en participation et impôts",
    "exploitation_part": "Part de la partie 'exploitation' dans le total du compte de résultat",
    "data_availability": "Indicateur de bon remplissage de la déclaration comptable",
}
FEATURES_COLUMNS = [
    "exploitation_share",
    "overall_wages_weight",
    "wage_quality",
    "average_wage",
    "profit_sharing",
    "exploitation_part",
]

st.set_page_config(
    page_title="Enthic",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)


@st.cache
def load_data(data_path: Union[PathLike, str]):

    indicateurs_df = pd.read_csv(data_path, index_col=0)
    return indicateurs_df


indicateurs_df = load_data(DATA_PATH)


with st.sidebar:
    st.image(
        "static/enthic_without_bg.e0d245c1.png",
    )
    codes_ape = list(CODES_APE.keys())
    codes_ape.sort()
    selected_cat = st.selectbox(
        label="Sélectionner une catégorie d'entreprise :",
        options=codes_ape,
        help="Permet de filtrer les entreprises selon leur code APE.",
    )

    selected_df = indicateurs_df.loc[
        (indicateurs_df.code_ape_complete.str.match("|".join(CODES_APE[selected_cat])))
    ]
    selected_df = selected_df.rename(columns=FEATURES_NAME_MAPPING)

    total_company_count = selected_df.shape[0]

    selected_df_filtered = selected_df.dropna(
        subset=list(FEATURES_NAME_MAPPING.values())
        + ["nom", "Chiffres d’affaires nets", "Effectif moyen du personnel"]
    )

    st.markdown(
        f"**{len(selected_df_filtered):,d}** entreprises sans données manquantes sur **{total_company_count:,d}**"
        f" au total dans cette catégorie ({len(selected_df_filtered)/total_company_count:.2%}).",
    )

    company_names = np.sort(selected_df_filtered.nom.unique())

    selected_company_name = st.selectbox(
        label="Sélectionner une entreprise :",
        options=company_names,
        help="Sélectionnez une entreprise pour afficher des informations et sa position sur les graphiques.",
    )

    company_df = selected_df_filtered.loc[
        selected_df.nom == selected_company_name,
    ].iloc[0]

    company_df_formated = (
        company_df[
            [
                "siren",
                "code_postal",
                "commune",
                "Chiffres d’affaires nets",
                "Effectif moyen du personnel",
                "Salaire moyen",
            ]
        ]
        .rename(" ")
        .rename(
            index={
                "siren": "SIREN",
                "code_postal": " Code postal",
                "commune": "Commune",
            }
        )
    )

    company_df_formated["Effectif moyen du personnel"] = format_numerical_value(
        company_df_formated["Effectif moyen du personnel"]
    )
    company_df_formated["Salaire moyen"] = format_numerical_value(
        company_df_formated["Salaire moyen"]
    )

    st.markdown(company_df_formated.to_markdown())
    st.write(
        f"Lien vers la fiche Enthic: https://enthic-dataviz.netlify.app/entreprises/{company_df['siren']}"
    )


fig_1 = create_bubble_chart(
    selected_df_filtered,
    company_series=company_df,
    x_var="Part des 3 résultats (exploitation, financier et exceptionnel) distribuée en participation et impôts",
    y_var="Ratio entre les cotisations sociales et les salaires",
    size_var="Effectif moyen du personnel",
    color_var="Chiffres d’affaires nets",
)
st.plotly_chart(fig_1, use_container_width=True)

fig_2 = create_hist(selected_df_filtered, company_series=company_df)
st.plotly_chart(fig_2, use_container_width=True)

st.write("Vous pouvez explorer les données qui ont permis d'éditer ces graphiques :")
AgGrid(
    selected_df_filtered[
        [
            "siren",
            "nom",
            "code_postal",
            "commune",
            "Chiffres d’affaires nets",
            "Effectif moyen du personnel",
        ]
        + list(FEATURES_NAME_MAPPING.values())
    ]
)
