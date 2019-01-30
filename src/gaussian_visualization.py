# By Joh Schoeneberg, 2019
import numpy as np

def visualize_3D_gaussians(image_raw,gaussians):
    '''
    This function takes a raw image from which gaussians have been segmented
    and fitted. And the list of the gaussians to draw them into a new 3D array
    that can then be visualized or outputted as a tiff.
    '''

    image_gaussians = np.zeros(image_raw.shape)
    for gaussian in gaussians:

        if(gaussian!=-1):
            amplitude = 100*gaussian[0]

            #print(gaussian)
            mu_x     = int(gaussian[1][0])
            mu_y     = int(gaussian[1][1])
            mu_z     = int(gaussian[1][2])
            sigma_x  = int(gaussian[2][0])
            sigma_y  = int(gaussian[2][1])
            sigma_z  = int(gaussian[2][2])



            n_neighbors_x = int(3 * sigma_x ) + 1
            n_neighbors_y = int(3 * sigma_y ) + 1
            n_neighbors_z = int(3 * sigma_z ) + 1

            for kx in range(max(0, mu_x - n_neighbors_x), min(image_gaussians.shape[0], mu_x + n_neighbors_x)):
                for ky in range(max(0, mu_y - n_neighbors_y), min(image_gaussians.shape[1], mu_y + n_neighbors_y)):
                    for kz in range(max(0, mu_z - n_neighbors_z), min(image_gaussians.shape[2], mu_z + n_neighbors_z)):
            #                for ky in range(max(0, iy - n_neighbors), min(ngrid, iy + n_neighbors)):
                        d2 = (kx-mu_x)**2 + (ky-mu_y)**2+ (kz-mu_z)**2
                        if((2*sigma_x*sigma_y*sigma_z)!=0):
                            #value = amplitude*np.exp(-d2 / (2*sigma_x*sigma_y*sigma_z))
                            value = amplitude*np.exp(-(  (kx-mu_x)**2/2*sigma_x  + (ky-mu_y)**2/2*sigma_y + (kz-mu_z)**2/2*sigma_z))
                        image_gaussians[kx, ky, kz] += value
    return image_gaussians
