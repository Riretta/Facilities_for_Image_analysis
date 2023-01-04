"""CLassify Images From Folder"""
"""Rita Pucci - Naturalis - 2023"""

import cv2
import os
import shutil

def check_class_value(c, classes):
    check_class = False
    while not check_class:
        if not chr(c).isnumeric():
            if chr(c) == 'q':
                print("Exit....... bye")
                return -1
            print("You digit not a number, please digit the correct class ")
            c = cv2.waitKey(0)
            check_class = False
        else:
            class_ = int(chr(c))
            if class_ > classes-1:
                print(f"You digit a not existent class {class_} the classes are in range [0,{classes-1}].\nPlease digit the correct class ")
                c = cv2.waitKey(0)
                check_class = False
            else:
                check_class = True
    return class_

def main(argv):
    print("### Welcome to HAIF: Human Annotation for Images From Folder ###")
    print("We are going to create an annotated dataset")
    #ask where is the dataset:
    path = input("Digit the path of the dataset: ")
    print(f"I am checking if {path} exists")
    if os.path.exists(path):
        images = [file for file in os.listdir(path) if not os.path.isdir(os.path.join(path, file))]
        print(f"Ok, I found {len(images)} images")
    else:
        print("Path not found, that is the end")
        return -1
    #ask final path
    path_classification = input("Where do you want to save the classified images? "
                                "(write the complete path of the folder) ")
    print(path_classification)
    if not os.path.exists(path_classification):
        print("I am creating the folder ...")
        os.mkdir(path_classification)
        exist = False
    else:
        print("The folder exists, so this is a resumed procedure.")
        classes = os.listdir(path_classification)
        print(f"We have {len(classes)} classes available:: {classes}")
        classes = len(classes)
        exist = True

    if not exist:
        #ask  how many classes user what to identify:
        ordinal = input("Digit how many classes you want to identify in your dataset: ")
        if ordinal.isnumeric(): classes = int(ordinal)
        else:
            print(f"You typed {ordinal} and it is not a number, I accept only numbers.")
            return -1
        print("I create the folder for the classification:")
        for i in range(classes):
            os.mkdir(os.path.join(path_classification,str(i)))
            print(os.path.join(path_classification,str(i)))

    print("\033[1mCopy (cp)\033[0m:: the images are copied and you can resume the classification procedure if interrupted.\n"
          "\033[1mMove (mv)\033[0m:: the images are moved and you can interrupt and resume later on.")
    modality = input("Do you want to copy (type cp) or to move (type mv) the images? ")
    if modality == 'cp': function = shutil.copy
    elif modality == 'mv': function = shutil.move
    else:
        print("Not recongnised modality, I accept only cp or mv ")
        return -1

    print("Ok we are ready, just last question:")
    print("\033[1mDouble check\033[0m:: each image: I am going to ask twice the classification of each image to be sure of the classification;\n"
          "\033[1mSingle check\033[0m:: I will ask you only one time the classification of the image. (The default is single check).")
    check = input("Do you want to double check each image (digit DC), otherwise just press a button ")

    if check == "DC": double_activate = True
    else: double_activate = False
    print("We start the annotation,\nEach image is going to be opened, check the opened windows on you PC.\n"
          "Type the class that you want keeping the image open in foreground, if you want to exit digit:: q ")
    for filename in images:
        image = os.path.join(path,filename)
        img = cv2.imread(image)  # load a dummy image
        cv2.imshow('img', img)
        c = cv2.waitKey(0)
        class_ = check_class_value(c,classes)
        if class_ == -1: return class_
        if double_activate:
            print(f"You asked for double check, the current class is {class_}, do you confirm the class? (y/n)")
            confirm = chr(cv2.waitKey(0))
            if confirm == 'n':
                print("Class not confirmed.\nDigit the new class:")
                c = cv2.waitKey(0)
                class_ = check_class_value(c,classes)
                if class_ == -1: return class_
        folder_MC = os.path.join(path_classification,str(class_))
        function(os.path.join(path,filename),folder_MC)

    print("### We are done, bye thank you for coming. ###")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('data')