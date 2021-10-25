# Description 
**Heatmap Analysis of Robot Exploration (HARE)** is a debugging, visualization, and optimization tool for occupancy-grid based robot exploration built for UC Berkeley's Mechanical Systems Control (MSC) Lab. HARE is structured as a ROS package and nodes combined with Jupyter Notebook visualization tools and is designed to be easily integrated into your robot exploration research workflow. 

Provided a ROS topic containing an OccupancyGrid that a given robot exploration experiment updates continuously, HARE takes snapshots of the OccupancyGrid at user-defined stages exploration and logs them to ```logs/heatmaps``` under the experiment's name. These snapshots of progress are aggregated across trials of the same experiment methodology to form heatmaps and visualizations viewable through the Jupyter Notebook ```scripts/analyzer.ipynb```. 

# Usage 
1. Clone HARE to your catkin workspace's ```src``` directory. 
2. Install all [dependencies](#Dependencies).
3. Build the package. 
4. Edit ```configuration/exploration_progress_config.json``` to name your experiment, define the stages where snapshots are taken, scale your OccupancyGrid, set the map topic, and more. 
5. Begin running your existing robot exploration experiment, then start the ```src/exploration_progress.py``` ROS node through adding it to an existing launch file or manually ```rosrun```.
6. When ```src/exploration_progress.py``` and/or your experiment finishes, open ```scripts/analyzer.ipynb``` through Jupyter Notebook and select your experiment to analyze. 


# Examples

# Dependencies 
