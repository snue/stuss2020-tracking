#!/bin/bash
# Dieses Script generiert fortlaufende Barcodes auf A4 Seiten
# requires barcode
echo "Wie viele Barcodes sollen generiert werden?"
read num
seq 10001 $(( 10000 + num )) | barcode -umm -t 1x10+80+10 -g 20x19+100+4 -o armband.ps


seq 10001 10010 | barcode -t 2x5 -m 100,50 -o example.ps

barcode -b "kommt" -b "geht" -b "reserviert" -o status.ps -t 1x3 -m 150,60

echo "Fertig"
