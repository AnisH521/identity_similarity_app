import os

# Store Gemini 2.0 Flash API Key
from google import genai
from google.genai import types

def extract_img_info(
    image1_bytes: bytes,
    image1_mime_type: str,
    image2_bytes: bytes,
    image2_mime_type: str
) -> str:
    client = genai.Client(
        api_key = os.getenv("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"

    prompt = (
        "Extract only the **name** and **DOB** from each image. "
        "Return a Python list where each item is a dictionary in the following format:\n\n"
        "{'image': 'image_name.jpg', 'name': 'Full Name', 'dob': 'DD-MM-YYYY'}\n\n"
        "Ensure the keys are lowercase and use only this format in the response without any markdown or additional text."
    )

    contents = [
        types.Part(inline_data=types.Blob(mime_type=image1_mime_type, data=image1_bytes)),
        types.Part(inline_data=types.Blob(mime_type=image2_mime_type, data=image2_bytes)),
        types.Part(text=prompt)
    ]
    
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
        response_mime_type="application/json",
    )
    
    output_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        output_text += chunk.text
    return output_text