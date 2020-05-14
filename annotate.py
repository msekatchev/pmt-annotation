import cv2
import os
import numpy as np
import shutil

#Set up callbacks for drawing circles on click and drag, bound to left and middle mouse 
def draw_circle(event,x,y,flags,param):
    if(inputting==False):
        global mouseX,mouseY
        global ix, iy, drawing, rdrawing, mode
        global count
        
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix,iy = x,y
            cv2.circle(img, (x, y), large_size,(255,0,0),-1)
            print(ix, "x  ", iy,"y")
          
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False


        if event == cv2.EVENT_MBUTTONDOWN:
            rdrawing = True
            ix,iy = x,y
            cv2.circle(img, (x, y), small_size,(255,0,0),-1)
            print(ix, "x  ", iy,"y")

        elif event == cv2.EVENT_MBUTTONUP:
            rdrawing = False
       





                


        
##Set up for a single image
##function: annotate_img
    ##inputs
        ##img_path - name and location of the image, example "B.jpg"
        ##size1 - size of the 1st brush circle, in px
        ##size2 - size of the 2nd brush circle, in px
        ##initials - First name and last name initials of the person doing the labelling. Recorded next to every PMT feature ID line in the text file.
    ##outputs
        ##label.jpg - A map of all the features in binary (white on black)
        ##{image_name}.txt - A text file. Each line contains a PMT feature ID and its pixel coordinates on the image. The text file has the same name as the image.

    ##User keypresses (make sure the image window is selected):
        ## click on image to grab pixel coordinates
        ## s to close image and exit program
        ## r to write coordinates to file (you will be prompted for the PMT feature ID)
def annotate_img(img_path, size1, size2, initials) :
    print("image path is: ",img_path)
    global count
    global inputting
    inputting = False
    global pmtSelected
    pmtSelected = False
    global nextPMT
    nextPMT = False
    count = 0
    global coords
    coords = [[], []]
    #Create window and put it in top left corner of screen
    cv2.namedWindow('image',cv2.WINDOW_GUI_EXPANDED) # Added cv2.WINDOW_NORMAL flag to allow to resize window.
    #cv2.moveWindow('image', 40, 30) ##40 and 30 are x and y coordinates on the screen
    cv2.moveWindow('image', 0, 0)
    global drawing, rdrawing, large_size, small_size, img
    large_size=size1
    small_size=size2
    
    img = cv2.imread(img_path) ##read the image specified in the input
    cv2.setMouseCallback('image',draw_circle) ##Link mouse position and button states to the draw_circle function.

    #Extract the name of the image from the inputted path to the image.
    base = os.path.basename(img_path)
    filename = os.path.splitext(base)[0]
    file = open("%s.txt" %filename,"w")
    print("Saving to: ",filename,".txt")

    #Drawing callbacks
    drawing=False
    rdrawing=False

    print("\n Click on image to grab pixel coordinates.\n Press s to close image and exit program.\n Press r to write coordinates to file. \n    (you will be prompted for the PMT feature ID)")
    
    while(1):
        cv2.imshow('image',img)     ##keep displaying the image even if the user exits.
        k = cv2.waitKey(20) & 0xFF
        if(k == ord('s')):          ##if the s key is pressed, exit the loop.
            #cv2.destroyWindow('image')
            break

        
