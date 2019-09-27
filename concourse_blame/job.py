import os
import re


class ConcourseJob:

    @staticmethod
    def get_latest(concourse_target: str, concourse_job_name: str):
        latest_job = os.popen('fly -t {} builds -j {} -c 1'.format(concourse_target, concourse_job_name)).read()
        columns = re.split('\s+', latest_job)
        return ConcourseJob(columns[2], columns[3])

    def __init__(self, id: int, status: str):
        self.id = id
        self.status = status

    def __eq__(self, other):
        return self.id == other.id and self.status == other.status


def get_latest_job(concourse_target: str, concourse_job_name: str) -> ConcourseJob:
    latest_job = os.popen('fly -t {} builds -j {} -c 1'.format(concourse_target, concourse_job_name)).read()
    columns = re.split('\s+', latest_job)
    return ConcourseJob(columns[2], columns[3])


def get_latest_committer(bare_repo_path: str) -> str:
    return_path = os.getcwd()
    os.chdir(bare_repo_path)
    os.system('git fetch')
    latest_committer = os.popen("git log -1 --pretty=format:'%an'").read()
    os.chdir(return_path)
    return latest_committer
