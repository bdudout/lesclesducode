// Jeux « écrire » : sous chaque image, l'enfant écrit le graphème du mot-référent
// avec un clavier intégré au jeu (seulement les lettres utiles, accents visibles).
// Le clavier physique reste utilisable sur ordinateur.
// Après 2 erreurs sur une image, la voix redit le référent ; après 3, les touches de
// la réponse brillent.

import { melanger } from './data.js';
import { decouper, pointsSeries } from './series.js';

const LONGUEUR_MAX = 8;

// Tolérant sur la casse, les espaces et « oe » pour « œ » ;
// exigeant sur les accents (é, è, ê, ç), car c'est ce qu'on apprend.
function normaliser(texte) {
  return texte.trim().toLowerCase().replace(/\s+/g, '').replace(/oe/g, 'œ');
}

// Touches : toutes les lettres des graphèmes de la famille, lettres simples d'abord,
// puis les lettres accentuées (é è ê ç œ), pour qu'elles soient bien visibles.
function touchesDe(famille) {
  const lettres = [...new Set(famille.flatMap(i => [...i.graphie.toLowerCase()]))];
  const simples = lettres.filter(l => /^[a-z]$/.test(l)).sort();
  const speciales = lettres.filter(l => !/^[a-z]$/.test(l)).sort((a, b) => a.localeCompare(b, 'fr'));
  return [...simples, ...speciales];
}

export function lancerEcriture(plateau, partie) {
  const { jeu, items } = partie;
  const series = partie.seriesCourtes ? decouper(melanger(items), 'tout') : [melanger(items)];
  const parId = id => items.find(i => i.id === id);
  let numero = 0;
  let trouvesDansSerie = 0;
  let erreursSerie = 0;
  let active = null; // la fiche où l'on écrit
  const erreursSur = {};

  // ---------- clavier intégré, entre le plateau et la barre d'outils ----------
  const clavier = document.createElement('div');
  clavier.className = 'clavier';
  clavier.setAttribute('role', 'group');
  clavier.setAttribute('aria-label', 'Clavier');
  clavier.innerHTML = touchesDe(partie.famille).map(l =>
    `<button type="button" class="touche ${/^[a-z]$/.test(l) ? '' : 'speciale'}" data-lettre="${l}">${l}</button>`).join('')
    + '<button type="button" class="touche effacer" data-action="effacer" aria-label="Effacer">⌫</button>'
    + '<button type="button" class="touche valider" data-action="valider" aria-label="Valider">✔</button>';
  document.querySelector('.barre').before(clavier);
  document.body.classList.add('avec-clavier');

  function activer(fiche) {
    if (!fiche || fiche.classList.contains('trouve')) return;
    plateau.querySelectorAll('.fiche.active').forEach(f => f.classList.remove('active'));
    clavier.querySelectorAll('.indice').forEach(t => t.classList.remove('indice'));
    active = fiche;
    fiche.classList.add('active');
    fiche.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    // indice déjà mérité sur cette fiche : on le remontre
    if ((erreursSur[fiche.dataset.id] || 0) >= 3) montrerTouches(parId(fiche.dataset.id));
  }

  function montrerTouches(item) {
    for (const l of new Set(item.graphie.toLowerCase())) {
      clavier.querySelector(`[data-lettre="${l}"]`)?.classList.add('indice');
    }
  }

  function afficherSerie() {
    trouvesDansSerie = 0;
    erreursSerie = 0;
    plateau.innerHTML = `
      ${pointsSeries(series, numero)}
      <div class="zone-ecrire">
        ${series[numero].map(it => `
          <div class="fiche" data-id="${it.id}">
            <button type="button" class="case image" aria-label="Écouter : ${it.mot || 'h muet'}">${partie.visuel(it)}</button>
            <input type="text" inputmode="none" autocomplete="off" autocapitalize="off" autocorrect="off"
              spellcheck="false" maxlength="${LONGUEUR_MAX}" aria-label="Écris le son de ${it.mot || 'cette image'}">
          </div>`).join('')}
      </div>`;
    activer(plateau.querySelector('.fiche'));
  }

  function valider() {
    if (!active) return;
    const champ = active.querySelector('input');
    const item = parId(active.dataset.id);
    if (!champ.value.trim()) return;
    partie.essai();

    if (normaliser(champ.value) === normaliser(item.graphie)) {
      active.classList.add('trouve');
      active.classList.remove('active');
      champ.disabled = true;
      clavier.querySelectorAll('.indice').forEach(t => t.classList.remove('indice'));
      partie.dire(item);
      partie.reussite();
      trouvesDansSerie++;
      if (trouvesDansSerie === series[numero].length) {
        active = null;
        numero++;
        // la dernière série est célébrée par l'écran de fin (jeu.js)
        if (numero < series.length) partie.celebrerSerie(erreursSerie, series[numero - 1].length, afficherSerie);
      } else {
        activer(plateau.querySelector('.fiche:not(.trouve)'));
      }
    } else {
      active.classList.remove('secoue');
      void active.offsetWidth;
      active.classList.add('secoue');
      partie.erreur();
      erreursSerie++;
      partie.confusion(item.id, `« ${champ.value.trim()} »`);
      erreursSur[item.id] = (erreursSur[item.id] || 0) + 1;
      if (erreursSur[item.id] === 2) partie.direIndice(item);
      if (erreursSur[item.id] === 3) { montrerTouches(item); partie.aide(); }
      champ.value = '';
    }
  }

  clavier.addEventListener('click', e => {
    const touche = e.target.closest('.touche');
    if (!touche || !active) return;
    const champ = active.querySelector('input');
    if (touche.dataset.action === 'effacer') champ.value = champ.value.slice(0, -1);
    else if (touche.dataset.action === 'valider') valider();
    else if (champ.value.length < LONGUEUR_MAX) champ.value += touche.dataset.lettre;
  });

  // toucher une fiche (n'importe où, même celle déjà active) la rend active et fait
  // entendre son mot. Rien n'est dit tout seul : un seul son par geste de l'enfant.
  plateau.addEventListener('click', e => {
    const fiche = e.target.closest('.fiche');
    if (!fiche || fiche.classList.contains('trouve')) return;
    activer(fiche);
    partie.direMot(parId(fiche.dataset.id));
  });

  // clavier physique (ordinateur) : on écrit dans le champ, Entrée valide
  plateau.addEventListener('focusin', e => { if (e.target.matches('input')) activer(e.target.closest('.fiche')); });
  plateau.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); valider(); } });

  afficherSerie();
}
