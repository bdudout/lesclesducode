// Découpage d'une partie en séries courtes (8 paires au plus), commun aux jeux
// « lire » et « écrire » : séances plus courtes, cases plus grandes.

import { melanger } from './data.js';

export const PAR_SERIE = 8;

// Les rangées du référentiel pour les jeux « par rangée », sinon des paquets
// équilibrés de `taille` au plus (26 lettres → 7, 7, 6, 6 plutôt que 8, 8, 8, 2).
export function decouper(items, melange, taille = PAR_SERIE) {
  if (items.length <= taille) return [items];
  if (melange.endsWith('par-rangee') && items[0].rangee) {
    const rangees = [...new Set(items.map(i => i.rangee))];
    return rangees.map(r => items.filter(i => i.rangee === r));
  }
  // graphèmes fixes (ex. alphabet de A à Z) : les séries suivent l'ordre (A-G, H-N…)
  const base = melange === 'tout' ? melanger(items) : items;
  const nb = Math.ceil(base.length / taille);
  const series = Array.from({ length: nb }, () => []);
  base.forEach((it, i) => series[Math.floor(i * nb / base.length)].push(it));
  return series;
}

// Petits points de progression : ● faite, ◉ en cours, ○ à venir.
export function pointsSeries(series, numero) {
  if (series.length < 2) return '';
  return `<div class="series" aria-label="Série ${numero + 1} sur ${series.length}">${series.map((_, i) =>
    `<span class="${i < numero ? 'faite' : i === numero ? 'en-cours' : ''}"></span>`).join('')}</div>`;
}
