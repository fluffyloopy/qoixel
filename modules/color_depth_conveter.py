import numpy as np
from sklearn.cluster import KMeans


def rgba_to_rgb(rgba_list, background_color=(255, 255, 255)):
    rgb_list = []
    for r, g, b, a in rgba_list:
        alpha = a / 255.0
        new_r = int((1 - alpha) * background_color[0] + alpha * r)
        new_g = int((1 - alpha) * background_color[1] + alpha * g)
        new_b = int((1 - alpha) * background_color[2] + alpha * b)
        rgb_list.append((new_r, new_g, new_b))
    return rgb_list

def fix_color_issues(rgb_list, num_colors=256):
    pixels = np.array(rgb_list).reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors, random_state=0)
    kmeans.fit(pixels)
    quantized_pixels = kmeans.cluster_centers_[kmeans.labels_]
    fixed_pixels_list = [tuple(map(int, color)) for color in quantized_pixels]
    return fixed_pixels_list