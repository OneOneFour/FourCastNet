#!/bin/bash
#SBATCH --partition serc
#SBATCH -c 4
#SBATCH -t 12:00:00
ml python/3.9.0
python3 get_data_sfc_short_length.py 
echo "done"
