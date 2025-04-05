from app.core.logger import logger
from typing import Union

def calculate_final_score(
    face_score: Union[float, int],
    text_score: Union[float, int],
    face_weight: float = 0.6,
    text_weight: float = 0.4
) -> float:
    """
    Calculates the final weighted score from face and text similarity scores.

    Args:
        face_score (Union[float, int]): Similarity score based on face recognition.
        text_score (Union[float, int]): Similarity score based on text comparison.
        face_weight (float, optional): Weight for face score. Defaults to 0.6.
        text_weight (float, optional): Weight for text score. Defaults to 0.4.

    Returns:
        float: Final weighted similarity score rounded to two decimal places.
    """
    try:
        final_score = face_score * face_weight + text_score * text_weight
        return round(final_score, 2)
    except Exception as e:
        logger.error(f"Error calculating final score: {e}")
        return 0.0