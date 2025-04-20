#!/bin/bash

# We use sylabs cloud builder to build containers, because of permission restriction on the cluster

singularity remote login
singularity build --remote aiScientist.sif aiScientist.def

