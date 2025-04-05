import re
import ast
from difflib import SequenceMatcher
from app.core.logger import logger
from typing import List, Dict, Union

def extract_name_dob(text_list: List[str]) -> List[Dict[str, Union[str, None]]]:
    """
    Extracts structured data containing name and date of birth from a list of strings.

    Args:
        text_list (List[str]): A list of strings that may contain a markdown-formatted Python dictionary or list.

    Returns:
        List[Dict[str, Union[str, None]]]: A list of dictionaries with extracted 'name' and 'dob' values.
    """
    # Join the list into a single string
    text = " ".join(text_list)
    
    # Attempt to extract the content within the ```python ... ``` code block
    match = re.search(r"```python\n(.*?)\n```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()

    try:
        # Safely evaluate the Python literal expression
        extracted_data = ast.literal_eval(text)
        if isinstance(extracted_data, list):
            return extracted_data
        else:
            logger.warning("Parsed data is not a list.")
            return []
    except (SyntaxError, ValueError) as e:
        logger.error(f"Error parsing data: {e}")
        return []

def text_similarity(data_list: List[Dict[str, Union[str, None]]]) -> float:
    """
    Computes similarity score between two data dictionaries containing 'name' and 'dob'.

    Args:
        data_list (List[Dict[str, Union[str, None]]]): A list of two dictionaries, each with 'name' and 'dob' keys.

    Returns:
        float: A score between 0.0 and 1.0 indicating the average similarity of names and DOBs.
    """
    try:
        if not isinstance(data_list, list) or len(data_list) != 2:
            raise ValueError("Expected a list of exactly 2 dictionaries")

        data1, data2 = data_list

        name1 = data1.get("name", "")
        dob1 = data1.get("dob", "")
        name2 = data2.get("name", "")
        dob2 = data2.get("dob", "")

        name_score = SequenceMatcher(None, name1, name2).ratio() if name1 and name2 else 0.0
        dob_score = 1.0 if dob1 and dob2 and dob1 == dob2 else 0.0

        return round((name_score + dob_score) / 2, 2)

    except Exception as e:
        logger.error(f"Error computing text similarity: {e}")
        return 0.0