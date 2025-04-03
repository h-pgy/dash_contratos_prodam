from typing import Dict, List, Union

JSON_basic_obj = Union[str, int, float, bool, None]
JSON_dict = Dict[str, Union[JSON_basic_obj, Dict[str, JSON_basic_obj]]]
JSON_list = List[Union[JSON_basic_obj, JSON_dict, List[Union[JSON_basic_obj, JSON_dict]]]]
JSONType = Dict[str, Union[JSON_basic_obj, JSON_dict, JSON_list]]
