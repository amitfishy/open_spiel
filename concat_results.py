from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import os

from absl import app
from absl import flags
from absl import logging

import numpy as np

FLAGS = flags.FLAGS

flags.DEFINE_string("game_name", "kuhn_poker", "Name of the game")
flags.DEFINE_integer("num_steps", 100, "Number of iterations")
flags.DEFINE_integer("print_freq", 1, "Log progress every this many steps")
flags.DEFINE_float("init_lr", 0.1, "The initial learning rate")
flags.DEFINE_float("regularizer_scale", 0.001,
                   "Scale for L2 regularization of NN weights")
flags.DEFINE_integer("num_hidden", 64, "Hidden units.")
flags.DEFINE_integer("num_layers", 1, "Hidden layers.")

# flags.DEFINE_integer("seed", 42, "Random Seed")
flags.DEFINE_string("results_folder", "Results", "Location for outputting result data.")
flags.DEFINE_string("actorcritic_method", "QPG", "Type of actor critic algorithm to use.")

#ppo params
flags.DEFINE_integer("N_epochs", 4, "Number of epochs for PPO")
flags.DEFINE_float("ppo_eps", 0.1, "Clipping parameter for PPO")
flags.DEFINE_float("min_policy_eps", 0.0001, "Minimum value for each action in old policy")

def main(argv):
	del argv

	nash_conv_values_s = []
	steps_s = []

	if FLAGS.actorcritic_method == 'PPO':
		args_list = [str(FLAGS.game_name), str(FLAGS.num_steps), str(FLAGS.print_freq), str(FLAGS.init_lr), str(FLAGS.regularizer_scale), str(FLAGS.num_hidden), str(FLAGS.num_layers), str(FLAGS.actorcritic_method), str(FLAGS.N_epochs), str(FLAGS.ppo_eps), str(FLAGS.min_policy_eps)]
	else:
		args_list = [str(FLAGS.game_name), str(FLAGS.num_steps), str(FLAGS.print_freq), str(FLAGS.init_lr), str(FLAGS.regularizer_scale), str(FLAGS.num_hidden), str(FLAGS.num_layers), str(FLAGS.actorcritic_method)]
	output_folder = os.path.join(FLAGS.results_folder, '_'.join(args_list))
	assert os.path.exists(output_folder), 'The output folder: ' + output_folder + ' does not exist to concatenate random seed results within.'
	for filename in os.listdir(output_folder):
		filepath = os.path.join(output_folder, filename)
		if os.path.isfile(filepath):
			res = np.load(filepath)
			nash_conv_values_s.append(res['nash_conv_values'])
			steps_s.append(res['steps'])

	np.savez(os.path.join(output_folder, 'concat_result.npz'), nash_conv_values_s = nash_conv_values_s, steps_s = steps_s)

if __name__ == "__main__":
	app.run(main)