# Revue à trois voix — propositions pour le handoff (27 octobre 2026)

Trois revues en lecture seule, chacune d'un point de vue : **enfant** de 5-7 ans non lecteur,
**professeur** (GS/CP/CE1, ULIS, RASED, orthophoniste), **adulte apprenant le français**
(FLE, alphabétisation) et son formateur. Les points déjà corrigés dans
`AUDIT_UTILISABILITE.md` sont exclus. Les doublons entre revues sont fusionnés ; la colonne
« Vu par » indique qui l'a relevé (E enfant, P prof, A adulte).

Effort : S ≤ ½ journée, M 1-3 jours, L au-delà. ⚠️ = à valider par l'autrice (méthode) ou
Retz (droits) avant de coder.

## P1 — à faire en premier

| # | Sujet | Constat | Proposition | Vu par | Effort |
|---|---|---|---|---|---|
| 1 | **Graphèmes qui s'écrivent pareil** (pas un bug) | `er` de cahier [e] / de vert [ɛʁ], `œu` de œuf [œ] / de nœud [ø] : même graphie, sons différents, c'est voulu par la méthode. Mais les deux cartes sont identiques à l'œil et muettes au toucher : l'enfant ne peut les distinguer qu'au hasard. | Faire entendre le son d'une carte graphème quand on la touche (voir 19), au moins pour ces deux paires. Les confusions affichent déjà le référent (« er (cahier) → er (vert) »). | E, P | S |
| 2 | **Sauvegarde et transfert des données** | Profils, réglages et scores sont dans le `localStorage` de chaque appareil (`js/data.js:47-60`) : 25 prénoms à ressaisir sur chaque tablette, suivi éparpillé. | Dans ⚙️ : « Exporter » en fichier JSON et « Importer » avec fusion par élève et par date. Fichier local uniquement, jamais de serveur. | P | M |
| 3 | **Perte des scores sur iPad/Safari** | Safari peut vider le stockage d'un site après 7 jours sans visite (vacances). Aucun appel à `navigator.storage.persist()` hors Capacitor ; l'aide à l'installation n'existe que pour Android (`js/menu.js:259`). | Appeler `storage.persist()` ; ajouter la marche à suivre iPad (Partager → « Sur l'écran d'accueil ») dans ⚙️ et le guide ; rappeler d'exporter avant les vacances. | P | S |
| 4 | **Démonstration animée de la consigne** | « Touche un son, et ensuite l'image » est abstrait pour un enfant de GS et incompréhensible pour un adulte A0. | Au premier lancement de chaque type de jeu : une main animée touche un graphème, puis l'image, puis ✔ (3 s, sans texte). Elle revient après 10 s d'inactivité. | E, A | M |
| 5 | **Thème « adulte »** ⚠️ | Confettis, 🦄🎈🐢, « champion », avatars animaux : un adulte décroche dès le premier écran. L'original avait une version ados-adultes. | Réglage `theme: 'adulte'` (et `?theme=adulte`) : célébration sobre, phrases neutres (« Très bien. », « Série terminée. ») avec leurs mp3, initiales ou couleurs à la place des animaux. La version enfant ne change pas. | A | M |

## P2 — important

