#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    con = connect()
    cursor = con.cursor()
    query = "DELETE FROM matches"
    cursor.execute(query)
    con.commit()
    con.close()


def deletePlayers():
    """Remove all the player records from the database."""
    con = connect()
    cursor = con.cursor()
    query = "DELETE FROM competitor"
    cursor.execute(query)
    con.commit()
    con.close()


def countPlayers():
    """Returns the number of players currently registered."""
    con = connect()
    cursor = con.cursor()
    query = "SELECT COUNT(*) FROM competitor"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    con.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    con = connect()
    cursor = con.cursor()
    cursor.execute("insert into competitor (competitor_name) values (%s)", (name,))
    con.commit()
    con.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    con = connect()
    cursor = con.cursor()
    query = "SELECT * FROM statuses;"
    cursor.execute(query)
    outcome = cursor.fetchall()
    # If the top two outcome have more than 0 wins AND are equal then reorder them
    # by total wins divided by total games played
    if (outcome[0][2] != 0) and (outcome[0][2] == outcome[1][2]):
        query = "SELECT competitor_id, competitor_name, won, played " \
                "FROM statuses ORDER BY (cast(won AS DECIMAL)/played)  DESC;"
        cursor.execute(query)
        outcome = cursor.fetchall()
    con.close()

    return outcome


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    con = connect()
    cursor = con.cursor()
    cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser,))
    con.commit()
    con.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    con = connect()
    cursor = con.cursor()
    query = "SELECT * FROM statuses"
    cursor.execute(query)
    outcome = cursor.fetchall()
    pairings = []
    count = len(outcome)

    for y in range(0, count - 1, 2):
        paired_list = (outcome[y][0], outcome[y][1], outcome[y + 1][0], outcome[y + 1][1])
        pairings.append(paired_list)

    con.close()
    return pairings