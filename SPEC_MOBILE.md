# Spécifications — applis Android et iPhone

Version 1, 25 octobre 2026.

## 1. Quelle technologie ?

L'appli est petite : 12 jeux, 2 moteurs, environ 1 500 lignes de code, 91 dessins et
aucun serveur. Son contenu est déjà écrit en HTML/CSS/JS et marche sur tous les écrans.

| Option | Ce que c'est | Code réutilisé | Travail pour 2 plateformes | Entretien par 1 personne | Verdict |
|---|---|---|---|---|---|
| **A. Site installable (PWA)** | Le site, « ajouté à l'écran d'accueil » | 100 % | Déjà fait | Très simple | ✅ à garder en parallèle |
| **B. Web embarqué (Capacitor)** | Le même site, emballé dans une vraie appli native avec accès au téléphone (voix, stockage, bouton retour) | ~100 % | Quelques jours | Simple : une seule base de code | ✅ **retenu** |
| C. React Native / Expo | Interface réécrite en composants React, rendue en natif | ~10 % (seulement les données) | 3 à 5 semaines : tout l'écran est à réécrire, sans CSS Grid, SVG par une bibliothèque | Moyen : 2 bases de code (web + appli) | ❌ |
| D. Natif Swift + Kotlin | 2 applis écrites séparément | 0 % | 2 × 4 à 6 semaines | Lourd : 3 bases de code | ❌ |
| E. Flutter | Interface réécrite en Dart | ~10 % | 3 à 5 semaines | Moyen : 2 bases de code | ❌ |

**Pourquoi pas React Native ?** Son intérêt est d'avoir des écrans natifs fluides pour
des applis riches : listes infinies, navigation complexe, animations lourdes. Ici, un
plateau de cases touchées une à une ne profite d'aucun de ces avantages. Il faudrait en
revanche tout réécrire (la grille qui s'ajuste, les dessins SVG, les polices) et
maintenir le site web à part.

**Et React tout court (pour le web) ?** Pas utile à cette taille. Si l'appli grossit
(profils élèves, parcours, statistiques), Preact ou React avec Vite resteraient
compatibles avec Capacitor : la question pourra être rouverte sans rien jeter.

**Risque connu de l'option B.** Apple refuse parfois les applis qui ne sont « qu'un site
web » (règle 4.2 des App Store Review Guidelines). Nos parades : jeu entièrement
hors-ligne et embarqué, voix native, stockage natif, aucune page web distante.

## 2. Périmètre

Mêmes fonctions que la version web : 12 jeux, espace adulte, fiche de scores, affiche des
référents. **Aucune connexion nécessaire**, aucun compte, aucune publicité, aucun
traceur.

| | Android | iOS / iPadOS |
|---|---|---|
| Version minimale | Android 7.0 (API 24, fixé par Capacitor 8) | iOS 15 |
| Appareils visés | tablettes de classe, téléphones des parents | iPad de classe, iPhone |
| Orientation | libre (portrait et paysage) | libre |
| Identifiant | `fr.lesclesducode.app` | `fr.lesclesducode.app` |

## 3. Exigences natives

| # | Exigence | Pourquoi | Comment | Lot |
|---|---|---|---|---|
| N1 | **Voix française du système** | La WebView Android n'a pas de synthèse vocale | Module `@capacitor-community/text-to-speech` ; si aucune voix française n'est installée, l'espace adulte le signale avec la marche à suivre | 1 (voix faite, alerte à faire) |
| N2 | **Stockage durable** des réglages et des scores | iOS peut vider le stockage d'une WebView quand l'appareil manque de place | Module `@capacitor/preferences`, recopié dans `localStorage` au démarrage ; chaque écriture va aux deux | 1 |
| N3 | **Bouton retour Android** sans sortie accidentelle | Un enfant qui appuie sur « retour » perdrait sa partie | Dans un jeu : ignoré, et 🏠 clignote pour montrer la sortie (appui long). Au menu : comportement normal (quitter) | 1 |
| N4 | **Mise en arrière-plan** | La voix continuait et le chrono tournait appli fermée | Événements `pause` / `resume` du module `@capacitor/app` : couper la voix, figer le chrono | 1 |
| N5 | **Plein écran pendant le jeu** | Moins de distractions, plus de place | Barre d'état masquée dans les jeux, visible au menu (`@capacitor/status-bar`) ; marges de sécurité déjà gérées | 1 |
| N6 | **Retour tactile** léger à chaque paire trouvée | Renforce la réussite, surtout en mode muet | `@capacitor/haptics`, désactivable dans l'espace adulte | 1 |
| N7 | Icônes et écran de démarrage | Identité, exigence des stores | `npm run icones` (fait) | ✅ |
| N8 | Aucune donnée collectée | Règles Google Play « Familles » et Apple « Kids » | Aucun SDK tiers ; politique de confidentialité d'une page | 3 |
| N9 | Verrouiller l'appli pendant la séance | La tablette passe d'un enfant à l'autre | Expliquer l'Accès guidé (iOS) et l'Épinglage d'écran (Android) dans le guide enseignant | 3 |

## 4. Exigences non fonctionnelles

- Taille installée de moins de 15 Mo, démarrage en moins de 2 s sur une tablette
  d'entrée de gamme.
- Toute l'appli fonctionne en mode avion.
- Un seul code source : le dossier `www/` est régénéré depuis le site
  (`npm run www`), et l'on ne modifie jamais `android/app/src/main/assets` ni
  `ios/App/App/public` à la main.
- Les modules natifs sont appelés uniquement depuis `js/natif.js`. Dans un navigateur,
  ce fichier ne fait rien et le site continue de marcher tel quel.

## 5. Lots

| Lot | Contenu | Qui | Prérequis |
|---|---|---|---|
| **1 — Socle natif** | N2 à N6 et l'alerte de N1 dans le code, projets synchronisés | ✅ fait le 25/10, validé avec des modules simulés (pas encore sur un vrai appareil) | aucun |
| 2 — Premiers essais sur appareil | Compiler, tester sur 1 tablette Android et 1 iPad, corriger | Vous + Claude | Android Studio, Xcode |
| 3 — Publication | Fiches des stores, captures, politique de confidentialité, classement « Éducation 3+ », signature | Vous + Claude | Comptes Google Play (25 $) et Apple Developer (99 $/an), **accord des auteurs / Retz** |
| 4 — Automatisation | Compilation automatique (GitHub Actions) à chaque version | Claude | dépôt GitHub |

## 6. Tests (lot 2)

| Appareil | Ce qu'on vérifie |
|---|---|
| Tablette Android 10″ d'entrée de gamme | voix FR, fluidité, bouton retour, mode avion |
| Téléphone Android récent | séries de 8, encoches et barre de gestes |
| iPad (9ᵉ génération ou équivalent) | voix, Accès guidé, rotation |
| iPhone | séries de 8, encoche, son en mode silencieux |

Pour chaque appareil : une partie complète d'un jeu « lire » et d'un jeu « écrire »,
l'espace adulte, puis fermer et rouvrir l'appli pour vérifier que réglages et scores
sont conservés.
