def view_raw_data_and_detected_maxima(image,maximas):




	from peak_local_max_3d import peak_local_max_3d 

	import numpy as np
	import pims
	import skimage
	import matplotlib.pyplot as plt
	from mpl_toolkits.mplot3d import Axes3D


	peaks = image >11000
	maxima = maximas
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(np.nonzero(peaks)[0],np.nonzero(peaks)[1],np.nonzero(peaks)[2],alpha = 0.1)
	# plot the max coordinates
	ax.scatter(maxima[:,0],maxima[:,1],maxima[:,2],c='red')
	#ax.view_init(30, 0)