import cv2


def resize_image(image, target_size=(640, 640)):
    """Resize the image to the target size."""
    resized_image = cv2.resize(image, target_size)
    return resized_image

def normalize_image(image):
    """Normalize the image pixel values to the range [0, 1]."""
    normalized_image = image / 255.0
    return normalized_image

def denoise_image(image):
    """Reduce noise in the image using Gaussian Blur."""
    denoised_image = cv2.GaussianBlur(image, (5, 5), 0)
    return denoised_image


def preprocces_image(image):
    pre_im = resize_image(image)
    pre_im = normalize_image(pre_im)
    pre_im = denoise_image(pre_im)
    return pre_im
# Örnek kullanım
if __name__ == "__main__":
    image_path = "C:/Users/Acer/Desktop/plate_images/1.jpg"
    image = cv2.imread(image_path)
    
    image = preprocces_image(image)
   
    

    # İşlenmiş görüntüyü kaydetme veya gösterme
    cv2.imshow("Processed Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
