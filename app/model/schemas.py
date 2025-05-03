from pydantic import BaseModel

class SimilarityResponse(BaseModel):
    face_score: float
    text_score: float
    overall_score: float

class TextExtractionResponse(BaseModel):
    extracted_text: str

class FaceSimilarityResponse(BaseModel):
    similarity_score: float