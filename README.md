# Les clés du code — version web (MVP)

**En ligne : https://bdudout.github.io/lesclesducode/** (non référencé par les moteurs
de recherche). Chaque envoi sur la branche `main` republie le site automatiquement
(`.github/workflows/pages.yml`) ; le cache hors-ligne des tablettes se met à jour tout
seul.

Portage web responsive des 12 jeux de [lesclesducode.fr](http://www.lesclesducode.fr/)
pour apprendre le code alphabétique (mots-référents « a de ananas », « ou de rouge »…).

## Lancer

Les modules JavaScript ne s'ouvrent pas en double-cliquant le fichier : il faut un petit
serveur local.

```bash
python3 -m http.server 8123
```

Puis ouvrir <http://localhost:8123>. Pour tester sur une tablette du même réseau :
`http://<adresse-ip-du-mac>:8123`.

## Pour l'enseignant

Le mode d'emploi complet est dans `enseignants.html` (lien en bas du menu).

Espace adulte : **appui long** sur ⚙️ en bas à droite du menu. On y gère les élèves
(prénom + animal), la voix, les graphèmes travaillés (seuls ceux-là apparaissent dans
les jeux), les séances courtes, l'affichage, et la fiche de scores par élève avec les
confusions fréquentes.

Lien de séance (par exemple pour le TBI ou l'ENT) : ajouter à l'adresse d'un jeu `&g=`
suivi des graphèmes voulus, et `&classe=1` pour le mode TBI (tout en plus grand), par
exemple `jeu.html?id=complexes1&g=ou,on,an,au&classe=1`.

## Installer sur tablette ou téléphone

**Sans store (le plus simple).** Une fois le site en ligne (GitHub Pages, Netlify), ouvrir
l'adresse dans Chrome (Android) ou Safari (iPhone/iPad), puis « Ajouter à l'écran
d'accueil ». L'appli se met en cache et fonctionne ensuite sans connexion.

**Applis natives Android et iPhone (Capacitor).** Les projets sont déjà générés dans
`android/` et `ios/`. Il reste à installer les outils :

| Pour | À installer | Compte pour publier |
|---|---|---|
| Android | [Android Studio](https://developer.android.com/studio) (inclut Java et le SDK) | Google Play Console, 25 $ une fois |
| iPhone / iPad | Xcode (App Store du Mac), puis `sudo xcode-select -s /Applications/Xcode.app` | Apple Developer, 99 $ par an (gratuit pour tester sur son propre iPhone) |

Ensuite, à chaque modification du jeu :

```bash
npm run android
```

```bash
npm run ios
```

Ces commandes recopient le jeu dans `www/`, mettent à jour le projet natif et l'ouvrent
dans Android Studio ou Xcode. Le bouton ▶︎ y lance l'appli sur un émulateur ou un
appareil branché. `npm run icones` régénère les icônes depuis `assets/icon-only.png`.

Dans les applis natives, la voix passe par le module
`@capacitor-community/text-to-speech`, car la WebView Android ne fournit pas la
synthèse vocale du navigateur.

## Organisation

- `data/referentiel.json` : les 91 graphèmes, leurs mots-référents et la phrase dite
- `data/jeux.json` : les 12 jeux (famille, type d'écriture, mélange)
- `js/moteur-association.js` : jeux « lire » · `js/moteur-ecriture.js` : jeux « écrire »
- `js/jeu.js` : écran de jeu commun (barre, aide, score) · `js/menu.js` : menu, « Qui joue ? », espace adulte
- `js/series.js` : découpage en séries de 8 · `js/natif.js` : accès au téléphone (appli)
- `enseignants.html` : guide enseignant
- `img/referents/` : les 91 dessins SVG, générés par `outils/svg_referents.py`
  (`python3 outils/svg_referents.py .` après une retouche)
- `referents.html` : affiche imprimable de tous les référents
- `sw.js` + `manifest.webmanifest` : appli installable et hors-ligne
- `android/`, `ios/`, `capacitor.config.json` : applis natives

## Ajouter ses images et ses sons

- Image : déposer `img/referents/<famille>/<id>.svg` (ou .webp/.png/.jpg) et ajouter
  `"<famille>/<id>.svg"` dans `img/images.json`.
- Son : déposer `son/<famille>/<id>.mp3` (« ou de rouge ») et, au besoin,
  `<id>_mot.mp3` (« rouge »), puis les lister dans `son/sons.json`.

Les `id` sont ceux de `data/referentiel.json` (ex. `complexes/eacute`).

Sans fichier, l'appli affiche un emoji et utilise la voix de synthèse du navigateur.

## Droits

Les mots-référents viennent de *La boîte à outils pour l'apprentissage du code en
lecture-écriture* (Retz). Les images et sons du site d'origine ne sont pas repris. Avant
toute diffusion publique, demander l'accord des auteurs.

Voir `AMELIORATIONS.md` pour la suite.
