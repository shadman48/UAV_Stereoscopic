########################################################################
#
# Copyright (c) 2017, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import pyzed.sl as sl
import cv2
import math
import numpy as np #needed for OpenCV
import sys

#Global Variables
NUMBER_OF_ROWS = 5
NUMBER_OF_COLUMNS = 5
NUMBER_OF_BLOCKS = NUMBER_OF_ROWS * NUMBER_OF_COLUMNS





def main():
# Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_ULTRA  # Can be set to PERFORMANCE, MEDIUM, ULTRA, OR QUALITY
    init_params.coordinate_units = sl.UNIT.UNIT_MILLIMETER  # Use millimeter units (for depth measurements)
    #init_params.depth_minimum_distance = 0.15 # Set the minimum depth perception distance to 15cm


    # Open the camera
    if not zed.is_opened():
   	 print("Opening ZED Camera...")	
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.sensing_mode = sl.SENSING_MODE.SENSING_MODE_STANDARD  # Use STANDARD sensing mode but can also test with FILL

    # Capture 50 images and depth, then stop
    i = 0
    image = sl.Mat()
    depth_map = sl.Mat()
    point_cloud = sl.Mat()
    
    

    key = ''
    while key != 113:  # for 'q' key
        err = zed.grab(runtime_parameters)
        if err == sl.ERROR_CODE.SUCCESS:
            # Retrieve depth map AND DISPLAY IT
            zed.retrieve_image(image, sl.VIEW.VIEW_DEPTH)
            
            #zed.retrieve_image(image, sl.VIEW.VIEW_LEFT)
            cv2.imshow("ZED Live View.", image.get_data())
            key = cv2.waitKey(5)
            # A new image is available if grab() returns SUCCESS
            if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:

                # Retrieve left image
                #zed.retrieve_image(image, sl.VIEW.VIEW_LEFT)
                # Retrieve depth map. Depth is aligned on the left image
                zed.retrieve_measure(depth_map, sl.MEASURE.MEASURE_DEPTH)
                # Retrieve colored point cloud. Point cloud is aligned on the left image.
                zed.retrieve_measure(point_cloud, sl.MEASURE.MEASURE_XYZRGBA)
                
              
                # Get and print distance value in mm at the center of the image
                # We measure the distance camera - object using Euclidean distance
                x = round(image.get_width() / 2)
                y = round(image.get_height() / 2)
                err, point_cloud_value = point_cloud.get_value(x, y)

                distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                                     point_cloud_value[1] * point_cloud_value[1] +
                                     point_cloud_value[2] * point_cloud_value[2])

            if not np.isnan(distance) and not np.isinf(distance):
                distance = round(distance)
                print("Distance to Camera at ({0}, {1}): {2} mm\n".format(x, y, distance))
                print("Resolution: {0}, {1}.".format(round(zed.get_resolution().width, 2), zed.get_resolution().height)) #Use to get resolution
                # Increment the loop
                i = i + 1
            else:
                print("Can't estimate distance at this position, move the camera\n")
                sys.stdout.flush()
        else:
            key = cv2.waitKey(5)
            cv2.destroyAllWindows()
            zed.close()
            print("\nFINISH")



    # Close the camera
   # zed.close()



###########################
#def OverlayGrid():

### Look up
def lookUpTable():




if __name__ == "__main__":
    main()
