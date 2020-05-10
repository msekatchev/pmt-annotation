import cv2
import os
import numpy as np


#Set up callbacks for drawing circles on click and drag, bound to left and middle mouse 
def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    global ix, iy, drawing, rdrawing, mode


    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        cv2.circle(img, (x, y), large_size,(255,0,0),-1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
                cv2.circle(img, (x, y), large_size,(255,0,0),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False



    if event == cv2.EVENT_MBUTTONDOWN:
        rdrawing = True
        ix,iy = x,y
        cv2.circle(img, (x, y), small_size,(255,0,0),-1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if rdrawing == True:
                cv2.circle(img, (x, y), small_size,(255,0,0),-1)
    elif event == cv2.EVENT_MBUTTONUP:
        rdrawing = False
    

        
##Set up for a single image
##function: annotate_img
    ##inputs
        ##img_path - name and location of the image, example "B.jpg"
        ##size1 - size of the 1st brush circle, in px
        ##size2 - size of the 2nd brush circle, in px
def annotate_img(img_path, size1, size2) :
    #Create window and put it in top left corner of screen
    cv2.namedWindow('image',cv2.WINDOW_NORMAL) ####################### Added cv2.WINDOW_NORMAL flag to allow to resize window.
    ##cv2.moveWindow('image', 40, 30) ##40 and 30 are x and y coordinates on the screen
    cv2.moveWindow('image', 0, 0)
    global drawing, rdrawing, large_size, small_size, img
    large_size=size1
    small_size=size2
    
    img = cv2.imread(img_path) ##read the image specified in the input
    cv2.setMouseCallback('image',draw_circle) ##Link mouse position and button states to the draw_circle function.
    
    #Drawing and keyboard callbacks a to skip and delete, s to save image
    drawing=False
    rdrawing=False

#    while(1):
#        cv2.imshow('image',img)     ##keep displaying the image even if the user exits.
#        k = cv2.waitKey(20) & 0xFF
#        if k == ord('s'):           ##if the s key is pressed, exit the loop.
#            #cv2.destroyWindow('image')
#            break

    k = cv2.waitKey(20) & 0xFF
    
    while(k!=ord('s')):
        cv2.imshow('image',img)
        k = cv2.waitKey(20) & 0xFF
        
        

    #Make mask same colour as drawing and output binarised image
    train_labels = img[:,:,:3]
    lower = np.array([254,0,0], dtype = "uint16")
    upper = np.array([255,0,0], dtype = "uint16")
    mask = cv2.inRange(train_labels, lower, upper)
    mask[mask < 250] = 0
    mask[mask != 0 ] = 255 ##set =1 for binary or =255 for visible white
    
    #save label in code directory
    cv2.imwrite('label.png', mask )
    cv2.destroyWindow('image')
    return
            











#Set up for directory of images with file structure for image segmentation
#Function: annotate_dir
#   input:
#       img_dir - working directory
#       dataset
#       subset - Preffix for the two folders inside img_dir where images are located and labels are saved. Folders are subset_frames and subset_masks
#       size1 - size of the 1st brush circle, in px
#       size2 - size of the 2nd brush circle, in px
#Set up for directory of images with file structure for image segmentation
def annotate_dir(img_dir, dataset, subset, size1, size2) :
    #Create window and put it in top left corner off screen
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.moveWindow('image', 40, 30)
    global drawing, rdrawing, large_size, small_size, img
    large_size=size1
    small_size=size2

    
    cv2.setMouseCallback('image',draw_circle)
    #Array of names in directory to iterate over
    f = []
    for (dirpath, dirnames, filenames) in os.walk(f'{img_dir}{dataset}/{subset}_frames/{subset}'):
        f.extend(filenames)
        break
    
    print(f)
    
    for i in f :
        skip = False
        drawing = False
        rdrawing = False
        img = cv2.imread(f'{img_dir}{dataset}/{subset}_frames/{subset}/{str(i)}')
        
        #Drawing and keyboard callbacks a to skip and delete, s to save image
        while(1):
            cv2.imshow('image',img)
            k = cv2.waitKey(20) & 0xFF
            if k == ord('s'):
                #cv2.destroyWindow('image')
                break
            elif k == ord('a'):
                skip = True
                #cv2.destroyWindow('image')
                break
        #Make mask same colour as drawing and output binarised image
        train_labels = img[:,:,:3]
        lower = np.array([254,0,0], dtype = "uint16")
        upper = np.array([255,0,0], dtype = "uint16")
        mask = cv2.inRange(train_labels, lower, upper)
        mask[mask < 250] = 0
        mask[mask != 0 ] = 255
        #Save mask or delete image if it isnt good
        if skip == False :
            cv2.imwrite(f'{img_dir}{dataset}/{subset}_masks/{subset}/{str(i)}', mask )
        else :
            os.remove(f'{img_dir}{dataset}/{subset}_frames/{subset}/{str(i)}')
    cv2.destroyWindow('image')
