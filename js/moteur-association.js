// Jeux « lire » : toucher un graphème puis l'image de son mot-référent (ou l'inverse).
// Le jeu se joue par séries de 8 au plus (les rangées de l'original) quand l'adulte a
// choisi des séances courtes, ou quand l'écran est trop petit pour tout afficher.
// Après 2 erreurs sur un même son, la voix redit le référent ; après 3, la bonne
// réponse brille.

import { melanger } from './data.js';
import { PAR_SERIE, decouper, pointsSeries } from './series.js';

const TAILLE_CONFORT = 64; // en dessous, on découpe en séries
const TAILLE_MIN = 44;     // en dessous, on fait défiler plutôt que de rapetisser
const TAILLE_MAX = 170;
const TAILLE_MAX_CLASSE = 280; // mode classe : visible du fond de la salle au TBI

function ordonner(items, melange, cible) {
  if (melange === 'tout' || melange === cible) return melanger(items);
  if (melange === `${cible}-par-rangee`) {
    const rangees = [...new Set(items.map(i => i.rangee))];
    return rangees.flatMap(r => melanger(items.filter(i => i.rangee === r)));
  }
  return [...items];
}

// Taille de police selon la longueur du graphème (« a » … « ouille »).
function echelle(texte) {
  return [0, .62, .5, .4, .32, .27, .23][Math.min(texte.length, 6)];
}

// Plus grande case possible pour n paires sans défilement (colonnes imposées ou non).
function calculer(plateau, n, colonnesImposees, max = TAILLE_MAX) {
  const style = getComputedStyle(plateau);
  const gap = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gap')) || 8;
  const L = plateau.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
  const H = plateau.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom) - 30
    - (plateau.querySelector('.series') ? plateau.querySelector('.series').offsetHeight + 20 : 0);
  const taillePour = c => {
    const r = Math.ceil(n / c);
    return Math.min((L - (c - 1) * gap) / c, (H / 2 - (r - 1) * gap) / r);
  };
  let meilleur = { c: 1, s: 0 };
  const candidats = colonnesImposees ? [colonnesImposees] : Array.from({ length: n }, (_, i) => i + 1);
  for (const c of candidats) {
    const s = taillePour(c);
    if (s > meilleur.s) meilleur = { c, s };
  }
  if (meilleur.s < TAILLE_MIN) {
    // ça ne tient pas : cases minimales, et on défile (les graphèmes restent en haut)
    const c = Math.max(1, Math.floor((L + gap) / (TAILLE_MIN + gap)));
    meilleur = { c, s: (L - (c - 1) * gap) / c };
  }
  return { c: meilleur.c, s: Math.floor(Math.min(meilleur.s, max)) };
}

function appliquer(plateau, { c, s }) {
  plateau.style.setProperty('--cols', c);
  plateau.style.setProperty('--taille', `${s}px`);
}

