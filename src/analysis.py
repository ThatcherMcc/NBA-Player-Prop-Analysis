"""
This module provides functions for analyzing and visualizing NBA player statistics.

Generates a simple bar plot from the given inputs
"""

import pandas as pd
import plotly.express as px
import plotly.io as pio
import webbrowser
from utils import Utils


def graph_dataframe(df: pd.DataFrame, player_name: str, prop_line: float, stat: str = 'PTS', last_games_count: int = 10,  year: int = 2025):
    """
    Adds and cleans the given dataframe for plotting.
    Given the stat, line, and amount of games to plot, it shows a bar plot.

    Args:
        df (pd.DataFrame): Player's cleaned gamelog data.
        player_name (str): Player's full name.
        prop_line (float): The 'line' or what determines a win or loss.
        stat (str): The statistic plotted.
        last_games_count (int): The number of most recent games included in the plot.

    Returns:
        matplotlib.pyplot: A visual of the input information in bar plot format
    """
    df_last = df.copy()
    df_last = df_last.tail(last_games_count)
    df_last[stat] = pd.to_numeric(df_last[stat], errors='coerce').fillna(0)

    df_last['Game_Label'] = df_last['OPPONENT'] + '<br>' + \
        df_last['DATE'].dt.strftime('%m/%d/%y')  # <br> for newline in Plotly
    df_last['Outcome'] = ['Over' if s > prop_line else 'Under' if s <
                          prop_line else 'Push' for s in df_last[stat]]

    # Define colors for Plotly
    color_map = {
        'Over': 'forestgreen',
        'Under': 'firebrick',
        'Push': 'grey'
    }

    # Plotting with Plotly Express
    fig = px.bar(
        df_last,
        x='Game_Label',
        y=stat,
        color='Outcome',  # Color bars based on 'Outcome' column
        color_discrete_map=color_map,  # Map outcomes to specific colors
        title=f'<b>{player_name}</b> <br>Last {last_games_count} Games : {prop_line} {stat}',
        labels={stat: f'{stat} Value', 'Game_Label': 'Opponent & Game Date'},
        text=stat  # Display numerical value on top of bars
    )

    # Add the prop line using graph_objects (go)
    fig.add_hline(
        y=prop_line,
        line_dash="dash",
        line_color="navy",
        annotation_text=f"Prop Line: {prop_line}",
        annotation_position="top right"
    )

    # Further customization
    fig.update_layout(
        xaxis_title_font_size=12,
        yaxis_title_font_size=12,
        title_font_size=18,
        hovermode="x unified",  # Shows tooltip for all traces at a specific X-position
        bargap=0.2,  # Adjust gap between bars

        # Move legend outside
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(
        tickfont=dict(
            # Adjust this value to make ticks smaller (e.g., 8, 10, 12)
            size=10
        ),
        categoryorder='array',
        categoryarray=df_last['Game_Label']
    )
    fig.update_yaxes(
        tickfont=dict(
            # Adjust this value to make ticks smaller (e.g., 8, 10, 12)
            size=10
        )
    )

    utils = Utils()
    output_html_path = utils.get_plots_folder(
    ) + f'/{player_name.replace(' ', '')}_{prop_line}_{stat}_plot.html'

    # Show the plot
    # auto_open=False here means we'll open it manually below
    fig.write_html(output_html_path, auto_open=False)

    # Open the HTML file in the default web browser
    webbrowser.open_new_tab(output_html_path)
    print(f"Interactive plot opened in your browser: {output_html_path}")
