#!/bin/bash
# Dieses Script generiert fortlaufende Barcodes auf A4 Seiten
# requires barcode
echo "Wie viele Barcodes sollen generiert werden?"
read num
seq 10001 $(( 10000 + num )) | barcode -umm -t 1x20 -g 20x10+85+0 -p A4 -o armband.ps
# Keine Rotation moeglich ...
# WORKAROUND #
ps2pdf armband.ps armbandA3.pdf
mutool poster -y 2 armbandA3.pdf armbandA4.pdf
# In Wirklichkeit wird A4 zu A5 gesplittet
# Das Resultat sind senkrechte Barcodes
rm armband.ps armbandA3.pdf

barcode -b "KOMMT" -b "GEHT" -b "RESERVIERT" -o status.ps -t 1x3 -m 150,60

echo "Fertig"
