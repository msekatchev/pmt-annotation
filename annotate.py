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

        #if event == cv2.EVENT_LBUTTONDOWN:
        #    drawing = True
        #    ix,iy = x,y
        #    cv2.circle(img, (x, y), large_size,(0,0,255),-1)
        #    print(ix, "x  ", iy,"y")
        #  
        #elif event == cv2.EVENT_LBUTTONUP:
        #    drawing = False
 

        if event == cv2.EVENT_MBUTTONDOWN:
            rdrawing = True
            ix,iy = x,y
            cv2.circle(img, (x, y), small_size,(0,0,255),-1)
            print(ix, "x", iy,"y")

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
def annotate_img(img_path, initials, size1=1, size2=1) :
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
    coords = [[],[]]

    #Extract the name of the image from the inputted path to the image.
    base = os.path.basename(img_path)
    filename = os.path.splitext(base)[0]
    file = open("%s.txt" %filename,"w")
    print("Saving to: ",filename+".txt")

    #Create window and put it in top left corner of screen
    cv2.namedWindow(filename,cv2.WINDOW_GUI_EXPANDED) ####################### Added cv2.WINDOW_NORMAL flag to allow to resize window.
    ##cv2.moveWindow(filename, 40, 30) ##40 and 30 are x and y coordinates on the screen
    cv2.moveWindow(filename, 0, 0)
    global drawing, rdrawing, large_size, small_size, img
    large_size=size1
    small_size=size2
    
    img = cv2.imread(img_path) ##read the image specified in the input
    cv2.setMouseCallback(filename,draw_circle) ##Link mouse position and button states to the draw_circle function.

    #Drawing callbacks
    drawing=False
    rdrawing=False

    print("\n Click on image to grab pixel coordinates.\n Press s to close image and exit program.\n Press r to write coordinates to file. \n    (you will be prompted for the PMT feature ID)")



    while(1):
        cv2.imshow(filename,img)     ##keep displaying the image even if the user exits.
        k = cv2.waitKey(20) & 0xFF
        if(k == ord('s')):          ##if the s key is pressed, exit the loop.
            print("Saving to: ",filename+".txt\n")
            for i in range(len(coords[0])):
                if(coords[0][i]!="N"):
                    writestartingVal = f'{i:02}'

                    print(filename+"\t"+writepmtID+"-"+writestartingVal+"\t"+str(coords[0][i])+"\t"+str(coords[1][i])+"\t"+initials+"\n")
                    file.write("%s\t%s-%s\t%s\t%s\t%s\n" %(filename,writepmtID,writestartingVal, str(coords[0][i]), str(coords[1][i]),initials))
                    coords[0][i]="N"
                    coords[1][i]="N"  
            break

        
###############################Add line to text output###############################
        if(k==ord('f')):
           nextPMT = True
           pmtSelected = False
           print("Saving to: ",filename+".txt\n")
           
           
           for i in range(len(coords[0])):
                if(coords[0][i]!="N"):
                    writestartingVal = f'{i:02}' 
                    print(filename+"\t"+writepmtID+"-"+writestartingVal+"\t"+str(coords[0][i])+"\t"+str(coords[1][i])+"\t"+initials+"\n")
                    file.write("%s\t%s-%s\t%s\t%s\t%s\n" %(filename,writepmtID,writestartingVal, str(coords[0][i]), str(coords[1][i]),initials))
                    coords[0][i]="N"
                    coords[1][i]="N"  
           print("Ended recording for PMT ",str(pmtID)+". Record first feature for another by selecting a point and pressing r.")
        elif(k==ord('n')):
           startingVal = startingVal+1
           print("Ready to record", startingVal)

        elif(k==ord('b')):
            if(startingVal==0):
                print("Error, can't decrement feature ID below 0.")
            else:
                startingVal = startingVal-1
                print("Ready to record",startingVal)

        if(k==ord('r')):
            if(pmtSelected == True):
                
                #startingVal = startingVal+1
                writestartingVal = f'{startingVal:02}'
                writepmtID = pmtID.zfill(5)   
                print("Recording ", writepmtID+"-"+writestartingVal, ix, "x", iy,"y\n")
                    
                
                
                while(startingVal>=len(coords[0])):
                    coords[0].append("N")
                    coords[1].append("N")

                coords[0][startingVal] = ix
                coords[1][startingVal] = iy
                
                

            else:
                inputting = True ##used to pause the draw_circle function from recording more coordinates
                pmtID = input("Input PMT number to add it to the list, or input 'd' to not register:\n-->")
                if(pmtID != 'd'):
                    startingFeature = input("Input starting feature number, or press enter to start from 0.\n-->")
                    if(not startingFeature):
                        startingVal = 0
                    else:
                        startingVal = int(startingFeature)
                      
                    writepmtID = pmtID.zfill(5)
                    writestartingVal = f'{startingVal:02}'   
                    print("Recording ", writepmtID+"-"+writestartingVal, ix, "x", iy,"y\n")
                    print("Record another selected point by pressing r.\nPress x to skip recording a number.\nPress f to finish recording features for this PMT.")
                    
                    while(startingVal>=len(coords[0])):
                        coords[0].append("N")
                        coords[1].append("N")

                    coords[0][startingVal] = ix
                    coords[1][startingVal] = iy

                    
                    
                    #startingVal = startingVal+1

                    pmtSelected = True
                    nextPMT = True
                print("\n")
                inputting = False
