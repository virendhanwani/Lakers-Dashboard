import streamlit as st
import pandas as pd
from typing import List, Optional
import markdown
import io
from nba_api.stats.endpoints import teamgamelog, teamdashboardbyopponent
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def main():
    gamelog = teamgamelog.TeamGameLog(team_id=1610612747, season='2020-21', season_type_all_star='Regular Season')
    oppdetails = teamdashboardbyopponent.TeamDashboardByOpponent(measure_type_detailed_defense='Opponent', season_type_all_star='Regular Season',per_mode_detailed='PerGame',season='2020-21', team_id=1610612747)
    df = gamelog.get_data_frames()[0]
    df = df.sort_values(by = 'GAME_DATE')
    df.reset_index(inplace=True)
    del df['index']
    df['Opponent'] = df['MATCHUP'].str.strip().str[-3:]
    df['location'] = df['MATCHUP'].apply(lambda x: 'away' if x[-5] == '@' else 'home')
    oppdf = oppdetails.get_data_frames()[0]
    fgpct_fig = px.line(df, x='GAME_DATE', y=['FG_PCT','FG3_PCT','FT_PCT'])
    stl_tov_fig = px.line(df, x='GAME_DATE', y=['STL','TOV'])
    blk_pf_fig = px.line(df, x='GAME_DATE', y=['BLK','PF'])
    ast_fig = px.bar(df, x='GAME_DATE', y='AST')
    reb_fig = go.Figure(data=[go.Bar(
        name = 'OREB',
        x = df['GAME_DATE'],
        y = df['OREB']
    ),
        go.Bar(
        name = 'DEEB',
        x = df['GAME_DATE'],
        y = df['DREB']
    )
    ])
    reb_fig.update_layout(barmode='stack')
    fg_plot = go.Figure(data=[go.Bar(
        name = 'FGM',
        x = df['GAME_DATE'],
        y = df['FGM']
    ),
        go.Bar(
        name = 'FGA',
        x = df['GAME_DATE'],
        y = df['FGA']
    )
    ])
    fg_plot.update_layout(barmode='stack')

    st.set_page_config(layout="wide")
    st.write(df)
    st.write(oppdf)
    # Space out the maps so the first one is 2x the size of the other three
    c1, c2 = st.beta_columns(2)
    c1.title('Lakers Dashboard')
    c1.header(f'Wins: {oppdf.W[0]}')
    c1.header(f'Losses: {oppdf.L[0]}')
    winpct_fig = px.line(df, x='GAME_DATE', y='W_PCT')
    c2.plotly_chart(winpct_fig, use_container_width=True)
    fig_stat = ['Overall', 'Home', 'Away']
    classifier = st.selectbox('Filter', fig_stat, index=0)
    c3, c4 = st.beta_columns([3,2])
    c5, c6 = st.beta_columns([3,2])
    if classifier == 'Overall':
        c3.plotly_chart(fgpct_fig, use_container_width=True)
        c4.plotly_chart(ast_fig, use_container_width=True)
        st.plotly_chart(reb_fig, use_container_width=True)
        c5.plotly_chart(stl_tov_fig, use_container_width=True)
        c6.plotly_chart(blk_pf_fig, use_container_width=True)
    elif classifier == 'Home':
        home_figs(df[df['location'] == 'home'],c3,c4,c5,c6)
        
    elif classifier == 'Away':
        away_figs(df[df['location'] == 'away'],c3,c4,c5,c6)


def home_figs(home_df,c3,c4,c5,c6):    
    home_fgpct_fig = px.line(home_df, x='GAME_DATE', y='FG_PCT')
    home_ast_fig = px.bar(home_df, x='GAME_DATE', y='AST')
    home_stl_tov_fig = px.line(home_df, x='GAME_DATE', y=['STL','TOV'])
    home_blk_pf_fig = px.line(home_df, x='GAME_DATE', y=['BLK','PF'])
    home_fg_plot = go.Figure(data=[go.Bar(
        name = 'FGM',
        x = home_df['GAME_DATE'],
        y = home_df['FGM']
    ),
        go.Bar(
        name = 'FGA',
        x = home_df['GAME_DATE'],
        y = home_df['FGA']
    )
    ])
    home_fg_plot.update_layout(barmode='stack')
    home_reb_fig = go.Figure(data=[go.Bar(
        name = 'OREB',
        x = home_df['GAME_DATE'],
        y = home_df['OREB']
    ),
        go.Bar(
        name = 'DEEB',
        x = home_df['GAME_DATE'],
        y = home_df['DREB']
    )
    ])
    home_reb_fig.update_layout(barmode='stack')
    c3.plotly_chart(home_fgpct_fig, use_container_width=True)
    c4.plotly_chart(home_ast_fig, use_container_width=True)
    st.plotly_chart(home_reb_fig, use_container_width=True)
    c5.plotly_chart(home_stl_tov_fig, use_container_width=True)
    c6.plotly_chart(home_blk_pf_fig, use_container_width=True)

def away_figs(away_df,c3,c4,c5,c6):
    away_fgpct_fig = px.line(away_df, x='GAME_DATE', y='FG_PCT')
    away_ast_fig = px.bar(away_df, x='GAME_DATE', y='AST')
    away_stl_tov_fig = px.line(away_df, x='GAME_DATE', y=['STL','TOV'])
    away_blk_pf_fig = px.line(away_df, x='GAME_DATE', y=['BLK','PF'])
    away_fg_plot = go.Figure(data=[go.Bar(
        name = 'FGM',
        x = away_df['GAME_DATE'],
        y = away_df['FGM']
    ),
        go.Bar(
        name = 'FGA',
        x = away_df['GAME_DATE'],
        y = away_df['FGA']
    )
    ])
    away_fg_plot.update_layout(barmode='stack')
    away_reb_fig = go.Figure(data=[go.Bar(
        name = 'OREB',
        x = away_df['GAME_DATE'],
        y = away_df['OREB']
    ),
        go.Bar(
        name = 'DEEB',
        x = away_df['GAME_DATE'],
        y = away_df['DREB']
    )
    ])
    away_reb_fig.update_layout(barmode='stack')
    c3.plotly_chart(away_fgpct_fig, use_container_width=True)
    c4.plotly_chart(away_ast_fig, use_container_width=True)
    st.plotly_chart(away_reb_fig, use_container_width=True)
    c5.plotly_chart(away_stl_tov_fig, use_container_width=True)
    c6.plotly_chart(away_blk_pf_fig, use_container_width=True)

main()