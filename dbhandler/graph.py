#! /usr/bin/python

import plotly.offline as py
from plotly.graph_objs import Scatter, Line, Marker, Figure, Data, Layout, XAxis, YAxis

import networkx as nx

import random

import sqlite3

def copy_players(soccer_cursor, G):
    soccer_cursor.execute('''SELECT id FROM Player''')

    for row in soccer_cursor.fetchall():
        G.add_node(row[0])

def create_edges(soccer_cursor, G):
    soccer_cursor.execute('''SELECT id FROM Team''')

    for row in soccer_cursor.fetchall():
        soccer_cursor.execute(''' SELECT player_id FROM History WHERE team_id=%s''' % row[0])
        players_same_team = soccer_cursor.fetchall()
        for player1 in players_same_team:
            for player2 in players_same_team:
                if(player1[0] != player2[0]):
                    G.add_edge(player1[0], player2[0])

soccer_db = sqlite3.connect('../db/soccer.sqlite')
soccer_cursor = soccer_db.cursor()

G = nx.Graph()

copy_players(soccer_cursor, G)
create_edges(soccer_cursor, G)

pos = {i:(random.randint(0,50),random.randint(0,100)) for i in G.nodes()}

nx.set_node_attributes(G, pos, 'pos')

pos=nx.get_node_attributes(G,'pos')

dmin=1
ncenter=0
for n in pos:
    x,y=pos[n]
    d=(x-0.5)**2+(y-0.5)**2
    if d<dmin:
        ncenter=n
        dmin=d

p=nx.single_source_shortest_path_length(G,ncenter)

edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

for node, adjacencies in G.adjacency():
    node_trace['marker']['color'].append(len(adjacencies))
    node_info = '# of connections: '+str(len(adjacencies))
    node_trace['text'].append(node_info)

fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

py.plot(fig, filename='networkx.html')

soccer_db.close()