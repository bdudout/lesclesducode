// Enregistre le service worker (hors-ligne) dans un navigateur, et garde l'invitation
// à installer l'appli que Chrome envoie sur Android (bouton dans l'espace adulte).
// Inutile dans l'appli Android/iPhone, où les fichiers sont déjà embarqués.

const natif = Boolean(window.Capacitor?.isNativePlatform?.());

if (!natif && 'serviceWorker' in navigator && location.protocol !== 'file:') {
  navigator.serviceWorker.register('sw.js').catch(() => { /* le jeu marche aussi sans */ });
}

// Chrome peut envoyer l'invitation très tôt, avant que le menu soit prêt : on la garde.
let invitation = null;
window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  invitation = e;
  window.dispatchEvent(new Event('installation-possible'));
});
window.addEventListener('appinstalled', () => {
  invitation = null;
  window.dispatchEvent(new Event('installation-possible'));
});

export const estAndroid = /Android/i.test(navigator.userAgent);
export const dejaInstallee = () => natif || window.matchMedia('(display-mode: standalone)').matches;
export const peutInviter = () => invitation !== null;

// Ouvre la fenêtre d'installation de Chrome ; renvoie true si la personne a accepté.
export async function installer() {
  if (!invitation) return false;
  const e = invitation;
  invitation = null;
  e.prompt();
  const { outcome } = await e.userChoice;
  window.dispatchEvent(new Event('installation-possible'));
  return outcome === 'accepted';
}
