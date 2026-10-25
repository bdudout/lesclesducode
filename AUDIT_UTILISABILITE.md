# Audit de facilité d'utilisation — Les clés du code (version web)

Audit de la version web (MVP avec dessins SVG), en octobre 2026, vu par deux utilisateurs :

- **l'élève** : 5-7 ans (GS, CP, CE1), ne lit pas ou peu, joue au doigt sur tablette, sur
  téléphone ou au TBI ;
- **le professeur** : prépare la séance, choisit les jeux, suit les progrès, souvent sans
  temps ni aide informatique.

Méthode : parcours complets des 12 jeux dans le navigateur à 375×812 (téléphone),
768×1024 et 1024×768 (tablette) et 1920×1080 (TBI), mesures dans la page, et
comparaison avec l'application d'origine. **Rien n'a été testé avec de vrais enfants ou
enseignants** : à faire en priorité pour confirmer ce classement.

Priorités : **P1** empêche l'usage réel en classe · **P2** gêne fortement ou fait
perdre son intérêt pédagogique · **P3** confort et finition.

## Corrections faites (25 octobre 2026)

- **#2 Choix des graphèmes** : dans l'espace adulte, cases à cocher par famille (et par
  rangée pour les complexes). Le menu affiche « 8/40 ». Lien de séance possible :
  `jeu.html?id=doubles&g=cr,br,dr`.
- **#3 Consigne et son** : grand bouton ▶ au départ, qui débloque le son et dit la
  consigne. Le réglage de la voix est passé dans l'espace adulte ; 👂 sert seulement à
  réécouter.
- **#4 Sortie accidentelle** : 🏠 demande un appui long d'une seconde (anneau de
  progression).
- **#5 et #11 Petits écrans** : quand les cases feraient moins de 64 px, le jeu passe en
  séries de 8 au plus, avec un ⭐ entre les séries et des points de progression. Mesuré :
  103 px sur téléphone au lieu de 51 px, 147 px sur tablette paysage en complexes 1 et 2.
- **#1 Hors-ligne** : polices embarquées et service worker en place (non testable dans le
  navigateur de l'app Claude). L'hébergement reste à faire.

P2, corrigés le même jour :

- **#6 Clavier intégré** : les jeux « écrire » ont leur propre clavier, en gros, avec
  seulement les lettres de la famille et les accents en évidence (é è ê ç œ), ⌫ et ✔.
  Le clavier du système ne s'ouvre plus ; le clavier physique marche sur ordinateur.
- **#7 Aide après erreurs** : après 2 erreurs sur un même son, la voix redit le référent
  complet ; après 3, la bonne image (ou les bonnes touches) brille. Les aides sont
  comptées dans la fiche.
- **#8 Menu sans texte** : chemin en 4 étapes numérotées et colorées, dans l'ordre de la
  méthode, et badge 👀 lire / ✏️ écrire sur chaque jeu. Les titres écrits sont masqués
  (réglage adulte pour les afficher).
- **#9 Profils et confusions** : élèves ajoutés dans l'espace adulte (prénom + animal),
  écran « Qui joue ? » à l'arrivée, ⭐ par élève, fiche de scores filtrable par élève
  avec les confusions fréquentes (« on → ou ×4 »).
- **#10 Aide au professeur** : page `enseignants.html` (lien en bas du menu et dans ⚙️),
  avec l'indication « Adulte : rester appuyé sur ⚙️ » visible au menu.
- **#11 Séances courtes** : séries de 8 paires par défaut, sur tous les écrans et dans les
  deux types de jeux (réglage adulte pour revenir au plateau complet).

P3, corrigés le même jour :

- **#12 Pression** : chrono et erreurs masqués par défaut (réglables) ; la fin de partie
  annonce seulement « 26 trouvés ! ». Les erreurs restent dans la fiche de l'adulte.
- **#13 Dessins** : les 6 couleurs sont un crayon de couleur et son trait, au lieu d'une
  tache. Les référents doubles montrent les deux objets (carotte + cerise, pot + pomme,
  salade + rose, gâteau + girafe). « Point » est le point qui finit une phrase. Toucher
  une carte de la fiche d'aide dit son référent. Validation par un enseignant ou les
  auteurs toujours conseillée.
