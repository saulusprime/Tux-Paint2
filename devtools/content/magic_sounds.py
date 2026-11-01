#!/usr/bin/env python3
"""Synthesize the sound effects of some Magic tools (magic/sounds/).

usage: devtools/content/magic_sounds.py [REPOSITORY_ROOT]

Needs numpy and oggenc (Debian: vorbis-tools). Writes, mono at 44.1 kHz:

  crossstitch.ogg   Cross Stitch: the needle goes through, the thread is
                    pulled
  halftone.ogg      Halftone: a little printing press
  puzzle.ogg        Puzzle: two pieces of cardboard clack into place
  colornwhite.ogg   Color & White (Tint plugin): a shimmer that drains away

Loudness is like the other sounds: peaks around -4 dB, about 0.4 seconds.
The noise is seeded, so the files come out the same every time.
"""
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "..")
RATE = 44100
rng = np.random.default_rng(2026)


def t_axis(seconds):
    return np.arange(int(seconds * RATE)) / RATE


def band_noise(seconds, center, width):
    """Noise in a band around center Hz (both may be functions of time,
    in seconds), made frame by frame."""
    n = int(seconds * RATE)
    frame, hop = 1024, 256
    window = np.hanning(frame)
    out = np.zeros(n + frame)
    freqs = np.fft.rfftfreq(frame, 1.0 / RATE)
    for start in range(0, n, hop):
        t = start / RATE
        c = center(t) if callable(center) else center
        w = width(t) if callable(width) else width
        spectrum = np.fft.rfft(rng.standard_normal(frame))
        spectrum *= np.exp(-0.5 * ((freqs - c) / w) ** 2)
        out[start:start + frame] += np.fft.irfft(spectrum, frame) * window
    out = out[:n]
    return out / (np.abs(out).max() + 1e-9)


def click(seconds, freq, decay):
    """A struck, quickly fading tone."""
    t = t_axis(seconds)
    return np.sin(2 * np.pi * freq * t) * np.exp(-t / decay)


def place(total, sound, at):
    """Mix sound into total, starting at 'at' seconds; its last 5 ms fade
    out, so that it doesn't end with a click."""
    fade = min(len(sound), int(0.005 * RATE))
    sound = sound.copy()
    sound[len(sound) - fade:] *= np.linspace(1.0, 0.0, fade)
    i = int(at * RATE)
    j = min(len(total), i + len(sound))
    total[i:j] += sound[:j - i]


def envelope(seconds, attack, release):
    t = t_axis(seconds)
    env = np.minimum(1.0, t / attack) if attack > 0 else np.ones(len(t))
    return env * np.clip((seconds - t) / release, 0.0, 1.0)


def crossstitch():
    total = np.zeros(int(0.42 * RATE))
    # The needle goes through the fabric
    place(total, click(0.03, 2100, 0.004) * 0.8 +
          band_noise(0.03, 4500, 1200) * np.exp(-t_axis(0.03) / 0.003) * 0.6, 0.0)
    # The thread is pulled through: a rising, rough swish
    pull = 0.30
    swish = band_noise(pull, lambda t: 1300 + 2600 * t / pull, 600)
    rough = 0.75 + 0.25 * np.sin(2 * np.pi * 38 * t_axis(pull))
    place(total, swish * rough * envelope(pull, 0.08, 0.12) * 0.55, 0.06)
    return total


def halftone():
    total = np.zeros(int(0.42 * RATE))
    # Paper running through
    place(total, band_noise(0.42, 2500, 1500) * envelope(0.42, 0.03, 0.1) * 0.08, 0.0)
    # The press, five strokes
    for i in range(5):
        at = 0.02 + i * 0.075
        strength = 1.0 if i % 2 == 0 else 0.7
        tick = band_noise(0.02, 3200, 900) * np.exp(-t_axis(0.02) / 0.003)
        place(total, tick * 0.6 * strength, at)
        place(total, click(0.06, 150, 0.018) * 0.5 * strength, at)
    return total


def puzzle():
    total = np.zeros(int(0.26 * RATE))
    for at, freq, strength in ((0.0, 320, 1.0), (0.095, 270, 0.8)):
        clack = band_noise(0.05, 1400, 700) * np.exp(-t_axis(0.05) / 0.008)
        place(total, clack * 0.7 * strength, at)
        place(total, click(0.07, freq, 0.02) * 0.5 * strength, at)
    return total


def colornwhite():
    seconds = 0.45
    t = t_axis(seconds)
    total = np.zeros(len(t))
    # Partials gliding down an octave, with a little tremolo
    for base, strength in ((1320, 0.5), (1980, 0.3), (2640, 0.2)):
        freq = base * 2.0 ** (-t / seconds)
        phase = 2 * np.pi * np.cumsum(freq) / RATE
        total += np.sin(phase) * strength
    total *= 0.8 + 0.2 * np.sin(2 * np.pi * 14 * t)
    total += band_noise(seconds, lambda s: 3000 - 2000 * s / seconds, 800) * 0.25
    return total * envelope(seconds, 0.02, 0.3)


def write_ogg(name, samples):
    samples = samples / np.abs(samples).max() * 10 ** (-4.0 / 20)
    pcm = (samples * 32767).astype("<i2")
    path = os.path.join(ROOT, "magic", "sounds", name + ".ogg")
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, name + ".wav")
        with wave.open(wav, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(RATE)
            f.writeframes(pcm.tobytes())
        subprocess.run(["oggenc", "--quiet", "-q", "4", "--serial", "2026",
                        "-o", path, wav], check=True)
    print(os.path.normpath(path))


for maker in (crossstitch, halftone, puzzle, colornwhite):
    write_ogg(maker.__name__, maker())
