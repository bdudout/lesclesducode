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

// Joue son/<fichier> s'il existe, sinon lit le texte avec la voix du système.
function jouer(fichier, texte, sons) {
  taire();
  if (sons.has(fichier)) {
    lecteur = new Audio(`son/${fichier}`);
    lecteur.playbackRate = lente ? 0.95 : 1.05;
    lecteur.play().catch(() => parler(texte));
  } else {
    parler(texte);
  }
}

// mode 1 : « ou de rouge » · mode 2 : le mot seul · mode 3 : muet
// item.voix : le même texte écrit pour être bien prononcé (« gne, de peigne »)
export function dire(famille, item, mode, sons) {
  if (mode === 3) return;
  if (mode === 1) jouer(`${famille}/${item.id}.mp3`, item.voix || item.dit, sons);
  else direMot(famille, item, sons);
}

export function direMot(famille, item, sons) {
  jouer(`${famille}/${item.id}_mot.mp3`, item.mot || item.voix || item.dit, sons);
}

// Phrases fixes (consignes, encouragements) : data/phrases.json, son/phrases/<cle>.mp3
export function direPhrase(cle, texte, sons) {
  jouer(`phrases/${cle}.mp3`, texte, sons);
}
