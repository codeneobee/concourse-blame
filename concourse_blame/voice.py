import pyttsx3


def play_system_voices():
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
