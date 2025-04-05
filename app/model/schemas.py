from pydantic import BaseModel
from typing import Dict, List, Union

class SimilarityResponse(BaseModel):
    face_score: float
    text_score: float
    overall_score: float

class TextExtractionResponse(BaseModel):
    extracted_text: List[Dict[str, Union[str, None]]]

class FaceSimilarityResponse(BaseModel):
    similarity_score: float