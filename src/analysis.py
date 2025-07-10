"""
This module provides functions for analyzing and visualizing NBA player statistics.

Generates a simple bar plot from the given inputs
"""

import pandas as pd
import matplotlib.pyplot as plt


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
    df = df.fillna(0)  # fill nulls with 0

    # drop stats that are unused in props
    df = df.drop(columns=['FT%', '3P%', 'FG%'])

    # change whole number columns to numeric
    columns_to_numeric = ['PTS', 'TRB', 'AST', 'ORB', 'DRB',
                          'STL', 'BLK', 'TOV', 'FT', '3P', 'FG', 'FGA', '3PA']

    # Iterate through the columns and apply pd.to_numeric
    for col in columns_to_numeric:
        # Use errors='coerce' to turn unconvertible values into NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['PRA'] = df[['PTS', 'TRB', 'AST']].sum(
        axis=1)  # points + rebounds + assists
    df['PR'] = df[['PTS', 'TRB']].sum(axis=1)  # points + rebounds
    df['PA'] = df[['PTS', 'AST']].sum(axis=1)  # points + assists
    df['RA'] = df[['TRB', 'AST']].sum(axis=1)  # rebounds + assists

    df_last = df.tail(last_games_count)  # last 'x' amount of games
    # coloring the bars based on prop_line
    colors = ["green" if used_stat > prop_line else "red" if used_stat <
              prop_line else "grey" for used_stat in df_last[stat]]

    # Count hits, pushes, and misses
    hits = sum(df_last[stat] > prop_line)
    pushes = sum(df_last[stat] == prop_line)
    misses = last_games_count - hits - pushes

    # Calculate percentages
    hit_percent = (hits / last_games_count) * 100
    push_percent = (pushes / last_games_count) * 100
    miss_percent = (misses / last_games_count) * 100  # optional

    # Print hit/push rates
    print(f"Hit Rate: {hit_percent:.2f}% ({hits}/{last_games_count})")
    print(f"Push Rate: {push_percent:.2f}% ({pushes}/{last_games_count})")

    # graph
    bars = plt.bar(df_last['Date'].dt.strftime('%Y-%m-%d') + ' ' + df_last['Opponent'],
                   df_last[stat], color=colors)
    for bar in bars:
        yval = bar.get_height()
        if yval > 0:
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5,
                     f'{float(yval)}', ha='center', va='bottom', fontsize=9)

    # Prop line
    plt.axhline(prop_line, color='black', linestyle='--',
                label=f'Prop Line: {prop_line}')

    # Labels and title
    plt.xlabel('Game Date')
    plt.ylabel(stat)
    plt.title(f'{player_name} {stat} line')
    plt.xticks(rotation=75)
    plt.legend()
    plt.tight_layout()

    # Adjust y-axis to give space for bar labels
    max_val = df_last[stat].max()
    # Add buffer space above tallest bar or prop line
    plt.ylim(top=max(max_val, prop_line) * 1.1)

    plt.show()
