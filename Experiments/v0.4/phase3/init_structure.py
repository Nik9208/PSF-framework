import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dirs = [
    "registry",
    "physiology/raw",
    "physiology/processed",
    "climate/raw",
    "climate/processed",
    "economics/raw",
    "economics/processed",
    "synthesis"
]

for d in dirs:
    os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

# Move registry file
old_registry = os.path.join(BASE_DIR, "dataset_registry.md")
new_registry = os.path.join(BASE_DIR, "registry", "dataset_registry.md")
if os.path.exists(old_registry):
    shutil.move(old_registry, new_registry)

# Move setup script
old_setup = os.path.join(BASE_DIR, "setup_environment.py")
new_setup = os.path.join(BASE_DIR, "registry", "setup_environment.py")
if os.path.exists(old_setup):
    shutil.move(old_setup, new_setup)
    
print("Directory structure updated.")
