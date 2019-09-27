import getpass
import os
import random
import time

from playsound import playsound

from concourse_blame.job import *
from concourse_blame.tts import TTS


class ConcourseBlame:

    def __init__(self, config: dict):
        self.config = config

    def run(self):
        # initialize bare repository if not exists
        if not os.path.isdir(self.config['git']['clone_path']):
            os.system('git clone --bare {} {}'.format(
                self.config['git']['repository_url'],
                self.config['git']['clone_path']))

        # fly login
        password = getpass.getpass('Enter concourse password: ')
        error = os.system('fly login -t {} -u {} -p {}'.format(
            self.config['concourse']['target'],
            self.config['concourse']['user'],
            password))
        if error:
            exit(1)

        # init tts
        tts = TTS(self.config['tts']['voice_id'], self.config['tts']['words_per_minute'])
        tts.say(self.config['tts']['greeting'])

        # get latest job for initialization
        latest_job = get_latest_job(self.config['concourse']['target'], self.config['concourse']['job'])
        print('Initialized job {}: ID {} / status {}'.format(
            self.config['concourse']['job'], latest_job.id, latest_job.status))

        while True:
            time.sleep(self.config['update_rate_seconds'])

            # get latest job
            current_job = get_latest_job(self.config['concourse']['target'], self.config['concourse']['job'])
            if latest_job == current_job:
                continue

            # status has changed

            latest_job = current_job
            print('Update on job {}: ID {} / status {}'.format(
                self.config['concourse']['job'], latest_job.id, latest_job.status))

            if latest_job.status not in self.config['sounds']['status']:
                print('... but no notification has been configured for this status.')
                continue

            # there is a sound configured to be played for the new status

            latest_committer = get_latest_committer(self.config['git']['clone_path'], self.config['teams'])
            print('Committer {} in team {}'.format(latest_committer.name, latest_committer.team))

            # start sound
            if 'start' in self.config['sounds']:
                playsound(self.config['sounds']['start'])
            # status sound
            playsound(self.config['sounds']['status'][latest_job.status])
            # tts
            if latest_job.status in self.config['texts']['status']:
                texts = self.config['texts']['status'][latest_job.status]
                if len(texts) > 0:
                    text = random.choice(texts)
                    if latest_committer.team:
                        committer_text = self.config['texts']['committer']['from_team'].replace('%name', latest_committer.name).replace('%team', latest_committer.team)
                    else:
                        committer_text = self.config['texts']['committer']['no_team'].replace('%name', latest_committer.name)
                    tts.say(text.replace('%committer', committer_text))
            # end sound
            if 'end' in self.config['sounds']:
                playsound(self.config['sounds']['end'])
