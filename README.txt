annotate.py has two functions:

annotate_img(img_path, size1, size2)
    takes a path to an image (png is best) and two brush sizes for drawing a label on an image, calling the function opens the image to be drawn on with a mouse, and inputs taken are:
    
    size1 -> left mouse
    size2 -> middle mouse
    save image -> s
    
    This will save a 2D array as a png in the same directory as annotate.py code. It is currently set up to make a binary array (background=0, label=1). In order to make the label visible set line 61 to 255, (mask[mask != 0 ] = 255).
    
annotate_dir(img_dir, dataset, subset, size1, size2)
    Takes a directory of images as input, requiring a specific directory structure that I use but shouldnt be too hard to alter if needed:
    image_dir -> dataset -> subset_frames -> subset (images taken from here)
                         -> subset_masks -> subset  (labels saved here)
    
    Inputs are:
    
    size1 -> left mouse
    size2 -> middle mouse
    save image -> s
    skip and delete image -> a
    
the draw_circle function can be edited to change mouse bindings if necessary.
In order to make the label visible set line 111 to 255.

For IDBottomSurvey images I use size1:   (150 for whole pmt, 7 bolt, 35 dynode ), size2: (50 for whole, 5 bolt, 10 dynode)
