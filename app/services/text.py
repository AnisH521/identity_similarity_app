import re
import ast
import json
from difflib import SequenceMatcher
from app.core.logger import logger

def text_similarity(data_list: str) -> float:
    """
    Computes similarity score between two data dictionaries containing 'name' and 'dob'.

    Args:
        data_list (List[Dict[str, Union[str, None]]]): A list of two dictionaries, each with 'name' and 'dob' keys.

    Returns:
        float: A score between 0.0 and 1.0 indicating the average similarity of names and DOBs.
    """
    try:
        data = json.loads(data_list)
        if not isinstance(data, list) or len(data) != 2:
            raise ValueError("Expected a list of exactly 2 dictionaries")

        data1 = data[0]
        data2 = data[1]
        
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