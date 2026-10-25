// Copie les fichiers du jeu dans www/ : le dossier publié sur GitHub Pages et celui
// que Capacitor embarque dans les applis Android et iPhone (il ne peut pas pointer
// sur la racine du projet).

import { cpSync, rmSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';

const A_COPIER = [
  'index.html', 'jeu.html', 'referents.html', 'enseignants.html', 'manifest.webmanifest', 'sw.js',
  'css', 'js', 'data', 'img', 'son', 'fonts',
];

rmSync('www', { recursive: true, force: true });
mkdirSync('www');
for (const chemin of A_COPIER) cpSync(chemin, `www/${chemin}`, { recursive: true });

// Nouvelle version du cache hors-ligne à chaque publication : les tablettes
// récupèrent la mise à jour sans qu'on pense à changer VERSION à la main.
const version = `cdc-${(process.env.GITHUB_SHA || Date.now().toString(36)).slice(0, 10)}`;
const sw = readFileSync('www/sw.js', 'utf8').replace(/const VERSION = '[^']*';/, `const VERSION = '${version}';`);
writeFileSync('www/sw.js', sw);
writeFileSync('www/.nojekyll', ''); // GitHub Pages : servir les fichiers tels quels

console.log(`www/ prêt (${version}) :`, A_COPIER.join(', '));
