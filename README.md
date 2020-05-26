# annotate.py

`annotate.py` contains two functions that you call from the python console.


Set up for a single image:

### annotate_img(img_path, initials, size1, size2)
 * #### Inputs
    * img_path - name and location of the image, example "B.jpg"
    * size1 - size of the 1st brush circle, in px
    * size2 - size of the 2nd brush circle, in px
    * initials - First name and last name initials of the person doing the labelling. Recorded next to every PMT feature ID line in the text file.
 * #### Outputs
    * {image_name}.png - A map of all the features in binary - features labelled in blue are recorded as RGB (1,1,1), and features in red are recorded as RGB (2,2,2).
    * {image_name}.txt - A text file. Each line contains a PMT feature ID and its pixel coordinates on the image. The text file has the same name as the image.



-----------------------  
Set up for directory of images with file structure for image segmentation. This function calls `annotate_img()` for every image in the specified directory, and then saves the output texts and masks in separate folders.

### annotate_dir(img_dir, initials, size1, size)
 * #### Inputs
    * img_dir - image directory. Images are contained inside this folder.
    * initials - First name and last name initials of the person doing the labelling. Recorded next to every PMT feature ID line in the text file.
    * size1 - size of the 1st brush circle, in px.
    * size2 - size of the 2nd brush circle, in px.
 * #### Outputs (for every image in {img_dir})
    * {image_name}.png - A map of all the features in binary - features labelled in blue are recorded as RGB (1,1,1), and features in red are recorded as RGB (2,2,2).
    * {image_name}.txt - A text file. Each line contains a PMT feature ID and its pixel coordinates on the image. The text file has the same name as the image.
 * #### Folder Structure
    * {img_dir}
        - Source images are stored here.
    * {img_dir}_texts
        - Output text files are stored here.
    * {img_dir}_masks
        - Output mask files are stored here. 


-----------------------

### User keypresses (make sure the image window is selected):
* click on image to grab pixel coordinates
* s to close image and exit program
* r to write coordinates to file (you will be prompted for the PMT feature ID)
* f to select new PMT
* Left-click to label with red, middle-click to label with blue.




