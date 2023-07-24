from googletrans import Translator

translator = Translator()

def translate_rus_to_eng(text: str) -> str:
    return translator.translate(text, src='ru', dest='en').text

def translate_eng_to_rus(text: str) -> str:
    return translator.translate(text, src='en', dest='ru').text

if __name__ == "__main__":
    print(translate_rus_to_eng("Е-мое! Эта хрень работает!"))
    print(translate_eng_to_rus("Or not work properly, I don't know..."))