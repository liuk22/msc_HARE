#!/usr/bin/env python
import rospy
from nav_msgs.msg import OccupancyGrid
import time 
import numpy as np
import os
import json

CONFIG_FOLDER_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/../configuration/exploration_progress_config.json"
LOG_FOLDER_PATH = f"{os.path.dirname(os.path.realpath(__file__))}../logs/heatmaps/"

config_file = None
with open(CONFIG_FOLDER_PATH) as fh: 
    config_file = json.load(fh)

if config_file["unit"] == "second": 
    keys = sorted(map(int, config_file["stages"]))
elif config_file["unit"] == "proportion":
    keys = sorted(map(float, config_file["stages"]))
STAGES = {key : False for key in keys}

SAMPLING_PERIOD = 1

TIME_LAST = 0
TIME_FIRST = 0

def callback(message):
    if rospy.get_time() - TIME_LAST < SAMPLING_PERIOD:  
        return 
    map_grid = np.reshape(message.data, (message.info.height, message.info.width))
    x1, x2 = 0, map_grid.shape[0]
    y1, y2 = 0, map_grid.shape[1]
    if len(config_file["map_bounds_x"]) == 2: 
        x1, x2 = config_file["map_bounds_x"][0], config_file["map_bounds_x"][1]
    if len(config_file["map_bounds_y"]) == 2: 
        y1, y2 =  config_file["map_bounds_y"][0],  config_file["map_bounds_y"][1]
    map_grid = map_grid[x1:x2, y1:y2]
    if config_file["unit"] == "proportion":  
        num_grid_squares = np.abs((x1 - x2) * (y1 - y2))
        num_unmapped_squares = np.sum(map_grid < 0)
        fraction_mapped = 1.0 - (float(num_unmapped_squares) / float(num_grid_squares))
        
        global STAGES  
        for i, k in enumerate(sorted(STAGES.keys())): 
            if not STAGES[k] and k <= fraction_mapped:
                STAGES[k] = True 
                log_file_proportion(map_grid, i, k) 
                break 
    elif config_file["unit"] == "second":
        global STAGES
        global TIME_FIRST
        for i, k in enumerate(sorted(STAGES.keys())): 
            if not STAGES[k] and k <= rospy.get_time().secs - TIME_FIRST.secs:
                STAGES[k] = True 
                log_file_second(map_grid, i, k)
                break  
    if all(STAGES.values()): 
        os.system("rosnode kill --all")

    global TIME_LAST
    TIME_LAST = rospy.get_time()


def log_file_second(grid_as_np, stage_num, stage_second): 
    named_tuple = time.localtime() # get struct_time
    log_name = "{}{}".format(LOG_FOLDER_PATH, time.strftime("%m-%d-%YT%H-%M-%S", named_tuple))
    log_name += "_stage{}_second{}.txt".format(stage_num, int(stage_second * 100))
    with open(log_name, 'w') as fh: 
        np.savetxt(fh, grid_as_np, fmt='%3.4f')

def log_file_proportion(grid_as_np, stage_num, stage_proportion): 
    named_tuple = time.localtime() # get struct_time
    log_name = "{}{}".format(LOG_FOLDER_PATH, time.strftime("%m-%d-%YT%H-%M-%S", named_tuple))
    log_name += "_stage{}_proportion{}.txt".format(stage_num, int(stage_proportion * 100))
    with open(log_name, 'w') as fh: 
        np.savetxt(fh, grid_as_np, fmt='%3.4f')


def node(): 
    rospy.init_node('exploration_progress', anonymous=True)
    map_topic = rospy.get_param("~map_topic", "map")
    global TIME_LAST
    TIME_LAST = rospy.get_time()
    global TIME_FIRST
    TIME_FIRST = TIME_LAST
    rospy.Subscriber(map_topic, OccupancyGrid, callback)
    rospy.spin()


if __name__ == '__main__':
    node()