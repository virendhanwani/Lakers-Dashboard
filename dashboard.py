from re import template
from plotly.graph_objs import layout
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
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    df = df.sort_values(by = 'GAME_DATE')
    df.reset_index(inplace=True)
    del df['index']
    pct_cols = ['W_PCT', 'FG_PCT', 'FG3_PCT', 'FT_PCT']
    for col in pct_cols:
        df[col] = df[col] * 100
    df['Opponent'] = df['MATCHUP'].str.strip().str[-3:]
    df['location'] = df['MATCHUP'].apply(lambda x: 'away' if x[-5] == '@' else 'home')
    oppdf = oppdetails.get_data_frames()[0]
    layout = go.Layout(
        template='plotly_white',
        xaxis=dict(title_text=''),
        yaxis=dict(title_text=''),
        legend=dict(title_text=''),
        title=dict(x=0.5, y=0.9)
    )
    fgpct_fig = px.line(df, x='GAME_DATE', y=['FG_PCT','FG3_PCT','FT_PCT'],template='plotly_white', color_discrete_map={'FG_PCT': '#FDB827','FG3_PCT': '#542583', 'FT_PCT': '#000000'})
    fgpct_fig.update_layout(layout)
    stl_tov_fig = px.line(df, x='GAME_DATE', y=['STL','TOV'],template='plotly_white', color_discrete_map={'STL': '#FDB827','TOV': '#542583'})
    stl_tov_fig.update_layout(layout)
    blk_pf_fig = px.line(df, x='GAME_DATE', y=['BLK','PF'],template='plotly_white', color_discrete_map={'BLK': '#FDB827','PF': '#542583'})
    blk_pf_fig.update_layout(layout)
    ast_fig = px.bar(df, x='GAME_DATE', y='AST',template='plotly_white', title='Assists')
    ast_fig.update_traces(marker_color='#542583')
    ast_fig.update_layout(layout)
    reb_fig = go.Figure(data=[go.Bar(
        name = 'OREB',
        x = df['GAME_DATE'],
        y = df['OREB'],
        marker=dict(color= '#FDB827')
    ),
        go.Bar(
        name = 'DREB',
        x = df['GAME_DATE'],
        y = df['DREB'],
        marker=dict(color= '#542583')
    )
    ])
    reb_fig.update_layout(barmode='stack', template='plotly_white')

    st.set_page_config(layout="wide")
    st.write(df)
    st.write(oppdf)
    # Space out the maps so the first one is 2x the size of the other three
    c1, c2 = st.beta_columns(2)
    c1.title('Lakers Dashboard')
    c1.header(f'Wins: {oppdf.W[0]}')
    c1.header(f'Losses: {oppdf.L[0]}')
    winpct_fig = px.line(df, x='GAME_DATE', y='W_PCT',template='plotly_white')
    winpct_fig.update_traces(line_color='#FDB827')
    winpct_fig.update_xaxes(title_text='',zeroline=False)
    winpct_fig.update_yaxes(title_text='Win %',zeroline=False)
    # winpct_fig.update_layout({
    #     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    # })
    c2.plotly_chart(winpct_fig, use_container_width=True)
    fig_stat = ['Overall', 'Home', 'Away', 'Wins', 'Losses']
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
        home_figs(df[df['location'] == 'home'],c3,c4,c5,c6, layout)
        
    elif classifier == 'Away':
        away_figs(df[df['location'] == 'away'],c3,c4,c5,c6, layout)
    elif classifier == 'Wins':
        win_figs()
    elif classifier == 'Losses':
        loss_figs()


def home_figs(home_df,c3,c4,c5,c6, layout):    
    home_fgpct_fig = px.line(home_df, x='GAME_DATE', y=['FG_PCT','FG3_PCT','FT_PCT'],template='plotly_white', color_discrete_map={'FG_PCT': '#FDB827','FG3_PCT': '#542583', 'FT_PCT': '#000000'})
    home_fgpct_fig.update_layout(layout)
    home_ast_fig = px.bar(home_df, x='GAME_DATE', y='AST',template='plotly_white', title='Assists')
    home_ast_fig.update_traces(marker_color='#542583')
    home_ast_fig.update_layout(layout)
    home_stl_tov_fig = px.line(home_df, x='GAME_DATE', y=['STL','TOV'],template='plotly_white', color_discrete_map={'STL': '#FDB827','TOV': '#542583'})
    home_stl_tov_fig.update_layout(layout)
    home_blk_pf_fig = px.line(home_df, x='GAME_DATE', y=['BLK','PF'],template='plotly_white', color_discrete_map={'BLK': '#FDB827','PF': '#542583'})
    home_blk_pf_fig.update_layout(layout)
    home_reb_fig = go.Figure(data=[go.Bar(
        name = 'OREB',
        x = home_df['GAME_DATE'],
        y = home_df['OREB'],
        marker=dict(color= '#FDB827')
    ),
        go.Bar(
        name = 'DREB',
        x = home_df['GAME_DATE'],
        y = home_df['DREB'],
        marker=dict(color= '#542583')
    )
    ])
    home_reb_fig.update_layout(barmode='stack', template='plotly_white')
    c3.plotly_chart(home_fgpct_fig, use_container_width=True)
    c4.plotly_chart(home_ast_fig, use_container_width=True)
    st.plotly_chart(home_reb_fig, use_container_width=True)
    c5.plotly_chart(home_stl_tov_fig, use_container_width=True)
    c6.plotly_chart(home_blk_pf_fig, use_container_width=True)

def away_figs(away_df,c3,c4,c5,c6,layout):
    away_fgpct_fig = px.line(away_df, x='GAME_DATE', y=['FG_PCT','FG3_PCT','FT_PCT'],template='plotly_white', color_discrete_map={'FG_PCT': '#FDB827','FG3_PCT': '#542583', 'FT_PCT': '#000000'})
    away_fgpct_fig.update_layout(layout)
    away_ast_fig = px.bar(away_df, x='GAME_DATE', y='AST',template='plotly_white', title='Assists')
    away_ast_fig.update_traces(marker_color='#542583')
    away_ast_fig.update_layout(layout)
    away_stl_tov_fig = px.line(away_df, x='GAME_DATE', y=['STL','TOV'],template='plotly_white', color_discrete_map={'STL': '#FDB827','TOV': '#542583'})
    away_stl_tov_fig.update_layout(layout)
    away_blk_pf_fig = px.line(away_df, x='GAME_DATE', y=['BLK','PF'],template='plotly_white', color_discrete_map={'BLK': '#FDB827','PF': '#542583'})
    away_blk_pf_fig.update_layout(layout)
    away_reb_fig = go.Figure(data=[go.Bar(
        name = 'OREB',
        x = away_df['GAME_DATE'],
        y = away_df['OREB'],
        marker=dict(color= '#FDB827')
    ),
        go.Bar(
        name = 'DREB',
        x = away_df['GAME_DATE'],
        y = away_df['DREB'],
        marker=dict(color= '#542583')
    )
    ])
    away_reb_fig.update_layout(barmode='stack', template='plotly_white')
    c3.plotly_chart(away_fgpct_fig, use_container_width=True)
    c4.plotly_chart(away_ast_fig, use_container_width=True)
    st.plotly_chart(away_reb_fig, use_container_width=True)
    c5.plotly_chart(away_stl_tov_fig, use_container_width=True)
    c6.plotly_chart(away_blk_pf_fig, use_container_width=True)

main()