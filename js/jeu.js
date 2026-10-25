// Écran de jeu commun : lit ?id=…, prépare la barre d'outils, l'aide, le score,
// puis confie le plateau au moteur du jeu (association ou écriture).

import './pwa.js';
import { charger, lireReglages, ajouterHistorique, itemsDuJeu, joueurCourant } from './data.js';
import { dire, direMot, direPhrase, taire, debloquer, reglerVitesse } from './audio.js';
import { celebrerSerie, preparerFin } from './celebration.js';
import { surRetour, surPause, surReprise, pleinEcran, vibrer } from './natif.js';
import { lancerAssociation } from './moteur-association.js';
import { lancerEcriture } from './moteur-ecriture.js';
import { appuiLong } from './appui-long.js';

const donnees = await charger();
const parametres = new URLSearchParams(location.search);
const jeu = donnees.jeux.find(j => j.id === parametres.get('id')) || donnees.jeux[0];
const reglages = lireReglages();
const items = itemsDuJeu(donnees.familles[jeu.famille], jeu.famille, reglages, parametres.get('g'));
const joueur = joueurCourant();

document.title = `${jeu.numero}. ${jeu.titre} — Les clés du code`;
// Mode classe (TBI) : réglage adulte, ou ?classe=1 dans l'adresse du jeu.
const modeClasse = reglages.classe || parametres.get('classe') === '1';
document.body.classList.add(`ecriture-${jeu.ecriture}`, `famille-${jeu.famille}`);
document.body.classList.toggle('mode-classe', modeClasse);
reglerVitesse(reglages.voixLente);
debloquer();

const $ = sel => document.getElementById(sel);
$('bloc-chrono').hidden = !reglages.chrono || modeClasse;
$('bloc-erreurs').hidden = !reglages.erreurs || modeClasse;
if (joueur) $('joueur').textContent = joueur.avatar;

// Son : 1 « ou de rouge », 2 le mot seul, 3 muet. Réglé par l'adulte (menu ⚙️),
// pour qu'un enfant ne coupe pas la voix sans s'en rendre compte.
const modeSon = reglages.son;
const sons = donnees.sons;

// Phrase fixe (data/phrases.json) : dite si le son est actif, et renvoyée pour l'affichage.
function phrase(cle) {
  const texte = donnees.phrases[cle] || '';
  if (modeSon !== 3) direPhrase(cle, texte, sons);
  return texte;
}
const consigne = () => phrase(`consigne-${jeu.moteur}`);
$('b-consigne').addEventListener('click', consigne);

// Retour au menu par appui long : un toucher accidentel ne fait plus perdre la partie.
appuiLong($('b-menu'), () => { location.href = 'index.html'; });

// Bouton retour Android : ne quitte pas la partie, montre seulement où est la sortie.
surRetour(() => {
  $('b-menu').classList.remove('montre');
  void $('b-menu').offsetWidth;
  $('b-menu').classList.add('montre');
});
pleinEcran(true);

// ---------- Visuel d'un mot-référent : image déposée, sinon emoji, sinon le mot ----------
function visuel(item) {
  for (const ext of ['svg', 'webp', 'png', 'jpg']) {
    const f = `${jeu.famille}/${item.id}.${ext}`;
    if (donnees.images.has(f)) return `<img src="img/referents/${f}" alt="${item.mot || ''}" draggable="false">`;
  }
  if (item.emoji) return `<span class="emoji" aria-hidden="true">${item.emoji}</span>`;
  // police réduite pour les mots longs (« xylophone ») afin qu'ils tiennent dans la case
  return `<span class="mot" style="font-size: calc(var(--taille, 80px) * ${Math.min(.2, 1.5 / item.mot.length).toFixed(3)})">${item.mot}</span>`;
}

// ---------- Aide : fiche de tous les référents de la famille ----------
// Se ferme seulement avec ✖ (un toucher ailleurs ne la ferme plus par erreur) ;
// toucher une carte fait entendre son référent.
$('aide').innerHTML = `
  <button class="fermer-aide" id="b-fermer-aide" aria-label="Fermer la fiche">✖</button>
  <div class="grille-aide">${items.map(it => `
    <button class="carte-aide" data-id="${it.id}" aria-label="${it.dit}">
      <div class="grapheme ${jeu.famille === 'alphabet' && it.voyelle ? 'voyelle' : ''}">${it.graphie}</div>
      <div class="visuel-aide">${visuel(it)}</div>
      <div class="mot">${it.mot || '(muet)'}</div>
    </button>`).join('')}
  </div>`;