###############################Add line to text output###############################
        if(k==ord('f')):
           nextPMT = True
           pmtSelected = False
           print("Ended recording for PMT ",pmtID, ". Record first feature for another by selecting a point and pressing r.")

        elif(k==ord('x')):
           print("Skipping feature #", startingVal)
           startingVal = startingVal+1

        if(k==ord('r')):
            if(pmtSelected == True):
                print("Recording ", pmtID, "-",startingVal, " ",ix, "x  ", iy,"y\n")
                if(startingVal<10 or startingVal == 0):
                    file.write("%s\t%s-0%d\t%d\t%d\t%s\n" %(filename,pmtID,startingVal, ix, iy,initials))
                else:
                    file.write("%s\t%s-%d\t%d\t%d\t%s\n" %(filename,pmtID,startingVal, ix, iy,initials))
                startingVal = startingVal+1   
            else:
                inputting = True ##used to pause the draw_circle function from recording more coordinates
                pmtID = input("Input PMT number to add it to the list, or input 'd' to not register:\n")
                if(pmtID != 'd'):
                    startingFeature = input("Input starting feature number, or press enter to start from 0.\n")
                    if(not startingFeature):
                        startingVal = 0
                    else:
                        startingVal = int(startingFeature)
                        
                    print("Recording ", pmtID, "-",startingVal, " ",ix, "x  ", iy,"y\n")
                    print("Record another selected point by pressing r.\nPress x to skip recording a number.\nPress f to finish recording features for this PMT.")
                    if(startingVal<10 or startingVal == 0):
                        file.write("%s\t%s-0%d\t%d\t%d\t%s\n" %(filename,pmtID,startingVal, ix, iy,initials))
                    else:
                        file.write("%s\t%s-%d\t%d\t%d\t%s\n" %(filename,pmtID,startingVal, ix, iy,initials))
                    startingVal = startingVal+1
                    coords[0].append(ix)
                    coords[1].append(iy)
                    pmtSelected = True
                    nextPMT = True
                print("\n")
                inputting = False
###############################Add line to text output###############################

            
    file.close
###############################Image Output##########################################
    #Make mask same colour as drawing and output binarised image
    train_labels = img[:,:,:3]
    # print("TRAIN LABELS = ")
    #print(train_labels)
    lower = np.array([254,0,0], dtype = "uint16")
    upper = np.array([255,0,0], dtype = "uint16")
    mask = cv2.inRange(train_labels, lower, upper)
    mask[mask < 250] = 0
    mask[mask != 0 ] = 255 ##set =1 for binary or =255 for visible white
    maskName = os.path.join(filename+'.png')
    print("MASKNAME: ",maskName)
    #save label in code directory
    cv2.imwrite(maskName, mask )
    #cv2.imwrite(f'{str(maskName)}',mask)
    #print("SAVED")
    #cv2.imwrite(maskName, mask )
    #print(mask)
###############################Image Output##########################################

    cv2.destroyWindow('image')

    np.savetxt("array.txt", coords, fmt="%s")
    return
            











#Set up for directory of images with file structure for image segmentation
#Function: annotate_dir
#   input:
#       img_dir & dataset - working directory. (directory named {img_dir}{dataset}).
#       subset - Preffix for the two folders inside img_dir where images are located and labels are saved. Folders are subset_frames and subset_masks.
#       size1 - size of the 1st brush circle, in px.
#       size2 - size of the 2nd brush circle, in px.
#       initials - First name and last name initials of the person doing the labelling. Recorded next to every PMT feature ID line in the text file.
#       filename - The name of the .txt file that will be created.
#Set up for directory of images with file structure for image segmentation
def annotate_dir(img_dir, size1, size2,initials) :
    #Create window and put it in top left corner off screen

 
####### Creating text and mask save directories #######
    text_save_path = os.path.join(img_dir+"_texts")
    mask_save_path = os.path.join(img_dir+"_masks")    
    if not os.path.exists(text_save_path):
        os.mkdir(text_save_path)
    if not os.path.exists(mask_save_path):
        os.mkdir(mask_save_path)
    #save_path = os.path.join(img_dir+"_texts",filename+".txt")

    #file = open("%s" %save_path,"w")

    print("Saving texts to: ",text_save_path)
    print("Saving masks to: ",mask_save_path)

    #Array of names in directory to iterate over
    f = []
    for (dirpath, dirnames, filenames) in os.walk(f'{img_dir}'):
        f.extend(filenames)
        break
    
    print(f)
    
    for i in f :
        skip = False

        #img = cv2.imread(f'{img_dir}/{str(i)}')
        print("IMG=",i)
        base = os.path.basename(i)
        imageName = os.path.splitext(base)[0]
        imageLocation = os.path.join(img_dir,i)

        annotate_img(imageLocation,size1,size2,initials)


        textName = os.path.join(imageName+".txt")
        maskName = os.path.join(imageName+".png")
        print("------- Moving ",textName, "to ", text_save_path)
        #sleep(500)
        shutil.move(textName,text_save_path)
        shutil.move(maskName,mask_save_path)

        #Drawing and keyboard callbacks a to skip and delete, s to save image
        
         
