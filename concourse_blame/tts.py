import pyttsx3


class TTS:

    @staticmethod
    def play_system_voice_examples():
        tts = pyttsx3.init()
        tts.setProperty('rate', 150)

        voices = tts.getProperty('voices')
        print('Your system has {} voices installed. Playing examples ...'.format(len(voices)))

        for i in range(len(voices)):
            tts.setProperty('voice', voices[i].id)
            tts.say('This is an English example of your system\'s voice with the id {}'.format(i))
            tts.runAndWait()
            tts.say('Das ist ein deutsches Beispiel der Systemstimme mit der ID {}'.format(i))
            tts.runAndWait()

        print('Finished playing examples. Enter the desired voice\'s id in your configuration file.')

    def __init__(self, voice_id: int, words_per_minute: int):
        self.tts = pyttsx3.init()
        self.tts.setProperty('voice', self.tts.getProperty('voices')[voice_id].id)
        self.tts.setProperty('rate', words_per_minute)

    def say(self, text: str):
        self.tts.say(text)
        self.tts.runAndWait()
