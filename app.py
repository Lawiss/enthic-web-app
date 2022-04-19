from os import PathLike
from typing import Union

import json
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
NON_VARIABLES_COLUMNS = [
    "SIREN",
    "Code postal",
    "Commune",
    "code_ape",
    "code_ape_complete",
    "nom",
    "description",
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

    indicateurs_df = indicateurs_df.rename(
        columns={
            "siren": "SIREN",
            "code_postal": "Code postal",
            "commune": "Commune",
        }
        | FEATURES_NAME_MAPPING
    )
    return indicateurs_df


indicateurs_df = load_data(DATA_PATH)


available_variables: pd.Series = indicateurs_df.columns[
    ~indicateurs_df.columns.isin(NON_VARIABLES_COLUMNS)
    & ~indicateurs_df.columns.str.contains("error_")
].sort_values()


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

    selected_df_filtered = selected_df.dropna(subset=NON_VARIABLES_COLUMNS)

    is_full_na = selected_df_filtered.isna().sum() == len(selected_df_filtered)
    full_na_variables = selected_df_filtered.columns[is_full_na]
    print(full_na_variables)
    selected_df_filtered = selected_df_filtered.loc[:, ~is_full_na]

    available_variables_list = available_variables[
        ~available_variables.isin(full_na_variables)
    ].tolist()

    st.markdown(
        f"**{total_company_count:,d}** au total dans cette catégorie ({len(selected_df_filtered)/indicateurs_df['SIREN'].nunique():.2%} du total).",
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

    company_df_formated = company_df[
        [
            "SIREN",
            "Code postal",
            "Commune",
            "Chiffres d’affaires nets",
            "Effectif moyen du personnel",
            "Salaire moyen",
        ]
    ].rename(" ")

    company_df_formated["Chiffres d’affaires nets"] = format_numerical_value(
        company_df_formated["Chiffres d’affaires nets"], " €"
    )
    company_df_formated["Effectif moyen du personnel"] = format_numerical_value(
        company_df_formated["Effectif moyen du personnel"]
    )
    company_df_formated["Salaire moyen"] = format_numerical_value(
        company_df_formated["Salaire moyen"], " €"
    )

    st.markdown(company_df_formated.to_markdown())
    st.write(
        f"Lien vers la fiche Enthic: https://enthic-dataviz.netlify.app/entreprises/{company_df['SIREN']}"
    )

col1, col2, col3, col4 = st.columns(4)
with col1:
    x_var = st.selectbox(
        "Abscisse :",
        help="Sélectionner une variable pour l'axe des abscisses :",
        options=available_variables_list,
        index=available_variables_list.index(
            "Part des 3 résultats (exploitation, financier et exceptionnel) distribuée en participation et impôts"
        ),
    )

with col2:
    y_var = st.selectbox(
        "Ordonnée :",
        help="Sélectionner une variable pour l'axe des ordonnées :",
        options=available_variables_list,
        index=available_variables_list.index(
            "Ratio entre les cotisations sociales et les salaires"
        ),
    )
with col3:
    size_var = st.selectbox(
        "Taille :",
        help="Sélectionner une variable pour la taille des bulles :",
        options=available_variables_list,
        index=available_variables_list.index("Effectif moyen du personnel"),
    )
with col4:
    color_var = st.selectbox(
        "Couleur :",
        help="Sélectionner une variable pour la couleur des bulles :",
        options=available_variables_list,
        index=available_variables_list.index("Chiffres d’affaires nets"),
    )

fig_1_df = selected_df_filtered.dropna(subset=[x_var, y_var, size_var, color_var])
fig_1_companies_count = len(fig_1_df)
if fig_1_companies_count:
    st.markdown(
        f"Avec votre sélection, il reste **{len(fig_1_df)}** entreprises à afficher.",
        unsafe_allow_html=True,
    )
    if company_df[[x_var, y_var]].isna().all():
        st.info(
            f"Il ny a pas les données suffisantes pour afficher la position de {company_df['nom']} dans le graphique."
        )

    fig_1 = create_bubble_chart(
        fig_1_df,
        company_series=company_df,
        x_var=x_var,
        y_var=y_var,
        size_var=size_var,
        color_var=color_var,
    )
    st.plotly_chart(fig_1, use_container_width=True)
else:
    st.error("Il n'y a pas de données pour la sélection actuelle")


fig_2 = create_hist(selected_df_filtered, company_series=company_df)
st.plotly_chart(fig_2, use_container_width=True)

st.write("Vous pouvez explorer les données qui ont permis d'éditer ces graphiques :")
AgGrid(
    selected_df_filtered[
        [
            "SIREN",
            "nom",
            "Code postal",
            "Commune",
            "Chiffres d’affaires nets",
            "Effectif moyen du personnel",
        ]
        + list(FEATURES_NAME_MAPPING.values())
    ]
)
