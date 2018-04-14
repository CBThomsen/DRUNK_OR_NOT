import numpy as np


def shrink(img, size, defined_size):  # Change - Issue #1
    result = np.zeros((defined_size, defined_size, 3), dtype=np.uint8)  # Change - Issue #2

    scale_factor = size / defined_size
    for i in range(defined_size):
        for j in range(defined_size):
            temp = np.array([0, 0, 0])
            for x in range(scale_factor):  # Change - Issue #3
                for y in range(scale_factor):  # Change - Issue #3
                    temp += img[i * scale_factor + x, j * scale_factor + y]  # Change - Issue #3

            result[i, j] = temp / (scale_factor * scale_factor)  # Change

    return result
