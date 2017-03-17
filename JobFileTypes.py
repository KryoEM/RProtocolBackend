from os import path

job_types = ['Import', 'UnblurTBZ', 'MotionCorr', 'CtfFind', 'ManualPick',
             'AutoPick', 'Extract', 'Sort', 'Class2D', 'Class3D', 'Refine3D', 'MovieRefine', 'Polish',
             'Select', 'MaskCreate', 'JoinStar', 'Subtract', 'PostProcess', 'LocalRes']


class JobFileBase:
    def __init__(self, filename):
        self.filename = filename
        with open(filename) as f:
            self.contents = f.read()


class JobStarFile(JobFileBase):
    def __init__(self, filename):
        super().__init__(filename=filename)
        self.inputs = []
        self.outputs = []
        self.parse_star()

    def parse_star(self):
        if "data_pipeline_input_edges" in self.contents:
            input1 = self.contents[self.contents.index('data_pipeline_input_edges'):
            self.contents.index('data_pipeline_output_edges')]  # ; print(input1)

            in_substr = '_rlnPipeLineEdgeProcess #2'
            input2 = input1[input1.index(in_substr) + len(in_substr):].strip()

            input3 = input2.splitlines()
            for inp in input3:
                in_fn = inp.split(' ')[0]
                self.inputs.append(in_fn[2:] if inp.startswith('./') else in_fn)

        if "data_pipeline_output_edges" in self.contents:
            output1 = self.contents[self.contents.index('data_pipeline_output_edges'):]

            out_substr = '_rlnPipeLineEdgeToNode #2'
            # output2 = output1.substring(output1.indexOf(outputSubstr) + outputSubstr.length()).trim();
            output2 = output1[output1.index(out_substr) + len(out_substr):].strip()

            output3 = output2.splitlines()
            for out in output3:
                out_fn = out.split(' ')[1]
                self.outputs.append(out_fn[2:] if out.startswith('./') else out_fn)


class JobRunFile(JobFileBase):
    pass


class Job:
    def __init__(self, directory):
        self.directory = directory
        job_star_fn = directory + "/job_pipeline.star"
        job_run_fn = directory + "/run.job"

        self.job_star = JobStarFile(job_star_fn) if path.exists(job_star_fn) else None
        self.run_star = JobRunFile(job_run_fn) if path.exists(job_run_fn) else None

        idx = directory.index('job')
        self.job_number = int(directory[idx + 3:idx + 6])
