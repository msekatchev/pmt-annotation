(working on proper readme in Markdown format)
`annotate.py` contains two functions that you call from the python console.
Set up for a single image
#function: annotate_img
    inputs
        img_path - name and location of the image, example "B.jpg"
        size1 - size of the 1st brush circle, in px
        size2 - size of the 2nd brush circle, in px
        initials - First name and last name initials of the person doing the labelling. Recorded next to every PMT feature ID line in the text file.
    outputs
        label.jpg - A map of all the features in binary (white on black)
        {image_name}.txt - A text file. Each line contains a PMT feature ID and its pixel coordinates on the image. The text file has the same name as the image.

    User keypresses (make sure the image window is selected):
        click on image to grab pixel coordinates
        s to close image and exit program
        r to write coordinates to file (you will be prompted for the PMT feature ID)
        f to select new PMT
        Left-click to label with red, middle-click to label with blue.


Set up for directory of images with file structure for image segmentation
Function: annotate_dir
   input:
       img_dir & dataset - working directory. (directory named {img_dir}{dataset}).
       subset - Preffix for the two folders inside img_dir where images are located and labels are saved. Folders are subset_frames and subset_masks.
       size1 - size of the 1st brush circle, in px.
       size2 - size of the 2nd brush circle, in px.
       initials - First name and last name initials of the person doing the labelling. Recorded next to every PMT feature ID line in the text file.
       filename - The name of the .txt file that will be created.
Set up for directory of images with file structure for image segmentation



