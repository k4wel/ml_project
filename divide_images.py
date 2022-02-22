import cv2  
import os
from pathlib import Path 

def split_file(img_path, out_folder):
    p = Path(img_path)
    out = Path(out_folder)

    # load image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    ##########################################
    # At first vertical devide image         #
    ##########################################
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    left1 = img[:, :width_cutoff]
    right1 = img[:, width_cutoff:]
    # finish vertical devide image

    ##########################################
    # At first Horizontal devide left1 image #
    ##########################################
    #rotate image LEFT1 to 90 CLOCKWISE
    img = cv2.rotate(left1, cv2.ROTATE_90_CLOCKWISE)
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    l2 = img[:, :width_cutoff]
    l1 = img[:, width_cutoff:]
    # finish vertical devide image
    #rotate image to 90 COUNTERCLOCKWISE
    l2 = cv2.rotate(l2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(f"{out}/{p.stem}_2{p.suffix}", l2)
    #rotate image to 90 COUNTERCLOCKWISE
    l1 = cv2.rotate(l1, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(f"{out}/{p.stem}_1{p.suffix}", l1)

    ##########################################
    # At first Horizontal devide right1 image#
    ##########################################
    #rotate image RIGHT1 to 90 CLOCKWISE
    img = cv2.rotate(right1, cv2.ROTATE_90_CLOCKWISE)
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    r4 = img[:, :width_cutoff]
    r3 = img[:, width_cutoff:]
    # finish vertical devide image
    #rotate image to 90 COUNTERCLOCKWISE
    r4 = cv2.rotate(r4, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(f"{out}/{p.stem}_4{p.suffix}", r4)
    #rotate image to 90 COUNTERCLOCKWISE
    r3 = cv2.rotate(r3, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(f"{out}/{p.stem}_3{p.suffix}", r3)


img_dir="BOSSbase_1.01"
out_dir="bossbase_1.01_divided"

img_dir = os.path.abspath(img_dir)
out_dir = os.path.abspath(out_dir)

if not os.path.exists(out_dir):
    os.mkdir(out_dir)
   
for filename in os.listdir(img_dir):
    f = os.path.join(img_dir, filename)
    
    if os.path.isfile(f):
        split_file(f, out_dir)
