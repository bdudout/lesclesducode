"""Enregistre toutes les voix du jeu avec Piper (synthèse neuronale libre, hors-ligne).

Produit, dans son/ :
  <famille>/<id>.mp3      le référent complet  (« ou, de rouge »)  — champ `voix`
  <famille>/<id>_mot.mp3  le mot seul          (« rouge »)
  phrases/<clé>.mp3       consignes et encouragements (data/phrases.json)
et met à jour son/sons.json, la liste que lit le jeu.

Prérequis (une fois) :
  python3 -m venv piper-env && piper-env/bin/pip install piper-tts
  voix fr_FR-siwis-medium (.onnx + .onnx.json) depuis huggingface.co/rhasspy/piper-voices
  ffmpeg (brew install ffmpeg)

Usage :
  piper-env/bin/python outils/generer_voix.py <modèle.onnx> [--tout]
Sans --tout, seuls les fichiers absents sont créés (pratique après un ajout).

Voix SIWIS : base de données de l'université d'Édimbourg, licence CC BY 4.0
(crédit dans enseignants.html).
"""
import json
import os
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import piper
from piper import PiperVoice, SynthesisConfig

RACINE = Path(__file__).resolve().parent.parent
SON = RACINE / 'son'

# Débit un peu posé pour des enfants de 5-7 ans, et intonation pas trop monotone.
REGLAGE = SynthesisConfig(length_scale=1.12, noise_scale=0.6, noise_w_scale=0.8)


def charger_voix(modele):
    # espeak-ng tronque les chemins longs : on lui donne un chemin relatif court.
    os.chdir(Path(piper.__file__).parent)
    return PiperVoice.load(modele, espeak_data_dir='espeak-ng-data')


def enregistrer(voix, texte, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as dossier:
        brut = Path(dossier) / 'brut.wav'
        with wave.open(str(brut), 'wb') as w:
            voix.synthesize_wav(texte, w, syn_config=REGLAGE)
        # mp3 mono léger, avec le silence de fin retiré pour enchaîner sans attendre
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(brut),
                        '-af', 'areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse',
                        '-ac', '1', '-ar', '22050', '-b:a', '48k', str(destination)], check=True)


def main():
    modele = Path(sys.argv[1]).resolve()
    tout = '--tout' in sys.argv
    referentiel = json.loads((RACINE / 'data/referentiel.json').read_text())['familles']
    phrases = json.loads((RACINE / 'data/phrases.json').read_text())

    a_faire = []
    for famille, items in referentiel.items():
        for it in items:
            a_faire.append((f'{famille}/{it["id"]}.mp3', it.get('voix') or it['dit']))
            if it.get('mot'):
                a_faire.append((f'{famille}/{it["id"]}_mot.mp3', it['mot']))
    for cle, texte in phrases.items():
        a_faire.append((f'phrases/{cle}.mp3', texte))

    voix = charger_voix(modele)
    crees = 0
    for fichier, texte in a_faire:
        destination = SON / fichier
        if tout or not destination.exists():
            enregistrer(voix, texte, destination)
            crees += 1
    liste = sorted(str(p.relative_to(SON)) for p in SON.rglob('*.mp3'))
    (SON / 'sons.json').write_text(json.dumps(liste, ensure_ascii=False, indent=0) + '\n')
    print(f'{crees} enregistrements créés, {len(liste)} au total')


if __name__ == '__main__':
    main()
