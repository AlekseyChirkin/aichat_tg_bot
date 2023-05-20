# -*- coding: utf8 -*-
"""
Конвертация wav -> текст
"""
import json
import os
import subprocess
from datetime import datetime
import wave

from vosk import KaldiRecognizer, Model  # оффлайн-распознавание от Vosk


class STT:
    """
    Класс для распознования аудио через Vosk и преобразования его в текст.
    Поддерживаются форматы аудио: wav, ogg
    """
    default_init = {
        "model_path": "model",  # путь к папке с файлами STT модели Vosk
        "sample_rate": 16000
    }

    """
        Настройка модели Vosk для распознования аудио и
        преобразования его в текст.

        :arg model_path:  str  путь до модели Vosk
        :arg sample_rate: int  частота выборки, обычно 16000
        :arg ffmpeg_path: str  путь к ffmpeg
        """

        model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(model, 16000)
        self.recognizer.SetWords(True)

    def _check_model(self):
        """
        Проверка наличия модели Vosk на нужном языке в каталоге приложения
        """
        if not os.path.exists(self.model_path):
            raise Exception(
                "Vosk: сохраните папку model в папку vosk\n"
                "Скачайте модель по ссылке https://alphacephei.com/vosk/models"
                            )

    def audio_to_text(self, audio_file_name=None) -> str:
        """
        Offline-распознавание аудио в текст через Vosk
        :param audio_file_name: str путь и имя аудио файла
        :return: str распознанный текст
        """
        if audio_file_name is None:
            raise Exception("Укажите путь и имя файла")
        if not os.path.exists(audio_file_name):
            raise Exception("Укажите правильный путь и имя файла")

        # Открываем файл для чтения
        wf = wave.open(audio_file_name, "rb")

        # Чтение данных кусками и распознование через модель
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                pass

        # Возвращаем распознанный текст в виде str
        result_json = self.recognizer.FinalResult()  # это json в виде str
        result_dict = json.loads(result_json)    # это dict
        return result_dict["text"]               # текст в виде str


if __name__ == "__main__":
    # Распознование аудио
    start_time = datetime.now()
    stt = STT()
    print(stt.audio_to_text('/files/voices/decoder-test.wav'))
    print("Время выполнения:", datetime.now() - start_time)