###############################Add line to text output###############################
            
###############################Add line to text output###############################
    
###############################Image Output##########################################
      
###############################Image Output##########################################
    #file.close
    #cv2.destroyWindow('image')

















































#Set up for directory of images with file structure for image segmentation
#Function: annotate_dir
#   input:
#       img_dir & dataset - working directory. (directory named {img_dir}{dataset}).
#       subset - Preffix for the two folders inside img_dir where images are located and labels are saved. Folders are subset_frames and subset_masks.
#       size1 - size of the 1st brush circle, in px.
#       size2 - size of the 2nd brush circle, in px.
#       initials - First name and last name initials of the person doing the labelling. Recorded next to every PMT feature ID line in the text file.
#       filename - The name of the .txt file that will be created.
#Set up for directory of images with file structure for image segmentation
def annotate_dir_old(img_dir, size1, size2,initials,filename) :
    #Create window and put it in top left corner off screen
    global inputting
    global count
    count = 0
    inputting = False
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.moveWindow('image', 40, 30)
    global drawing, rdrawing, large_size, small_size, img
    large_size=size1
    small_size=size2

    global coords
    coords = [[], []]

    text_save_path = os.path.join(img_dir+"_texts")
    mask_save_path = os.path.join(img_dir+"_masks")    
    if not os.path.exists(text_save_path):
        os.mkdir(text_save_path)
    if not os.path.exists(mask_save_path):
        os.mkdir(mask_save_path)
    save_path = os.path.join(img_dir+"_texts",filename+".txt")

    file = open("%s" %save_path,"w")

    print("Saving to: ",save_path)


    cv2.setMouseCallback('image',draw_circle)
    #Array of names in directory to iterate over
    f = []
    for (dirpath, dirnames, filenames) in os.walk(f'{img_dir}'):
        f.extend(filenames)
        break
    
    print(f)
    
    for i in f :
        skip = False
        drawing = False
        rdrawing = False
        img = cv2.imread(f'{img_dir}/{str(i)}')
        
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
###############################Add line to text output###############################
            if k == ord('r'):
                inputting = True
                print("Recording: Pixels: ", ix, "x  ", iy,"y")
                imageName = os.path.splitext(i)[0]
                pmtID = input("Input PMT feature ID to add it to the list, or input 'd' to not register:\n")
                print("\n")
                if(pmtID!='d'):
                    file.write("%s\t%s\t%d\t%d\t%s\n" %(imageName,pmtID, ix, iy,initials))
                    coords[0].append(ix)
                    coords[1].append(iy)
                    count = count+1
                inputting = False
###############################Add line to text output###############################
    
###############################Image Output##########################################
        #Make mask same colour as drawing and output binarised image
        train_labels = img[:,:,:3]
        lower = np.array([254,0,0], dtype = "uint16")
        upper = np.array([255,0,0], dtype = "uint16")
        mask = cv2.inRange(train_labels, lower, upper)
        mask[mask < 250] = 0
        mask[mask != 0 ] = 255
        #Save mask or delete image if it isnt good
        if skip == False :
            cv2.imwrite(f'{img_dir}_masks/{str(i)}', mask )
        else :
            os.remove(f'{img_dir}_masks/{str(i)}')
###############################Image Output##########################################
    file.close
    cv2.destroyWindow('image')

