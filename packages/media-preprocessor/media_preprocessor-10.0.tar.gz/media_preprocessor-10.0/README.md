Overview:
The objective of this package, as the name suggest, is to act as a media pre-processing tool. It simplifies the process of importing media to the python environment.
It takes input from the user in the form of images or video capture and lets the user define certain parameters, pertaining to which the function gives the output. The package primarily consists of two functions:
1.	img_pre()
2.	nbg_vc()
Functions:
1.	img_pre(location, shape, edges)

This function takes input from the user in the form of images and performs pre-processing operations on it like reshape, resize (1:1 ratio) and standardize. It also gives the users an option to remove the background from the images and retain only the edges of the subject of the image. 

Parameters:
•	location (string)
input folder path of where the images are stored

•	shape (integer)
input desired shape of image

•	edges (boolean)
False: original pictures after pre-processing
True: output images have edges of the subject without the background
2.	nbg_vc(shape)
It allows the user to capture video using their webcam and removes the background by only capturing objects that move in the frame.

Parameters: 
shape (integer): defines shape of the desired output image. 

