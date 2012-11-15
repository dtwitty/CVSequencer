import cv2
import numpy as np
from scipy import ndimage

def threshold(img, level, inv = True):
    # creates a thresholded image from a color image
    c = cv2.THRESH_BINARY_INV
    if inv:
        c =  cv2.THRESH_BINARY
    #convert to binary
    bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    bl = cv2.blur(bw, (9,9))
    (un, mask) = cv2.threshold(bl, level, 255, c)
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    # Remove small white regions
    close_img = cv2.morphologyEx(mask,cv2.MORPH_CLOSE, element)
    # Remove small black holes
    open_img = cv2.morphologyEx(close_img,cv2.MORPH_OPEN, element)
    return open_img

def get_points(img):
    # given a binary image, will return a list of mass centers
    lab = ndimage.measurements.label(img)
    l =  ndimage.measurements.center_of_mass(img, lab[0], range(1,lab[1] + 1))
    if type(l) != type([]):
        l = [l]
    # convert to ints
    r = [tuple([int(b) for b in a]) for a in l]

    return r

def get_grid_cell(img, pt):
    # given a point and an image, assigns a grid cell
    h = img.shape[0]
    w = img.shape[1]
    dx = int(w / 8.0)
    dy = int(h / 8.0)
    y = pt[0]
    x = pt[1]
    return(y / dy, x / dx)

def read_frame(src, level, threshold, inv = True):
    # returns a dict of rows
    if inv:
        mask = threshold(src, level, False)
    else:
        mask = threshold(src, level)
    rows = {i:[] for i in range(8)}
    pts = get_points(mask)
    for p in pts:
        (i,j) = get_grid_cell(src, p)
        rows[i].append(j)
    return rows
