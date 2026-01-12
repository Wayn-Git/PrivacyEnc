# PrivacyEnc

**PrivacyEnc** is an image processing and privacy protection tool designed to detect and process sensitive features (such as faces, number plates, addresses, ids etc) in images. It utilizes computer vision techniques to automate the handling of image data, likely for privacy preservation purposes.

## Features

* **Image Pre-processing**: Robust image loading and normalization pipeline.
    * Automatic orientation correction (EXIF transpose).
    * Standardization to RGB color space.
    * Smart resizing to maintain aspect ratio while fitting within maximum dimensions.
* **Object Detection**:
    * Face detection using Haar Cascade Classifiers.
    * Eye detection using Haar Cascade Classifiers.
    * *Experimental:* Integration with Keras VGGFace for advanced face recognition (in development).

## Installation

To use this project, you will need Python installed along with several dependencies.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/wayn-git/privacyenc.git](https://github.com/wayn-git/privacyenc.git)
    cd privacyenc
    ```

2.  **Install dependencies:**
    The project depends on the following libraries:
    * `Pillow` (PIL)
    * `opencv-python` (cv2)
    * `numpy`
    * `matplotlib`
    * `tensorflow` / `keras` (for VGGFace integration)
    * `keras-vggface`

    You can install them via pip:
    ```bash
    pip install Pillow opencv-python numpy matplotlib tensorflow keras keras-vggface
    ```

## 💻 Usage

### The 'Image Processor' class is responsible for handling the iamges that the user inputs 

#### What each method actually does: 
- load_image(): Loads the image making sure the height and width is stable and the file is not invalid
- orientation_fix(): Fixes the orientation of the image by extracting the exif meta data of the image
- normalize_to_rgb(): Normalizes the image colors to RGB mode
- normalize_size(): Normalize Size (Don't know how it works yet)
- image_processor_pipeline(): Puts everything together

