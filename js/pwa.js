// Enregistre le service worker (hors-ligne) dans un navigateur.
// Inutile dans l'appli Android/iPhone, où les fichiers sont déjà embarqués.

const natif = Boolean(window.Capacitor?.isNativePlatform?.());

if (!natif && 'serviceWorker' in navigator && location.protocol !== 'file:') {
  navigator.serviceWorker.register('sw.js').catch(() => { /* le jeu marche aussi sans */ });
}
