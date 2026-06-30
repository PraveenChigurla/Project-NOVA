"""
OCR Preprocessor.
Applies computer vision filters to optimize images for text extraction.
"""
import cv2
import numpy as np
import logging
from PIL import Image

from nova.providers.vision.ocr.models import OCRConfiguration

logger = logging.getLogger(__name__)

class OCRPreprocessor:
    """Prepares raw screenshots for OCR inference."""
    
    @staticmethod
    def process(image_path: str, config: OCRConfiguration) -> np.ndarray:
        """
        Executes the preprocessing pipeline on an image.
        Returns a cv2 image matrix (numpy array).
        """
        # Load image via cv2
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at path: {image_path}")
            
        if not config.enable_preprocessing:
            return img
            
        logger.debug(f"Preprocessing image (Scale: {config.scale_factor}, Denoise: {config.enable_denoise})")
        
        # 1. Scaling (Upscaling helps Tesseract/OCR engines find smaller text)
        if config.scale_factor != 1.0:
            width = int(img.shape[1] * config.scale_factor)
            height = int(img.shape[0] * config.scale_factor)
            dim = (width, height)
            # INTER_CUBIC is generally better for zooming text
            img = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
            
        # 2. Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 3. Contrast Enhancement (CLAHE - Contrast Limited Adaptive Histogram Equalization)
        if config.enable_contrast:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray = clahe.apply(gray)
            
        # 4. Noise Reduction (Bilateral Filter preserves edges better than Gaussian)
        if config.enable_denoise:
            gray = cv2.bilateralFilter(gray, 9, 75, 75)
            
        # 5. Thresholding (Binarization) - Optional depending on the engine, 
        # but often helps baseline Tesseract significantly.
        # We will use Otsu's thresholding for now if mode is ACCURATE
        if config.mode == "accurate":
            # Apply Gaussian Blur before Otsu for better results
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, gray = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return gray
