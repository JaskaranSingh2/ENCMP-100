## CORONASIMULATE  Simulate coronagraph and Gerchberg-Saxton algorithm
#
# A simulation of a coronagraph and the Gerchberg-Saxton algorithm, in the
# context of NASA's Roman Space Telescope, developed to help teach ENCMP
# 100 Computer Programming for Engineers at the University of Alberta. The
# program saves output figures to PNG files for subsequent processing.
#
# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: Jaskaran Singh (100%)
# Student CCID: jaskara8
# Others:
#
# To avoid plagiarism, list the names of persons, Version 0 author(s)
# excluded, whose code, words, ideas, or data you used. To avoid
# cheating, list the names of persons, excluding the ENCMP 100 lab
# instructor and TAs, who gave you compositional assistance.
#
# After each name, including your own name, enter in parentheses an
# estimate of the person's contributions in percent. Without these
# numbers, adding to 100%, follow-up questions will be asked.
#
# For anonymous sources, enter pseudonyms in uppercase, e.g., SAURON,
# followed by percentages as above. Email a link to or a copy of the
# source to the lab instructor before the assignment is due.
#
import numpy as np
import matplotlib.pyplot as plt

def main():
    """
    The main function that runs the simulation by initializing the class and invoking each function as required.
    """
    im = loadImage('300_26a_big-vlt-s.jpg')
    im, Dphi, mask = opticalSystem(im, 300)
    images, errors = gerchbergSaxton(im, 10, Dphi, mask)
    saveFrames(images, errors)

def loadImage(name):
    """
    Load the image used by the system, and preprocess it.

    Parameters:
    - name (str): The name of the image file.

    Returns:
    - numpy.ndarray: The preprocessed image.
    """
    # Load the image
    im = plt.imread(name)/255
    
    # Convert to grayscale if necessary
    if len(im.shape) > 2:
        im = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3
    
    # Clip pixel values to the range [0, 1]
    im[im < 0] = 0
    im[im > 1] = 1
    
    return im

def occultCircle(im, diameter):
    """
    Occults a circle region in the given image.

    Parameters:
    - im (numpy.ndarray): The input image.
    - diameter (int): The diameter of the circle region to be occulted.

    Returns:
    - numpy.ndarray: The image with the circle region occulted.
    - numpy.ndarray: The mask indicating the occulted pixels.
    """
    # Define the center of the image
    h, w = im.shape
    center_h = h // 2
    center_w = w // 2

    # Calculate the radius of the circle
    radius = diameter // 2

    # Create a grid of coordinates for the image
    y, x = np.ogrid[:h, :w]

    # Create a mask that identifies the pixels within the circle
    mask = (x - center_w)**2 + (y - center_h)**2 <= radius**2

    # Set the pixels within the circle to 0 (black)
    im[mask] = 0

    # Return the modified image and the mask
    return im, mask

def opticalSystem(im, diameter):
    """
    Apply occultation to the image, compute the 2D discrete Fourier transform of the image,
    generate random phase for the inverse transform, and perform inverse transform with phase correction.

    Parameters:
    - im (numpy.ndarray): The input image.
    - diameter (int): The diameter of the circle region to be occulted.

    Returns:
    - numpy.ndarray: The modified image.
    - numpy.ndarray: The random phase for the inverse transform.
    - numpy.ndarray: The mask indicating the occulted pixels.
    """
    # Apply occultation to the image
    im, mask = occultCircle(im, diameter)
    
    # Compute the 2D discrete Fourier transform of the image
    (IMa, IMp) = dft2(im)
    
    # Generate random phase for the inverse transform
    rng = np.random.default_rng(12345)
    imR = rng.random(im.shape)
    (_, Dphi) = dft2(imR)
    
    # Perform inverse transform with phase correction
    im = idft2(IMa, IMp - Dphi)
    
    return im, Dphi, mask

def dft2(im):
    """
    Compute the 2D discrete Fourier transform of a grayscale image.

    Parameters:
    - im (numpy.ndarray): The input image.

    Returns:
    - tuple: A tuple containing the magnitude and phase of the Fourier transform.
    """
    IM = np.fft.rfft2(im)
    IMa = np.abs(IM)
    IMp = np.angle(IM)
    return (IMa, IMp)

