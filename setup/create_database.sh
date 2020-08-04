#!/bin/bash

mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS besuchertracker;

CREATE TABLE IF NOT EXISTS besuchertracker.stammdaten (
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

CREATE TABLE IF NOT EXISTS besuchertracker.verlaufsdaten (
  id BIGINT NULL AUTO_INCREMENT,
  zeitstempel DATE,
  besucher_id BIGINT NULL,
  aktion VARCHAR(45) NULL,
  PRIMARY KEY (id));

CREATE TABLE IF NOT EXISTS besuchertracker.zustandsdaten (
  besucher_id BIGINT NULL,
  zustand VARCHAR(45) NULL,
  PRIMARY KEY (besucher_id));

USE besuchertracker

DELIMITER $$
CREATE PROCEDURE sp_besucherSpeichern (
  IN p_besucher_id VARCHAR(45),
  IN p_name VARCHAR(45),
  IN p_addresse1 VARCHAR(45),
  IN p_plz VARCHAR(5),
  IN p_addresse2 VARCHAR(45),
  IN p_telefon VARCHAR(20),
  IN p_email VARCHAR(45),
  IN p_status VARCHAR(10),
  IN p_coronawarn BIGINT
)
BEGIN
    insert into stammdaten
    (
       besucher_id,
       name,
       addresse1,
       plz,
       addresse2,
       telefon,
       email,
       status,
       coronawarn
    )
    values
    (
       p_besucher_id,
       p_name,
       p_addresse1,
       p_plz,
       p_addresse2,
       p_telefon,
       p_email,
       p_status,
       p_coronawarn
    );
END$$
DELIMITER ;

EOF
