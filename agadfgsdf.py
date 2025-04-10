import aubio
import numpy as np
import librosa

def detect_pitch_and_silence(filename):
    win_s = 4096  # FFT size
    hop_s = 4096   # hop size
    samplerate = 44100
    
    s = aubio.source(filename, samplerate, hop_s)
    tolerance = 0.8
    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(tolerance)

    silence_threshold = -40  # dB
    pitch_o.set_silence(silence_threshold)

    pitches = []
    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        energy = np.sum(samples**2) / len(samples)

        if energy < 10**(silence_threshold / 10):
            pitches.append((total_frames, 'silence'))
        else:
            pitches.append((total_frames, pitch))

        total_frames += read
        if read < hop_s:
            break

    return pitches

# Example usage
filename = "exemplo.wav"
pitches_and_silences = detect_pitch_and_silence(filename)
for frame, pitch in pitches_and_silences:
    print(f"Frame {frame}: {pitch}")