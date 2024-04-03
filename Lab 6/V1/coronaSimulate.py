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
import matplotlib.pyplot as plt
import numpy as np
def occultSquare(im, width):
    """
    Apply occultation to the input image.

    Parameters:
    - im: numpy.ndarray
        The input image.
    - width: int
        The width of the occultation square.

    Returns:
    - numpy.ndarray
        The image with occultation applied.
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

def dft2(im):
    """
    Perform 2D Discrete Fourier Transform (DFT) on the input image.

    Parameters:
    - im: numpy.ndarray
        The input image.

    Returns:
    - tuple
        A tuple containing the magnitude and phase of the Fourier Transform.
    """
    # Compute the 2D Discrete Fourier Transform (DFT)
    IM = np.fft.rfft2(im)

    # Compute the magnitude and phase of the DFT
    IM_a = np.abs(IM)  # Magnitude
    IM_p = np.angle(IM)  # Phase

    return (IM_a, IM_p) # Return the magnitude and phase

def idft2(IM_a, IM_p):
    """
    Perform 2D Inverse Discrete Fourier Transform (IDFT) using the given magnitude and phase.

    Parameters:
    - IM_a: numpy.ndarray
        The magnitude of the Fourier Transform.
    - IM_p: numpy.ndarray
        The phase of the Fourier Transform.

    Returns:
    - numpy.ndarray
        The reconstructed image after inverse Fourier Transform.
    """
    # Reconstruct the complex Fourier Transform using magnitude and phase
    IM = IM_a * (np.cos(IM_p) + 1j * np.sin(IM_p))
    # Perform inverse Fourier Transform
    im = np.fft.irfft2(IM)
    # Essentially just clipping the values to the range [0, 1]
    im = np.clip(im, 0, 1)
    return im # Return the reconstructed image

def gerchbergSaxton(im, maxIters, Dphi):
    """
    Perform the Gerchberg-Saxton algorithm on the input image.

    Parameters:
    - im: numpy.ndarray
        The input image.
    - maxIters: int
        The maximum number of iterations for the algorithm.
    - Dphi: numpy.ndarray
        The phase correction to be applied.

    Returns:
    - list
        A list of images at each iteration of the algorithm.
    """
    (IM_a, IM_p) = dft2(im)
    images = []
    for k in range(maxIters + 1):
        print("Iteration %d of %d" % (k, maxIters))
        if k == 0:
            corrected_phase = IM_p
        elif k == maxIters:
            corrected_phase = IM_p + Dphi
        else:
            alpha = k / maxIters
            corrected_phase = (1 - alpha) * IM_p + alpha * (IM_p + Dphi)
        im = idft2(IM_a, corrected_phase)
        images.append(im)
    return images


def saveFrames(images):
    """
    Save the frames of the images as PNG files.

    Parameters:
    - images: list
        A list of images to be saved.

    Returns:
    - None
    """
    shape = (images[0].shape[0], images[0].shape[1], 3)
    image = np.zeros(shape, images[0].dtype)
    maxIters = len(images) - 1
    for k in range(maxIters + 1):
        image[:, :, 0] = images[k]
        image[:, :, 1] = images[k]
        image[:, :, 2] = images[k]
        plt.imshow(image)
        plt.title("Iteration " + str(k) + " of " + str(maxIters))

        plt.axis('off')
        plt.savefig('coronagraph' + str(k) + '.png')
        plt.show()
