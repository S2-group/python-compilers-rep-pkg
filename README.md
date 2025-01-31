# An Empirical Study on the Performance and Energy Usage of Compiled Python Code

This repository contains the replication package for the study 'An Empirical Study on the Performance and Energy Usage of Compiled Python Code'

## Structure

`data`: contains the measurements on the experiement
`notebooks`:contains the scripts used for the data analysis.
`subjects`: contains the code executed per compiler and the test cases.
`runners`: contains the script of ExperimentRunner used to orchestrate the experiment. 
`setup_experimental_machine.sh`: script that setups Condon, PyPy, and EnergiBridge on the testbed 

## Benchmarks 

We selected 7 functions from the Computer Language Benchmark Game (CLBG) following these criteria to mitigate any threat to validity related to code characteristics and to discover if they can influence our results.

1. well-defined developer profile
2. no parallelism (single-thread) 
3. no third-party library
4. execution time > 1 min to collect enough data for our results. As we use tools having granularity of 1 second. The table reports data taken from the CBLG

| Name                                                                                                                | Execution Time | Memory Busy Time (s) | Notes               |
| ------------------------------------------------------------------------------------------------------------------- | -------------- | -------------------- | ------------------- |
| [spectral-norm](https://benchmarksgame-team.pages.debian.net/benchmarksgame/program/spectralnorm-python3-8.html)    | 6 min          | 19.4                 |                     |
| [binary-trees](https://benchmarksgame-team.pages.debian.net/benchmarksgame/program/binarytrees-python3-8.html)      | 9 min          | 798.336              |                     |
| [fasta](https://benchmarksgame-team.pages.debian.net/benchmarksgame/program/fasta-python3-8.html)                   | 259.98 sec     | 19.31                |                     |
| [k-nucleotide](https://benchmarksgame-team.pages.debian.net/benchmarksgame/program/knucleotide-python3-8.html)      | 238.78 sec     | 623.448              |                     |
| [n-body](https://benchmarksgame-team.pages.debian.net/benchmarksgame/program/nbody-python3-8.html)                  | 8 min          | 19.312               |                     |
| [mandelbrot](https://benchmarksgame-team.pages.debian.net/benchmarksgame/program/mandelbrot-python3-3.html)         | 14 min         | 19.312               |                     |
| [fannxkuch-redux](https://benchmarksgame-team.pages.debian.net/benchmarksgame/program/fannkuchredux-python3-8.html) | 37 min         | 19.312               |                     |

NB: The functions on the CLBG were executed on a quad core. Our NUC should be more powerful.

## Subjects (Execution Modes)

| Subject     | Type   | Description | Notes | Build                                                                    |
| -------     | ------ | ----------- | ----- | ------------------------------------------------------------------       | 
| PyPy        | JIT    |             | pypy3 | `pypy --opt=2` No need to set --opt=2, it is the default value           |
| Nuitka      | AOT    |             |       | `python -m nuitka --standalone --python-flag=no_site your_script.py`     |
| Cython      | AOT    |             |       | `-O3` check the output of `build.py`                                     | 
| CPython     | Inter. |             |       |                                                                          |
| Codon       | AOT    |             |       | `codon build -release -exe "$py_file" -o "build/${py_file%.*}"`          |
| mypyc       | AOT    |             |       | `-O3` check the output of `build.py`                                     | 
| Numba       | JIT    |             |       | no flags, just decorator                                                 |
| Pyston-lite | JIT    |             |       | enable upon installation of the JIT compiler (Python 3.10 needed)        |
| Py3.13 JIT  | JIT    |             |       |                                                                          | 


## Experiment CheckList 

This is the checklist that we used to control all the fixed factors of the experiment

- [x] define run_table.csv (function, exec_mode, cpu_usage, execution_time, energy_usage, llc, vms, rss, etc.)
- [x] randomization
- [x] cooling down period of 2 min
- [x] warm up run: prior to the experiment run a function to warm up the machine (e.g., fibonacci.py) for 1m and then cool the machine for 30 seconds.
- [x] save the output of the functions
- [x] add validation of result for each function
- [x] remember to use `taskset -c 0` to bind the execution to 1 core
- [x] compile and test all code 
- [x] check Hyperthreading OFF
- [x] check Turbo boost OFF (Linux Governor Powersave)

## Measurements Tools

We use the [Experiment Runner](https://github.com/S2-group/experiment-runner) framework to automate our experiment.

The metrics we collect are as follows:
- [Perf](https://perfwiki.github.io/main/):
    - LLC Hits - Count, Percentage
    - LLC Misses - Count, Percentage
    - Cache-references - Count, Percentage
    - Cache-misses - Count, Percentage
    - LLC-loads - Count, Percentage
    - LLC-load-misses - Count, Percentage
    - LLC-stores - Count, Percentage
    - LLC-store-misses - Count, Percentage

- [Energibridge](https://github.com/andrei-calin-dragomir/EnergiBridge.git):
    - Per CPU core:
        - Frequency - MHz
        - Temperature - Celsius
        - Usage - Percentage
    - Per Process:
        - CPU Usage - Percentage
        - Used Memory - Bytes
        - Used Swap Memory - Bytes
    - Energy Consumption
        - Package - Joules
        - PP0 - Joules
        - PP1 - Joules
        - DRAM - Joules
    - Execution Time - ms

## Installation

### Orchestration Machine
```bash
git clone --recursive {repository_link}
cd ./{repository_name}
poetry install --with orchestration
```

Create a `.env` file containing:
```python
# Ip of the experimental machine
HOSTNAME='127.0.0.1'
# Username of account on experimental machine
USERNAME='username'
# Password of account on experimental machine
PASSWORD='1234abcd'
```

### Experimental Machine
```bash
git clone --recursive {repository_link}
cd ./{repository_name}
poetry install --with experiment

# Builds Energibridge and sets up compiler dependencies
sudo ./setup_experimental_machine.sh

# Must do this on every machine reboot
sudo setcap cap_sys_rawio=ep ./EnergiBridge/target/release/energibridge
```

## Execution

```bash
poetry shell

# Control Group
python ./experiment-runner/experiment-runner/ RunnerConfig_execution.py

# Experimental Group
python ./experiment-runner/experiment-runner/ # TODO
```

## Data Analysis

