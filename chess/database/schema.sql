CREATE TABLE IF NOT EXISTS
players (id SERIAL PRIMARY KEY, name TEXT NOT NULL, bot BOOLEAN);

CREATE TABLE IF NOT EXISTS games (id SERIAL PRIMARY KEY,
white_id INTEGER, black_id INTEGER, status TEXT NOT NULL
CHECK ( status IN ('ongoing', 'white_wins', 'black_wins')),
turn TEXT NOT NULL CHECK ( turn IN ('black', 'white', 'finished')), board JSONB);

CREATE TABLE IF NOT EXISTS moves (id SERIAL PRIMARY KEY,
game_id INTEGER, move_number INTEGER, start_square TEXT NOT NULL,
end_square TEXT NOT NULL, piece TEXT NOT NULL, captured_piece TEXT);