---
name: copernicus-sar-veille
description: >
  Veille satellite Copernicus (Sentinel-1/2) pour la recherche de personnes
  disparues et l'appui aux opérations de sauvetage (SAR) d'une ONG. Utiliser
  dès que l'utilisateur mentionne : Copernicus, Sentinel, imagerie satellite,
  zone de recherche, personne disparue, veille d'une zone, détection de
  changement, nouvelles images d'une zone, "surveille cette zone", ou demande
  des liens Copernicus Browser pour des coordonnées. Le skill interroge l'API
  STAC publique du CDSE (sans authentification), liste les acquisitions
  disponibles sur une zone/période, filtre par couverture nuageuse et génère
  des liens Copernicus Browser prêts à ouvrir (True Color, False Color, NDVI).
---

# Veille Copernicus pour recherche de personnes disparues

## Rappel critique (à communiquer à l'utilisateur si pertinent)

Sentinel-2 = 10 m/pixel : **un corps humain n'est pas détectable par satellite**,
y compris en imagerie commerciale. Ce skill sert à l'appui indirect :
cartographie de zone, détection de changement à l'échelle du paysage,
priorisation des secteurs pour battues et vols drone. Toute anomalie repérée
est une hypothèse à vérifier par drone thermique ou équipe terrain — jamais
une conclusion.

## Ce que fait le script

`scripts/copernicus_search.py` (Python 3 standard, aucune dépendance,
aucune authentification) interroge `https://stac.dataspace.copernicus.eu/v1/search` :

```bash
# Autour d'un point (rayon en km), Sentinel-2, nuages <= 30 %
python3 scripts/copernicus_search.py --lat 44.92 --lon 6.36 --radius 8 \
    --from 2026-06-01 --to 2026-07-09 --collection s2 --max-cloud 30

# Bbox explicite, Sentinel-1 radar (tout-temps, nuit)
python3 scripts/copernicus_search.py --bbox 6.2,44.85,6.5,45.0 \
    --from 2026-06-01 --to 2026-07-09 --collection s1

# Mode veille : nouvelles acquisitions des N derniers jours
python3 scripts/copernicus_search.py --lat 44.92 --lon 6.36 --radius 8 \
    --since-days 5 --collection s2 --max-cloud 40

# Sortie JSON pour traitement
... --json resultats.json
```

Sortie par acquisition : date/heure, identifiant produit (traçabilité
judiciaire), % nuages, lien quicklook, liens Copernicus Browser True Color /
False Color / NDVI centrés sur la zone.

## Workflow recommandé quand l'utilisateur signale une disparition

1. Demander : coordonnées du dernier point connu (ou lieu à géocoder),
   date de disparition, rayon de recherche (défaut 8 km).
2. Lancer une recherche S2 de J-15 (image de référence *avant*) à aujourd'hui.
3. Présenter le tableau : identifier la **dernière image claire avant** la
   disparition et **toutes les images après** avec nuages < 40 %.
4. Donner les liens Browser par paires (référence / après) et rappeler
   l'outil de comparaison split du Browser + couche False Color et NDVI.
5. Si toutes les images récentes sont nuageuses → relancer en `--collection s1`
   (radar, insensible aux nuages).
6. Proposer une **veille automatique** : tâche planifiée quotidienne exécutant
   le mode `--since-days 2` et signalant toute nouvelle image exploitable
   (utiliser le skill `schedule` de Cowork si disponible).

## Interprétation à fournir avec les résultats

- Revisite Sentinel-2 : 3–5 jours ; Sentinel-1 : 1–3 jours.
- `eo:cloud_cover` est calculé sur la tuile entière (100 km) — une image à
  60 % peut être claire sur la zone d'intérêt : vérifier le quicklook.
- Couches conseillées dans le Browser : False Color (ruptures de végétation
  en forêt), NDVI (parcelles remaniées), NDWI (eau/inondation), SWIR (feux,
  sols nus). Réglages : sampling **Bicubic**, gain 1,2–2,0 en zone sombre.
- Le téléchargement des produits complets exige un compte CDSE gratuit
  (quota mensuel de volume ; visualisation illimitée).

## Notes techniques

- Collections STAC : `sentinel-2-l2a`, `sentinel-1-grd` (vérifiées actives).
- Filtre nuages : CQL2-JSON `eo:cloud_cover <= N` (Sentinel-2 uniquement).
- Les liens Browser utilisent `datasetId=S2_L2A_CDSE` / `S1_CDAS_IW_VVVH` ;
  si le layer exact ne se charge pas, la position/date/zoom restent corrects.
- Limite API : 200 items par requête ; découper la période si nécessaire.
- Si le réseau de la sandbox bloque `stac.dataspace.copernicus.eu`, exécuter
  le script sur la machine de l'utilisateur ou utiliser l'outil web_fetch
  sur l'endpoint GET `/v1/collections/{collection}/items?bbox=...&datetime=...`.
