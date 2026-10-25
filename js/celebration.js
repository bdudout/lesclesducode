// Célébrations, adaptées au nombre d'erreurs : toujours positives, mais plus
// éclatantes quand c'est parfait. Entre deux séries, l'enfant a le temps de savourer :
// le jeu continue quand il touche ▶ (ou tout seul après quelques secondes).

const NIVEAUX = {
  parfait: {
    etoiles: 3, confettis: 140,
    emojis: ['🏆', '👑', '🚀', '🦄'],
    serie: ['parfait-1', 'parfait-2', 'parfait-3'],
    fin: 'fin-parfait',
  },
  bravo: {
    etoiles: 2, confettis: 70,
    emojis: ['🌟', '🎉', '🥳', '🎈'],
    serie: ['bravo-1', 'bravo-2', 'bravo-3'],
    fin: 'fin-bravo',
  },
  courage: {
    etoiles: 1, confettis: 25,
    emojis: ['👍', '💪', '🌈', '🐢'],
    serie: ['courage-1', 'courage-2', 'courage-3'],
    fin: 'fin-courage',
  },
};

const DUREE_AVANT_BOUTON = 1200; // ms : on laisse la célébration se jouer
const DUREE_AUTO = 6000;         // ms : on enchaîne seul si personne ne touche ▶

const auHasard = liste => liste[Math.floor(Math.random() * liste.length)];

// 0 erreur : parfait ; jusqu'à un quart d'erreurs (2 au moins) : bravo ; au-delà : courage.
export function niveau(erreurs, total) {
  if (erreurs === 0) return 'parfait';
  if (erreurs <= Math.max(2, Math.round(total / 4))) return 'bravo';
  return 'courage';
}

function etoilesHtml(n) {
  return `<div class="etoiles" aria-label="${n} étoile${n > 1 ? 's' : ''} sur 3">${[1, 2, 3].map(i =>
    `<span class="${i <= n ? 'gagnee' : 'vide'}" style="animation-delay:${.25 + i * .25}s">⭐</span>`).join('')}</div>`;
}

export function lancerConfettis(conteneur, nombre) {
  const couleurs = ['#e76f51', '#2a9d8f', '#ffb703', '#8338ec', '#d62828', '#219ebc'];
  for (let i = 0; i < nombre; i++) {
    const c = document.createElement('span');
    c.className = 'confetti';
    c.style.left = `${Math.random() * 100}vw`;
    c.style.background = couleurs[i % couleurs.length];
    c.style.animationDuration = `${2.2 + Math.random() * 2.5}s`;
    c.style.animationDelay = `${Math.random() * 1.2}s`;
    conteneur.append(c);
    c.addEventListener('animationend', () => c.remove());
  }
}

// Entre deux séries. dire(cle) fait entendre une phrase enregistrée.
export function celebrerSerie({ erreurs, total, dire, ensuite }) {
  const n = niveau(erreurs, total);
  const config = NIVEAUX[n];
  const phrase = auHasard(config.serie);
  const calque = document.createElement('div');
  calque.className = `calque celebration ${n}`;
  calque.innerHTML = `
    <div class="contenu">
      <div class="grand-emoji">${auHasard(config.emojis)}</div>
      ${etoilesHtml(config.etoiles)}
      <p class="texte-celebration" data-phrase="${phrase}"></p>
      <button class="suivant" aria-label="Continuer" disabled>▶</button>
    </div>`;
  document.body.append(calque);
  calque.querySelector('.texte-celebration').textContent = dire(phrase);
  lancerConfettis(calque, config.confettis);

  let fini = false;
  const continuer = () => {
    if (fini) return;
    fini = true;
    calque.remove();
    ensuite();
  };
  const bouton = calque.querySelector('.suivant');
  setTimeout(() => { bouton.disabled = false; bouton.classList.add('pret'); }, DUREE_AVANT_BOUTON);
  bouton.addEventListener('click', continuer);
  setTimeout(continuer, DUREE_AUTO);
}

// Fin de partie : remplit l'écran #fin selon le résultat.
export function preparerFin({ erreurs, total, dire, ecran }) {
  const n = niveau(erreurs, total);
  const config = NIVEAUX[n];
  ecran.classList.remove('parfait', 'bravo', 'courage');
  ecran.classList.add(n);
  ecran.querySelector('.etoile-geante').textContent = auHasard(config.emojis);
  ecran.querySelector('.etoiles-fin').innerHTML = etoilesHtml(config.etoiles);
  ecran.querySelector('h2').textContent = dire(config.fin);
  lancerConfettis(ecran, config.confettis);
}