export function lancerAssociation(plateau, partie) {
  const { jeu, items } = partie;
  const parRangee = jeu.melange.endsWith('par-rangee');
  const voyelles = jeu.famille === 'alphabet';

  // Séances courtes demandées, ou cases trop petites pour tout afficher : séries de 8.
  // (les jeux « par rangée » s'affichent en 8 colonnes : c'est cette taille-là qui compte)
  const max = partie.classe ? TAILLE_MAX_CLASSE : TAILLE_MAX;
  const tailleUnique = calculer(plateau, items.length, parRangee ? PAR_SERIE : null, max).s;
  const series = partie.seriesCourtes || tailleUnique < TAILLE_CONFORT
    ? decouper(items, jeu.melange)
    : [items];
  let numero = 0;
  let serie = [];
  let trouvesDansSerie = 0;
  let erreursSerie = 0;

  function ajusterIci() {
    let mesure = calculer(plateau, serie.length, null, max);
    // jeux par rangées en une seule série : garder 8 colonnes si les cases restent assez grandes
    if (parRangee && series.length === 1) {
      const enRangees = calculer(plateau, serie.length, PAR_SERIE, max);
      if (enRangees.s >= TAILLE_MIN + 8) mesure = enRangees;
    }
    appliquer(plateau, mesure);
  }

  function afficherSerie() {
    serie = series[numero];
    trouvesDansSerie = 0;
    erreursSerie = 0;
    const graphemes = ordonner(serie, jeu.melange, 'graphemes');
    const images = ordonner(serie, jeu.melange, 'images');
    plateau.innerHTML = `
      ${pointsSeries(series, numero)}
      <div class="zone zone-graphemes" role="group" aria-label="Sons">
        ${graphemes.map(it => `
          <button class="case grapheme ${voyelles && it.voyelle ? 'voyelle' : ''}" data-type="g" data-id="${it.id}"
            style="font-size: calc(var(--taille) * ${echelle(it.graphie)})" aria-label="${it.graphie}">${it.graphie}</button>`).join('')}
      </div>
      <hr class="separateur">
      <div class="zone zone-images" role="group" aria-label="Images">
        ${images.map(it => `
          <button class="case image" data-type="i" data-id="${it.id}" aria-label="${it.mot || 'image'}">${partie.visuel(it)}</button>`).join('')}
      </div>`;
    ajusterIci();
  }

  function serieSuivante() {
    numero++;
    // la dernière série est célébrée par l'écran de fin (jeu.js)
    if (numero < series.length) partie.celebrerSerie(erreursSerie, series[numero - 1].length, afficherSerie);
  }

  afficherSerie();
  new ResizeObserver(ajusterIci).observe(plateau);

  const parId = id => items.find(i => i.id === id);
  let selection = null; // le bouton choisi en premier
  const erreursSur = {}; // id du son → erreurs commises en le cherchant

  function choisir(bouton) {
    if (selection) selection.classList.remove('selection');
    selection = bouton;
    if (bouton) bouton.classList.add('selection');
  }

  // Étayage progressif sur le son (ou l'image) que l'enfant cherche à associer.
  function aider(choisi) {
    const id = choisi.dataset.id;
    erreursSur[id] = (erreursSur[id] || 0) + 1;
    if (erreursSur[id] === 2) partie.direIndice(parId(id));
    if (erreursSur[id] >= 3) {
      const autreZone = choisi.dataset.type === 'g' ? 'i' : 'g';
      plateau.querySelector(`.case[data-type="${autreZone}"][data-id="${id}"]`)?.classList.add('indice');
      if (erreursSur[id] === 3) partie.aide();
    }
  }

  plateau.addEventListener('click', e => {
    const bouton = e.target.closest('.case');
    if (!bouton || bouton.classList.contains('trouve')) return;
    partie.essai();
    const item = parId(bouton.dataset.id);

    // rien de choisi, ou on change d'avis dans la même zone
    if (!selection || selection.dataset.type === bouton.dataset.type) {
      choisir(bouton === selection ? null : bouton);
      if (bouton.dataset.type === 'i' && selection) partie.direMot(item);
      return;
    }

    if (selection.dataset.id === bouton.dataset.id) {
      for (const b of [selection, bouton]) {
        b.classList.add('bravo');
        b.addEventListener('animationend', () => { b.classList.remove('bravo'); b.classList.add('trouve'); }, { once: true });
      }
      plateau.querySelectorAll('.indice').forEach(b => b.classList.remove('indice'));
      choisir(null);
      partie.dire(item);
      partie.reussite();
      trouvesDansSerie++;
      if (trouvesDansSerie === serie.length) serieSuivante();
    } else {
      // erreur douce : ça tremble, la première sélection reste active
      bouton.classList.remove('secoue');
      void bouton.offsetWidth;
      bouton.classList.add('secoue');
      partie.erreur();
      erreursSerie++;
      partie.confusion(selection.dataset.id, bouton.dataset.id);
      aider(selection);
    }
  });
}
