# now package it all into a function

import numpy as np
from skimage.feature import peak_local_max

def peak_local_max_3d(image3d,min_distance):

    """Find peaks in an 3D image as intensity array.
    Peaks are the local maxima in a region of `2 * min_distance + 1`
    (i.e. peaks are separated by at least `min_distance`).
    If there are multiple local maxima with identical pixel intensities
    inside the region defined with `min_distance`,
    the coordinates of all such pixels are returned.

    ----------
    image : ndarray
        Input image.
    min_distance : int
        Minimum number of pixels separating peaks in a region of `2 *
        min_distance + 1` (i.e. peaks are separated by at least
        `min_distance`).
        To find the maximum number of peaks, use `min_distance=1`.

    Returns
    -------
    output : ndarray
        * If `indices = True`  : [[x1,y1,z1],[x2,y2,z2],...] coordinates of peaks.

    Notes
    -----
    The function relies on applying scikit image's 2D peak_local_max function
    to generate a candidate list of 3D maxima which then get elliminated in a
    subsequent step to fulfill the min_distance criterion.


    """



    ######### setup
    # make an array of zeros
    accumulator = np.zeros(image3d.shape)

    # accumulator for the coordinates and the coordinate intensities
    coordinateAccumulator = []

    ######### 2D
    # find all maxima in every 2D slice of the image
    for iz in range(0,image3d.shape[0]):

        coordinates=peak_local_max(image3d[iz],min_distance=min_distance)

        #write the max values into the accumulator at the right positions
        for coord in coordinates:
            coordValue = image3d[iz][coord[0],coord[1]]
            accumulator[iz,coord[0],coord[1]] = coordValue
            coordinateAccumulator.append([np.array([iz,coord[0],coord[1]]),coordValue])
    #return coordinateAccumulator
    #print(coordinateAccumulator)
    ######### 3D
    # Elliminate all that are too close together


    for maxCandidate in coordinateAccumulator:
        maxCandidate_z = maxCandidate[0][0]
        maxCandidate_x = maxCandidate[0][1]
        maxCandidate_y = maxCandidate[0][2]

        maxCandidate_value = maxCandidate[1]
        windowSizeHalf = int(min_distance/2)

        from_x = max(0,maxCandidate_x-windowSizeHalf)
        to_x = min(image3d.shape[1],maxCandidate_x+windowSizeHalf)

        from_y = max(0,maxCandidate_y-windowSizeHalf)
        to_y = min(image3d.shape[2],maxCandidate_y+windowSizeHalf)

        from_z = max(0,maxCandidate_z-windowSizeHalf)
        to_z = min(image3d.shape[0],maxCandidate_z+windowSizeHalf)
        # print('x')
        # print(from_x)
        # print(to_x)
        # print('y')
        # print(from_y)
        # print(to_y)
        # print('z')
        # print(from_z)
        # print(to_z)

        temp = np.amax(accumulator[from_z:to_z,from_x:to_x,from_y:to_y])
        # print(temp)

        if(maxCandidate_value < temp):
            #print("test")
            accumulator[maxCandidate_z,maxCandidate_x,maxCandidate_y] = 0

    ########## output
    #
    result = np.transpose(np.nonzero(accumulator))
    return(result)




# # now package it all into a function

# import numpy as np
# from skimage.feature import peak_local_max

# def peak_local_max_3d(image3d,min_distance):

#     """Find peaks in an 3D image as intensity array.
#     Peaks are the local maxima in a region of `2 * min_distance + 1`
#     (i.e. peaks are separated by at least `min_distance`).
#     If there are multiple local maxima with identical pixel intensities
#     inside the region defined with `min_distance`,
#     the coordinates of all such pixels are returned.

#     ----------
#     image : ndarray
#         Input image.
#     min_distance : int
#         Minimum number of pixels separating peaks in a region of `2 *
#         min_distance + 1` (i.e. peaks are separated by at least
#         `min_distance`).
#         To find the maximum number of peaks, use `min_distance=1`.

#     Returns
#     -------
#     output : ndarray
#         * If `indices = True`  : [[x1,y1,z1],[x2,y2,z2],...] coordinates of peaks.

#     Notes
#     -----
#     The function relies on applying scikit image's 2D peak_local_max function
#     to generate a candidate list of 3D maxima which then get elliminated in a
#     subsequent step to fulfill the min_distance criterion.


#     """



#     ######### setup
#     # make an array of zeros
#     accumulator = np.zeros(image3d.shape)

#     # accumulator for the coordinates and the coordinate intensities
#     coordinateAccumulator = []

#     ######### 2D
#     # find all maxima in every 2D slice of the image
#     for iz in range(0,image3d.shape[2]):

#         coordinates=peak_local_max(image3d[iz],min_distance=min_distance)

#         #write the max values into the accumulator at the right positions
#         for coord in coordinates:
#             coordValue = image3d[iz][coord[0],coord[1]]
#             accumulator[iz,coord[0],coord[1]] = coordValue
#             coordinateAccumulator.append([np.array([iz,coord[0],coord[1]]),coordValue])

#     ######### 3D
#     # Elliminate all that are too close together


#     for maxCandidate in coordinateAccumulator:
#         maxCandidate_z = maxCandidate[0][0]
#         maxCandidate_x = maxCandidate[0][1]
#         maxCandidate_y = maxCandidate[0][2]

#         maxCandidate_value = maxCandidate[1]
#         windowSizeHalf = int(min_distance/2)

#         from_x = max(0,maxCandidate_x-windowSizeHalf)
#         to_x = min(image3d.shape[0],maxCandidate_x+windowSizeHalf)

#         from_y = max(0,maxCandidate_y-windowSizeHalf)
#         to_y = min(image3d.shape[1],maxCandidate_y+windowSizeHalf)

#         from_z = max(0,maxCandidate_z-windowSizeHalf)
#         to_z = min(image3d.shape[2],maxCandidate_z+windowSizeHalf)

#         if(maxCandidate_value < np.amax(accumulator[from_z:to_z,from_x:to_x,from_y:to_y])):
#             #print("test")
#             accumulator[maxCandidate_z,maxCandidate_x,maxCandidate_y] = 0

#     ########## output
#     #
#     result = np.transpose(np.nonzero(accumulator))
#     return(result)
