import re
import ast
from difflib import SequenceMatcher
from app.core.logger import logger
from typing import List, Dict, Union

def extract_name_dob(text_list: List[str]) -> List[dict]:
    """
    Converts a markdown-wrapped string containing either a single dictionary or a list of two dictionaries
    into a list with two dictionaries.

    If a single dictionary is detected, it duplicates it.
    If two dictionaries are already present, it returns as is.

    Args:
        text_list (List[str]): List containing a single markdown-wrapped string.

    Returns:
        List[dict]: List of two dictionaries.
    """
    if not text_list:
        return []

    text = " ".join(text_list)

    # Extract content between the markdown code block
    match = re.search(r"```python\n(.*?)\n```", text, re.DOTALL)
    if not match:
        return []

    try:
        parsed = ast.literal_eval(match.group(1).strip())

        if isinstance(parsed, dict):
            # Duplicate single dictionary
            return [parsed.copy(), parsed.copy()]

        elif isinstance(parsed, list) and len(parsed) == 2:
            return parsed

    except Exception as e:
        print(f"Error parsing input: {e}")
        return []

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