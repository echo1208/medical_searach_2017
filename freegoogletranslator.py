from googletrans import Translator

def googletranslate(text):
    translator = Translator()
    return translator.translate(text, dest='ja').text
