"""Enregistre toutes les voix du jeu avec Piper (synthèse neuronale libre, hors-ligne).

Produit, dans son/<dossier>/ (une voix par dossier : femme, homme) :
  <famille>/<id>.mp3      le référent complet  (« ou, de rouge »)
  <famille>/<id>_mot.mp3  le mot seul          (« rouge »)
  phrases/<clé>.mp3       consignes et encouragements (data/phrases.json)
et met à jour son/sons.json, la liste que lit le jeu.

Le son du graphème (ou le nom de la lettre) est donné en phonétique exacte (champ
`api` du référentiel) : laissée à elle-même, la synthèse lit « é » « e accent aigu »
ou « y, » comme le pronom « i ». La fin de phrase (champ `suite`) est lue normalement,
sauf les mots mal lus par la synthèse, dont la phonétique est imposée (champ `api_mot` :
« ananas » avec son s, le [ɥ] de « huit »…).

Prérequis (une fois) :
  python3 -m venv piper-env && piper-env/bin/pip install piper-tts
  une voix (.onnx + .onnx.json) depuis huggingface.co/rhasspy/piper-voices
  ffmpeg (brew install ffmpeg)

Usage :
  piper-env/bin/python -I outils/generer_voix.py <modèle.onnx> --dossier femme [--locuteur N] [--tout]
  piper-env/bin/python -I outils/generer_voix.py <modèle.onnx> [--locuteur N] --essai <fichier.mp3>
Sans --tout, seuls les fichiers absents sont créés (pratique après un ajout).
--essai enregistre seulement quelques phrases témoins, pour comparer des voix.

Crédits des voix : voir enseignants.html.
"""
import argparse
import json
import os
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np
import piper
from piper import PiperVoice, SynthesisConfig

RACINE = Path(__file__).resolve().parent.parent
SON = RACINE / 'son'
TAUX = 22050

# Les témoins pour comparer des voix : un son, un mot difficile, une consigne, un bravo.
ESSAI = [('wa', 'de oiseau'), ('iɡʁɛk', 'de pyjama'), (None, "Touche un son, puis l'image qui va avec."),
         (None, 'Bravo, tu as tout trouvé !')]


def charger_voix(modele):
    # espeak-ng tronque les chemins longs : on lui donne un chemin relatif court.
    os.chdir(Path(piper.__file__).parent)
    return PiperVoice.load(modele, espeak_data_dir='espeak-ng-data')


def phonemes(voix, api, texte, api_mot=None):
    """Le son en phonétique exacte (s'il y en a un), une courte pause, puis le texte.
    Avec api_mot, le dernier mot du texte est remplacé par sa phonétique imposée."""
    if api_mot:
        debut = texte.rsplit(' ', 1)[0] if ' ' in texte else ''
        suite = [p for phrase in voix.phonemize(debut) for p in phrase] + [' '] * bool(debut) + list(api_mot)
    else:
        suite = [p for phrase in voix.phonemize(texte) for p in phrase]
    if api is None:
        return suite
    return ['ˈ', *api, ',', ' ', *suite]


def audio(voix, api, texte, reglage, api_mot=None):
    ids = voix.phonemes_to_ids(phonemes(voix, api, texte, api_mot))
    brut = voix.phoneme_ids_to_audio(ids, reglage)
    brut = brut / max(1e-6, float(np.abs(brut).max())) * 0.9
    return (brut * 32767).astype(np.int16)


def ecrire_mp3(echantillons, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as dossier:
        wav = Path(dossier) / 'brut.wav'
        with wave.open(str(wav), 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(TAUX)
            w.writeframes(echantillons.tobytes())
        # silences de début et de fin raccourcis sans toucher aux sons (on garde 0,1 s),
        # puis un fondu très court pour ne pas finir sur un clic
        filtre = ('silenceremove=start_periods=1:start_threshold=-60dB:start_silence=0.05,'
                  'areverse,silenceremove=start_periods=1:start_threshold=-60dB:start_silence=0.1,areverse,'
                  'afade=t=out:st=0:d=0.01:curve=tri,apad=pad_dur=0.05')
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(wav), '-af', filtre,
                        '-ac', '1', '-ar', str(TAUX), '-b:a', '64k', str(destination)], check=True)


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument('modele')
    arguments.add_argument('--dossier', default='femme')
    arguments.add_argument('--locuteur', type=int, default=None)
    arguments.add_argument('--tout', action='store_true')
    arguments.add_argument('--essai')
    a = arguments.parse_args()
    modele = Path(a.modele).resolve()
    essai = Path(a.essai).resolve() if a.essai else None

    # débit naturel, intonation un peu vivante (valeurs par défaut de Piper : 1 / 0.667 / 0.8)
    reglage = SynthesisConfig(speaker_id=a.locuteur, length_scale=1.05, noise_scale=0.667, noise_w_scale=0.8)
    voix = charger_voix(modele)

    if essai:
        silence = np.zeros(int(TAUX * 0.6), dtype=np.int16)
        morceaux = [x for api, texte in ESSAI for x in (audio(voix, api, texte, reglage), silence)]
        ecrire_mp3(np.concatenate(morceaux), essai)
        print('essai :', essai)
        return

    referentiel = json.loads((RACINE / 'data/referentiel.json').read_text())['familles']
    phrases = json.loads((RACINE / 'data/phrases.json').read_text())
    a_faire = []
    for famille, items in referentiel.items():
        for it in items:
            a_faire.append((f'{famille}/{it["id"]}.mp3', it['api'], it['suite'], it.get('api_mot')))
            if it.get('mot'):
                a_faire.append((f'{famille}/{it["id"]}_mot.mp3', None, it['mot'], it.get('api_mot')))
    for cle, texte in phrases.items():
        a_faire.append((f'phrases/{cle}.mp3', None, texte, None))

    crees = 0
    for fichier, api, texte, api_mot in a_faire:
        destination = SON / a.dossier / fichier
        if a.tout or not destination.exists():
            ecrire_mp3(audio(voix, api, texte, reglage, api_mot), destination)
            crees += 1
    liste = sorted(str(p.relative_to(SON)) for p in SON.rglob('*.mp3'))
    (SON / 'sons.json').write_text(json.dumps(liste, ensure_ascii=False, indent=0) + '\n')
    print(f'{crees} enregistrements créés, {len(liste)} au total')


if __name__ == '__main__':
    main()
