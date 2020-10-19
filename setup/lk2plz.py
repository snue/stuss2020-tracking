#!/usr/bin/env python3
import mysql.connector
import csv
import os.path
import sys

def print_e(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_e("expected exactly one search string to generate zip codes (e.g.", sys.argv[0], " <district_match>)")
        sys.exit(1)
    needle = sys.argv[1]
    csvfile = os.path.join(sys.path[0], "zuordnung_plz_ort_landkreis_sorted.csv")
    plz_res = []
    last_lk = None
    with open(csvfile, mode='r') as c:
        r = csv.reader(c)
        next(r) # skip header
        for row in r:
            plz = row[3]
            lk = row[4]
            if needle in lk:
                if last_lk and last_lk != lk:
                    print_e(f"error: multiple matches for needle \"{needle}\": \"{last_lk}\" and \"{lk}\"")
                    sys.exit(1)
                plz_res.append(plz)
                last_lk = lk

    print("\n".join(plz_res))
    print_e("found", len(plz_res), "zip codes for district:", last_lk)
