# Solving Handwritten Mathematical Equations Using Neural Network Techniques

The utilization of Convolutional Neural Networks (CNNs) in image processing has opened up new avenues for developing a powerful handwritten equation solver. The primary objective of this endeavor is to create a robust system capable of accurately recognizing and solving mathematical equations written by hand. The system's prowess extends beyond simply deciphering regular equations; it must also possess the capability to tackle more complex mathematical problems such as linear system equations, quadratic equations, cubic equations, and even differential equations. Ultimately, the system should furnish the roots of the equations as the final results.

To bring this vision to life, the system is implemented and simulated using PyQt5, a versatile and user-friendly graphical user interface (GUI) framework. PyQt5 provides an intuitive platform for developing the visual components of the equation solver, enabling users to interact seamlessly with the system. This integration of CNN-based equation recognition and the PyQt5 GUI empowers users to input handwritten equations effortlessly and witness the system's adeptness in swiftly interpreting and solving them.

By combining the power of Convolutional Neural Networks with the user-friendly interface offered by PyQt5, the handwritten equation solver sets the stage for an efficient and intuitive mathematical problem-solving experience. It bridges the gap between the traditional pen-and-paper approach and the digital realm, empowering users to effortlessly convert their handwritten equations into tangible solutions.


## Environment
Install and activate the environment using conda

`conda env create -f environment.yaml`

`conda activate tf`

## Dataset
The symbol recognition model is trained using the Kaggle handwritten symbol dataset https://www.kaggle.com/datasets/xainano/handwrittenmathsymbols.

Add a folder called "Data" in the base directory. Inside this folder add '+', '-', 'times', '=', 'X', 'Y' and 0-9 folders. You may need to use `expand.py` to augment certain datasets.

Run `solver_data.py` to create the training dataset.

## Training
Run `solver_training.py` to train the model.

## Run PyQt5 application
Start the application.
In the Anaconda Prompt enter `python main.py`

## Results
![RESULT1](https://github.com/Hetvi-Nilesh-Natvarlal/Solving-Handwritten-Mathematical-Equations-Using-Neural-Network-Techniques/assets/82942652/f92c88a5-9f89-4d4a-a660-c3694826851a)
![RESULT2](https://github.com/Hetvi-Nilesh-Natvarlal/Solving-Handwritten-Mathematical-Equations-Using-Neural-Network-Techniques/assets/82942652/0f06b68b-5caa-4690-a450-ddf35ab27850)
![RESULT3](https://github.com/Hetvi-Nilesh-Natvarlal/Solving-Handwritten-Mathematical-Equations-Using-Neural-Network-Techniques/assets/82942652/12e8f721-8586-4e9c-a2e3-d6439b3e1031)
![RESULT4](https://github.com/Hetvi-Nilesh-Natvarlal/Solving-Handwritten-Mathematical-Equations-Using-Neural-Network-Techniques/assets/82942652/cceb17a1-bde3-42e7-8d64-b04204622522)
![RESULT5](https://github.com/Hetvi-Nilesh-Natvarlal/Solving-Handwritten-Mathematical-Equations-Using-Neural-Network-Techniques/assets/82942652/5d4f876d-c4a5-4a4a-9e9a-0deec92f10dc)
![RESULT6](https://github.com/Hetvi-Nilesh-Natvarlal/Solving-Handwritten-Mathematical-Equations-Using-Neural-Network-Techniques/assets/82942652/f360dab2-639b-4307-adbe-2aeccc09c92d)
