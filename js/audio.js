// Voix : joue son/<famille>/<id>.mp3 s'il est listé dans son/sons.json,
// sinon synthèse vocale française du navigateur.

let voix = null;
let lente = true;
let lecteur = null;

function choisirVoix() {
  if (!('speechSynthesis' in window)) return;
  const toutes = speechSynthesis.getVoices();
  voix = toutes.find(v => v.lang === 'fr-FR' && /Amélie|Audrey|Thomas|Google/.test(v.name))
    || toutes.find(v => v.lang && v.lang.startsWith('fr'))
    || null;
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
    voixNative.speak({ text: texte, lang: 'fr-FR', rate: lente ? 0.8 : 1 }).catch(() => {});
    return;
  }
  if (!('speechSynthesis' in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(texte);
  u.lang = 'fr-FR';
  if (voix) u.voice = voix;
  u.rate = lente ? 0.8 : 1;
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

// mode 1 : « ou de rouge » · mode 2 : le mot seul · mode 3 : muet
export function dire(famille, item, mode, sons) {
  if (mode === 3) return;
  taire();
  const fichier = `${famille}/${item.id}${mode === 2 ? '_mot' : ''}.mp3`;
  const texte = mode === 1 ? item.dit : (item.mot || item.dit);
  if (sons.has(fichier)) {
    lecteur = new Audio(`son/${fichier}`);
    lecteur.play().catch(() => parler(texte));
  } else {
    parler(texte);
  }
}