###############################Add line to text output###############################

    #print(coords)
    file.close   

###############################Image Output##########################################
    #Make mask same colour as drawing and output binarised image
    train_labels = img[:,:,:3]
    # print("TRAIN LABELS = ")
    #print(train_labels)
    lower = np.array([0,0,254], dtype = "uint16")
    upper = np.array([0,0,255], dtype = "uint16")
    mask = cv2.inRange(train_labels, lower, upper)
    mask[mask < 250] = 0
    mask[mask != 0 ] = 255 ##set =1 for binary or =255 for visible white
    maskName = os.path.join(filename+'.png')
    print("MASKNAME: ",maskName)
    #save label in code directory
    cv2.imwrite(maskName, mask )
    #print(mask)
###############################Image Output##########################################

    cv2.destroyWindow(filename)

#    np.savetxt("array.txt", coords, fmt="%s") #for later implementing feature to save to array.
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
def annotate_dir(img_dir, initials, size1=1, size2=1) :
    #Create window and put it in top left corner off screen

 
####### Creating text and mask save directories #######
    text_save_path = os.path.join(img_dir+"_texts")
    if not os.path.exists(text_save_path):
        os.mkdir(text_save_path)

    mask_save_path = os.path.join(img_dir+"_masks")    
    if not os.path.exists(mask_save_path):
        os.mkdir(mask_save_path)

    print("Saving texts to: ",text_save_path)
    print("Saving masks to: ",mask_save_path)

    #Array of names in directory to iterate over
    f = []
    for (dirpath, dirnames, filenames) in os.walk(f'{img_dir}'):
        f.extend(filenames)
        break
    
    print("Found: ",f,"\n\n")
    
    for i in f :
        skip = False

        base = os.path.basename(i)
        imageName = os.path.splitext(base)[0]
        imageLocation = os.path.join(img_dir,i)

        annotate_img(imageLocation, initials, size1, size2)


        textName = os.path.join(imageName+".txt")
        maskName = os.path.join(imageName+".png")


        saveText=True
        if(os.path.exists(os.path.join(text_save_path,textName))):
            print("File", textName, "already exists in", text_save_path+". Would you like to overwrite it?")            
            overwriteText = input("(y/n)\n-->")
            if(overwriteText.lower() == "y"):
                saveText = True
                os.remove(os.path.join(text_save_path,textName))
            else:
                saveText = False

        if(saveText == True):
            print("Moving",textName, "to", text_save_path)        
            shutil.move(textName,text_save_path)
        else:
            os.remove(textName)
            print("Removed new", textName)


        print("\n")


        saveMask=True
        if(os.path.exists(os.path.join(mask_save_path,maskName))):
            print("File", maskName, "already exists in", mask_save_path+". Would you like to overwrite it?")
            overwriteMask = input("(y/n)\n-->")
            if(overwriteMask.lower() == "y"):
                saveMask=True
                os.remove(os.path.join(mask_save_path,maskName))
            else:
                saveMask=False
        
        
        if(saveMask == True):
            print("Moving",maskName, "to", mask_save_path)
            shutil.move(maskName,mask_save_path)
        else:
            os.remove(maskName)
            print("Removed new", maskName)

        #Drawing and keyboard callbacks a to skip and delete, s to save image
        
         
###############################Add line to text output###############################
            
###############################Add line to text output###############################
    
###############################Image Output##########################################
      
###############################Image Output##########################################
    #file.close
    #cv2.destroyWindow('image')
