#!/bin/bash
# Dieses Script generiert fortlaufende Barcodes auf A4 Seiten
# requires barcode
echo "Wie viele Barcodes sollen generiert werden?"
read num
for (( i = 1; i <= $num; ++i ));
do
echo $i >> tmp
done
barcode -i "tmp" -umm -t 1x10+80+10 -g 20x19+100+4 -o printThis.ps&&
rm "tmp"&
echo "Fertig"
