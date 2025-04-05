from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
import tempfile
import os
import shutil

from app.model.schemas import SimilarityResponse, TextExtractionResponse, FaceSimilarityResponse

from app.services.face import get_face_similarity
from app.services.text import text_similarity, extract_name_dob
from app.services.score import calculate_final_score
from app.services.ocr_inference import extract_name_dob_with_qwen

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
        # Create temp directory to store uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            image1_path = os.path.join(temp_dir, image1.filename)
            image2_path = os.path.join(temp_dir, image2.filename)
            
            with open(image1_path, "wb") as buffer:
                shutil.copyfileobj(image1.file, buffer)
            
            with open(image2_path, "wb") as buffer:
                shutil.copyfileobj(image2.file, buffer)
            
            # Process the images
            face_score = get_face_similarity(image1_path, image2_path)
            output_text = extract_name_dob_with_qwen([image1_path, image2_path])
            extracted_text = extract_name_dob(output_text)
            text_similarity_score = text_similarity(extracted_text)
            final_score = calculate_final_score(face_score, text_similarity_score)
            
            # Determine if name and DOB match
            name_match = None
            dob_match = None
            if 'name_match' in extracted_text:
                name_match = extracted_text['name_match']
            if 'dob_match' in extracted_text:
                dob_match = extracted_text['dob_match']
            
            return SimilarityResponse(
                face_score=face_score,
                text_score=text_similarity_score,
                overall_score=final_score,
                name_match=name_match,
                dob_match=dob_match,
                extracted_text=extracted_text
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
    images: List[UploadFile] = File(...)
):
    """
    Extract text from identity document images
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            image_paths = []
            for img in images:
                img_path = os.path.join(temp_dir, img.filename)
                image_paths.append(img_path)
                
                with open(img_path, "wb") as buffer:
                    shutil.copyfileobj(img.file, buffer)
            
            output_text = extract_name_dob_with_qwen(image_paths)
            extracted_text = extract_name_dob(output_text)
            
            return {"extracted_text": extracted_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")