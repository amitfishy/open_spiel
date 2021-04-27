#!/usr/bin/env bash
userhome=~
vm_dir=~/python-vms
project_name=ED_project_final
virtualhome=${vm_dir}/${project_name}

mkdir -p $userhome/scratch/${project_name}

MEM=2G
TIME=02:00:00

results_dir=${virtualhome}/results
num_steps=10000
print_freq=10
regularizer_scale=0.001
num_hidden=64
num_layers=1

actorcritic_methods=(QPG RPG RMPG)

game_names=(kuhn_poker)

seeds=(0 1 2 3 4)

init_lrs=(0.06 0.08 0.1 0.2 0.3 0.4 0.5 0.6)


if [ $1 = cat ]
then
	echo 'Concatenating data from random seeds into a single file...'
	eval "source $virtualhome/bin/activate"
	eval "cd $virtualhome/code/open_spiel"
	for actorcritic_method in ${actorcritic_methods[@]}
	do
		for game_name in ${game_names[@]}
		do
			for init_lr in ${init_lrs[@]}
			do
				eval "python concat_results.py --game_name=${game_name} --num_steps=${num_steps} --print_freq=${print_freq} --init_lr=${init_lr} --regularizer_scale=${regularizer_scale} --num_hidden=${num_hidden} --num_layers=${num_layers} --results_folder=${results_dir} --actorcritic_method=${actorcritic_method}"
			done
		done
	done
else
	echo 'Submitting SBATCH jobs...'
	for actorcritic_method in ${actorcritic_methods[@]}
	do
		for game_name in ${game_names[@]}
		do
			for init_lr in ${init_lrs[@]}
			do
				for seed in ${seeds[@]}
				do
					echo "#!/bin/bash" >> temprun.sh
					echo "#SBATCH --account=def-adityam" >> temprun.sh
					echo "#SBATCH --job-name=actorcritic-method-${actorcritic_method}_game-name-${game_name}_init-lr-${init_lr}_seed-${seed}" >> temprun.sh
					echo "#SBATCH --output=$userhome/scratch/${project_name}/%x-%j.out" >> temprun.sh
					echo "#SBATCH --cpus-per-task=1" >> temprun.sh
					echo "#SBATCH --mem=${MEM}" >> temprun.sh
					echo "#SBATCH --time=${TIME}" >> temprun.sh

					echo "source $virtualhome/bin/activate" >> temprun.sh
					echo "cd $virtualhome/code/open_spiel/open_spiel/python/examples" >> temprun.sh
					echo "python exploitability_descent.py --game_name=${game_name} --num_steps=${num_steps} --print_freq=${print_freq} --init_lr=${init_lr} --regularizer_scale=${regularizer_scale} --num_hidden=${num_hidden} --num_layers=${num_layers} --results_folder=${results_dir} --actorcritic_method=${actorcritic_method} --seed=${seed}"

					eval "sbatch temprun.sh"
					#added to submit job again if slurm error occurs (timeout error send/recv)
					while [ ! $? == 0 ]
					do
						eval "sbatch temprun.sh"
					done

					# sleep 1
					rm temprun.sh
				done
			done
		done
	done
fi