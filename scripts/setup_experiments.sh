my_repo=https://github.com/amitfishy/open_spiel
vm_dir=~/python-vms
project_name=ED_project_final

# module load cuda/10.0
module load python/3.6
mkdir -p ${vm_dir}
virtualenv --no-download ${vm_dir}/${project_name}
source ${vm_dir}/${project_name}/bin/activate
pip install --no-index --upgrade setuptools pip
# pip3 install open_spiel
pip install attrs absl-py numpy
pip install tensorflow


#setup code
mkdir -p ${vm_dir}/${project_name}/code
cd ${vm_dir}/${project_name}/code
git clone ${my_repo}
cd open_spiel/open_spiel
mkdir -p ${vm_dir}/${project_name}/lib/python3.6/site-packages/open_spiel
cp -r python ${vm_dir}/${project_name}/lib/python3.6/site-packages/open_spiel/python
touch ${vm_dir}/${project_name}/lib/python3.6/site-packages/open_spiel/__init__.py
cp ${vm_dir}/${project_name}/code/open_spiel/pyspiel.so ${vm_dir}/${project_name}/lib/python3.6/site-packages
cp ${vm_dir}/${project_name}/code/open_spiel/open_spiel/python/algorithms/exploitability_descent.py ${vm_dir}/${project_name}/lib/python3.6/site-packages/open_spiel/python/algorithms/