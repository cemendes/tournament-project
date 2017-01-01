-- Table definitions for the tournament project.

-- Drop tournament database if it exists
DROP DATABASE IF EXISTS tournament;

-- Create Database 'Tournament'
CREATE DATABASE tournament;

-- Connect to the tournament database
\connect tournament

-- Drop all tables and views if they exist
DROP TABLE IF EXISTS competitor CASCADE;
DROP tABLE IF EXISTS matches CASCADE;
DROP VIEW IF EXISTS statuses CASCADE;

-- Creates competitor table
CREATE TABLE competitor(
  competitor_id serial PRIMARY KEY,
  competitor_name text
);

-- Creates matches table with FK to competitor
CREATE TABLE matches (
  matches_id serial PRIMARY KEY,
  winner INTEGER,
  loser INTEGER,
  FOREIGN KEY(winner) REFERENCES competitor(competitor_id),
  FOREIGN KEY(loser) REFERENCES competitor(competitor_id)
);

-- Creates a view of matcheses played sorted by won count
CREATE VIEW statuses AS
SELECT p.competitor_id as competitor_id, p.competitor_name,
(SELECT count(*) FROM matches WHERE matches.winner = p.competitor_id) as won,
(SELECT count(*) FROM matches WHERE p.competitor_id in (winner, loser)) as played
FROM competitor p
GROUP BY p.competitor_id
ORDER BY won DESC;