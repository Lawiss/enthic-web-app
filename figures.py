import math
from typing import Callable, Dict

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from utils import format_to_pretty_decimal


def create_bubble_chart(
    df: pd.DataFrame,
    company_series: pd.Series,
    x_var: str,
    y_var: str,
    color_var: str,
    log_x: bool = False,
    log_y: bool = False,
    log_color: bool = False,
) -> go.Figure:
    """Creates a plotly bubble chart with the given variables for x axis, y axis, and the color of the bubbles.

    Parameters
    ----------
    df : DataFrame
        DataFrame including the variables needed to create the plot.
    company_series: Series
        Series object with data from one company that will be highlighted in the graph,
        either with an annotation if both x_var and y_var data is available or with an vertical/horizontal line depending
        on the availability of only x_var/y_var.
    x_var: str
        Variable to use for the x-axis.
    y_var: str
        Variable to use for the y-axis.
    color_var: str
        Variable to use for the color gradient of the bubbles. If some data points are not available, a default color is displayed.
    log_x: bool
        If True, transform the x-axis to logarithmic scale. Default False.
    log_y: bool
        If True, transform the y-axis to logarithmic scale. Default False.
    log_color: bool
        If True, transform the y-axis to logarithmic scale. Default False.

    Returns
    -------
    go.Figure
        Plotly figure object ready to be displayed.
    """

    epsilon = 10e-7  # Used to avoid -inf after log transformations

    df = df.copy()
    company_series = company_series.copy()

    x_series = df[x_var].copy()
    y_series = df[y_var].copy()
    color_series = df[color_var].copy()

    hover_data_df = df[["nom"]].copy()

    # We use hover text along with hover template to be able to apply custom formating and
    # add extra tag to show company name in the secondary box
    hover_text = (
        f"<b>{x_var} : </b>"
        + (x_series).apply(format_to_pretty_decimal)
        + f"<br><b>{y_var} : </b> "
        + (y_series).apply(format_to_pretty_decimal)
        + f"<br><b>{color_var} : </b> "
        + color_series.apply(format_to_pretty_decimal)
    )
    hover_template = "%{text}<extra>%{customdata[0]}</extra>"

    if log_color:
        color_series = color_series.apply(np.log10)

        colorbar_tickvals = np.arange(0, np.ceil(color_series).max(), 1)
        colorbar_ticktext = [f"{10**int(e): ,d}" for e in colorbar_tickvals]

    else:
        colorbar_tickvals = None
        colorbar_ticktext = None

    fig = go.Figure(
        [
            go.Scatter(
                x=x_series if not log_x else (x_series + epsilon),
                y=y_series if not log_y else (y_series + epsilon),
                marker_color=color_series,
                hoverinfo="text",
                text=hover_text,
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

    if log_x:
        fig.update_xaxes(type="log")
    if log_y:
        fig.update_yaxes(type="log")

    # We add the highlighting of the given company data by creating either an annotation
    # or a vertical/horizontal line if data is missing for one of the variable.
    if not company_series[[x_var, y_var]].isna().any():

        fig.add_annotation(
            x=math.log(company_series[x_var], 10) if log_x else company_series[x_var],
            y=math.log(company_series[y_var], 10) if log_y else company_series[y_var],
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


def create_hist(series: pd.DataFrame, company_series: pd.Series) -> go.Figure:
    """Creates a plotly histogram chart for the wage ("Salaire moyen") data
    with a vertical line to show the value for the selected company if it is available.


    Parameters
    ----------
    df : DataFrame
        DataFrame including the variable needed to create the plot.
    company_series: Series
        Series object with data from one company that will be highlighted in the graph,
        if data is available, a dotted vertical line will appear to show the company's value for wage.

    Returns
    -------
    go.Figure
        Plotly figure object ready to be displayed.
    """
    fig = go.Figure(
        data=[
            go.Histogram(
                x=series["Salaire moyen"],
                marker_color="#d59f64",
                marker_line_color="#636e72",
                marker_line_width=1,
                xbins_size=5000,
                xbins_start=0,
                hovertemplate="Salaire moyen compris dans l'intervalle <b>%{x}</b> ??? pour <b>%{y}</b> entreprises<extra></extra>",
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
            + f'{int(company_series["Salaire moyen"]):,d} ???'.replace(",", " "),
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
