#!/bin/bash

mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS besuchertracker;

CREATE TABLE IF NOT EXISTS besuchertracker.stammdaten (
  besucher_id BIGINT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  adresse1 VARCHAR(45) NULL,
  plz VARCHAR(5) NULL,
  adresse2 VARCHAR(45) NULL,
  telefon VARCHAR(20) NULL,
  email VARCHAR(45) NULL,
  status VARCHAR(10) NULL,
  coronawarn BIGINT NULL,
  PRIMARY KEY (besucher_id));

CREATE TABLE IF NOT EXISTS besuchertracker.verlaufsdaten (
  id BIGINT NULL AUTO_INCREMENT,
  zeitstempel DATETIME,
  besucher_id BIGINT NULL,
  aktion VARCHAR(45) NULL,
  PRIMARY KEY (id));

CREATE TABLE IF NOT EXISTS besuchertracker.zustandsdaten (
  besucher_id BIGINT NULL,
  zustand VARCHAR(45) NULL,
  PRIMARY KEY (besucher_id));

EOF
