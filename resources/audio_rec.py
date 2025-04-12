#imports are inside the function to avoid audio glitching for a split second after running.

def record_system(output_path,duration=15):
    import soundcard as sc
    import soundfile as sf

    output_file_name = output_path
    samplerate = 48000
    record_sec = duration

    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=samplerate) as mic:
        data = mic.record(numframes=samplerate*record_sec)
        

    sf.write(file=output_file_name, data=data[:, 0], samplerate=samplerate)

def record_audio(output_file="microphone.mp3", duration=15):
    import sounddevice as sd
    import soundfile as sf

    samplerate = 44100

    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()

    sf.write(output_file, audio_data, samplerate)