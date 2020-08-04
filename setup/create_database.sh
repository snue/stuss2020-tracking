#!/bin/bash

mysql -u root <<EOF
DROP DATABASE besuchertracker;
CREATE DATABASE besuchertracker;
CREATE TABLE besuchertracker.stammdaten (
  besucher_id BIGINT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  addresse1 VARCHAR(45) NULL,
  plz VARCHAR(5) NULL,
  addresse2 VARCHAR(45) NULL,
  telefon VARCHAR(20) NULL,
  email VARCHAR(45) NULL,
  status VARCHAR(10) NULL,
  coronawarn BIGINT NULL,
  PRIMARY KEY (besucher_id));

CREATE TABLE besuchertracker.verlaufsdaten (
  id BIGINT NULL AUTO_INCREMENT,
  zeitstempel DATE,
  besucher_id BIGINT NULL,
  aktion VARCHAR(45) NULL,
  PRIMARY KEY (id));

CREATE TABLE besuchertracker.zustandsdaten (
  besucher_id BIGINT NULL,
  zustand VARCHAR(45) NULL,
  PRIMARY KEY (besucher_id));

EOF
