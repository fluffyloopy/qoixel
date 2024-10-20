from sys import argv
from modules.qoi import QoiDecoder
from modules.sixel import SixelConverter
import modules.color_depth_conveter as ColorConverter

qoi_filename = argv[1]

with open(qoi_filename, "rb") as qoi_file:
    qoi_data = qoi_file.read()

decoder = QoiDecoder()
headers = decoder.headers(qoi_data)
width = headers.width
height = headers.height

original_pixels = decoder.decoder(qoi_data, headers)

no_alpha = ColorConverter.rgba_to_rgb(original_pixels)

pixels = ColorConverter.fix_color_issues(no_alpha, num_colors=256)

sixel_converter = SixelConverter(pixels, width, height)
sixel_data = sixel_converter.generate_sixel()

print(sixel_data)