def idft2(IMa, IMp):
    """
    Compute the inverse 2D discrete Fourier transform.

    Parameters:
    - IMa (numpy.ndarray): The magnitude of the Fourier transform.
    - IMp (numpy.ndarray): The phase of the Fourier transform.

    Returns:
    - numpy.ndarray: The inverse Fourier transformed image.
    """
    IM = IMa * (np.cos(IMp) + 1j * np.sin(IMp))
    im = np.fft.irfft2(IM)
    
    # Clip pixel values to the range [0, 1]
    im[im < 0] = 0
    im[im > 1] = 1
    
    return im

def occultError(im, mask):
    """
    Compute the occultation error of the image.

    Parameters:
    - im (numpy.ndarray): The input image.
    - mask (numpy.ndarray): The mask indicating the occulted pixels.

    Returns:
    - float: The occultation error.
    """
    error = np.sum(im[mask]**2)
    return error

def gerchbergSaxton(im, maxIters, Dphi, mask):
    """
    Perform the Gerchberg-Saxton algorithm.

    This function takes an input image, performs the Gerchberg-Saxton algorithm for a specified number of iterations,
    and returns a list of generated images and a list of errors for each iteration.

    Parameters:
    - im (numpy.ndarray): The input image.
    - maxIters (int): Maximum number of iterations.
    - Dphi (numpy.ndarray): Random phase for the inverse transform.
    - mask (numpy.ndarray): The mask indicating the occulted pixels.

    Returns:
    - list: List of generated images.
    - list: List of errors for each iteration.
    """
    # Perform the Gerchberg-Saxton algorithm
    (IMa, IMp) = dft2(im)  # Compute the magnitude and phase of the Fourier transform
    images = []  # List to store generated images
    errors = []  # List to store errors for each iteration
    
    for k in range(maxIters + 1):
        print("Iteration %d of %d" % (k, maxIters))
        
        if k == 0:
            im = idft2(IMa, IMp)  # Perform inverse transform without phase correction
        elif k == maxIters:
            im = idft2(IMa, IMp + Dphi)  # Perform inverse transform with phase correction
        else:
            alpha = k / maxIters
            im = idft2(IMa, (1 - alpha) * IMp + alpha * (IMp + Dphi))  # Perform inverse transform with interpolated phase
        
        images.append(im)  # Add generated image to the list
        error = occultError(im, mask)  # Compute the occultation error
        errors.append(error)  # Add error to the list
    
    return images, errors  # Return the list of generated images and errors

def saveFrames(images, errors):
    """
    Save frames as images and plot the errors.

    Parameters:
    - images (list): List of images to be saved.
    - errors (list): List of errors for each iteration.

    Returns:
    - None
    """
    # Create an empty image with the same shape as the first generated image
    shape = (images[0].shape[0], images[0].shape[1], 3)
    image = np.zeros(shape, images[0].dtype)

    # Calculate the maximum number of iterations and maximum error value
    maxIters = len(images) - 1
    maxErrors = max(errors)

    # Iterate over each iteration
    for k in range(maxIters + 1):
        # Plot the errors for each iteration
        plt.plot(errors[:k+1], color='red')
        plt.xlabel("Iteration")
        plt.ylabel("Sum Square Error")
        plt.xlim(0, maxIters)
        plt.ylim(0, maxErrors)
        
        # Set the RGB channels of the image to the current generated image
        image[:, :, 0] = images[k]
        image[:, :, 1] = images[k]
        image[:, :, 2] = images[k]
        
        # Display the image with the errors as the background
        plt.imshow(image, extent=(0, maxIters, 0, maxErrors))
        plt.gca().set_aspect(maxIters / maxErrors)
        
        # Set the title of the plot
        plt.title("Coronagraph Simulation")
        
        # Save the plot as a PNG file
        plt.savefig('coronagraph' + str(k) + '.png')
        
        # Display the plot
        plt.show()

main() # Call the main function to run the simulation