// ---------- Écran de départ : un grand ▶ qui débloque le son et dit la consigne ----------
const [texteVignette, idVignette] = jeu.vignette;
$('apercu').innerHTML = `<span class="grapheme">${texteVignette}</span>`
  + (jeu.moteur === 'ecriture' ? '<span>✏️</span>' : '')
  + `<img src="img/referents/${jeu.famille}/${idVignette}.svg" alt="" draggable="false">`;
$('b-jouer').addEventListener('click', () => {
  $('depart').hidden = true;
  consigne();
});

$('b-aide').addEventListener('click', () => { $('aide').hidden = false; });
$('b-fermer-aide').addEventListener('click', () => { $('aide').hidden = true; });
$('aide').addEventListener('click', e => {
  const carte = e.target.closest('.carte-aide');
  if (carte && modeSon !== 3) dire(jeu.famille, items.find(i => i.id === carte.dataset.id), 1, sons);
});

// ---------- Score et chrono (démarre au premier essai, pas au chargement) ----------
let reussites = 0;
let erreurs = 0;
let secondes = 0;
let tic = null;
let enPause = false;
let aides = 0;
const confusions = []; // [son cherché, réponse donnée] pour la fiche de l'enseignant

function demarrerChrono() {
  if (tic) return;
  tic = setInterval(() => {
    if (enPause) return;
    secondes++;
    $('c-chrono').textContent = `${Math.floor(secondes / 60)}:${String(secondes % 60).padStart(2, '0')}`;
  }, 1000);
}

const partie = {
  jeu,
  items,
  visuel,
  seriesCourtes: reglages.seriesCourtes,
  classe: modeClasse,
  // toute la famille, même si l'enseignant en a retiré : le clavier des jeux « écrire »
  // en tire ses touches, sans trahir les seuls graphèmes du jeu
  famille: donnees.familles[jeu.famille],
  dire: item => dire(jeu.famille, item, modeSon, sons),
  // un toucher sur une image sans sélection : on dit seulement le mot, pour aider
  direMot: item => { if (modeSon !== 3) direMot(jeu.famille, item, sons); },
  // indice après 2 erreurs : on redit le référent complet, quel que soit le réglage de voix
  direIndice: item => { if (modeSon !== 3) dire(jeu.famille, item, 1, sons); },
  // entre deux séries : célébration selon les erreurs de la série, puis la suite
  celebrerSerie: (erreursSerie, total, ensuite) => celebrerSerie({ erreurs: erreursSerie, total, dire: phrase, ensuite }),
  aide() { aides++; },
  confusion(cherche, donne) { confusions.push([cherche, donne]); },
  essai() { demarrerChrono(); },
  reussite() {
    if (reglages.vibrations) vibrer();
    reussites++;
    $('c-reussites').textContent = reussites;
    if (reussites === items.length) finir();
  },
  erreur() {
    erreurs++;
    $('c-erreurs').textContent = erreurs;
  },
};

function finir() {
  clearInterval(tic);
  ajouterHistorique({ jeu: jeu.id, date: Date.now(), erreurs, secondes, joueur: joueur?.id || null, aides, confusions });
  const temps = `${Math.floor(secondes / 60)} min ${String(secondes % 60).padStart(2, '0')} s`;
  // fin toujours positive : les erreurs vont dans la fiche de l'adulte, pas sous les yeux de l'enfant
  const morceaux = [`${items.length} trouvés !`];
  if (reglages.chrono && !modeClasse) morceaux.push(temps);
  $('fin-stats').textContent = morceaux.join(' · ');
  setTimeout(() => {
    $('fin').hidden = false;
    preparerFin({ erreurs, total: items.length, dire: phrase, ecran: $('fin') });
  }, 900);
}

// Appli mise en arrière-plan : on coupe la voix et on fige le chrono.
surPause(() => { enPause = true; taire(); });
surReprise(() => { enPause = false; });

$('b-rejouer').addEventListener('click', () => location.reload());

const moteurs = { association: lancerAssociation, ecriture: lancerEcriture };
moteurs[jeu.moteur]($('plateau'), partie);
