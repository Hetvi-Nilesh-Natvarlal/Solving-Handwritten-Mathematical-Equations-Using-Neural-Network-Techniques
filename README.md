# Solving Handwritten Mathematical Equations Using Neural Network Techniques

Using Convolutional Neural Network to create a robust handwritten equation solver in image processing. The aim is to develop a system that recognizes and solves handwritten mathematical equations. The system must be able to find solutions for normal equations, linear system equations, quadratic equations, cubic equations, and differential equations. The system returns the roots as the results of the equation.

The system is implemented and simulated using PyQt5 (GUI).

Environment Install and activate the environment using conda

conda env create -f environment.yaml

conda activate tf

Datasets

The symbol recognition model is trained using the Kaggle handwritten symbol dataset https://www.kaggle.com/datasets/xainano/handwrittenmathsymbols.

Add a folder called "Data" in the base directory. Inside this folder add '+', '-', 'times', '=', 'X', 'Y' and 0-9 folders. You may need to use expand.py to augment certain datasets.

Run solver_data.py to create the training dataset.

To train model

Run solver_training.py to train the model.

To run PyQt5 application

Start the application.

python main.py
