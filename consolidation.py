from __future__ import print_function
import os
import numpy as np
import cv2 as cv
import time

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

cap = cv.VideoCapture(0)
cap2 = cv.VideoCapture(2)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
cap2.set(3,640) # set Width
cap2.set(4,480) # set Height

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')

while(True):
    if __name__ == '__main__':
        print('loading images...')
        bool1, image1 = cap.read()
        bool2, image2 = cap2.read()
        cv.imwrite('opencvL'+'.jpg', image1)
        cv.imwrite('opencvR'+'.jpg', image2)
        imgL = cv.imread('opencvL.jpg')  # downscale images for faster processing
        imgR = cv.imread('opencvR.jpg')

        # disparity range is tuned for 'aloe' image pair
        window_size = 7
        min_disp = 0
        max_disp = 160
        num_disp = 112-min_disp
        stereo = cv.StereoSGBM_create(minDisparity = min_disp,
            numDisparities = num_disp,
            blockSize = 5,
            P1 = 8*3*window_size**2,
            P2 = 32*3*window_size**2,
            disp12MaxDiff = 1,
            uniquenessRatio = 15,
            speckleWindowSize = 50,
            speckleRange = 2
            preFilterCap=63
        )

        print('computing disparity...')
        disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

        print('generating 3d point cloud...',)
        h, w = imgL.shape[:2]
        f = 0.8*w                          # guess for focal length
        Q = np.float32([[1, 0, 0, -0.5*w],
                        [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                        [0, 0, 0,     -f], # so that y-axis looks up
                        [0, 0, 1,      0]])
        points = cv.reprojectImageTo3D(disp, Q)
        colors = cv.cvtColor(imgL, cv.COLOR_BGR2RGB)
        mask = disp > disp.min()
        out_points = points[mask]
        out_colors = colors[mask]
        out_fn = 'out.ply'
        write_ply('out.ply', out_points, out_colors)
        print('%s saved' % 'out.ply')
        cv.imshow('left', imgL)
        cv.imshow('right', imgR)
        cv.imshow('disparity', (disp-min_disp)/num_disp)
        os.remove("opencvL.jpg")
        os.remove("out.ply")
        os.remove("opencvR.jpg")

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(1)
    else:
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
