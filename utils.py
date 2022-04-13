import numpy as np
import pandas as pd
import plotly.graph_objects as go


def create_fig(
    df: pd.DataFrame, company_series: pd.Series, x_var: str, y_var: str
) -> go.Figure:
    hover_text = (
        df.nom
        + "<br><b>Chiffre d'affaire :<b> "
        + df["Chiffres d’affaires nets"].apply(lambda x: "{:,} €".format(int(x)))
        + f"<br><b>{x_var} :<b> "
        + df[x_var].astype(str)
        + f"<br><b>{y_var} :<b> "
        + df[y_var].astype(str)
    )
    fig = go.Figure(
        [
            go.Scatter(
                x=df[x_var],
                y=df[y_var],
                marker_size=df["Chiffres d’affaires nets"].apply(np.log),
                marker_color=df["Chiffres d’affaires nets"].apply(np.log10),
                hoverinfo="text",
                hovertext=hover_text,
                mode="markers",
                marker_colorscale=[
                    "#659999",
                    "#f4791f",
                ],
                marker_colorbar_title="Chiffre d'affaire",
                marker_colorbar_tickvals=np.arange(0, 10, 1),
                marker_colorbar_ticktext=[
                    f"{10**e: ,d} €" for e in np.arange(0, 10, 1)
                ],
                marker_colorbar_ticks="outside",
                marker_colorbar_tickmode="array",
                marker_sizeref=1,
            )
        ]
    )
    fig.update_layout(
        xaxis_title=x_var,
        yaxis_title=y_var,
    )
    fig.add_annotation(
        x=company_series[x_var],
        y=company_series[y_var],
        text=company_series["nom"],
        font_size=15,
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
    fig.add_vline(
        x=company_series["Salaire moyen"],
        line_dash="longdashdot",
        annotation_text=company_series["nom"]
        + " - "
        + f'{int(company_series["Salaire moyen"]):,d} €'.replace(",", " "),
        annotation_position="top right",
    )
    fig.update_layout(
        xaxis_title="Salaire moyen (en euros)",
        yaxis_title="Nombre d'entreprises",
    )
    fig.update_xaxes(nticks=20)

    return fig
