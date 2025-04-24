# The AI Scientist (AI-S) Reproduced

## Setup

Follow these setup steps to run our templates with AI-S. For more information visit the [official README](https://github.com/SakanaAI/AI-Scientist/blob/main/README.md).

### Environment:
We use [singularity](https://docs.sylabs.io/guides/latest/user-guide/) to run AI-S inside a container.
If you want to do so as well you can use the container definition file `aiScientist.def`.
If you run `buildContainer.sh` it will use the sylabs cloud builder to build the container.

Furthermore, our computing cluster uses [slurm](https://slurm.schedmd.com/overview.html) to manage jobs.
If you do so as well, you can use the provided `launch_scientist.slurm` and `launch_reviewer.slurm` job scripts as a starting point.
They will run AI-S inside the container and they expect a `.env` file with API keys.
If you want to use OpenAI model (like we did) you can make a copy of `.env.example` and add in you API keys:
```sh
cp .env.example .env
# Fill out .env
```

### Datasets:
Out templates need a few additional datasets. These scripts will download and unzip them:
```sh
python data/AI-Scientist/data/ml-100k/prepare.py
python data/AI-Scientist/data/iris/prepare.py
python data/AI-Scientist/data/wine/prepare.py
```
### Baseline runs:
The official documentation recommends to run the baseline yourself as well, since the results are machine depended. We have included our results in this repository, but if you want to re-run them yourself you can do so with these commands:
```sh
cd data/AI-Scientist/templates/<template_name>/
python experiment.py --out_dir run_0
python plot.py
```
- <template_name> refers to one of {`knn`, `sgd`}. These are the two templates currently implemented (See Experiments/Templates below).


### Adding More Papers to Review Functionality:
We used papers from [openreview.net](https://openreview.net/) to test the review functionality of AI-S individually.
If you want to add more papers you can add their IDs from openreview (i.e. `openreview.net/forum?id=<this id>`) and the reviewers decision (`accept`/`reject`) to `data/AI-Scientist/ai_reviewer/papers.csv`


## Starting the AI Scientist (AI-S)
After you completed the setup above, you can start the AI-S in two ways:

#### Same Environment As Above:
When you have the same environment setup like we have, you can adjust the slurm scripts (`launch_scientist.slurm` and `launch_reviewer.slurm`) to your needs and start them using
```sh
sbatch launch_scientist.slurm
# OR
sbatch launch_reviewer.slurm
```

#### Custom Environment:
If you have your own environment, please orient yourself on the official README and the contents of the job scripts to see which command line options are available. Generally you should be able to start an experiment with something like:
```sh
python launch_scientist.py --model "gpt-4o-2024-05-13" --experiment knn --num-ideas 10
```
See the "Experiments/Templates" section below for information on the two experiments (`knn` and `sgd`) to choose from.

For the review functionality you can use our script `launch_reviewer.py`.
It does not require any additional parameters and will only generate reviews if they do not exist already.


## Experiments/Templates
**KNN:**
Simple k-Nearest Neighbors (KNN) classifier for classification on the Iris and the Wine dataset.
It uses Euclidean distance to measure the similarity between data points.
Accuracy, precision, recall and f1-score are tracked and reported.

**SGD:**
Collaborative filtering model using stochastic gradient descent (SGD) for matrix factorization on MovieLens-100k dataset. Outputs test RMSE.


## Tools
The `tools/` directory contains a few useful scripts, this currently includes:

**check_decision.py** - Verify that decisions made by ai reviewer match the actual decision from openreview.net.

**code_metrics.py** - Gathers some metrics about the code that the AI scientist wrote to quantify how many changes it did. 

**extract_cost.py** - Extract API cost from aider logs. 

**generate_prompt_from_pdf.py** - Generate prompts from a pdf file that can be used to make AI-S reproduce papers.

## Overview of Other Files in This Repository
**aiScientist.def** - Singularity container definition to build a container. It is based on the official (experimental) docker image

**data/AI-Scientist/** - This directory is mounted into the container and is a clone of the [official repository](https://github.com/SakanaAI/AI-Scientist).

**data/AI-Scientist/templates/sgd/** - This directory contains the necessary files for a custom template. Refer to the ["Making Your Own Template" section of the original README](https://github.com/SakanaAI/AI-Scientist/blob/c19f0f8ac575fd2426f56af526adc7a80341a761/README.md#making-your-own-template).

**buildContainer.sh** - Builds the singularity container using the sylabs cloud builder. We use the cloud builder because of permission restriction on our cluster.

**launch_scientist.slurm** - Slurm jobscript to queue a job that starts the ai scientist inside the singularity container.

**launch_reviewer.slurm** - Slurm jobscript to queue a job that starts the review functionality of ai scientist inside the singularity container.

**runShell.sh** - Runs an interactive shell inside the singularity container. Since all the files that ai scientist uses are in the *data/* directory this probably only has to be used rarely.

**tools/** - A directory with some useful scripts, see section `Tools` for more info.