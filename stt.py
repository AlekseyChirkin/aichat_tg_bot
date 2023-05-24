from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import json
import os


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


def any2wav(ofn):
    wfn = ofn[:-4] + '.wav'
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format='wav')


def recognize_speech(path_to_file):
    # Конвертируем в wav
    any2wav(path_to_file)
    path_to_file = path_to_file[:-4] + '.wav'

    # Используя библиотеку pydub делаем предобработку аудио
    prepared_audio_file = AudioSegment.from_wav(path_to_file)
    prepared_audio_file = prepared_audio_file.set_channels(CHANNELS)
    prepared_audio_file = prepared_audio_file.set_frame_rate(FRAME_RATE)

    # Преобразуем вывод в json
    rec.AcceptWaveform(prepared_audio_file.raw_data)
    result = rec.Result()

    # Возвращаем только текст
    return json.loads(result)["text"]


if __name__ == "__main__":
    print(recognize_speech('test/test-2.wav'))
    print(recognize_speech('test/test-2.ogg'))
