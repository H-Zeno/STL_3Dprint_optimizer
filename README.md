# STL Optimizer for 3D Printing

## Project Overview

The aim of this project is to enhance the precision and quality of (large) 3D-printed parts for industrial usage. 
This is done by optimizing STL (Stereolithography) files by compensating for material shrinkage (rescaling) and transforming the STL model in real-time based on a 3D model of the actual print, reconstructed from camera images.
By addressing material shrinkage and model inaccuracies, the project ensures that the final print closely aligns with the original design specifications.

Before printing, the user can upload their STL model to the GUI and specify in which material they would like to print it. The software will automatically rescale the STL file to compensate for expected shrinkage factors per material.
After the automatic rescaling, the user can apply additional transformations to the STL model before printing (rescale, translate, rotate).

![](https://github.com/H-Zeno/STL_3Dprint_optimizer/blob/main/STLPrintAdjusterGUI.png)


To further increase the accuracy of the prints, a code skeleton was formed for a perception pipeline which:
1) Construct a 3D model (mesh) from camera images (using either photogrammetry (SfM), Nerfs or Gaussian splatting)
2) Compare the STL file for printing with the 3D reconstruction and calculate an error metric
3) Optimise the error with an optimal control algorithm over the model transform parameters


## Project Structure

The codebase consists of three Python files and one YAML configuration file:

1. `STL_edit.py`: Handles the reading, writing, and transformation of STL files, including rescaling, translating, and rotating operations.
2. `STLPrintAdjusterGUI.py`: A graphical user interface that allows users to select an STL file and its printing material, then automatically adjusts the file based on predefined shrinkage factors.
3. `real-time_STL_model_optimisation.py`: Optimizes STL files in real-time by comparing them with a 3D reconstruction of the actual print, obtained from camera images. (in progress)
4. `material_scale_factors.yaml`: Contains the scale factors for different materials to compensate for shrinkage.

## Getting Started

### Prerequisites

- Python 3.x
- NumPy
- Tkinter
- PyYAML

### Setup

1. Clone the repository or download the source files.
2. Install the required dependencies:

```bash
pip install numpy pyyaml
