from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import json
import os


def recognize_speech(path_to_file):
    # Проверяем наличие модели
    if not os.path.exists("model"):
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current "
              "folder.")
        exit(1)

    # Устанавливаем Frame Rate
    FRAME_RATE = 16000
    CHANNELS = 1

    model = Model("model")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    # Используя библиотеку pydub делаем предобработку аудио
    wav = AudioSegment.from_wav(path_to_file)
    wav = wav.set_channels(CHANNELS)
    wav = wav.set_frame_rate(FRAME_RATE)

    # Преобразуем вывод в json
    rec.AcceptWaveform(wav.raw_data)
    result = rec.Result()
    text = json.loads(result)["text"]

    # Записываем результат в файл "data.txt"
    with open('data.txt', 'w', encoding='utf-8') as f:
        json.dump(text, f, ensure_ascii=False, indent=4)

    return text


if __name__ == "__main__":
    print(recognize_speech('test-2.wav'))
