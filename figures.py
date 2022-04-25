import math
from tkinter import Y
from typing import Callable, Dict

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pyparsing import col

from utils import format_to_pretty_decimal


def create_bubble_chart(
    df: pd.DataFrame,
    company_series: pd.Series,
    x_var: str,
    y_var: str,
    color_var: str,
    transformations: Dict[str, Callable] = {},
) -> go.Figure:

    df = df.copy()
    company_series = company_series.copy()

    x_series = df[x_var].copy()
    y_series = df[y_var].copy()
    color_series = df[color_var].copy()

    hover_data_df = df[["nom", x_var, y_var, color_var]].copy()

    hover_text = (
        df.nom
        + f"<br><b>{color_var} : </b> "
        + color_series.apply(format_to_pretty_decimal)
        + f"<br><b>{x_var} : </b>"
        + (x_series).apply(format_to_pretty_decimal)
        + f"<br><b>{y_var} : </b> "
        + (y_series).apply(format_to_pretty_decimal)
        + "<extra>"
        + df.nom
        + "</extra>"
    )

    hover_template = f"{x_var} : %{{customdata[1]:,.2f}}<br> {y_var} : %{{customdata[2]:,.2f}}<br> {color_var} : %{{customdata[3]:,.2f}}<br><extra>%{{customdata[0]}}</extra>"

    if transformations.get("color") == np.log10:
        color_series = color_series.apply(np.log10)

        colorbar_tickvals = np.arange(0, np.ceil(color_series).max(), 1)
        colorbar_ticktext = [f"{10**int(e): ,d}" for e in colorbar_tickvals]

    else:
        colorbar_tickvals = None
        colorbar_ticktext = None
    fig = go.Figure(
        [
            go.Scatter(
                x=x_series,
                y=y_series,
                marker_color=color_series,
                # hoverinfo="text",
                # hovertext=hover_text,
                hovertemplate=hover_template,
                mode="markers",
                marker_colorscale=[
                    "#659999",
                    "#f4791f",
                ],
                marker_colorbar_title=color_var,
                marker_colorbar_tickvals=colorbar_tickvals,
                marker_colorbar_ticktext=colorbar_ticktext,
                marker_colorbar_ticks="outside",
                marker_colorbar_thickness=15,
                customdata=hover_data_df,
            )
        ]
    )
    fig.update_layout(
        xaxis_title=x_var,
        yaxis_title=y_var,
        title_font_size=30,
        title_font_color="#2d3436",
        margin_t=10,
    )
    if transformations.get("x") == np.log10:
        fig.update_xaxes(type="log")
    if transformations.get("y") == np.log10:
        fig.update_yaxes(type="log")

    if not company_series[[x_var, y_var]].isna().any():

        fig.add_annotation(
            x=math.log(company_series[x_var], 10)
            if (transformations.get("x") == np.log10)
            else company_series[x_var],
            y=math.log(company_series[y_var], 10)
            if (transformations.get("y") == np.log10)
            else company_series[y_var],
            text=company_series["nom"],
            font_size=15,
            arrowhead=2,
        )
    elif not np.isnan(company_series[x_var]):
        fig.add_vline(
            x=company_series[x_var],
            line_dash="longdashdot",
            annotation_text=company_series["nom"]
            + " - "
            + f"{company_series[x_var]:,.2f}",
            annotation_position="top right",
        )
    elif not np.isnan(company_series[y_var]):
        fig.add_hline(
            y=company_series[y_var],
            line_dash="longdashdot",
            annotation_text=company_series["nom"]
            + " - "
            + f"{company_series[y_var]:,.2f}",
            annotation_position="top right",
        )
    return fig


def create_hist(series: pd.Series, company_series: pd.Series) -> go.Figure:

    fig = go.Figure(
        data=[
            go.Histogram(
                x=series["Salaire moyen"],
                marker_color="#d59f64",
                marker_line_color="#636e72",
                marker_line_width=1,
                xbins_size=5000,
                xbins_start=0,
                hovertemplate="Salaire moyen compris dans l'intervalle <b>%{x}</b> € pour <b>%{y}</b> entreprises<extra></extra>",
                hoverinfo="x+y",
            )
        ]
    )
    if not np.isnan(company_series["Salaire moyen"]):
        fig.add_vline(
            x=company_series["Salaire moyen"],
            line_dash="longdashdot",
            annotation_text=company_series["nom"]
            + " - "
            + f'{int(company_series["Salaire moyen"]):,d} €'.replace(",", " "),
            annotation_position="top right",
        )
    fig.update_layout(
        title="Comparaison des salaires moyen",
        title_font_size=30,
        title_font_color="#2d3436",
        title_pad_l=10,
        xaxis_title="Salaire moyen (en euros)",
        yaxis_title="Nombre d'entreprises",
        margin_b=3,
    )
    fig.update_xaxes(nticks=20)

    return fig
