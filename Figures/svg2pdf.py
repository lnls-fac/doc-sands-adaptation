#!/usr/bin/env python3

'''
Python script to compile all the figures in the 'Figures' folder into PDFs 
if they are newer than the 'sands-adaptation.pdf' file. This is used to ensure 
that all figures are up-to-date when compiling the main document and that users
don't need to manually convert them. 
'''

import os, time

# Sands PDF file path and existence check
sands_base_path = os.path.join(os.getcwd(), 'sands-adaptation.pdf')
sands_exists = os.path.exists(sands_base_path)

# In case make clean was used, ensure that all the figures are converted
if sands_exists:
    sands_modification_date = os.path.getmtime(sands_base_path)
else:
    sands_modification_date = 0

# Finding all SVG files in the 'Figures' folder
figures_base_path = os.path.dirname(os.path.realpath(__file__))
figures_to_convert = []

for (root, dirs, files) in os.walk(figures_base_path):
    for file in files:
        if file.endswith('.svg'):

            fig_path = os.path.join(root, file)
            fig_modification_date = os.path.getmtime(fig_path)

            # Triggers for new figure conversion:
            if (fig_modification_date > sands_modification_date):
                figures_to_convert.append(fig_path)

# Convert the SVG files to PDFs if needed
if len(figures_to_convert) == 0:
    print("No figures need to be converted. Skipping...")
else:
    print(f"Converting {len(figures_to_convert)} SVGs to PDFs...")

    for fig_path in figures_to_convert:
        try:
            os.system(f"inkscape {fig_path} --export-type=pdf --export-filename={os.path.join(root, file.replace('.svg', '.pdf'))} >/dev/null 2>&1")
        except Exception as e:
            print(f"\n Error converting {fig_path}: {e}")
    print("Done. Procceeding with document compilation...")