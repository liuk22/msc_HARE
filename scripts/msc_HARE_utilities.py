
import os 
import ipywidgets
import glob
import numpy as np
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import cm

class Log: 
    def __init__(self, full_path=None, unix_file=False): 
        self.experiment_name = None
        self.timestamp = None
        self.stage = None
        self.unit = None 
        self.unit_value = None
        self.path = full_path 
        self.unix_file = unix_file
        if full_path is not None: 
            parent_abs, log_title = os.path.split(full_path)
            self.experiment_name = parent_abs[parent_abs.rfind("/"):]
            details = log_title.split("_")
            self.timestamp = details[0][len(details[0]) - 19:]
            self.stage = int(details[1][5:])
            j = 0 
            while details[2][j] != ".": 
                j += 1
            if details[2][0] == "t": 
                self.unit = "proportion"
                self.unit_value = float(details[2][6:j]) / 100.0
            elif details[2][0] == "s":
                self.unit = "second"
                self.unit_value = details[2][6:j]


class Analysis: 
    def __init__(self, is_unix_filesystem):
        self.all_logs_path = f"{os.path.dirname(os.getcwd())}\\logs\\heatmaps\\*"
        self.is_unix_filesystem = is_unix_filesystem
        self.selected_experiments = [] 

    def select_experiments(self, x): 
        self.selected_experiments = [x] 
    
    def display_experiment_options(self):
        def strip_dir_func(is_unix):
            if is_unix:
                return lambda el : el[el.rfind("/") + 1:]
            else:
                return lambda el : el[el.rfind("\\") + 1:]
        dropdown_options = list(map(strip_dir_func(self.is_unix_filesystem), glob.glob(self.all_logs_path)))
        ipywidgets.interact(self.select_experiments, x=ipywidgets.widgets.Dropdown(options=dropdown_options, 
        description="Selected Experiment Folder:", 
        style={"description_width": "initial"}),
        )

    def generate_visualizations(self, save_fig_to=None):
        for i in range(len(self.selected_experiments)):
            exp_name = self.selected_experiments[i]
            experiment_path_matcher = f"{self.all_logs_path[:-1]}{exp_name}/*.txt"
            log_objects = [Log(full_path=file_path, unix_file=self.is_unix_filesystem) for file_path in glob.glob(experiment_path_matcher)]

            log_objects.sort(key=lambda el: el.stage)
            # Assuming each experiment had the same amount of stages completed, we can find the highest stage 
            # and figure out the number of experiments/sample size n 
            highest_stage = -1
            for i in range(len(log_objects)):
                if highest_stage < log_objects[i].stage: 
                    highest_stage = log_objects[i].stage
            num_trials = len(log_objects) // (highest_stage + 1) 
            fig, axs = plt.subplots(highest_stage + 1, 1, figsize= (10,20))
            for i in range(0, highest_stage + 1):    
                arr = None
                for j in range(num_trials): 
                    if arr is None: 
                        arr = (np.loadtxt(log_objects[j + i * num_trials].path) >= 0) / num_trials
                    else:
                        arr += (np.loadtxt(log_objects[j + i * num_trials].path) >= 0) / num_trials
                plot_i = axs[i].contourf(arr, cmap=cm.magma)
                if log_objects[i].unit == "second":
                    axs[i].set_title(f"Robot Environment Exploration at Stage {i}, {log_objects[i * num_trials].unit_value} Seconds Explored")
                else:
                    axs[i].set_title(f"Robot Environment Exploration at Stage {i}, {log_objects[i * num_trials].unit_value} Proportion Explored")
                plt.colorbar(plot_i, ax=axs[i], label="Frequentist Probability of Area Explored by Experiment Method")
                if save_fig_to:
                    plt.savefig(save_fig_to)