from PIL import Image, ImageOps


class ImageProcessor:
    def __init__(self, image_path: str, min_width: int = 50, min_height: int = 50):
        self.image_path = image_path
        self.min_width = min_width
        self.min_height = min_height

        self.original_size = None
        self.scale = 1.0
        self.image = None

    def load_image(self):
        try:
            img = Image.open(self.image_path)

            width, height = img.size
            if width < self.min_width or height < self.min_height:
                img.close()
                raise ValueError(
                    f"Image too small. Minimum {self.min_width}x{self.min_height}, "
                    f"got {width}x{height}"
                )

            self.original_size = img.size
            self.image = img
            return img

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.image_path}")

        except OSError as e:
            raise OSError(f"Invalid or unsupported image file: {e}")

    def fix_orientation(self):
        self.image = ImageOps.exif_transpose(self.image)
        return self.image

    def normalize_to_rgb(self):
        if self.image.mode != "RGB":
            self.image = self.image.convert("RGB")
        return self.image

    def normalize_size(self, max_long_side: int = 1280):
        width, height = self.image.size
        long_side = max(width, height)

        if long_side <= max_long_side:
            self.scale = 1.0
            return self.image

        self.scale = max_long_side / long_side
        new_width = int(width * self.scale)
        new_height = int(height * self.scale)

        self.image = self.image.resize(
            (new_width, new_height), Image.Resampling.LANCZOS
        )
        return self.image

    def process(self):
        self.load_image()
        self.fix_orientation()
        self.normalize_to_rgb()
        self.normalize_size()

        return {
            "image": self.image,
            "scale": self.scale,
            "original_size": self.original_size,
        }
