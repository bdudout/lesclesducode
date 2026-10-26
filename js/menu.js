import './pwa.js';
import {
  charger, echapper, lireReglages, ecrireReglages, lireHistorique, effacerHistorique, itemsDuJeu,
  AVATARS, lireProfils, ecrireProfils, joueurCourant, joueurAChoisi, choisirJoueur,
} from './data.js';
import { appuiLong } from './appui-long.js';
import { direPhrase, reglerVoix } from './audio.js';
import { estNatif, surRetour, quitterAppli, pleinEcran, voixFrancaiseDisponible } from './natif.js';

const { jeux, familles, sons, phrases } = await charger();
// phrase enregistrée (data/phrases.json), sauf si l'adulte a coupé le son
const phrase = cle => {
  const r = lireReglages();
  reglerVoix(r.voix);
  if (r.son !== 3) direPhrase(cle, phrases[cle], sons);
};
const $ = id => document.getElementById(id);

// Ordre de la méthode : on avance de l'alphabet vers les graphèmes plus rares.
const ORDRE = ['alphabet', 'complexes', 'doubles', 'autres'];
const TITRES_FAMILLES = { alphabet: 'Alphabet', complexes: 'Graphèmes complexes', doubles: 'Consonnes doubles', autres: 'Autres graphèmes' };

// ---------- Menu : un chemin de 4 étapes, lisible sans savoir lire ----------
function afficherMenu() {
  const reglages = lireReglages();
  const joueur = joueurCourant();
  const reussis = new Set(lireHistorique()
    .filter(p => !joueur || p.joueur === joueur.id)
    .map(p => p.jeu));
  document.body.classList.toggle('avec-titres', reglages.titres);

  $('parcours').innerHTML = ORDRE.map((f, etape) => `
    <section class="etape famille-${f}" aria-label="${TITRES_FAMILLES[f]}">
      <div class="numero-etape" aria-hidden="true">${etape + 1}</div>
      <div class="jeux-etape">
        ${jeux.filter(j => j.famille === f).map(j => {
          const total = familles[f].length;
          const retenus = itemsDuJeu(familles[f], f, reglages).length;
          const ecrire = j.moteur === 'ecriture';
          return `
          <a class="vignette ecriture-${j.ecriture}" href="jeu.html?id=${j.id}" aria-label="${j.titre}">
            <span class="numero">${j.numero}</span>
            ${reussis.has(j.id) ? '<span class="etoile" aria-label="déjà réussi">⭐</span>' : ''}
            <span class="visuel"><span class="grapheme">${j.vignette[0]}</span><img src="img/referents/${f}/${j.vignette[1]}.svg" alt="" draggable="false"></span>
            <span class="mode ${ecrire ? 'ecrire' : 'lire'}" aria-hidden="true">${ecrire ? '✏️' : '👀'}</span>
            <span class="titre">${j.titre}</span>
            ${retenus < total ? `<span class="filtre">${retenus}/${total}</span>` : ''}
          </a>`;
        }).join('')}
      </div>
    </section>`).join('');

  $('b-joueur').hidden = !joueur && lireProfils().length === 0;
  $('b-joueur').textContent = joueur ? joueur.avatar : '👤';
}

// ---------- « Qui joue ? » : chaque enfant touche son animal ----------
function afficherQuiJoue() {
  const profils = lireProfils();
  $('grille-joueurs').innerHTML = profils.map(p => `
    <button class="carte-joueur" data-id="${p.id}"><span class="avatar">${p.avatar}</span><span class="prenom">${echapper(p.prenom)}</span></button>`).join('')
    + '<button class="carte-joueur invite" data-id="invite"><span class="avatar">👤</span><span class="prenom">Sans nom</span></button>';
  $('qui-joue').hidden = false;
}

$('grille-joueurs').addEventListener('click', e => {
  const carte = e.target.closest('.carte-joueur');
  if (!carte) return;
  choisirJoueur(carte.dataset.id);
  $('qui-joue').hidden = true;
  const joueur = joueurCourant();
  if (joueur) phrase('bonjour');
  afficherMenu();
});
$('b-qui').addEventListener('click', () => phrase('qui-joue'));
$('b-joueur').addEventListener('click', afficherQuiJoue);

afficherMenu();
if (lireProfils().length > 0 && !joueurAChoisi()) afficherQuiJoue();

// Appli : barre d'état visible au menu ; « retour » au menu ferme l'appli
// (sinon Android reviendrait dans le jeu précédent).
pleinEcran(false);
surRetour(quitterAppli);

// ---------- Espace adulte (appui long d'une seconde) ----------
const dialogue = $('reglages');
appuiLong($('adulte'), ouvrir);

const cases = {
  chrono: 'r-chrono', erreurs: 'r-erreurs', vibrations: 'r-vibrations',
  seriesCourtes: 'r-series', titres: 'r-titres', classe: 'r-classe',
};
$('ligne-vibrations').hidden = !estNatif;

