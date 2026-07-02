import os
import sys

print("Starting v0.4 Falsification Lab...")
print("==================================\n")

lab_script = os.path.join(os.path.dirname(__file__), 'falsification_lab.py')

# Run via current python interpreter
result = os.system(f"{sys.executable} \"{lab_script}\"")

if result == 0:
    print("\nAll tasks completed successfully.")
else:
    print(f"\nLab execution failed with exit code {result}.")
