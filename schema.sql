drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  height integer not null,
  weight integer not null,
  bmi float not null
);