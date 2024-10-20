class SixelConverter:
    def __init__(self, pixels, width, height):
        self.pixels = pixels
        self.width = width
        self.height = height
        self.pixels = self.sixel_rgb()
        self.unique_pixels = self.extract_unique_pixels()
        self.generate_sixel()

    def sixel_rgb(self):
        sixel_rgb = []

        for pixel in self.pixels:
            r = int((pixel[0] / 255) * 100)
            g = int((pixel[1] / 255) * 100)
            b = int((pixel[2] / 255) * 100)
            sixel_rgb.append((r, g, b))
        return sixel_rgb

    def extract_unique_pixels(self):
        unique_pixels = {pixel: index for index, pixel in enumerate(set(self.pixels))}
        return unique_pixels

    def generate_sixel(self):
        image_data_list = []
        image_string = '\x1bPq"1;1;{};{}'.format(self.width, self.height)
        for pixel in self.unique_pixels:
            image_string += "#{};2;{};{};{}".format(
                self.unique_pixels[pixel], pixel[0], pixel[1], pixel[2]
            )

        sixel_characters = [
            "0b000001",
            "0b000010",
            "0b000100",
            "0b001000",
            "0b010000",
            "0b100000",
        ]
        sixel_index = 0
        i = 1
        last_color = None
        last_sixel = None
        for current_pixel in self.pixels:
            sixel_index = 0 if sixel_index == 6 else sixel_index
            color_index = self.unique_pixels[current_pixel]
            sixel = chr(int(sixel_characters[sixel_index], 2) + 63)

            match i % (self.width * 6):
                case 0:
                    match last_color == color_index and last_sixel == sixel:
                        case True:
                            image_string += "{}$-".format(sixel)
                        case False:
                            image_string += "#{}{}$-".format(color_index, sixel)
                    sixel_index += 1
                case _ if i % self.width == 0:
                    match last_color == color_index and last_sixel == sixel:
                        case True:
                            image_string += "{}$".format(sixel)
                        case False:
                            image_string += "#{}{}$".format(color_index, sixel)
                    sixel_index += 1
                case _:
                    match last_color == color_index and last_sixel == sixel:
                        case True:
                            image_string += "{}".format(sixel)
                        case False:
                            image_string += "#{}{}".format(color_index, sixel)
            i += 1
            last_color = color_index
            last_sixel = sixel
        image_string += "\x1b\\"

        image_data_list.append(image_string)
        return image_data_list[0]
