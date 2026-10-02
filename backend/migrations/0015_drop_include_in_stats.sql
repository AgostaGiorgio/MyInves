-- Rimozione del flag include_in_stats: i tipi di asset sono fissi, non serve
-- piu' escludere dinamicamente degli asset dalle statistiche.
ALTER TABLE assets DROP COLUMN include_in_stats;
