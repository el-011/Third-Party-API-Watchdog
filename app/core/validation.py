from typing import Any, Dict

async def validate_response_contract(response_json: Any, schema: Dict[str, Any]) -> bool:
    def match_schema(data, sch):
        if isinstance(sch, dict) and isinstance(data, dict):
            for key, val_type in sch.items():
                if key not in data:
                    return False
                if isinstance(val_type, dict):
                    if not match_schema(data[key], val_type):
                        return False
                else:
                    if val_type == "str" and not isinstance(data[key], str):
                        return False
                    if val_type == "int" and not isinstance(data[key], int):
                        return False
                    if val_type == "float" and not isinstance(data[key], float):
                        return False
                    if val_type == "bool" and not isinstance(data[key], bool):
                        return False
            return True
        return False
    try:
        return match_schema(response_json, schema)
    except Exception:
        return False
