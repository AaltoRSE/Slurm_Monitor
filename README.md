# OOD User Monitor App

This repo contains a small user monitor app, that allows users to get an overview of their current/recent jobs and the efficiency of those.

## Installation (dev)

On login node:

```console
# Clone the repo
mkdir /scratch/work/$USER/.ondemand/dev/
cd /scratch/work/$USER/.ondemand/dev/
git clone git@github.com:AaltoRSE/Slurm_Monitor.git slurm_monitor
cd slurm_monitor

# Build the frontend
module load mamba
mamba env create -f environment.yml
source activate frontend-builder
cd frontend && npm install && npm run build && cd ..
source deactivate
# we have to clean up any environment, to get to the base python. this includes the mamba module
module purge
# Create the environment for the app
python3 -m venv python-app
source python-app/bin/activate
pip install -r requirements.txt
```

Now in OnDemand you can click Develop -> My Sandbox Apps -> Launch Slurm User Monitor.

OnDemand might require you to restart your nginx server to launch the app. Click
the big red button to allow for the restart to happen.

## installation (prod)
