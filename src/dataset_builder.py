#!/usr/bin/python

import sqlite3

def create_db_tables(db_cursor):
    db_cursor.execute('''DROP TABLE IF EXISTS Player''')
    db_cursor.execute('''CREATE TABLE Player(id INTEGER PRIMARY KEY, name TEXT)''')

    db_cursor.execute('''DROP TABLE IF EXISTS Team''')
    db_cursor.execute('''CREATE TABLE Team(id INTEGER PRIMARY KEY, name TEXT)''')

    db_cursor.execute('''DROP TABLE IF EXISTS History''')
    db_cursor.execute('''CREATE TABLE History(id INTEGER PRIMARY KEY, team_id INTEGER REFERENCES Team(id),
                            player_id INTEGER REFERENCES Player(id))''')

def copy_players(original_db_cursor, db_cursor):
    original_db_cursor.execute('''SELECT Player.player_api_id, Player.player_name FROM Match LEFT JOIN Player 
                                    ON Match.home_player_1 = Player.player_api_id 
									OR Match.home_player_2 = PLAYER.player_api_id
									OR Match.home_player_3 = PLAYER.player_api_id
									OR Match.home_player_4 = PLAYER.player_api_id
									OR Match.home_player_5 = PLAYER.player_api_id
									OR Match.home_player_6 = PLAYER.player_api_id
									OR Match.home_player_7 = PLAYER.player_api_id
									OR Match.home_player_8 = PLAYER.player_api_id
									OR Match.home_player_9 = PLAYER.player_api_id
									OR Match.home_player_10 = PLAYER.player_api_id
									OR Match.home_player_11 = PLAYER.player_api_id
									OR Match.away_player_1 = Player.player_api_id 
									OR Match.away_player_2 = PLAYER.player_api_id
									OR Match.away_player_3 = PLAYER.player_api_id
									OR Match.away_player_4 = PLAYER.player_api_id
									OR Match.away_player_5 = PLAYER.player_api_id
									OR Match.away_player_6 = PLAYER.player_api_id
									OR Match.away_player_7 = PLAYER.player_api_id
									OR Match.away_player_8 = PLAYER.player_api_id
									OR Match.away_player_9 = PLAYER.player_api_id
									OR Match.away_player_10 = PLAYER.player_api_id
									OR Match.away_player_11 = PLAYER.player_api_id
									WHERE Match.league_id=17642 GROUP BY Player.player_api_id''')

    for row in original_db_cursor.fetchall():
        if(row[0] and row[1]):
            db_cursor.execute('''INSERT INTO Player(id, name) VALUES(?,?)''', (row[0], row[1].split(',')[0]))

def copy_teams(original_db_cursor, db_cursor):
    original_db_cursor.execute('''SELECT Team.team_api_id, Team.team_long_name FROM Match LEFT JOIN Team 
                                    ON Match.home_team_api_id = Team.team_api_id WHERE Match.league_id=17642 GROUP BY Team.team_api_id''')

    for row in original_db_cursor.fetchall():
        db_cursor.execute('''INSERT INTO Team(id, name) VALUES(?,?)''', (row[0], row[1]))

def create_players_history(original_db_cursor, db_cursor):
    original_db_cursor.execute('''SELECT home_team_api_id, away_team_api_id,
                                    home_player_1, home_player_2, home_player_3, home_player_4, home_player_5,
                                    home_player_6, home_player_7, home_player_8, home_player_9, home_player_10,
                                    home_player_11,
                                    away_player_1, away_player_2, away_player_3, away_player_4, away_player_5,
                                    away_player_6, away_player_7, away_player_8, away_player_9, away_player_10,
                                    away_player_11
                                    From Match WHERE league_id=17642
                                ''')

    for row in original_db_cursor.fetchall():
        for x in range(11):
            if row[2+x] != None:
                db_cursor.execute('''INSERT OR REPLACE INTO History(id, team_id, player_id) VALUES(?,?,?)''', (row[0]+row[2+x], row[0], row[2+x]))
            if row[13+x] != None:
                db_cursor.execute('''INSERT OR REPLACE INTO History(id, team_id, player_id) VALUES(?,?,?)''', (row[1]+row[13+x], row[1], row[13+x]))

original_soccer_db = sqlite3.connect("../db/soccer_original.sqlite")
soccer_db = sqlite3.connect("../db/soccer.sqlite")

original_db_cursor = original_soccer_db.cursor()
db_cursor = soccer_db.cursor()

create_db_tables(db_cursor)
copy_players(original_db_cursor, db_cursor)
copy_teams(original_db_cursor, db_cursor)
create_players_history(original_db_cursor, db_cursor)

original_soccer_db.close()

soccer_db.commit()
soccer_db.close()