import os
import sys

print("Starting v0.4 Phase 2A: Geometry Representation Study...")
print("========================================================\n")

lab_script = os.path.join(os.path.dirname(__file__), 'embedding_lab.py')

# Run via current python interpreter
result = os.system(f"{sys.executable} \"{lab_script}\"")

if result == 0:
    print("\nPhase 2A execution completed successfully.")
else:
    print(f"\nPhase 2A execution failed with exit code {result}.")
