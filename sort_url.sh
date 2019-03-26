#!/usr/bin/env bash
#petit script pour faire trier et supprimer les doublons
#zf190326.1444

#source: 

echo -e "site,url" > data/liste_url_unique.csv
echo -e "Avant: "`cat data/liste_url.csv |wc -l`
sort -u data/liste_url.csv >> data/liste_url_unique.csv
echo -e "Après: "`cat data/liste_url_unique.csv |wc -l`
