# OOD User Monitor App

This repo contains a small user monitor app, that allows users to get an overview of their current/recent jobs and the efficiency of those.

## Installation

On login node:

```console
mkdir /scratch/work/$USER/.ondemand/dev/
cd /scratch/work/$USER/.ondemand/dev/
git clone git@version.aalto.fi:AaltoScienceIT/ood-python-app-template.git
cd ood-python-app-template
python3 -m venv python-app
source python-app/bin/activate
pip install -r requirements.txt
```

Now in OnDemand you can click Develop -> My Sandbox Apps -> Launch BMI calculator.

OnDemand might require you to restart your nginx server to launch the app. Click
the big red button to allow for the restart to happen.
