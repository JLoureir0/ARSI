#!/usr/bin/env python

import sqlite3

nodes_csv = open('../db/nodes.csv', 'w')
nodes_csv.write('id, label, teams\n')

edges_csv = open('../db/edges.csv', 'w')
edges_csv.write('source, target\n')

soccer_db = sqlite3.connect('../db/soccer.sqlite')
soccer_cursor = soccer_db.cursor()

def create_nodes(soccer_cursor, nodes_csv):
    soccer_cursor.execute('''SELECT id,name FROM Player''')

    for row in soccer_cursor.fetchall():
        if(row[0] and row[1]):
            soccer_cursor.execute('''SELECT name from Team LEFT JOIN History
            ON History.team_id=Team.id WHERE player_id=%s''' % row[0])
            teams = ""
            for team in soccer_cursor.fetchall():
                teams += team[0]
            nodes_csv.write('%s, %s, %s\n' % (row[0], row[1], teams.replace(',', '')))

def create_edges(soccer_cursor, edges_csv):
    soccer_cursor.execute('''SELECT id FROM Team''')

    teams = soccer_cursor.fetchall()

    for row in teams:
        soccer_cursor.execute(''' SELECT player_id FROM History WHERE team_id=%s''' % row[0])
        players_same_team = soccer_cursor.fetchall()

        players_visited = []

        for player1 in players_same_team:
            players_visited.append(player1)
            for player2 in players_same_team:
                if(player2 not in players_visited and player1[0] != player2[0]):
                    edges_csv.write('%s, %s\n' % (player1[0], player2[0]))

create_nodes(soccer_cursor, nodes_csv)
create_edges(soccer_cursor, edges_csv)

soccer_db.close()
edges_csv.close()
