from skimage.feature import peak_local_max
from skimage.measure import label
from scipy.ndimage import distance_transform_edt

from scipy.optimize import curve_fit
import numpy as np

def gaussian_1d_output(x,a,x0,sigma):

    temp = a*np.exp(-(x-x0)**2/(2*sigma**2))

    return temp

def fit_gaussian(image, center, sigmas, width_parameters):

    try:
        x_center = center[1]
        y_center = center[2]
        z_center = center[0]

        peak =image[z_center,x_center,y_center]

        x_sigma = sigmas[1]
        y_sigma = sigmas[2]
        z_sigma = sigmas[0]

        from_x = max(0,x_center-x_sigma)
        to_x = min(image.shape[1],x_center+x_sigma)

        from_y = max(0,y_center-y_sigma)
        to_y = min(image.shape[2],y_center+y_sigma)

        from_z = max(0,z_center-z_sigma)
        to_z = min(image.shape[0],z_center+z_sigma)

        # x_range = np.arange(x_center - x_sigma, x_center + x_sigma + 1)
        # y_range = np.arange(y_center - y_sigma, y_center + y_sigma + 1)
        # z_range = np.arange(z_center - z_sigma, z_center + z_sigma + 1)
        x_range = np.arange(from_x,to_x)
        y_range = np.arange(from_y,to_y)
        z_range = np.arange(from_z,to_z)

        # x_data = np.array(image[x_center - x_sigma:x_center + x_sigma + 1, y_center, z_center])
        # y_data = np.array(image[x_center, y_center - y_sigma:y_center + y_sigma + 1, z_center])
        # z_data = np.array(image[x_center, y_center, z_center - z_sigma:z_center + z_sigma + 1])

        #stopped working in a middle-level iteration
        # x_data = np.array(image[z_center,from_x:to_x+1,y_center])
        # y_data = np.array(image[z_center,x_center,from_y:to_y+1])
        # z_data = np.array(image[from_z:to_z+1,x_center,y_center])

        x_data = np.array(image[z_center,x_range,y_center])
        y_data = np.array(image[z_center,x_center,y_range])
        z_data = np.array(image[z_range,x_center,y_center])

        # print('x')
        # print(x_range)
        # print(x_data)
        x_popt, x_pcov = curve_fit(gaussian_1d_output, x_range, x_data, bounds = ([peak-width_parameters,x_center-width_parameters,-np.inf],[peak+width_parameters,x_center+width_parameters,np.inf]))
        y_popt, y_pcov = curve_fit(gaussian_1d_output, y_range, y_data, bounds = ([peak-width_parameters,y_center-width_parameters,-np.inf],[peak+width_parameters,y_center+width_parameters,np.inf]))
        z_popt, z_pcov = curve_fit(gaussian_1d_output, z_range, z_data, bounds = ([peak-width_parameters,z_center-width_parameters,-np.inf],[peak+width_parameters,z_center+width_parameters,np.inf]))

    #     print('the optimal gaussian parameters (Amp, mu, sigma) for x:')
    #     print(x_popt)
    #     plt.plot(x_range, x_data, 'b-', label='data')
    #     plt.plot(x_range, gaussian_1d_output(x_range, *x_popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(x_popt))
    #     plt.xlabel("x_range")
    #     plt.ylabel("raw_data")
    #     plt.title('raw data in x dimension and gaussian fit')
    #     plt.show()


    #     print('the optimal gaussian parameters (Amp, mu, sigma) for y:')
    #     print(y_popt)
    #     plt.plot(y_range, y_data, 'b-', label='data')
    #     plt.plot(y_range, gaussian_1d_output(y_range, *y_popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(y_popt))
    #     plt.xlabel("y_range")
    #     plt.ylabel("raw_data")
    #     plt.title('raw data in y dimension and gaussian fit')
    #     plt.show()


    #     print('the optimal gaussian parameters (Amp, mu, sigma) for z:')
    #     print(z_popt)
    #     plt.plot(z_range, z_data, 'b-', label='data')
    #     plt.plot(z_range, gaussian_1d_output(z_range, *z_popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(z_popt))
    #     plt.xlabel("z_range")
    #     plt.ylabel("raw_data")
    #     plt.title('raw data in z dimension and gaussian fit')
    #     plt.show()

        optimal_parameters_each_dimension = []
        optimal_parameters_each_dimension.append(z_popt)
        optimal_parameters_each_dimension.append(x_popt)
        optimal_parameters_each_dimension.append(y_popt)

        optimal_parameter_one_gaussian = []
        mean_amplitude = np.mean([x_popt[0],y_popt[0],z_popt[0]])
        center = [z_popt[1],x_popt[1],y_popt[1]]
        sigmas = [z_popt[2],x_popt[2],y_popt[2]]
        optimal_parameter_one_gaussian.append(mean_amplitude)
        optimal_parameter_one_gaussian.append(center)
        optimal_parameter_one_gaussian.append(sigmas)

        return optimal_parameter_one_gaussian, optimal_parameters_each_dimension

    except:
        #print('gaussian parameters could not be optimized')
        return -1, -1


def fit_multiple_gaussians(image,centers,sigmas,width_parameters):

    net_gaussians = []
    individual_gaussians = []
    i = 0

    roundedPercent = 0
    for i in range(0,len(centers)):
        # joh: have some kind of progress bar
        if roundedPercent != int(10*i/len(centers)):
            roundedPercent = int(10*i/len(centers))
            print("{}%({} of {})".format(10*roundedPercent,i,len(centers)))

        #print('iteration: ' + str(i))
        one_gaussian, each_dimension_gaussians = fit_gaussian(image, centers[i], sigmas[i], width_parameters)

        net_gaussians.append(one_gaussian)

        individual_gaussians.append(each_dimension_gaussians)
        i += 1
        
    print("{}%({} of {})".format(100,len(centers),len(centers)))
    return net_gaussians, individual_gaussians



def check_fitting_error(image,maximas,net_gaussians,sigmas_guesses):

    absolute_errors = []

    for i in range(len(maximas)):
        temp_gaussian = net_gaussians[i]
        if temp_gaussian != -1:

            temp_absolute_error = []

            #print('temp gaussian')
            #print(temp_gaussian)
            temp_maxima = maximas[i]
            temp_sigmas = sigmas_guesses[i]
            #print('mean_absolute_error_amplitude')
            mean_absolute_error_amplitude = np.abs(temp_gaussian[0] - image[temp_maxima[0],temp_maxima[1],temp_maxima[2]])
            #print(mean_absolute_error_amplitude)
            mean_absolute_error_mean = [np.abs(temp_maxima[0]-temp_gaussian[1][0]),np.abs(temp_maxima[1]-temp_gaussian[1][1]),np.abs(temp_maxima[2]-temp_gaussian[1][2])]
            mean_absolute_error_sigmas = [np.abs(temp_sigmas[0]-temp_gaussian[2][0]),np.abs(temp_sigmas[1]-temp_gaussian[2][1]),np.abs(temp_sigmas[2]-temp_gaussian[2][2])]

            temp_absolute_error.append(mean_absolute_error_amplitude)
            temp_absolute_error.append(mean_absolute_error_mean)
            temp_absolute_error.append(mean_absolute_error_sigmas)

            absolute_errors.append(temp_absolute_error)
        else:
            print('the gaussian did not fit')

    return absolute_errors
