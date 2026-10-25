# Propositions d'amélioration

Comparaison entre l'application actuelle (lesclesducode.fr/classique, relevée en
octobre 2026) et ce MVP, puis les prochaines étapes conseillées.

## 1. Ce que le MVP améliore déjà

| Application actuelle | MVP |
|---|---|
| Pages en tableaux HTML à taille fixe (800×600) : minuscule sur TBI, illisible sur téléphone | Le plateau calcule la plus grande taille de case possible pour chaque écran, de 375 px à 1920 px |
| 12 pages de ~30 Ko qui recopient le même code, avec un `if` par son | 2 moteurs + 1 fichier de données : ajouter un jeu = ajouter une ligne dans `data/jeux.json` |
| Obligation de toucher la lettre **puis** l'image | Les deux ordres marchent, et on peut changer d'avis dans une même zone |
| Toucher une image ne fait rien | Toucher une image sans lettre choisie dit le mot (« renard ») : l'enfant qui ne reconnaît pas le dessin peut s'aider seul |
| Une erreur ne donne aucun retour visuel | La case tremble doucement, sans son qui gronde, et la sélection reste active |
| Le chrono démarre au chargement de la page | Il démarre au premier essai |
| Le mélange est biaisé (certaines positions reviennent plus souvent) | Mélange équitable (Fisher-Yates) |
| Jeux « écrire » : il faut taper l'identifiant interne (`eacute` au lieu de `é`) | Comparaison avec le graphème réel. Majuscules, espaces et « oe » pour « œ » sont acceptés, mais l'accent est exigé |
| Fiche de scores PDF à remplir à la main | Historique automatique sur l'appareil, consultable et imprimable dans l'espace adulte |
| Chrono et erreurs toujours visibles | Masquables par l'adulte (certains enfants se stressent) |
| Aucun réglage protégé | Espace adulte derrière un appui long d'une seconde sur ⚙️ |
| Jeux déjà réussis non signalés | ⭐ sur les vignettes des jeux terminés |

## 2. Prochaines étapes, par priorité

### Indispensable avant de diffuser
1. **Accord des auteurs / éditions Retz.** Les mots-référents font partie de la méthode.
   Les contacter via le formulaire du site : ils pourraient aussi fournir les
   illustrations et les sons officiels. Il suffirait alors de déposer les fichiers dans
   `img/` et `son/`.
2. **Vrais visuels.** Les emoji dépannent mais certains sont approximatifs (🩶 pour
   « gris », 👤 pour « tête », ⚫ pour « point »), et 9 référents n'en ont pas : le mot
   écrit apparaît à la place (table, xylophone, pyjama, banc, ceinture, bonnet, pelle,
   prune, timbre, yaourt). Or un enfant qui ne lit pas ne peut pas l'utiliser. Il faut
   des dessins SVG simples et cohérents.
3. **Sons enregistrés.** La synthèse vocale varie selon l'appareil et prononce mal les
   sons isolés. Proposition : une petite page « studio » où l'enseignant enregistre
   chaque référent au micro (MediaRecorder), puis télécharge les fichiers.
4. **Hors-ligne (PWA).** Manifest + service worker, polices embarquées en local. Sans
   ça, l'appli ne marche pas dans une école sans Wi-Fi.

### Confort de jeu
5. **Graphèmes complexes sur téléphone** : afficher une rangée de 8 à la fois, avec
   passage automatique à la suivante. Aujourd'hui les 40 graphèmes occupent la moitié de
   l'écran et les images défilent dessous.
6. **Police cursive scolaire.** « Playwrite FR Moderne » est lisible mais n'a pas les
   attaques de l'écriture enseignée en classe. Tester une police cursive française
   libre et l'embarquer.
7. **Clavier virtuel** pour les jeux « écrire » sur tablette : seulement les lettres et
   accents utiles, en gros. Le clavier du système cache la moitié de l'écran.
8. **Parcours progressif** : débloquer les familles dans l'ordre de la méthode
   (alphabet → complexes → doubles → autres), avec un réglage adulte pour tout ouvrir.
9. **Séries courtes** : option « 8 cartes au hasard » plutôt que 26 ou 40, pour des
   séances de 5 minutes.

### Pour l'enseignant
10. **Profils élèves** (prénom + avatar, sans compte) pour suivre plusieurs enfants sur
    une même tablette de classe.
11. **Repérage des confusions** : noter quelles paires sont souvent inversées (b/d, on/ou,
    an/en) et l'afficher dans la fiche de scores.
12. **Version ados-adultes** : un thème avec d'autres illustrations et des célébrations
    plus sobres, au lieu d'une seconde application.
13. **Mode TBI** : barre d'outils plus grande et affichage du score pour toute la classe.
14. **La Combinatoire** (logiciel associé) : un 3ᵉ moteur « fusion » qui réutilise les
    mêmes référents.
