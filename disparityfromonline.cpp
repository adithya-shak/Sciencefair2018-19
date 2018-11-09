int main(void)
{

   VideoCapture camLeft(0);
   VideoCapture camRight(2);

   camLeft.set(CV_CAP_PROP_FRAME_WIDTH, 500);
   camLeft.set(CV_CAP_PROP_FRAME_HEIGHT, 500);
   camRight.set(CV_CAP_PROP_FRAME_WIDTH, 500);
   camRight.set(CV_CAP_PROP_FRAME_HEIGHT, 500);



   if (!camLeft.isOpened() || !camRight.isOpened()) {
      cout << "Error: Stereo Cameras not found or there is some problem       connecting them. Please check your cameras.\n";
      exit(-1);
     }


//Read intrinsice parameters
string intrinsic_filepath = "C:/Users/Jerry/Documents/Visual Studio 2015/Projects/OctStereoCalibration/OctStereoCalibration/intrinsics.yml";
FileStorage fs(intrinsic_filepath, FileStorage::READ);
if (!fs.isOpened())
{
    printf("Failed to open intrinsics.yml");
    return -1;
}
Mat M1, D1, M2, D2;
fs["M1"] >> M1;
fs["D1"] >> D1;
fs["M2"] >> M2;
fs["D2"] >> D2;

//Read Extrinsic Parameters
string extrinsic_filepath = "C:/Users/Jerry/Documents/Visual Studio 2015/Projects/OctStereoCalibration/OctStereoCalibration/extrinsics.yml";
fs.open(extrinsic_filepath, FileStorage::READ);
if (!fs.isOpened())
{
    printf("Failed to open extrinsics");
    return -1;
}

Mat R, T, R1, P1, R2, P2;
fs["R"] >> R;
fs["T"] >> T;

Mat frame1, frame2, gray1, gray2, copyImageLeft, copyImageRight;
int counter = 0;

camLeft >> frame1;
camRight >> frame2;

Size img_size = frame1.size();
Rect roi1, roi2;
Mat Q;

stereoRectify(M1, D1, M2, D2, img_size, R, T, R1, R2, P1, P2, Q, CALIB_ZERO_DISPARITY, -1, img_size, &roi1, &roi2);

Mat map11, map12, map21, map22;
initUndistortRectifyMap(M1, D1, R1, P1, img_size, CV_16SC2, map11, map12);
initUndistortRectifyMap(M2, D2, R2, P2, img_size, CV_16SC2, map21, map22);



while (1) {
    createTrackbars();
    on_trackbar(0, 0);

    bm->setROI1(roi1);
    bm->setROI2(roi2);
    bm->setPreFilterCap(PreFilterCap);
    bm->setPreFilterSize(PrefilterSize);
    bm->setBlockSize(SADWindowSize);
    bm->setMinDisparity(MinDisparity);  //0
    bm->setNumDisparities(numberOfDisparities);
    bm->setTextureThreshold(TextureThreshold);
    bm->setUniquenessRatio(UniquenessRatio);
    bm->setSpeckleWindowSize(SpeckleWindowSize);
    bm->setSpeckleRange(SpeckleRange);
    bm->setDisp12MaxDiff(Disp12MaxDiff);    //1

    camLeft >> frame1;
    camRight >> frame2;
    if ((frame1.rows != frame2.rows) || (frame1.cols != frame2.cols)) {
        cout << "Error: Images from both cameras are not of some size. Please check the size of each camera.\n";
        exit(-1);
    }
    //frame1.copyTo(copyImageLeft);
    //frame2.copyTo(copyImageRight);
    imshow("Cam1", frame1);
    imshow("Cam2", frame2);

    /************************* STEREO ***********************/

    cvtColor(frame1, gray1, CV_RGB2GRAY);
    cvtColor(frame2, gray2, CV_RGB2GRAY);

    int64 t = getTickCount();

    Mat img1r, img2r;
    remap(gray1, img1r, map11, map12, INTER_LINEAR);
    remap(gray2, img2r, map21, map22, INTER_LINEAR);

    Mat disp, disp8;
    Mat XYZ;
    bm->compute(img1r, img2r, disp);
    t = getTickCount() - t;
    printf("Time elapsed: %fms\n", t * 1000 / getTickFrequency());

    disp.convertTo(disp8, CV_8U, 255 / (numberOfDisparities*16.));
    //normalize(disp, disp8, 0, 255, CV_MINMAX, CV_8U);
    imshow("disparity", disp8);

    //reprojectImageTo3D(disp8, XYZ, Q, false, CV_32F);

    char keyBoardInput = (char)waitKey(50);
    if (keyBoardInput == 'q' || keyBoardInput == 'Q') {
        break;
        return(0);
    }
}
