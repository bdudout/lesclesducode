// Accès au téléphone dans l'appli Android/iPhone (Capacitor).
// Dans un navigateur, toutes ces fonctions ne font rien : le site marche tel quel.
// Seul fichier qui parle aux modules natifs (voir SPEC_MOBILE.md).

const C = window.Capacitor;
export const estNatif = Boolean(C?.isNativePlatform?.());
const P = estNatif ? C.Plugins : {};

const sansErreur = promesse => promesse?.catch?.(() => {});

// ---------- N2 : stockage durable ----------
// iOS peut vider le localStorage d'une WebView ; on garde une copie dans les
// préférences natives et on la recopie au démarrage si besoin.
const CLES = ['cdc-reglages', 'cdc-historique', 'cdc-profils'];

export async function restaurerStockage() {
  if (!P.Preferences) return;
  for (const cle of CLES) {
    try {
      const { value } = await P.Preferences.get({ key: cle });
      const local = localStorage.getItem(cle);
      if (value !== null && local === null) localStorage.setItem(cle, value);
      else if (value === null && local !== null) await P.Preferences.set({ key: cle, value: local });
    } catch { /* on continue avec le localStorage seul */ }
  }
}

export function sauverNatif(cle, valeur) {
  sansErreur(P.Preferences?.set({ key: cle, value: valeur }));
}

export function effacerNatif(cle) {
  sansErreur(P.Preferences?.remove({ key: cle }));
}

// ---------- N3 : bouton retour Android ----------
export function surRetour(action) {
  sansErreur(P.App?.addListener('backButton', action));
}

export function quitterAppli() {
  sansErreur(P.App?.exitApp());
}

// ---------- N4 : mise en arrière-plan ----------
export function surPause(action) { sansErreur(P.App?.addListener('pause', action)); }
export function surReprise(action) { sansErreur(P.App?.addListener('resume', action)); }

// ---------- N5 : plein écran pendant le jeu ----------
export function pleinEcran(actif) {
  sansErreur(actif ? P.StatusBar?.hide() : P.StatusBar?.show());
}

// ---------- N6 : retour tactile ----------
export function vibrer() {
  sansErreur(P.Haptics?.impact({ style: 'LIGHT' }));
}

// ---------- N1 : une voix française est-elle installée ? ----------
// true / false dans l'appli, null dans un navigateur (non vérifiable).
export async function voixFrancaiseDisponible() {
  if (!P.TextToSpeech) return null;
  try {
    const { languages } = await P.TextToSpeech.getSupportedLanguages();
    return languages.some(l => l.toLowerCase().startsWith('fr'));
  } catch {
    return null;
  }
}
