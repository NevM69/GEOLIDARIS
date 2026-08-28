# Guide Copernicus pour la recherche de personnes disparues (SAR terrestre)

*Guide pratique pour ONG — compte public gratuit, environnements montagne/forêt, rural, conflit/catastrophe.*

---

## 1. La réalité physique — à lire en premier

Ce point conditionne toute votre stratégie : **aucun satellite Copernicus ne peut détecter un corps humain.**

| Capteur | Résolution | Un humain (~0,5 × 1,8 m) représente |
|---|---|---|
| Sentinel-2 (optique) | 10 m/pixel | ~1/100e d'un pixel |
| Sentinel-1 (radar SAR) | 5 × 20 m | invisible |
| Sentinel-3 | 300 m | invisible |
| Meilleur commercial (Maxar, Pléiades Neo) | 30 cm | 1–2 pixels, indétectable de façon fiable |

Même l'imagerie commerciale la plus chère du monde ne permet pas de repérer une personne. La détection directe de corps se fait par **drone** (caméra thermique + RGB, 30–90 m d'altitude, où une personne occupe des centaines de pixels) ou par équipes terrain.

**Le rôle réel de Copernicus est indirect mais précieux : cartographier, prioriser et surveiller la zone de recherche.** C'est là que ce guide vous rend efficace.

---

## 2. Ce que Copernicus peut réellement faire pour vous

**Cartographie de zone de recherche.** Image récente (revisite Sentinel-2 : 3–5 jours) de la zone : état de la végétation, enneigement, chemins, clairières, plans d'eau, zones brûlées. Indispensable pour sectoriser une battue ou planifier des vols drone.

**Détection de changement à l'échelle du paysage.** Comparaison avant/après une date de disparition : crue, glissement de terrain, incendie, coupe forestière, sols remaniés *sur de grandes surfaces*. Un véhicule isolé (~4,5 m) reste sous le seuil de détection fiable de Sentinel-2, mais un changement d'occupation du sol de quelques centaines de m² est visible.

**Conditions environnementales datées.** Quel était l'état du terrain le jour de la disparition ? Neige, crue, brouillard (via couverture nuageuse), étendue d'un incendie. Utile pour reconstituer les déplacements probables et pour les enquêtes post-mortem (fenêtres de dates).

**Radar tout-temps (Sentinel-1).** Voit à travers les nuages, de nuit. Détecte l'eau libre (inondations), les changements de rugosité du sol. Essentiel en zone de catastrophe quand l'optique est bouchée.

**Contexte post-mortem / forensique.** La littérature (détection de fosses, sols remaniés) repose sur de l'imagerie très haute résolution (VHR < 50 cm) et du thermique aéroporté — pas sur Sentinel. Copernicus sert ici à dater des perturbations de grande ampleur (NDVI anormal sur une parcelle, terrassements étendus) et à cibler où commander/demander de la VHR.

---

## 3. Copernicus Browser — outils et paramètres

Accès : **https://browser.dataspace.copernicus.eu** — compte gratuit sur https://dataspace.copernicus.eu (le compte débloque le téléchargement et les timelapses ; la visualisation est libre).

### 3.1 Réglages de base

1. **Collection** : `Sentinel-2 L2A` (corrigée atmosphériquement, à privilégier) ; `Sentinel-1 GRD` pour le radar.
2. **Couverture nuageuse** : filtre à **≤ 20 %** (curseur dans le panneau de recherche). En montagne, vérifiez visuellement — le filtre est calculé sur toute la tuile de 100 km.
3. **Période** : encadrez la date de disparition (une image avant, toutes les images après).

### 3.2 Couches de visualisation utiles (Sentinel-2)

| Couche | Usage recherche |
|---|---|
| **True Color** | Vue générale, briefing équipes |
| **False Color (8,4,3)** | Végétation en rouge vif — clairières, chemins et zones dénudées ressortent nettement en forêt |
| **NDVI** | Anomalies de végétation : parcelle remaniée, stress, coupe |
| **NDWI / NDMI** | Eau et humidité — plans d'eau, zones inondées, marécages (zones de risque) |
| **SWIR (12,8A,4)** | Zones brûlées, sols nus, distingue neige/nuages |
| **Highlight Optimized Natural Color** | Meilleur rendu en zone sombre (forêt dense, ombres de relief) |

### 3.3 « Effects and advanced options » — tirer le maximum du 10 m

En bas du panneau de gauche, cliquez **Show effects and advanced options** :