function modifier(changement) {
  ecrireReglages({ ...lireReglages(), ...changement });
  afficherMenu();
}

// ---------- Élèves ----------
let avatarChoisi = null;

function afficherEleves() {
  const profils = lireProfils();
  $('liste-eleves').innerHTML = profils.length === 0
    ? '<li class="note">Aucun élève : tout le monde joue « sans nom ».</li>'
    : profils.map(p => `<li><span class="avatar">${p.avatar}</span> ${echapper(p.prenom)}
        <button type="button" class="retirer" data-id="${p.id}" aria-label="Retirer ${echapper(p.prenom)}">✖</button></li>`).join('');
  const pris = new Set(profils.map(p => p.avatar));
  const libres = AVATARS.filter(a => !pris.has(a));
  if (!libres.includes(avatarChoisi)) avatarChoisi = libres[0] || AVATARS[0];
  $('choix-avatar').innerHTML = (libres.length ? libres : AVATARS).map(a =>
    `<button type="button" role="radio" aria-checked="${a === avatarChoisi}" class="${a === avatarChoisi ? 'choisi' : ''}" data-avatar="${a}">${a}</button>`).join('');
  remplirFiltreEleves();
}

$('choix-avatar').addEventListener('click', e => {
  const b = e.target.closest('[data-avatar]');
  if (!b) return;
  avatarChoisi = b.dataset.avatar;
  afficherEleves();
});

$('ajouter-eleve').addEventListener('click', () => {
  const prenom = $('prenom').value.trim();
  if (!prenom) { $('prenom').focus(); return; }
  ecrireProfils([...lireProfils(), { id: `e${Date.now().toString(36)}`, prenom, avatar: avatarChoisi }]);
  $('prenom').value = '';
  afficherEleves();
  afficherMenu();
});
$('prenom').addEventListener('keydown', e => { if (e.key === 'Enter') $('ajouter-eleve').click(); });

$('liste-eleves').addEventListener('click', e => {
  const b = e.target.closest('.retirer');
  if (!b) return;
  const p = lireProfils().find(x => x.id === b.dataset.id);
  if (!confirm(`Retirer ${p.prenom} ? Ses scores restent dans la fiche.`)) return;
  ecrireProfils(lireProfils().filter(x => x.id !== b.dataset.id));
  if (joueurCourant()?.id === b.dataset.id) choisirJoueur(null);
  afficherEleves();
  afficherMenu();
});

// ---------- Graphèmes travaillés ----------
// Cases à cocher par famille ; les graphèmes complexes sont groupés par rangée,
// dans l'ordre de la méthode, pour cocher une rangée d'un coup.
function afficherChoixGraphemes() {
  const choisis = lireReglages().graphemes;
  $('choix-graphemes').innerHTML = Object.entries(familles).map(([f, items]) => {
    const liste = choisis[f] || items.map(i => i.id);
    const groupes = items[0].rangee
      ? [...new Set(items.map(i => i.rangee))].map(r => ({ titre: `Rangée ${r}`, items: items.filter(i => i.rangee === r) }))
      : [{ titre: '', items }];
    return `
      <details class="famille-choix" data-famille="${f}">
        <summary>${TITRES_FAMILLES[f]} <b>${liste.length}/${items.length}</b></summary>
        <div class="actions-choix">
          <button type="button" data-tout="1">Tout cocher</button>
          <button type="button" data-tout="0">Tout décocher</button>
        </div>
        ${groupes.map(g => `
          <div class="groupe-choix">
            ${g.titre ? `<button type="button" class="titre-rangee" data-rangee="${g.items[0].rangee}">${g.titre}</button>` : ''}
            ${g.items.map(i => `<label class="puce"><input type="checkbox" value="${i.id}" ${liste.includes(i.id) ? 'checked' : ''}>${i.graphie}</label>`).join('')}
          </div>`).join('')}
      </details>`;
  }).join('');
}

function enregistrerFamille(bloc) {
  const f = bloc.dataset.famille;
  const coches = [...bloc.querySelectorAll('input:checked')].map(i => i.value);
  const graphemes = { ...lireReglages().graphemes };
  if (coches.length === familles[f].length) delete graphemes[f];
  else graphemes[f] = coches;
  modifier({ graphemes });
  bloc.querySelector('summary b').textContent = `${coches.length}/${familles[f].length}`;
  bloc.querySelector('summary b').classList.toggle('alerte', coches.length < 2);
}

