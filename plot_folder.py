import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--plot_folder', help='Folder to plot everything from')
parser.add_argument('--output_folder', help='Folder to plot everything into')
parser.add_argument('--env_name', help='Name of the environment')
parser.add_argument("--display_window", action="store_true", help="Display window or not", default=False)


args = parser.parse_args()

folder_name = args.plot_folder
output_folder = args.output_folder
environment_name = args.env_name
display_window = args.display_window

if not os.path.exists(output_folder):
	os.makedirs(output_folder)

colors = ["#1f77b4", "#ff7f0e", "#d62728", "#9467bd", "#2ca02c", "#8c564b", "#e377c2", "#bcbd22", "#17becf", "#1fb4a7", "#1f2db4", "#5c1fb4", "#a71fb4", "#b41f77", "#b41f2d", "#b45c1f", "#b4a71f", "#77b41f", "#2db41f", "#1fb45c", "#ded141", "#5d1fb3", "#8240de"]
color_index = 0


SMALL_SIZE = 22
MEDIUM_SIZE = 26
BIGGER_SIZE = 32

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

plt.figure(figsize=(16.0, 9.0))


plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

plt.xscale('log')
plt.yscale('log')

for filename in os.listdir(folder_name):
	if os.path.isfile(os.path.join(folder_name, filename)):
		#Loading the data
		plot_str = filename[:-4]
		data = np.load(os.path.join(folder_name, filename))

		nash_conv_values_s = data['nash_conv_values_s']
		steps_s = data['steps_s'][0]

		nc_data_median = np.median(nash_conv_values_s, axis=0)
		nc_upper_quartile = np.percentile(nash_conv_values_s, 75, axis=0)
		nc_lower_quartile = np.percentile(nash_conv_values_s, 25, axis=0)

		plt.plot(steps_s, nc_data_median, color=colors[color_index], linewidth=2.0, label=plot_str)
		plt.fill_between(steps_s, nc_upper_quartile, nc_lower_quartile, alpha=0.2, edgecolor=colors[color_index], facecolor=colors[color_index])
		color_index = color_index + 1

plt.xlabel("Steps")
plt.ylabel("NashConv")
plt.title(environment_name)
plt.legend()

if display_window:
	plt.show()
else:
	plt.savefig(os.path.join(output_folder, environment_name + '.png'))
	plt.clf()
	print("Performance Plot Saved...")