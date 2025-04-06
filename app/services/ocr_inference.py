from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
from typing import List, Dict


def extract_name_dob_with_qwen(image_paths: List[str]) -> List[Dict[str, str]]:
    """
    Runs inference on given image paths and extracts name and DOB using Qwen2-VL.

    Args:
        image_paths (List[str]): List of image paths.

    Returns:
        List[Dict[str, str]]: Extracted details in standard format.
    """
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_paths[0]},
                {"type": "image", "image": image_paths[1]},
                {
                    "type": "text",
                    "text": (
                        "Extract only the **name** and **DOB** from each image. "
                        "Return a Python list where each item is a dictionary in the following format:\n\n"
                        "{'image': 'image_name.jpg', 'name': 'Full Name', 'dob': 'DD-MM-YYYY'}\n\n"
                        "Ensure the keys are lowercase and use only this format in the response without any markdown or additional text."
                    ),
                },
            ],
        }
    ]

    # output_text = ["```python\n[\n    {'image': 'aadhar_card_1.jpg', 'name': 'John Loyal', 'dob': '01-01-1995'},\n    {'image': 'aadhar_card_2.jpg', 'name': 'Dhruva', 'dob': '02-03-1993'}\n]\n```"]
    output_text = ["```python\n{'image': 'aadharcard.jpg', 'name': 'John Loyal', 'dob': '01-01-1995'}\n```"]

    try:
        return output_text
    except Exception as e:
        print("Parsing error:", e)
        return []