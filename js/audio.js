// Voix : de préférence les enregistrements de son/ (voix neuronale naturelle, générée
// par outils/generer_voix.py et listée dans son/sons.json) ; à défaut, la meilleure
// voix française du système.

let voix = null;
let lente = true;
let lecteur = null;

// Les voix « naturelles » / « premium » des systèmes récents sont bien moins robotiques.
const VOIX_PREFEREES = [/natural|neural|naturel/i, /premium|enhanced|améliorée/i, /google/i, /amélie|audrey|denise|marie/i];

function choisirVoix() {
  if (!('speechSynthesis' in window)) return;
  const francaises = speechSynthesis.getVoices().filter(v => v.lang && v.lang.startsWith('fr'));
  const score = v => {
    const i = VOIX_PREFEREES.findIndex(re => re.test(v.name));
    return (i === -1 ? 0 : 10 - i) + (v.lang === 'fr-FR' ? 1 : 0);
  };
  voix = francaises.sort((a, b) => score(b) - score(a))[0] || null;
}

if ('speechSynthesis' in window) {
  choisirVoix();
  speechSynthesis.addEventListener('voiceschanged', choisirVoix);
}

export function reglerVitesse(estLente) { lente = estLente; }

// Dans l'appli Android/iPhone, on passe par la voix du système (la WebView Android
// ne fournit pas speechSynthesis).
const voixNative = window.Capacitor?.isNativePlatform?.() ? window.Capacitor.Plugins?.TextToSpeech : null;

export function parler(texte) {
  if (!texte) return;
  if (voixNative) {
    voixNative.stop().catch(() => {});
    voixNative.speak({ text: texte, lang: 'fr-FR', rate: lente ? 0.85 : 1 }).catch(() => {});
    return;
  }
  if (!('speechSynthesis' in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(texte);
  u.lang = 'fr-FR';
  if (voix) u.voice = voix;
  u.rate = lente ? 0.85 : 1;
  speechSynthesis.speak(u);
}

export function taire() {
  if (lecteur) lecteur.pause();
  if (voixNative) voixNative.stop().catch(() => {});
  else if ('speechSynthesis' in window) speechSynthesis.cancel();
}

// iOS n'autorise le son qu'après un geste : on « amorce » au premier toucher.
export function debloquer() {
  const amorcer = () => {
    if ('speechSynthesis' in window) speechSynthesis.speak(new SpeechSynthesisUtterance(''));
    window.removeEventListener('pointerdown', amorcer);
  };
  window.addEventListener('pointerdown', amorcer);
}

// Voix des enregistrements : 'femme', 'homme', ou 'alternee' (l'une puis l'autre,
// une voix par action : jamais deux sons pour un même geste).
let choixVoix = 'femme';
let derniere = 'homme';
export function reglerVoix(choix) { choixVoix = choix; }

function voixSuivante() {
  if (choixVoix !== 'alternee') return choixVoix;
  derniere = derniere === 'femme' ? 'homme' : 'femme';
  return derniere;
}

// Joue son/<voix>/<fichier> s'il existe (sinon l'autre voix), sinon lit le texte avec
// la voix du système. Chaque son coupe le précédent : un seul son à la fois.
function jouer(fichier, texte, sons) {
  taire();
  const voix = voixSuivante();
  const autre = voix === 'femme' ? 'homme' : 'femme';
  const chemin = [voix, autre].map(v => `${v}/${fichier}`).find(f => sons.has(f));
  if (chemin) {
    // lu tel quel : changer la vitesse de lecture déforme la voix (effet robot)
    lecteur = new Audio(`son/${chemin}`);
    lecteur.play().catch(() => parler(texte));
  } else {
    parler(texte);
  }
}

// Lance action quand le son en cours est fini (+ un petit temps de respiration) :
// les félicitations ne recouvrent jamais le son du dernier référent.
export function apresSon(suite, pause = 350) {
  let fait = false;
  const action = () => { if (!fait) { fait = true; suite(); } };
  setTimeout(action, 8000); // sécurité : si la fin du son n'est jamais signalée
  const enCours = lecteur && !lecteur.paused && !lecteur.ended;
  const parle = !voixNative && 'speechSynthesis' in window && speechSynthesis.speaking;
  if (enCours) {
    lecteur.addEventListener('ended', () => setTimeout(action, pause), { once: true });
  } else if (parle) {
    const attendre = () => (speechSynthesis.speaking ? setTimeout(attendre, 100) : setTimeout(action, pause));
    attendre();
  } else {
    setTimeout(action, pause);
  }
}

// mode 1 : « ou de rouge » · mode 2 : le mot seul · mode 3 : muet
// item.voix : la même phrase en texte, pour la voix de secours du navigateur
export function dire(famille, item, mode, sons) {
  if (mode === 3) return;
  if (mode === 1) jouer(`${famille}/${item.id}.mp3`, item.voix || item.dit, sons);
  else direMot(famille, item, sons);
}

export function direMot(famille, item, sons) {
  jouer(`${famille}/${item.id}_mot.mp3`, item.mot || item.voix || item.dit, sons);
}

// Phrases fixes (consignes, encouragements) : data/phrases.json, son/<voix>/phrases/<cle>.mp3
export function direPhrase(cle, texte, sons) {
  jouer(`phrases/${cle}.mp3`, texte, sons);
}
