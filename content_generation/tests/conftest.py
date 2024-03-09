import sys
from pathlib import Path

# Get the absolute path to the root directory of our project
project_root = Path(__file__).resolve().parents[2]

# Add the project root to the Python path
sys.path.insert(0, str(project_root))
