"""Refresh audited inputs and reproduce both supplementary analyses."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
packages = ROOT / 'supplementary'
first = packages / 'additional_data_analysis'
second = packages / 'likbez_1924_analysis'
shutil.copyfile(ROOT/'data/census1939_literacy_by_region_age_sex.csv', first/'inputs/census1939_literacy_by_region_age_sex.csv')
shutil.copyfile(ROOT/'results/W2_cells.csv', second/'inputs/W2_cells.csv')
for package, scripts in [(first, ['analyze_new_data.py', 'verify_1939_values.py', 'estimate_post1939.py', 'make_plot.py']),
                         (second, ['analyze_1924.py', 'estimate_1924.py', 'plot_1924.py'])]:
    for script in scripts:
        print(f'Running {package.name}/{script}', flush=True)
        subprocess.run([sys.executable, str(package/'scripts'/script)], cwd=ROOT, check=True)
subprocess.run([sys.executable, str(ROOT/'scripts/write_supplementary_numbers.py')], cwd=ROOT, check=True)
