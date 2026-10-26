// Chargement des données : référentiel des graphèmes, liste des jeux,
// et listes des fichiers image/son déposés (pour éviter des requêtes 404).

import { restaurerStockage, sauverNatif, effacerNatif } from './natif.js';

async function lireJson(url, parDefaut) {
  try {
    // revalidé à chaque fois (réponse « inchangé » très rapide) : jamais d'ancienne liste
    const r = await fetch(url, { cache: 'no-cache' });
    if (!r.ok) return parDefaut;
    return await r.json();
  } catch {
    return parDefaut;
  }
}

export async function charger() {
  await restaurerStockage();
  const [referentiel, jeux, images, sons, phrases] = await Promise.all([
    lireJson('data/referentiel.json', null),
    lireJson('data/jeux.json', []),
    lireJson('img/images.json', []),
    lireJson('son/sons.json', []),
    lireJson('data/phrases.json', {}),
  ]);
  return { familles: referentiel.familles, jeux, images: new Set(images), sons: new Set(sons), phrases };
}

// Pour insérer un texte saisi (prénom, réponse tapée) dans du HTML sans risque.
export function echapper(texte) {
  return String(texte).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
}

// Fisher-Yates : mélange uniforme (celui de l'original ne l'était pas).
export function melanger(tableau) {
  const t = [...tableau];
  for (let i = t.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [t[i], t[j]] = [t[j], t[i]];
  }
  return t;
}

// Réglages adultes, profils et historique, conservés sur l'appareil uniquement.
const CLE_REGLAGES = 'cdc-reglages';
const CLE_HISTO = 'cdc-historique';
const CLE_PROFILS = 'cdc-profils';
const CLE_JOUEUR = 'cdc-joueur'; // dans sessionStorage : chaque enfant se choisit en arrivant

function lireLocal(cle, parDefaut) {
  try { return JSON.parse(localStorage.getItem(cle)) ?? parDefaut; } catch { return parDefaut; }
}

function ecrireLocal(cle, valeur) {
  const texte = JSON.stringify(valeur);
  try { localStorage.setItem(cle, texte); } catch { /* navigation privée */ }
  sauverNatif(cle, texte);
}
// son : 1 « ou de rouge », 2 le mot seul, 3 muet ; voix : femme, homme ou alternee
// graphemes : { famille: [ids] } choisis par l'enseignant ; absent = toute la famille
// seriesCourtes : toujours jouer par séries de 8 (sinon seulement si l'écran est trop petit)
// titres : afficher les titres des jeux au menu
// chrono et erreurs masqués par défaut : pas de pression inutile à 5 ans (fiche adulte)
// classe : mode TBI (tout en plus grand, sans chrono ni erreurs)
const REGLAGES_DEFAUT = {
  chrono: false, erreurs: false, voixLente: true, vibrations: true, son: 1, voix: 'femme', graphemes: {},
  seriesCourtes: false, titres: false, classe: false,
};

// Graphèmes du jeu : ceux du lien de séance (?g=ou,on), sinon ceux cochés par
// l'enseignant, sinon toute la famille. Il en faut au moins 2 pour jouer.
export function itemsDuJeu(tous, famille, reglages, parametreG) {
  const choix = parametreG ? parametreG.split(',') : reglages.graphemes?.[famille];
  if (!choix) return tous;
  const retenus = tous.filter(i => choix.includes(i.id));
  return retenus.length >= 2 ? retenus : tous;
}

export function lireReglages() {
  return { ...REGLAGES_DEFAUT, ...lireLocal(CLE_REGLAGES, {}) };
}

export function ecrireReglages(r) {
  ecrireLocal(CLE_REGLAGES, r);
}

// Profils élèves : { id, prenom, avatar }. Aucun compte, rien ne quitte l'appareil.
export const AVATARS = ['🦊', '🐼', '🐸', '🦁', '🐯', '🐨', '🐰', '🐻', '🐵', '🦄', '🐙', '🐢',
  '🐱', '🐶', '🦉', '🐞', '🐝', '🐳', '🦋', '🐧', '🦖', '🐲', '🦔', '🐮'];

export function lireProfils() { return lireLocal(CLE_PROFILS, []); }
export function ecrireProfils(p) { ecrireLocal(CLE_PROFILS, p); }

export function joueurCourant() {
  try {
    const id = sessionStorage.getItem(CLE_JOUEUR);
    return lireProfils().find(p => p.id === id) || null;
  } catch { return null; }
}

// Vrai dès qu'un enfant s'est choisi (ou a choisi « sans nom ») pendant cette session.
export function joueurAChoisi() {
  try { return sessionStorage.getItem(CLE_JOUEUR) !== null; } catch { return true; }
}

export function choisirJoueur(id) {
  try {
    if (id) sessionStorage.setItem(CLE_JOUEUR, id);
    else sessionStorage.removeItem(CLE_JOUEUR);
  } catch { /* navigation privée */ }
}

export function effacerHistorique() {
  try { localStorage.removeItem(CLE_HISTO); } catch { /* navigation privée */ }
  effacerNatif(CLE_HISTO);
}

export function lireHistorique() {
  return lireLocal(CLE_HISTO, []);
}

// partie : { jeu, date, erreurs, secondes, joueur, aides, confusions: [[cherché, choisi], …] }
export function ajouterHistorique(partie) {
  ecrireLocal(CLE_HISTO, [...lireHistorique(), partie].slice(-1000));
}
