import face_recognition
from app.core.logger import logger

def get_face_similarity(image1_path: str, image2_path: str) -> float:
    """
    Calculates the similarity score between faces in two images using face embeddings.

    Args:
        image1_path (str): File path to the first image containing a face.
        image2_path (str): File path to the second image containing a face.

    Returns:
        float: A similarity score between 0.0 (no match) and 1.0 (exact match).
               Returns 0.0 if a face is not detected or if any error occurs.
    """
    try:
        # Load images
        img1 = face_recognition.load_image_file(image1_path)
        img2 = face_recognition.load_image_file(image2_path)

        # Extract face encodings
        encoding1 = face_recognition.face_encodings(img1)
        encoding2 = face_recognition.face_encodings(img2)

        if encoding1 and encoding2:
            distance = face_recognition.face_distance([encoding1[0]], encoding2[0])[0]
            similarity = 1 - distance
            return round(similarity, 2)
        else:
            logger.warning("Face not detected in one or both images.")
            return 0.0

    except Exception as e:
        logger.error(f"Error computing face similarity: {e}")
        return 0.0