- **#14 Mode classe (TBI)** : réglage adulte ou `&classe=1` dans l'adresse. Cases jusqu'à
  280 px (264 px mesurés sur 1920×1080), barre et clavier agrandis, sans chrono ni
  erreurs.
- **#15 Cursive** : « Playwrite FR Trad » (cursive française traditionnelle avec
  attaques, licence OFL), embarquée, à la place de la cursive moderne.
- **#16 Accessibilité** : « ? » blanc à la place du ❓ rouge peu contrasté, voyelles
  soulignées en plus du rouge, fiche d'aide qui ne se ferme plus qu'avec un gros ✖.

## Synthèse classée

| # | Prio | Pour | Problème | Effort |
|---|---|---|---|---|
| 1 | P1 | Prof | Il faut lancer un serveur en ligne de commande, et rien ne marche sans Internet | Moyen |
| 2 | P1 | Prof | Impossible de choisir les graphèmes travaillés cette semaine : c'est tout ou rien | Moyen |
| 3 | P1 | Élève | La consigne n'est jamais dite d'elle-même, et le réglage du son est incompréhensible | Faible |
| 4 | P1 | Élève | Un seul toucher sur 🏠 fait quitter la partie et tout perdre | Faible |
| 5 | P1 | Élève | Sur téléphone, cases de 51 px, et en « complexes » les graphèmes cachent 55 % de l'écran | Moyen |
| 6 | P2 | Élève | Jeux « écrire » : le clavier du système cache le jeu, et é è ê ç œ sont presque impossibles à taper | Moyen |
| 7 | P2 | Élève | Après plusieurs erreurs, aucune aide : l'enfant tourne en rond | Faible |
| 8 | P2 | Élève | Menu rempli de texte ; les 4 jeux « écrire » se ressemblent ; aucun ordre de progression | Faible |
| 9 | P2 | Prof | Pas de suivi par élève, et les scores ne montrent pas les confusions (b/d, on/ou…) | Moyen |
| 10 | P2 | Prof | L'espace adulte est invisible et rien n'explique comment utiliser l'outil | Faible |
| 11 | P2 | Élève | Séances trop longues : 40 paires d'affilée en graphèmes complexes | Faible |
| 12 | P3 | Élève | Chrono et compteur d'erreurs affichés par défaut : pression inutile à 5 ans | Faible |
| 13 | P3 | Élève | Certains dessins restent ambigus (taches de couleur, chiffres, point, 1+1, h muet) | Moyen |
| 14 | P3 | Prof | Mode TBI : barre minuscule, rien de prévu pour jouer en classe entière | Moyen |
| 15 | P3 | Prof | La cursive affichée n'est pas celle enseignée en classe | Faible |
| 16 | P3 | Les deux | Petits défauts d'accessibilité (contraste du ❓, mots-référents doubles) | Faible |

## Détail

### 1. P1 — Installer et utiliser hors connexion (professeur)
**Constat.** L'appli ne s'ouvre qu'avec `python3 -m http.server` lancé dans un terminal.
Une fois ouverte, les polices viennent de Google Fonts et il n'y a pas de cache : sans
Wi-Fi, ça ne marche plus. Beaucoup de classes ont un réseau instable ou des tablettes
sans connexion.
**Impact.** Aucun enseignant ne passera ce cap : l'outil ne sera pas utilisé.
**Recommandation.** Héberger gratuitement (GitHub Pages ou Netlify) pour avoir une
simple adresse à taper. En faire une application installable et hors-ligne (PWA :
manifest, service worker, polices en local). Proposer enfin les versions Android et
iPhone (étape suivante prévue).