| # | Sujet | Constat | Proposition | Vu par | Effort |
|---|---|---|---|---|---|
| 6 | **Erreur muette** | Une erreur fait seulement trembler la case ; avec « réduire les animations », il ne se passe rien. | Dire le mot de l'image touchée par erreur (aide sans donner la réponse) ; garder un contour même en mouvement réduit. | E | S |
| 7 | **Le référent coupé** | Chaque son coupe le précédent (`js/audio.js:79`) : un enfant rapide coupe « ou de rouge », le cœur de la méthode. | Pendant le son d'une paire trouvée, ignorer le mot d'une image explorée (ou le jouer après). | E | S |
| 8 | **Fin « courage » vécue comme un échec** | Étoiles grises et 🐢 (`js/celebration.js:20,40`) contredisent la règle « fin toujours positive ». | Pas d'étoiles vides (1 à 3 étoiles qui apparaissent) ; retirer 🐢 et « champion ». | E, A | S |
| 9 | **Aide de l'écriture sans ordre des lettres** | Après 3 erreurs, les touches s'allument sans ordre (`js/moteur-ecriture.js:60`) : inutile pour « eille ». Une erreur efface tout le champ (l. 115). | Graphème en gris dans le champ, à recopier ; saisie fausse laissée en rouge 1 s avant effacement. | E | S |
| 10 | **✔ de l'écriture pas compris** | L'enfant tape puis attend. | Faire pulser ✔ après 1,5 s sans frappe si le champ n'est pas vide. | E | S |
| 11 | **Graphèmes choisis par élève** | `reglages.graphemes` est global (`js/data.js:79`) ; en ULIS ou en groupes de besoin, chacun a sa progression. | Option « progression personnelle » sur la fiche élève, prioritaire sur le réglage de la classe. | P | M |
| 12 | **Lien de séance** | `?g=` attend des ids internes (`eacute`, `er1`) ; `g=é` est ignoré sans message. | Bouton « 🔗 Copier le lien de cette séance » (et QR code) dans ⚙️ ; accepter la graphie dans `g=`. Ajouter des séances nommées à rappeler (« Semaine 12 : ch, on, oi »). | P, A | S→M |
| 13 | **Synthèse de la classe et impression** | 30 dernières parties et top 10 des confusions, rien par graphème. L'impression sort toute la boîte de dialogue (`css/app.css:422`). | Tableau élèves × graphèmes (acquis / avec aide / confondu) avec filtre de période ; bilan A4 par élève pour le cahier et les parents ; export CSV. | P | M |
| 14 | **Données d'élève (RGPD)** | « Retirer » un élève garde ses scores ; le guide dit à tort qu'« Effacer les scores » efface aussi les prénoms (`enseignants.html:113`). | « Retirer et effacer ses scores », « Tout effacer (fin d'année) », phrase du guide corrigée, paragraphe « données d'élèves » pour le directeur. | P | S |
| 15 | **Atelier tournant** | Le joueur reste choisi pour la session : l'enfant suivant joue sous le nom du précédent. Au-delà de 24 élèves, les animaux sont en double (`js/menu.js:111`). | Réglage « redemander Qui joue ? après chaque partie » ; 32 avatars ou animal + couleur, sans doublon. | P | S |
| 16 | **Séries par défaut sur tablette** | `seriesCourtes: false` : 52 cases d'un coup pour l'alphabet sur iPad (charge forte pour les dys et les enfants qui ont du mal à se concentrer). | Séries de 8 par défaut pour les jeux « lire » ; le plateau complet devient un choix de l'adulte. Mettre aussi le bouton ⊞ / 1·2 en appui long. | E | S |
| 17 | **Le son seul (phonème)** ⚠️ | L'original avait un mode « son seul ». Ici les consonnes disent le **nom** de la lettre (« sé » pour c de carotte, « jé » pour g de gâteau) : contradictoire pour qui relie son et graphie. | Mode « /k/… carotte » généré par Piper depuis `api`. À valider par l'autrice. | A | M |
| 18 | **Mot écrit, graphème en couleur** | Le mot n'est que dans `alt` (`js/jeu.js:76`). | Après une paire trouvée et dans la fiche ❓ : « r**ou**ge » avec le graphème en couleur. Pont vers les mots réels. | A | S |
| 19 | **Découvrir avant d'être évalué** | Toucher un graphème ne dit rien ; l'affiche `referents.html` est muette. | Affiche parlante (toucher une carte = « ou de rouge ») accessible depuis le menu. | A | S |
| 20 | **Voix lente sans effet sur les mp3** | `voixLente` ne s'applique qu'à la synthèse de secours (`js/audio.js:45`). | Série lente Piper (length_scale ≈ 1,3) au moins pour les mots ; bouton 🐢 de réécoute dans le thème adulte. | A | S/M |
| 21 | **Poids et données mobiles** | `sw.js` met les deux voix en cache et retélécharge environ 5 Mo à chaque version. | Cacher seulement la voix choisie ; cache des médias séparé et stable ; ré-encodage Opus 24-32 kbps. | A | M |
| 22 | **Dessins ambigus** ⚠️ | tête / nez dans la même rangée (piège), lait → « verre d'eau », cahier → « livre » (autre référent), pigeon → « oiseau », point → « boule », couleurs seulement par la teinte (daltonisme). | Nez coloré sur visage estompé, tête avec repère, brique de lait, flèche sur la partie visée, motif ou objet en plus de la couleur. Passer par `outils/recette.html`. | E | M |
| 23 | **Mots-référents pour adultes** ⚠️ | fantôme, dragon, princesse, kangourou… peu utiles au quotidien. | Dans le thème adulte, une table de référents de rechange (pharmacie, adresse, taxi, zéro, kilo…). Accord de l'autrice et de Retz indispensable. | A | L |

## P3 — confort

| # | Sujet | Proposition | Vu par | Effort |
|---|---|---|---|---|
| 24 | Suite après la fin | Bouton ▶ « jeu suivant » sur l'écran de fin ; pulsation au menu sur le prochain jeu sans ⭐. | E | S |
| 25 | Clavier trop petit sur téléphone | Touches à 40 px (`css/app.css:323`) : ne garder que les lettres utiles à la série, plus quelques autres, pour agrandir. | E | M |
| 26 | Fiche ❓ chargée | Cartes de la série en cours d'abord, le reste plus bas. | E | S |
| 27 | « Qui joue ? » silencieux | Dire la consigne au premier toucher. | E | S |
| 28 | Guide enseignants | Corriger l'erreur sur la fiche ❓ (`enseignants.html:73` : « toucher pour fermer », alors qu'il faut toucher ✖) ; encadré « Démarrage en 5 minutes », sommaire, version 1 page, sections « Parc de tablettes » et « FLE / alphabétisation » ; manifeste moins centré sur GS-CE1. | P, A | S |
| 29 | Couleur des voyelles hors alphabet ⚠️ | Vérifier avec l'autrice si le rouge s'applique aussi aux graphèmes vocaliques et aux voyelles des consonnes doubles. | P | S |
| 30 | Élision « a de ananas » ⚠️ | Garder la formule de la méthode ; en thème adulte, « é, comme dans épée ». | A | S |
| 31 | Lire de vrais mots | 3ᵉ moteur « lire un mot » (3 images, 1 mot) à partir des graphèmes cochés ; hors périmètre de l'original. | A | L |

