import getpass
import os
import time

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
            latest_committer = get_latest_committer(self.config['git']['clone_path'])
            print('Update on job {}: ID {} / status {}'.format(
                self.config['concourse']['job'], latest_job.id, latest_job.status))
