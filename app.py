from os import PathLike
from typing import Union

import numpy as np
import pandas as pd
import streamlit as st

from utils import create_fig, create_hist

DATA_PATH = "https://entropeak-public-data.s3.eu-west-3.amazonaws.com/enthic/indicateurs_2020_full_20220412.csv"
CODES_APE = {
    "Supermarchés et Hypermarchés": ["^47\.11D", "^47\.11F"],
    "Cultures permanentes": ["^01\.2"],
    "Restauration": ["^56"],
    "Activités liées au sport": ["^93.1"],
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
    selected_cat = st.selectbox(
        label="Sélectionner une entreprise",
        options=CODES_APE.keys(),
        help="Sélectionnez une entreprise",
    )

    selected_df = indicateurs_df.loc[
        (indicateurs_df.code_ape_complete.str.match("|".join(CODES_APE[selected_cat])))
    ]
    selected_df = selected_df.rename(columns=FEATURES_NAME_MAPPING)
    selected_df_filtered = selected_df.dropna(
        subset=list(FEATURES_NAME_MAPPING.values())
        + ["nom", "Chiffres d’affaires nets"]
    )
    st.metric(
        "Nombre d'entreprises avec données complètes en base",
        value=len(selected_df_filtered),
    )
    company_names = selected_df_filtered.nom.unique()
    selected_company_name = st.selectbox(
        label="Sélectionner une entreprise",
        options=company_names,
        help="Sélectionnez une entreprise",
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
    if not np.isnan(company_df_formated["Chiffres d’affaires nets"]):
        company_df_formated[
            "Chiffres d’affaires nets"
        ] = f'{int(company_df_formated["Chiffres d’affaires nets"]):_d} €'.replace(
            "_", " "
        )
    if not np.isnan(company_df_formated["Effectif moyen du personnel"]):
        company_df_formated[
            "Effectif moyen du personnel"
        ] = f'{int(company_df_formated["Effectif moyen du personnel"]):_d}'.replace(
            "_", " "
        )
    if not np.isnan(company_df_formated["Salaire moyen"]):
        company_df_formated[
            "Salaire moyen"
        ] = f'{int(company_df_formated["Salaire moyen"]):_d} €'.replace("_", " ")
    st.markdown(company_df_formated.to_markdown())


fig_1 = create_fig(
    selected_df_filtered,
    company_series=company_df,
    x_var="Part des 3 résultats (exploitation, financier et exceptionnel) distribuée en participation et impôts",
    y_var="Ratio entre les cotisations sociales et les salaires",
)
st.plotly_chart(fig_1, use_container_width=True)

fig_2 = create_hist(selected_df_filtered, company_series=company_df)
st.plotly_chart(fig_2, use_container_width=True)