- **Sampling : Bicubic** — interpolation plus nette que le rendu par défaut quand vous zoomez au-delà de la résolution native. C'est le réglage n°1 pour la lisibilité.
- **Gain : 1,2–2,0** — éclaircit les zones sombres (sous-bois, versants à l'ombre). Montez progressivement.
- **Gamma : 0,8–1,5** — ajuste le contraste des tons moyens ; en forêt, un gamma ~1,3 aide.
- **Canaux R/G/B** — rehaussez légèrement le rouge en False Color pour accentuer les ruptures de végétation.

Limite honnête : ces réglages améliorent la *lisibilité*, pas la *résolution*. À 10 m/pixel, zoomer plus fort n'apporte aucune information nouvelle.

### 3.4 Outils d'analyse intégrés

- **Comparaison (icône double-flèche)** : superposez deux dates en mode *split* ou *opacity* — l'outil central pour la détection de changement avant/après disparition.
- **Timelapse** : animation sur plusieurs semaines pour repérer une perturbation et la dater.
- **Mesure** : distances et surfaces pour sectoriser la battue.
- **Marqueurs / dessin de zone (AOI)** : délimitez la zone de recherche, exportez le GeoJSON pour les scripts du skill.
- **Custom script (evalscript)** : couches sur mesure en JavaScript. Exemple utile — indice de sol nu (BSI) pour repérer les terrassements récents.

### 3.5 Téléchargement de qualité maximale

Icône de téléchargement → **Analytical** :
- Format **TIFF 32-bit float** (ou 16-bit), **résolution HIGH**, CRS UTM.
- Cochez les bandes brutes (B02, B03, B04, B08) plutôt qu'un rendu visuel : vous gardez toute la dynamique pour retravailler dans QGIS.
- L'image « Basic » (JPG/PNG) suffit pour un briefing, jamais pour l'analyse.

Quotas compte gratuit : la visualisation est illimitée ; les téléchargements ont un plafond mensuel de volume (au-delà, débit réduit, pas de blocage). Largement suffisant pour un usage ONG.

---

## 4. Workflow type — disparition en zone montagne/forêt

1. **J0** : dessinez l'AOI dans le Browser autour du dernier point connu (rayon selon profil : 5–10 km marcheur).
2. Chargez la **dernière image claire avant** la disparition (référence) et notez les conditions (neige, crue).
3. **Chaque nouvelle acquisition** (3–5 j) : comparaison split avec la référence en False Color + NDVI. Cherchez : perturbations de végétation, glissements, traces de feu, changements de plans d'eau.
4. Exportez la True Color en TIFF HIGH → fond de carte pour sectoriser les battues et les plans de vol drone.
5. Si nuages persistants : basculez sur **Sentinel-1 GRD** (VV+VH) pour l'eau libre et les changements majeurs.
6. Toute anomalie < 10 m d'intérêt → **vol drone thermique** sur ce secteur, pas de sur-interprétation satellite.

## 5. Ressources complémentaires gratuites (souvent plus décisives)

- **Copernicus EMS Rapid Mapping** (https://emergency.copernicus.eu) : en cas de catastrophe (inondation, séisme, zone de conflit), un « utilisateur autorisé » national (protection civile) peut activer le service — cartes d'impact livrées en 24–48 h, incluant parfois de la VHR commerciale gratuite. Votre ONG peut demander l'activation *via* l'autorité de son pays.
- **Maxar Open Data Program** : imagerie 30 cm gratuite publiée après les grandes catastrophes.
- **NASA FIRMS** : détection de feux actifs en quasi temps réel.
- **OpenAerialMap** : imagerie drone/aérienne partagée par la communauté humanitaire.
- **QGIS** (gratuit) : pour pousser l'analyse des TIFF téléchargés (compositions de bandes, différences NDVI, hillshade).

## 6. Limites déontologiques et pratiques

- Ne présentez jamais une anomalie satellite comme une localisation de corps : c'est une **hypothèse à vérifier terrain/drone**.
- Documentez chaque image utilisée (date, capteur, ID produit) si le dossier peut servir en justice — les produits Sentinel ont des identifiants uniques traçables.
- Coordonnez-vous avec les autorités de recherche officielles ; l'activation EMS et l'accès VHR passent par elles.

---

## Sources

- [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/)
- [Copernicus Browser — documentation](https://documentation.dataspace.copernicus.eu/Applications/Browser.html)
- [Quotas et limitations CDSE](https://documentation.dataspace.copernicus.eu/Quotas.html)
- [Sentinel-2 — documentation CDSE](https://documentation.dataspace.copernicus.eu/Data/Sentinel2.html)
- [API STAC CDSE](https://documentation.dataspace.copernicus.eu/APIs/STAC.html)
- [Guide de démarrage Copernicus Browser (FR, ESERO)](https://esero.fr/assets/uploads/2024/12/copernicus_browser_guide_FR.pdf)
- [EARSC — Satellite images contributing to rescue persons](https://earsc-portal.eu/display/EOwiki/Satellite+images+contributing+to+rescue+persons)
- [SaRNet: Deep Learning Assisted Search and Rescue with Satellite Imagery](https://arxiv.org/pdf/2107.12469)
- [Aerial Person Detection for Search and Rescue: Survey](https://spj.science.org/doi/10.34133/remotesensing.0474)
- [Résolution spatiale en imagerie satellite](https://eos.com/blog/spatial-resolution/)
