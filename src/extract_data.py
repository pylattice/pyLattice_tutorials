def extract_data_from_filename(file_name):
	# package for 3d visualization
	#from itkwidgets import view
	#from aicssegmentation.core.visual import seg_fluo_side_by_side,  single_fluorescent_view, segmentation_quick_view
	import matplotlib.pyplot as plt
	plt.rcParams["figure.figsize"] = [16, 12]

	# package for io
	from aicsimageio import AICSImage #, omeTifWriter


	reader = AICSImage(file_name)
	IMG = reader.data

	# #print(IMG.shape)

	structure_img = IMG[0,0,:,:,:]

	return structure_img
