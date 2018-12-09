
USE OSRSGE;

DROP TABLE IF EXISTS itemQuery;
CREATE TABLE itemQuery
(
  id              int unsigned NOT NULL auto_increment, #unique ID
  datetime        DATETIME,
  itemname        varchar(255) NOT NULL,                # Name of item
  members         varchar(255) NOT NULL,                # Members-only
  buyaverage      int NOT NULL,               # Average buy price
  buyquantity     int NOT NULL,         #Quantity bought in the last 30 min
  sellaverage     int NOT NULL,               # Average sell price
  sellquantity    int NOT NULL,         #Quantity sold in the last 30 min
  overallaverage  int NOT NULL,
  overallquantity int NOT NULL,
  PRIMARY KEY     (id)
);