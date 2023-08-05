Overview: PixelP (PixelProcessor) is an image augmentation and preprocessing package.This tool has 3 functions idg,create_gray_data and create_color_data

1.idg():Augments new images
	Arguements : Data_path - Path to source folder
		      CATEGORIES - Name of folders inside parent source folder
		      Data_out - Path to output folder
		      rotrange - Rotation range varying from 0-360
		      wshift - Width shift 0-1
		      hshift - Height shift 0-1
		      srange - Shear Range 0-1
		      zoom - Zoom Range 0.1
		      hflip - horizontal flip TRUE or FALSE
		      fill - Fill Mode 'wrap','nearest','constant','reflect'

2. create_gray_data():Turns image to grayscale and reshapes to user defined size
	Arguements : IMG_SIZE - no. of pixels (pixel x pixel)
		     training_data - empty list []
		     Data_train - Path to images
		     CATEGORIES - Name of folders inside parent source folder

3. create_color_data():reshapes to user defined size
	Arguements : IMG_SIZE - no. of pixels (pixel x pixel)
		     training_data - empty list []
		     Data_train - Path to images
		     CATEGORIES - Name of folders inside parent source folder