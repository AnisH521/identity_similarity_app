from fastapi import APIRouter, File, UploadFile, HTTPException
import tempfile
import os
import shutil

from app.model.schemas import SimilarityResponse, TextExtractionResponse, FaceSimilarityResponse

from app.services.face import get_face_similarity
from app.services.text import text_similarity
from app.services.score import calculate_final_score
from app.services.ocr_inference import extract_img_info

router = APIRouter()

@router.post("/compare", response_model=SimilarityResponse)
async def compare_identity_documents(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
):
    """
    Compare two identity documents and calculate similarity score
    """
    try:
        # Read file contents into bytes
        image1_bytes = await image1.read()
        image2_bytes = await image2.read()

        # Get mime types (important for the API)
        image1_mime_type = image1.content_type
        image2_mime_type = image2.content_type
        # Create temp directory to store uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            image1_path = os.path.join(temp_dir, image1.filename)
            image2_path = os.path.join(temp_dir, image2.filename)
            
            with open(image1_path, "wb") as buffer:
                buffer.write(image1_bytes)
            
            with open(image2_path, "wb") as buffer:
                buffer.write(image2_bytes)
  
            # Process the images
            face_score = get_face_similarity(image1_path, image2_path)
            extracted_text = extract_img_info(
                image1_bytes=image1_bytes,
                image1_mime_type=image1_mime_type,
                image2_bytes=image2_bytes,
                image2_mime_type=image2_mime_type
            )
            text_similarity_score = text_similarity(extracted_text)
            final_score = calculate_final_score(face_score, text_similarity_score)
            
            return SimilarityResponse(
                face_score=face_score,
                text_score=text_similarity_score,
                overall_score=final_score,
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing comparison: {str(e)}")

@router.post("/face-similarity", response_model=FaceSimilarityResponse)
async def face_similarity(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):
    """
    Calculate similarity score between two face images
    """
    try:
        # Create temp directory to store uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            image1_path = os.path.join(temp_dir, image1.filename)
            image2_path = os.path.join(temp_dir, image2.filename)
            
            with open(image1_path, "wb") as buffer:
                shutil.copyfileobj(image1.file, buffer)
            
            with open(image2_path, "wb") as buffer:
                shutil.copyfileobj(image2.file, buffer)
            
            # Process the images
            face_score = get_face_similarity(image1_path, image2_path)
            
            return {"similarity_score": face_score}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing face similarity: {str(e)}")

@router.post("/text-extraction", response_model=TextExtractionResponse)
async def extract_text(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):
    """
    Extract text from identity document images
    """
    try:
        # Read file contents into bytes
        image1_bytes = await image1.read()
        image2_bytes = await image2.read()

        # Get mime types (important for the API)
        image1_mime_type = image1.content_type
        image2_mime_type = image2.content_type

        # Call the function with bytes and mime types
        extracted_text = extract_img_info(
            image1_bytes=image1_bytes,
            image1_mime_type=image1_mime_type,
            image2_bytes=image2_bytes,
            image2_mime_type=image2_mime_type
        )
        return {"extracted_text": extracted_text}
    except Exception as e:
        # Catch any other exceptions, including those re-raised from extract_img_info
        print(f"Error during text extraction request: {e}") # Log the error server-side
        raise HTTPException(status_code=500, detail=f"Internal server error processing images.") #