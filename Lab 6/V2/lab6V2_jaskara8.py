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

# Load the image and preprocess it:
def loadImage(name):
    """
    Load the image and preprocess it.

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
    h, w = im.shape
    center_h = h // 2
    center_w = w // 2
    radius = diameter // 2
    y, x = np.ogrid[:h, :w]
    mask = (x - center_w)**2 + (y - center_h)**2 <= radius**2
    im[mask] = 0
    return im, mask

# Perform the optical system simulation
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
    im, mask = occultCircle(im, diameter)
    (IMa, IMp) = dft2(im)
    rng = np.random.default_rng(12345)
    imR = rng.random(im.shape)
    (_, Dphi) = dft2(imR)
    im = idft2(IMa, IMp - Dphi)
    return im, Dphi, mask

# Apply occultation to the image
def occultSquare(im, width):
    """
    Occults a square region in the given image.

    Parameters:
    - im (numpy.ndarray): The input image.
    - width (int): The width of the square region to be occulted.

    Returns:
    - numpy.ndarray: The image with the square region occulted.
    """
    h, w = im.shape
    center_h = h // 2
    center_w = w // 2
    start_h = center_h - width // 2
    end_h = start_h + width
    start_w = center_w - width // 2
    end_w = start_w + width
    im[start_h:end_h, start_w:end_w] = 0
    return im

# Compute the 2D discrete Fourier transform of a grayscale image
def dft2(im):
    IM = np.fft.rfft2(im)
    IMa = np.abs(IM)
    IMp = np.angle(IM)
    return (IMa, IMp)

# Compute the inverse 2D discrete Fourier transform
def idft2(IMa, IMp):
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

# Perform the Gerchberg-Saxton algorithm
def gerchbergSaxton(im, maxIters, Dphi, mask):
    """
    Perform the Gerchberg-Saxton algorithm.

    Parameters:
    - im (numpy.ndarray): The input image.
    - maxIters (int): Maximum number of iterations.
    - Dphi (numpy.ndarray): Random phase for the inverse transform.
    - mask (numpy.ndarray): The mask indicating the occulted pixels.

    Returns:
    - list: List of generated images.
    - list: List of errors for each iteration.
    """
    (IMa, IMp) = dft2(im)
    images = []
    errors = []
    
    for k in range(maxIters + 1):
        print("Iteration %d of %d" % (k, maxIters))
        
        if k == 0:
            im = idft2(IMa, IMp)
        elif k == maxIters:
            im = idft2(IMa, IMp + Dphi)
        else:
            alpha = k / maxIters
            im = idft2(IMa, (1 - alpha) * IMp + alpha * (IMp + Dphi))
        
        images.append(im)
        error = occultError(im, mask)
        errors.append(error)
    
    return images, errors

# Save the generated frames as PNG files

def saveFrames(images, errors):
    """
    Save frames as images and plot the errors.

    Parameters:
    - images (list): List of images to be saved.
    - errors (list): List of errors for each iteration.

    Returns:
    - None
    """
    shape = (images[0].shape[0], images[0].shape[1], 3)
    image = np.zeros(shape, images[0].dtype)
    maxIters = len(images) - 1
    maxErrors = max(errors)
    
    for k in range(maxIters + 1):
        image[:, :, 0] = images[k]
        image[:, :, 1] = images[k]
        image[:, :, 2] = images[k]
        
        plt.subplot(1, 2, 1)
        plt.imshow(image)
        plt.title("Iteration " + str(k) + " of " + str(maxIters))
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        plt.plot(errors[:k+1])
        plt.title("Occultation Error")
        plt.xlabel("Iteration")
        plt.ylabel("Error")
        plt.xlim(0, maxIters)
        plt.ylim(0, maxErrors)
        
        plt.savefig('coronagraph' + str(k) + '.png')
        plt.show()

# Main function
def main():
    im = loadImage('300_26a_big-vlt-s.jpg')
    im, Dphi, mask = opticalSystem(im, 300)
    images, errors = gerchbergSaxton(im, 10, Dphi, mask)
    saveFrames(images, errors)

# Call the main function
main()