## Phonétique

Les 91 champs `api` de `data/referentiel.json` ont été relus : aucune erreur. Une seule
convention est mêlée : voyelles notées par leur son, consonnes par leur nom. C'est ce qui motive le n° 17.

## Points forts à ne pas casser (consensus des trois revues)

1. **Tout se fait sans lire** : grand ▶ qui dit la consigne, chemin numéroté, aide graduée
   (référent redit à la 2ᵉ erreur, bonne case qui brille à la 3ᵉ), fin toujours positive.
2. **Tout reste sur l'appareil** : sans compte, sans traceur, hors-ligne. Toute fonction
   d'export doit rester un fichier local.
3. **Fidélité à la méthode** : « ou de rouge » à chaque paire, rangées des complexes,
   cursive à attaques, voyelles rouges. Également : clavier intégré avec é è ê ç œ, et
   appui long sur 🏠 / ⚙️.

## Ordre conseillé

1. Correctifs S sans dépendance : 3, 6, 7, 8, 9, 10, 14, 16, 28.
2. Pour les classes : 2, 11, 12, 13, 15.
3. Démonstration animée (4), puis cartes et affiche parlantes (1, 19) et mot écrit (18).
4. Après avis de l'autrice et de Retz : 5, 17, 22, 23, 29, 30.