$('choix-graphemes').addEventListener('change', e => enregistrerFamille(e.target.closest('details')));
$('choix-graphemes').addEventListener('click', e => {
  const bouton = e.target.closest('button');
  if (!bouton) return;
  const bloc = bouton.closest('details');
  const cibles = bouton.dataset.rangee
    ? [...bouton.parentElement.querySelectorAll('input')]
    : [...bloc.querySelectorAll('input')];
  const valeur = bouton.dataset.rangee ? !cibles.every(c => c.checked) : bouton.dataset.tout === '1';
  cibles.forEach(c => { c.checked = valeur; });
  enregistrerFamille(bloc);
});

// ---------- Fiche de scores, par élève, avec les confusions fréquentes ----------
const familleDuJeu = Object.fromEntries(jeux.map(j => [j.id, j.famille]));

function graphie(famille, id) {
  return familles[famille]?.find(i => i.id === id)?.graphie ?? id;
}

function remplirFiltreEleves() {
  const valeur = $('filtre-eleve').value || 'tous';
  $('filtre-eleve').innerHTML = '<option value="tous">Tous</option>'
    + lireProfils().map(p => `<option value="${p.id}">${p.avatar} ${echapper(p.prenom)}</option>`).join('')
    + '<option value="sans">👤 Sans nom</option>';
  $('filtre-eleve').value = [...$('filtre-eleve').options].some(o => o.value === valeur) ? valeur : 'tous';
}

function partiesFiltrees() {
  const filtre = $('filtre-eleve').value || 'tous';
  return lireHistorique().filter(p =>
    filtre === 'tous' || (filtre === 'sans' ? !p.joueur || p.joueur === 'invite' : p.joueur === filtre));
}

function afficherScores() {
  const parties = partiesFiltrees();
  const profils = Object.fromEntries(lireProfils().map(p => [p.id, p]));
  const titres = Object.fromEntries(jeux.map(j => [j.id, `${j.numero}. ${j.titre}`]));

  // « cherchait ou, a choisi on » × n, toutes parties confondues
  const comptes = new Map();
  for (const p of parties) {
    for (const [cherche, donne] of p.confusions || []) {
      const f = familleDuJeu[p.jeu];
      const cle = `${graphie(f, cherche)} → ${graphie(f, donne)}`;
      comptes.set(cle, (comptes.get(cle) || 0) + 1);
    }
  }
  const top = [...comptes].sort((a, b) => b[1] - a[1]).slice(0, 10);
  $('confusions').innerHTML = top.length === 0 ? '' : `
    <p><b>Confusions fréquentes</b> <span class="note">(son cherché → réponse donnée)</span></p>
    <div class="liste-confusions">${top.map(([c, n]) => `<span class="puce-confusion">${echapper(c)} <b>×${n}</b></span>`).join('')}</div>`;

  const recentes = parties.slice(-30).reverse();
  $('scores').innerHTML = recentes.length === 0
    ? '<p class="note">Aucune partie terminée pour l\'instant.</p>'
    : `<table><thead><tr><th>Date</th><th>Élève</th><th>Jeu</th><th>Erreurs</th><th>Aides</th><th>Temps</th></tr></thead><tbody>
        ${recentes.map(p => `<tr>
          <td>${new Date(p.date).toLocaleDateString('fr-FR')}</td>
          <td>${profils[p.joueur] ? `${profils[p.joueur].avatar} ${echapper(profils[p.joueur].prenom)}` : '—'}</td>
          <td>${titres[p.jeu] || p.jeu}</td><td>${p.erreurs}</td><td>${p.aides ?? 0}</td>
          <td>${Math.floor(p.secondes / 60)}:${String(p.secondes % 60).padStart(2, '0')}</td></tr>`).join('')}
      </tbody></table>`;
}
$('filtre-eleve').addEventListener('change', afficherScores);

function ouvrir() {
  const r = lireReglages();
  for (const [cle, id] of Object.entries(cases)) $(id).checked = r[cle];
  document.querySelector(`input[name=son][value="${r.son}"]`).checked = true;
  document.querySelector(`input[name=voix][value="${r.voix}"]`).checked = true;
  afficherEleves();
  afficherChoixGraphemes();
  afficherScores();
  dialogue.showModal();
  voixFrancaiseDisponible().then(ok => { $('alerte-voix').hidden = ok !== false; });
}

for (const [cle, id] of Object.entries(cases)) {
  $(id).addEventListener('change', e => modifier({ [cle]: e.target.checked }));
}
document.querySelectorAll('input[name=son]').forEach(r =>
  r.addEventListener('change', () => modifier({ son: Number(r.value) })));
// choisir une voix la fait entendre aussitôt
document.querySelectorAll('input[name=voix]').forEach(r =>
  r.addEventListener('change', () => { modifier({ voix: r.value }); phrase('bonjour'); }));

$('fermer').addEventListener('click', () => dialogue.close());
$('imprimer').addEventListener('click', () => window.print());
$('effacer').addEventListener('click', () => {
  if (!confirm('Effacer tous les scores enregistrés sur cet appareil ?')) return;
  effacerHistorique();
  afficherScores();
  afficherMenu();
});
