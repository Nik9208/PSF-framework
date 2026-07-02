# ICCS v0.4 Falsification Laboratory

This directory contains the frozen execution lab for identifying operational boundaries of ICCS v0.3.1.

## Structure
- `signal_generators.py`: Pure signal generation (no ICCS logic).
- `run_iccs.py`: Wrapper for ICCS invocation.
- `falsification_lab.py`: Lab protocol execution (generation, calculation, aggregation).
- `run_all.py`: Entry point for all lab experiments.
- `expectations.yaml`: Documented expected behavior prior to testing.
- `results/`: Output artifacts (tables, figures, raw JSON dumps).

## Execution
Run `python run_all.py` to execute the full falsification laboratory. This will generate 9 different types of signals (running 30 independent realizations for stochastic ones) and analyze them using the frozen ICCS v0.3.1 library. Results are outputted to the `results/` directory.
