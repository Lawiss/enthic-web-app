import numpy as np
import pandas as pd
import plotly.graph_objects as go


def create_fig(df: pd.DataFrame, company_df, x_var: str, y_var: str) -> go.Figure:
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
        x=company_df[x_var],
        y=company_df[y_var],
        text=company_df["nom"],
        font_size=15,
    )

    return fig
