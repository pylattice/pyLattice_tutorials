def import_dependencies():
	# package for 3d visualization
	from itkwidgets import view                              
	from aicssegmentation.core.visual import seg_fluo_side_by_side,  single_fluorescent_view, segmentation_quick_view
	import matplotlib.pyplot as plt
	plt.rcParams["figure.figsize"] = [16, 12]

	# package for io 
	from aicsimageio import AICSImage, omeTifWriter                            

	# packages for curve fitting, vector storage
	from scipy.optimize import curve_fit
	import numpy as np

	# packages for gaussian fitting and maximum intensity localization
	from peak_local_max_3d import peak_local_max_3d 
	from gaussian_fitting import gaussian_1d_output, fit_gaussian, fit_multiple_gaussians