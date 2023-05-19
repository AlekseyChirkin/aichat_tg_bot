from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import json
import wave
import os


def audio_to_text(path_to_file: str) -> str:
    # Convert .ogg to .wav
    path_to_wav_file = path_to_file[-3] + 'wav'
    audio = AudioSegment.from_ogg(path_to_file)
    audio.export(path_to_wav_file, format="wav", bitrate=16000)

    # check vosk model exists
    if not os.path.exists("model"):
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the "
              "current folder.")
        exit(1)

    # Use Test file
    # path_to_wav_file = 'C:\\temp\\aichat_tg_bot\\files\\voices\\decoder-test.wav'

    recognized_data = ""
    try:
        wave_audio_file = wave.open(path_to_wav_file, "rb")
        model = Model(r"model")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        print('reading frames')
        data = wave_audio_file.readframes(wave_audio_file.getnframes())

        print('frames read')
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()

                # получение данных распознанного текста из JSON-строки
                # (чтобы можно было выдать по ней ответ)
                print('получение данных распознанного текста из JSON-строки')
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        print("Sorry, speech service is unavailable. Try again later")

    print(recognized_data)
    return recognized_data
