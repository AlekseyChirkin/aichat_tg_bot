import speech_recognition as sr
from pydub import AudioSegment


def audio_to_text(path_to_file: str) -> str:
    r = sr.Recognizer()
    path_to_wav = path_to_file[-3] + 'wav'

    # # Temp
    # path_to_wav = path_to_file

    # Convert .ogg to .wav
    audio = AudioSegment.from_ogg(path_to_file)
    audio.export(path_to_wav, format="wav")
    print("File converted to .wav")

    audio_file = sr.AudioFile(path_to_wav)
    with audio_file as source:
        audio = r.record(source)

    print("Recognition...")
    return r.recognize_google(audio, language="RU-ru")