### 2. P1 — Choisir les graphèmes à travailler (professeur)
**Constat.** Chaque jeu impose sa famille entière (26, 40, 13 ou 12 paires). La méthode
avance pourtant graphème par graphème : en novembre de CP, faire associer « euille » ou
« ouille » n'a aucun sens.
**Impact.** L'outil n'accompagne pas la progression de la classe. Le prof doit tout
expliquer ou laisser l'enfant échouer.
**Recommandation.** Dans l'espace adulte, ajouter une liste « graphèmes étudiés » à
cocher (préremplie par rangées, dans l'ordre de la méthode). Les jeux ne tirent alors
que parmi ces graphèmes. Ajouter aussi un lien de séance partageable
(`jeu.html?id=complexes1&g=ou,on,an`) pour le TBI ou l'ENT.

### 3. P1 — Consigne et son (élève)
**Constat.** Sur l'écran de jeu, rien n'est dit tant que l'enfant n'a pas pensé à
toucher 👂. Le bouton son tourne sur 🔊 → 🔉 → 🔇 sans rien dire : un enfant le touche
par hasard et coupe le son sans le savoir. La voix de synthèse n'a pas été vérifiée à
l'oreille, et sa qualité dépend de l'appareil (souvent robotique sur Android d'entrée de
gamme).
**Impact.** Un non-lecteur ne sait pas quoi faire. Le son, qui est le cœur de la
méthode (« ou de rouge »), peut disparaître sans que l'adulte s'en aperçoive.
**Recommandation.** Dire la consigne au premier toucher sur le plateau. Déplacer le
réglage du son dans l'espace adulte et ne laisser à l'enfant que 👂 « réécouter ».
Enregistrer de vraies voix (une page « studio » pour l'enseignant, ou les sons fournis
par les auteurs).

### 4. P1 — Sortie accidentelle (élève)
**Constat.** 🏠 est collé à 👂 dans la barre. Un toucher ramène au menu sans
confirmation, et la partie en cours est perdue.
**Impact.** Fréquent avec de petits doigts. Frustrant pour l'enfant, qui recommence à
zéro, et pénible pour l'adulte, rappelé à chaque fois.
**Recommandation.** Appui long sur 🏠 (anneau de progression, comme pour ⚙️) ou
confirmation en image (« ✔ / ✖ »). Garder la partie en mémoire pour pouvoir la
reprendre.

### 5. P1 — Taille des cibles sur téléphone (élève)
**Constat (mesuré à 375×812).** Toutes les cases font 51 px, sous les 64 px
recommandés pour des doigts d'enfant. En graphèmes complexes, la zone des graphèmes
reste collée en haut et occupe 409 px sur 740 : les 40 images défilent dans les 330 px
restants. Sur tablette paysage, les cases des jeux complexes descendent aussi vers
60 px.
**Impact.** Erreurs de toucher comptées comme des erreurs de lecture. L'enfant perd de
vue l'image qu'il cherche.
**Recommandation.** Jouer **une rangée de 8 à la fois** (comme les rangées de
l'original), avec passage automatique à la suivante. Ça règle aussi le point 11.

### 6. P2 — Jeux « écrire » sur tablette (élève)
**Constat.** Le clavier du système couvre la moitié de l'écran et propose 26 lettres en
AZERTY, plus chiffres et symboles. Taper « é », « è », « ê », « ç » ou « œu » demande un
appui long que l'enfant ne connaît pas. La saisie exige l'accent, à raison, mais rend
le jeu impossible.
**Recommandation.** Clavier intégré au jeu, en gros : seulement les lettres utiles et
des touches é è ê ç œ visibles. Version simplifiée en option : choisir parmi 3 à 4
étiquettes au lieu de taper.

### 7. P2 — Aide après des erreurs (élève)
**Constat.** Une erreur fait seulement trembler la case. Rien ne change après 3, 5 ou
10 erreurs sur la même paire.
**Recommandation.** Étayage progressif. Après 2 erreurs sur une même lettre, redire
« a de ananas » ; après 3, faire briller la bonne image. Compter ces aides dans les
scores de l'adulte.

### 8. P2 — Menu lisible sans savoir lire (élève)
**Constat.** Chaque vignette a un titre écrit (« Graphèmes complexes — écrire ») et un
numéro. Les quatre jeux « écrire » ne se distinguent que par un petit dessin. Rien
n'indique par où commencer.
**Recommandation.** Un chemin visuel par famille (alphabet → complexes → doubles →
autres), dire le nom du jeu au toucher, une icône « lire » 👀 / « écrire » ✏️ plus
grande, et les jeux pas encore travaillés en grisé (réglable par l'adulte).

### 9. P2 — Suivi des élèves (professeur)
**Constat.** Les scores sont stockés par appareil, sans nom. Sur une tablette partagée
par 25 élèves, la fiche mélange tout le monde. Elle donne erreurs et temps, mais pas
**quelles** paires sont confondues, l'information la plus utile pour la remédiation.
**Recommandation.** Profils sans compte (prénom + avatar, choisis en début de
partie). Enregistrer les confusions (ex. « b choisi pour d », 4 fois) et les afficher
par élève. Export CSV ou impression par élève.

### 10. P2 — Espace adulte et aide au professeur (professeur)
**Constat.** ⚙️ est semi-transparent dans un coin et s'ouvre par un appui long que
rien n'annonce. Il n'y a ni notice ni explication de la méthode.
**Recommandation.** Une page « Pour les enseignants » visible depuis le menu (même
avec un appui long) : principe des référents, déroulé conseillé, réglages, affiche
imprimable (`referents.html`, déjà prête). Une ligne d'aide dans la fenêtre ⚙️ elle-même.

### 11. P2 — Durée des séances (élève)
**Constat.** 40 paires d'affilée en graphèmes complexes, soit 5 à 10 minutes pour un
bon lecteur et beaucoup plus pour un débutant. Aucun point de pause.
**Recommandation.** Séries courtes par défaut (8 paires, une rangée), avec une petite
célébration à chaque série et une barre de progression en images.

### 12. P3 — Pression du chrono et des erreurs (élève)
**Constat.** ❌ et ⏱️ s'affichent par défaut, et la fin de partie annonce « 3 erreurs ».
**Recommandation.** Les masquer par défaut pour l'élève (les garder dans la fiche
adulte). Fin de partie toujours positive (« 26 trouvés ! »).

### 13. P3 — Dessins ambigus (élève)
**Constat.** Les 91 dessins sont cohérents et lisibles, mais certains référents sont
abstraits par nature : les couleurs (rouge, jaune, bleu, vert, gris, blanc) sont des
taches, « deux / cinq / quatre / huit / cent » sont des chiffres, et « point »,
« addition » (1+1) et « h muet » (chut) restent difficiles sans explication. Les
référents doubles (« carotte ou cerise », « pot ou pomme », « salade ou rose », « gâteau
ou girafe ») n'ont qu'un dessin.
**Recommandation.** Faire valider les dessins par un enseignant ou les auteurs. Pour
les couleurs, dessiner un objet typique (pomme rouge, soleil jaune…) si la méthode le
permet. Ajouter le second dessin des référents doubles. Toucher une image dit déjà le
mot, ce qui aide beaucoup.

### 14. P3 — Usage au TBI (professeur)
**Constat.** À 1920×1080, la barre d'outils fait 52 px de haut, illisible du fond de
la classe, et les cases plafonnent à 170 px.
**Recommandation.** Mode « classe » : barre et cases agrandies, score collectif, sans
chrono.

### 15. P3 — Cursive scolaire (professeur)
**Constat.** « Playwrite FR Moderne » est lisible, mais ses lettres n'ont pas les
attaques de l'écriture cursive enseignée en maternelle et au CP.
**Recommandation.** Une police cursive scolaire française libre de droits, embarquée
dans l'appli.

### 16. P3 — Accessibilité et détails
- Le ❓ rouge sur la barre sombre manque de contraste.
- Les voyelles ne sont signalées que par la couleur rouge. C'est un repère de la
  méthode, mais un enfant daltonien ne le voit pas : ajouter un soulignement léger.
- La fiche d'aide se ferme en touchant n'importe où, y compris par erreur.

## Par où commencer

1. **Rapides et fort impact** (≈ 1 jour) : points 3, 4, 7, 12, et l'aide dans ⚙️ (10).
2. **Socle classe** (≈ 3-5 jours) : hébergement + hors-ligne (1), choix des graphèmes
   (2), une rangée à la fois (5 et 11).
3. **Ensuite** : clavier intégré (6), profils et confusions (9), menu en chemin (8).
4. **Avant toute diffusion** : tester avec 3 à 5 enfants et 2 enseignants, et obtenir
   l'accord des auteurs sur les référents et les dessins.
