import os
import json
import numpy as np
from shapely.geometry import Polygon

def read_json(json_fp):
    polys = []
    if os.path.exists(json_fp):
        with open(json_fp, 'r') as f:
            jsondata = json.load(f)
            for l in jsondata['shapes']:
                polys.append(l['points']) # [(x, y), (x, y), ]
                # x, y = np.array(l['points']).T
                # poly = Polygon(np.array([x, y]).T)
                # polys.append(np.array(poly.exterior.xy).T)
                # print(np.array(poly.exterior.xy).T.shape)
                # print("=========")
    return polys

def read_txt(txt_fp, w, h):
    with open(txt_fp, 'r') as f:
        boxes = []
        clses = []
        for line in f:
            c, bx, by, bw, bh = line.strip().split()
            c, bx, by, bw, bh = (int(c), *[float(i) for i in [bx, by, bw, bh]])
            xmin, xmax, ymin, ymax = (bx-bw/2)*w, (bx+bw/2)*w, (by-bh/2)*h, (by+bh/2)*h
            boxes.append([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])
            clses.append(c)
        return clses, np.array(boxes)