annotate.py has two functions:

annotate_img(img_path, size1, size2)
    takes a path to an image (png is best) and two brush sizes for drawing a label on an image, calling the function opens the image to be drawn on with a mouse, and inputs taken are:
    
    size1 -> left mouse
    size2 -> middle mouse
    save image -> s
    
    This will save a 2D array as a png in the same directory as annotate.py code. It is currently set up to make a binary array (background=0, label=1). In order to make the label visible set line 61 to 255, (mask[mask != 0 ] = 255).
    
annotate_img('B.JPG',10,20,"MS")
annotate_dir('images','1','test',5,10,"MS","filename")


annotate_dir(img_dir, dataset, subset, size1, size2, initials, filename)
    Takes a directory of images as input, requiring a specific directory structure that I use but shouldnt be too hard to alter if needed:
    image_dirdataset -> subset_frames -> subset (images taken from here)
                         -> subset_masks -> subset  (labels saved here)
    
    Inputs are:
    
    size1 -> left mouse
    size2 -> middle mouse
    save image -> s
    skip and delete image -> a
    
the draw_circle function can be edited to change mouse bindings if necessary.
In order to make the label visible set line 111 to 255.

For IDBottomSurvey images I use size1:   (150 for whole pmt, 7 bolt, 35 dynode ), size2: (50 for whole, 5 bolt, 10 dynode)



Michael Sekatchev - Updated:

- Worked on annotate_img function (will work on extending modifications to the annotate_dir function).
- The function now creates a text file. Each line contains a PMT feature ID and its pixel coordinates on the image. The text file has the same name as the image.

Instructions:
User keypresses (make sure the image window is selected):
        click on image to grab pixel coordinates
        s to close image and exit program
        r to write coordinates to file (you will be prompted for the PMT feature ID)

sample function call using "B.jpg":
annotate_img('B.JPG',10,20)


New Update:
- Worked on annotate_dir function
- The function now also creates a text file. 

Sample function call:
annotate_dir('images','1','test',5,10,"MS","filename")

