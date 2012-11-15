import sys
import cv2
import numpy as np
from utils import threshold, get_points, get_grid_cell
import os
import curses

def gen_grid(img):
    h = img.shape[0]
    w = img.shape[1]
    dx = int(w / 8.0)
    dy = int(h / 8.0)
    rectangles = []
    for i in xrange(8):
        for j in xrange(8):
            rectangles.append(((dx*i, dy*j), ((i+1)*dx, (j+1)*dy), (i, j)))
    return rectangles

def draw_grid(img, rectangles):
    for r in rectangles:
        pt1 = r[0]
        pt2 = r[1]
        cv2.rectangle(img, pt1, pt2, (255,0,255,0))
    

def nope( yep):
    pass

def print_dic(dic):
    for i in range(8):
        l = dic[i]
        p = [" " for k in range(8)]
        for j in l:
            p[j] = "O"
        stdscr.addstr(i,0, '|'.join(p))

if __name__ == '__main__':
    # start the capture
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    cv2.createTrackbar("level", "test", 150, 255, nope)
    cv2.createTrackbar("inv", "test", 0, 1, nope)
    while(1):
        (un,src) = cap.read()
        rects = gen_grid(src)
        r = cv2.getTrackbarPos("level","test")

        if cv2.getTrackbarPos("inv", "test") == 1:
            mask = threshold(src, r, False)
        else:
            mask = threshold(src, r)
        points = get_points(mask)
        rows = {i:[] for i in range(8)}
        for p in points:
            (i,j) = get_grid_cell(src, p)
            cv2.circle(mask, (p[1],p[0]), 10, (100,100,100,200))
            cv2.circle(mask, (p[1],p[0]), 5, (100,100,100,200))    
            rows[i].append(j)
        print_dic(rows)
        stdscr.refresh()
        draw_grid(mask,rects)
        cv2.imshow("test", mask)
        cv2.waitKey(1)
