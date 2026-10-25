// Appui long : l'action ne se déclenche qu'après un maintien (anneau de progression),
// pour qu'un enfant ne quitte pas la partie ou n'ouvre pas les réglages par hasard.

export function appuiLong(bouton, action, duree = 1000) {
  let declencheur = null; // minuteur qui lance l'action
  let anneau = null;      // animation de l'anneau (affichage seulement)
  let debut = 0;

  function dessiner() {
    const p = Math.min(1, (performance.now() - debut) / duree);
    bouton.style.setProperty('--p', `${p * 100}%`);
    if (p < 1) anneau = requestAnimationFrame(dessiner);
  }

  function annuler() {
    clearTimeout(declencheur);
    cancelAnimationFrame(anneau);
    bouton.classList.remove('charge');
    bouton.style.removeProperty('--p');
  }

  bouton.classList.add('appui-long');
  bouton.addEventListener('pointerdown', e => {
    e.preventDefault();
    debut = performance.now();
    bouton.classList.add('charge');
    anneau = requestAnimationFrame(dessiner);
    declencheur = setTimeout(() => { annuler(); action(); }, duree);
  });
  ['pointerup', 'pointerleave', 'pointercancel'].forEach(e => bouton.addEventListener(e, annuler));
  bouton.addEventListener('contextmenu', e => e.preventDefault());
  // un simple clic (souris, clavier) ne fait rien : seul le maintien compte
  bouton.addEventListener('click', e => e.preventDefault());
}
