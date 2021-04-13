import rpyc
import logging

from rpyc.utils.server import ThreadedServer

from video_file_organizer.scheduler import scheduler

logger = logging.getLogger('vfo.rpyc srv')


class SchedulerService(rpyc.Service):
    def exposed_add_job(self, func, *args, **kwargs):
        return scheduler.add_job(func, *args, **kwargs)

    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)

    def exposed_reschedule_job(
            self, job_id, jobstore=None, trigger=None, **trigger_args):
        return scheduler.reschedule_job(job_id, jobstore, trigger,
                                        **trigger_args)

    def exposed_pause_job(self, job_id, jobstore=None):
        return scheduler.pause_job(job_id, jobstore)

    def exposed_resume_job(self, job_id, jobstore=None):
        return scheduler.resume_job(job_id, jobstore)

    def exposed_remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)

    def exposed_remove_all_jobs(self, jobstore=None):
        scheduler.remove_all_jobs(jobstore)

    def exposed_get_job(self, job_id):
        return scheduler.get_job(job_id)

    def exposed_get_jobs(self, jobstore=None):
        return scheduler.get_jobs(jobstore)

    def on_connect(self, conn):
        logger.info(f"RPYC connection from {conn}")


protocol_config = {'allow_public_attrs': True}

server = ThreadedServer(
    SchedulerService, hostname='0.0.0.0',
    port=2324,
    protocol_config=protocol_config)
