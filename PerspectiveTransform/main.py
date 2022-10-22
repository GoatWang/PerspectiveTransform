import cv2
import numpy as np 

pts_image = [[0, 720], [471, 369], [803, 369], [1280, 720]]
pts_world = [[0, 0], [0, 200], [10, 200], [10, 0]]
def get_transform(pts_image=pts_image, pts_world=pts_world):
    """
    pts_image: default [[0, 720], [471, 369], [803, 369], [1280, 720]]
    pts_world: default [[0, 0], [0, 200], [10, 200], [10, 0]], that is 
               [[0, 0], [0, transform_size[0]], [transform_size[1], transform_size[0]], [transform_size[1], 0]]
               if transform_size = (200, 10) # row, col
    please arange pts through the order.
    - world: 
        1---2
        |   |
        0---3
    - image
        1--------2
           0--3
         \      /
          \    /

    the inner logic: https://theailearner.com/tag/cv2-getperspectivetransform/
    """
    pts_image = np.array(pts_image, dtype=np.float32)
    pts_world = np.array(pts_world, dtype=np.float32)
    M = cv2.getPerspectiveTransform(pts_image, pts_world) 
    return M


def transform_pts(pts, M):
    """
    pts: should be in shape (-1, 2)
    """
    pts = np.array(pts).reshape(-1, 1, 2).astype(np.float32)
    pts_trans = cv2.perspectiveTransform(pts, M)[:, 0, :]
    return pts_trans


def transform_polys(polys, M):
    """
    polys: should be in shape [(-1, 2), (-1, 2), ...]
    """
    n_pts_in_polys = [len(p) for p in polys]
    pts = np.concatenate(polys, axis=0)
    pts_trans = transform_pts(pts, M)
    polys_trans =[]
    cursor = 0
    for n_pts in n_pts_in_polys:
        cursor_end = cursor + n_pts
        polys_trans.append(pts_trans[cursor: cursor_end])
        cursor = cursor_end
    return polys_trans


if __name__ == '__main__':
    import os
    import cv2
    import numpy as np
    from pathlib import Path
    from matplotlib import pyplot as plt
    from Utils import read_json, read_txt
    from matplotlib.patches import Polygon

    img_fp = "Data/0000000167.png"
    txt_fp = "Data/0000000167.txt"
    json_fp = "Data/0000000167.json"
    img_size = (720, 1280) # row, col

    X = cv2.imread(img_fp)
    lake_polys = read_json(json_fp)
    clses, boxes = read_txt(txt_fp, img_size[1], img_size[0])
    person_boxes = np.array([b for c, b in zip(clses, boxes) if c==0])
    person_pts = np.mean(person_boxes[:, 1:3], axis=1)

    transform_size = (200, 10)    
    pts_image = [[0, 720], [471, 369], [803, 369], [1280, 720]]
    pts_world = [[0, 0], [0, transform_size[0]], [transform_size[1], transform_size[0]], [transform_size[1], 0]]
    M = get_transform(pts_image, pts_world)
    person_pts_trans = transform_pts(person_pts, M)
    lake_polys_trans = transform_polys(lake_polys, M)


    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 15))

    ax1.imshow(X[:, :, ::-1])
    ax1.add_patch(Polygon(pts_image, edgecolor='blue', linewidth=2, fill=False))
    for poly in lake_polys:
        ax1.add_patch(Polygon(poly, edgecolor='red', linewidth=2, fill=False))
    ax1.scatter(person_pts[:, 0], person_pts[:, 1], s=50, color='green')

    ax2.add_patch(Polygon(pts_world, edgecolor='blue', linewidth=2, fill=False))
    for poly in lake_polys_trans:
        ax2.add_patch(Polygon(poly, edgecolor='red', linewidth=2, fill=False))
    ax2.scatter(person_pts_trans[:, 0], person_pts_trans[:, 1], s=50, color='green')
        
    # plt.show()
    Path('temp').mkdir(exist_ok=True, parents=True)
    plt.savefig(os.path.join('temp', "test.png"))
    print("test image save to: " + os.path.join('temp', "test.png"))



    




