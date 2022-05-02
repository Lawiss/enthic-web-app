from os import PathLike
from typing import Union

import json
import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

from figures import create_bubble_chart, create_hist
from settings import (
    CODES_APE,
    DATA_PATH,
    FEATURES_NAME_MAPPING,
    NON_VARIABLES_COLUMNS,
    VARIABLES_TO_KEEP,
)
from utils import format_numerical_value


st.set_page_config(
    page_title="Enthic",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)


@st.cache
def load_data(data_path: Union[PathLike, str]) -> pd.DataFrame:
    """Loads the CSV dataset from either a local path or an URL. Also renames a few columns of the dataset.
    This function result is cached to avoid reload data each time user interacts with the application.

    Parameters
    ----------
    data_path : str or PathLike object
        Path or URL where CSV dataset is located

    Returns
    -------
    pd.DataFrame
        Dataframe with companies data
    """

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


with st.sidebar:
    st.image(
        "static/enthic_without_bg.e0d245c1.png",
    )

    codes_ape = list(CODES_APE.keys())
    codes_ape.sort()

    selected_cat = st.selectbox(
        label="Sélectionnez une catégorie d'entreprise :",
        options=codes_ape,
        help="Permet de filtrer les entreprises selon leur code APE.",
    )

    selected_df = indicateurs_df.loc[
        (indicateurs_df.code_ape_complete.str.match("|".join(CODES_APE[selected_cat])))
    ]

    total_company_count = selected_df.shape[0]

    selected_df_filtered = selected_df.dropna(subset=NON_VARIABLES_COLUMNS)

    is_full_na = selected_df_filtered.isna().sum() == len(selected_df_filtered)
    full_na_variables = selected_df_filtered.columns[is_full_na]

    selected_df_filtered = selected_df_filtered.loc[:, ~is_full_na]

    st.markdown(
        f"**{total_company_count:,d}** au total dans cette catégorie ({len(selected_df_filtered)/indicateurs_df['SIREN'].nunique():.2%} du total).",
    )

    company_names = np.sort(selected_df_filtered.nom.unique())

    selected_company_name = st.selectbox(
        label="Sélectionnez une entreprise :",
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


col1, col2, col3 = st.columns(3)
with col1:
    x_var = st.selectbox(
        "Abscisse :",
        help="Sélectionnez une variable pour l'axe des abscisses :",
        options=VARIABLES_TO_KEEP,
        index=VARIABLES_TO_KEEP.index(
            "Part des 3 résultats (exploitation, financier et exceptionnel) distribuée en participation et impôts"
        ),
    )
    x_var_log = st.checkbox(
        "Échelle logarithmique",
        False,
        help="Permet d'activer l'échelle logarithmique pour la variable.",
    )


with col2:
    y_var = st.selectbox(
        "Ordonnée :",
        help="Sélectionnez une variable pour l'axe des ordonnées :",
        options=VARIABLES_TO_KEEP,
        index=VARIABLES_TO_KEEP.index(
            "Ratio entre les cotisations sociales et les salaires"
        ),
    )
    y_var_log = st.checkbox(
        "Échelle logarithmique",
        False,
        help="Permet d'activer l'échelle logarithmique pour la variable.",
        key="y_var_log",
    )


with col3:
    color_var = st.selectbox(
        "Couleur :",
        help="Sélectionnez une variable pour la couleur des bulles :",
        options=VARIABLES_TO_KEEP,
        index=VARIABLES_TO_KEEP.index("Chiffres d’affaires nets"),
    )

    color_var_log = st.checkbox(
        "Échelle logarithmique",
        False,
        help="Permet d'activer l'échelle logarithmique pour la variable.",
        key="color_var_log",
    )


if x_var_log:
    na_to_remove = (selected_df_filtered[x_var] + 1e-7).apply(np.log10).isna()
    selected_df_filtered = selected_df_filtered.loc[~na_to_remove]
if y_var_log:
    na_to_remove = selected_df_filtered[y_var].apply(np.log10).isna()
    selected_df_filtered = selected_df_filtered.loc[~na_to_remove]


fig_1_df = selected_df_filtered.dropna(subset=[x_var, y_var])
fig_1_companies_count = len(fig_1_df)

if fig_1_companies_count:
    st.markdown(
        f"Avec votre sélection, il reste **{fig_1_companies_count}** entreprises à afficher.",
        unsafe_allow_html=True,
    )

    if company_df[[x_var, y_var]].isna().all():
        st.info(
            f"Il n'y a pas les données suffisantes pour afficher la position de {company_df['nom']} sur le graphique."
        )

    fig_1 = create_bubble_chart(
        fig_1_df,
        company_series=company_df,
        x_var=x_var,
        y_var=y_var,
        color_var=color_var,
        log_x=x_var_log,
        log_y=y_var_log,
        log_color=color_var_log,
    )
    st.plotly_chart(fig_1, use_container_width=True)
else:
    st.error("Il n'y a pas de données pour la sélection actuelle")


fig_2 = create_hist(selected_df_filtered, company_series=company_df)
st.plotly_chart(fig_2, use_container_width=True)
if np.isnan(company_df["Salaire moyen"]):
    st.info(
        f"Les données pour afficher le salaire moyen de {company_df['nom']} sont manquantes."
    )

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
            "Salaire moyen",
        ]
        + [x_var, y_var, color_var]
    ]
)
