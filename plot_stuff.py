import os
import argparse
from shutil import copyfile


def get_param(search_string, lines):
	for line in lines:
		if search_string == line[:len(search_string)]:
			param = line[len(search_string)+1:].strip()
			return param
	print ('{} not found'.format(search_string))
	return

def get_list_params(search_string, lines):
	params = []
	for i, line in enumerate(lines):
		if search_string == line[:len(search_string)]:
			string_part = line[len(search_string)+2:].strip()
			if string_part[-1] == ')':
				params = string_part[:-1].split(' ')
				return params
			else:
				params = string_part.split(' ')
				counter = 1
				while True:
					string_part = lines[i+counter].strip()
					if string_part[-1] == ')':
						params = params + string_part[:-1].split(' ')
						return params
					else:
						params = params + string_part.split(' ')
						counter = counter + 1
	print ('{} not found'.format(search_string))
	return



parser = argparse.ArgumentParser()

parser.add_argument('--config_file', help='The bash script used to generate results (run_minigrid_experiments.sh)')
parser.add_argument('--results_folder', help='The results folder generated from the bash script')
parser.add_argument('--output_folder', help='The output plots will be generated in this folder')
parser.add_argument('--primary_plot_feature', help='Parallel plots of this feature are made in the same graph. Options: [ac_methods] [init_lrs]', default=None)

args = parser.parse_args()

with open(args.config_file) as f: 
	lines = f.readlines() 



num_steps = get_param('num_steps', lines)
print_freq = get_param('print_freq', lines)
regularizer_scale = get_param('regularizer_scale', lines)
num_hidden = get_param('num_hidden', lines)
num_layers = get_param('num_layers', lines)

actorcritic_methods = get_list_params('actorcritic_methods', lines)
game_names = get_list_params('game_names', lines)
init_lrs =  get_list_params('init_lrs', lines)

sec_plot_feat_init_lrs = (len(init_lrs) > 1) and (args.primary_plot_feature != 'init_lrs')
sec_plot_feat_ac_methods = (len(actorcritic_methods) > 1) and (args.primary_plot_feature != 'ac_methods')



for game_name in game_names:
	for init_lr in init_lrs:
		for actorcritic_method in actorcritic_methods:
			results_args_list = [game_name, num_steps, print_freq, init_lr, regularizer_scale, num_hidden, num_layers, actorcritic_method]
			results_folder = os.path.join(args.results_folder , '_'.join(results_args_list))
			result_file = os.path.join(results_folder, 'concat_result.npz')

			output_args_list = [game_name]
			if sec_plot_feat_init_lrs:
				output_args_list.append('LR-' + init_lr)
			if sec_plot_feat_ac_methods:
				output_args_list.append('AC-' + actorcritic_method)


			output_folder = os.path.join(args.output_folder + '_temp' , '_'.join(output_args_list))
			if not os.path.exists(output_folder):
				os.makedirs(output_folder)

			if args.primary_plot_feature == None:
				output_filename = 'ED.npz'
			elif args.primary_plot_feature == 'init_lrs':
				output_filename = 'LR-' + init_lr + '.npz'
			elif args.primary_plot_feature == 'ac_methods':
				output_filename = 'AC-' + actorcritic_method + '.npz'
			output_file = os.path.join(output_folder, output_filename)

			copyfile(result_file, output_file)


for folder_to_plot in os.listdir(args.output_folder + '_temp'):
	plot_folder_path = os.path.join(args.output_folder + '_temp', folder_to_plot)
	output_path = os.path.join(args.output_folder, folder_to_plot)

	if not os.path.exists(output_path):
		os.makedirs(output_path)
	game_name = folder_to_plot.split('_')[0]

	cmd = 'python plot_folder.py --plot_folder {} --output_folder {} --env_name {}'.format(plot_folder_path, output_path, game_name)

	print (cmd)
	os.system(cmd)
	print