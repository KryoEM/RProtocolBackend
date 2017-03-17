import os

from JobFileTypes import *


class Workflow:
    def __init__(self, final_job_folder):
        self.final_job_folder = final_job_folder

        self.temp_steps = []
        self.preprocess_steps = []

        # Since the constructor final_job_folder argument is something like
        # /Users/restifoan/Desktop/bgal/PostProcess/job039
        # To get the project folder, we navigate up two directories using os.path.dirname and os.path.abspath
        # (in this case it would be folder "bgal")
        self.proj_base_dir = path.dirname(path.dirname(path.abspath(final_job_folder)))

    def get_protocol_steps(self):
        # Use list comprehensions to find the job directories by filtering out the directories we don't want
        nodedirs = [path.join(self.proj_base_dir, d) for d in os.listdir(self.proj_base_dir) if d in job_types]
        all_paths = []
        for node in nodedirs:
            jobdirs = [d for d in os.listdir(node) if not path.islink(d) and d.startswith('job')]
            all_paths.extend(jobdirs)

        # Traverse the job tree
        self.traverse_job_inputs(self.final_job_folder)

        # Remove duplicates from the list
        steps = []
        for pp_step in self.preprocess_steps:
            if pp_step not in steps:
                steps.append(pp_step)

        # Create final job list
        final_jobs = []
        for step in steps:
            final_jobs.append(Job(path.join(self.proj_base_dir, path.dirname(path.abspath(step)))))
        # Manually add the final job because the way traverse_job_inputs is designed means we need to add it manually
        final_jobs.append(Job(self.final_job_folder))

        # Sort the final job list
        print('final jobs:')
        final_jobs.sort(key=lambda x: x.job_number, reverse=True)
        for fj in final_jobs:
            print(fj.directory)

    def traverse_job_inputs(self, job_path):
        print('recurse')
        job = Job(job_path)
        if not any(temp_job.directory == job.directory for temp_job in self.temp_steps):
            self.temp_steps.append(job)

        inputs = job.job_star.inputs
        print('inputs for job #{0}: {1} '.format(job.job_number, inputs))
        for inp in inputs:
            self.traverse_job_inputs(path.join(self.proj_base_dir, path.join(self.proj_base_dir,
                                                                             path.dirname(inp))))
            self.preprocess_steps.append(inp)
