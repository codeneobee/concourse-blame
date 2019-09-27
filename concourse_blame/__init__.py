import os


class ConcourseBlame:

    def __init__(self, config: dict):
        self.config = config

    def run(self):
        # initialize bare repository if not exists
        if not os.path.isdir(self.config['git']['clone-path']):
            os.system('git clone --bare {} {}'.format(
                self.config['git']['repository-url'],
                self.config['git']['clone-path']))
