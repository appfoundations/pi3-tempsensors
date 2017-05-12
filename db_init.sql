/*
DB Initialization script
creates 'measure'   table
        'read_idx'  table
        'params'    table

*/

drop table if exists measure;
drop table if exists read_idx;
drop table if exists params;

CREATE TABLE measure(
   idx INTEGER PRIMARY KEY,
   time TEXT,
   probeId TEXT,
   measure TEXT,
   type TEXT
);

CREATE TABLE read_idx(
   table_name TEXT PRIMARY KEY,
   table_idx INTEGER
);

CREATE TABLE params(
   name TEXT PRIMARY KEY,
   type TEXT,
   value TEXT
);

INSERT INTO params (name,type,value)
VALUES ( 'API', 'URL', 'https://dweet.io/dweet/for/uOLM3xEV2gEhEeTJkTxt');

INSERT INTO params (name,type,value)
VALUES ( 'PI_KEY', 'STRING', '0000000000000000');
