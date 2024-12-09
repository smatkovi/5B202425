import numpy as np
import matplotlib.pyplot as plt


def julia_set(h_range, w_range, max_iterations):
    """
    A function to determine the values of the Julia set. Takes
    an array size specified by h_range and w_range, in pixels, along
    with the number of maximum iterations to try.  Returns an array with 
    the number of the last bounded iteration at each array value.
    """
    # top left to bottom right
    y, x = np.ogrid[1.4: -1.4: h_range*1j, -1.4: 1.4: w_range*1j]
    z_array = x + y*1j
    a = -0.744 + 0.148j #-0.744 + 0.148j
    iterations_until_divergence = max_iterations + np.zeros(z_array.shape)

    # Loop to iterate the Julia set calculation
    for i in range(max_iterations):
        z_array = z_array**2 + a

        # Check for divergence
        z_size_array = np.conj(z_array) * z_array  # More efficient modulus calculation
        diverging = z_size_array > 4
        diverging_now = diverging & (iterations_until_divergence == max_iterations)

        # Update iterations count and diverging mask
        iterations_until_divergence[diverging_now] = i
        iterations_until_divergence = np.where(diverging, i, iterations_until_divergence)  # Efficient update

        # Reset diverging elements (prevents overflow)
        z_array[diverging] = 0

    return iterations_until_divergence


# Example usage
plt.imshow(julia_set(2000, 2000, 70), cmap='twilight_shifted')
plt.axis('off')
plt.show()
plt.close()
