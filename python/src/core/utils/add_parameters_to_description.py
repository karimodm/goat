from zon import Zon, ZonOptional, ZonRecord, ZonString, ZonNumber, ZonBoolean, ZonList, ZonContainer

def add_parameters_to_description(description: str, schema: ZonRecord) -> str:
    """Add parameter descriptions to a tool description."""
    param_lines: list[str] = []
    
    if isinstance(schema, ZonRecord):
        shape = schema.shape
        if shape:
            for key, value in shape.items():
                is_optional = isinstance(value, ZonOptional)
                param_description = value.description or "" # pyright: ignore
                type_str = get_type_string(value)
                
                param_line = f"- {key}"
                if is_optional:
                    param_line += " (optional)"
                param_line += f" ({type_str}): {param_description}"
                
                param_lines.append(param_line)
    
    return f"{description}\n{"\n".join(param_lines)}" 

def get_type_string(field_type: Zon) -> str:
    """Get a string representation of a type."""
    if isinstance(field_type, ZonOptional):
        return get_type_string(field_type.unwrap())
    elif isinstance(field_type, ZonString):
        return "string"
    elif isinstance(field_type, ZonNumber):
        return "number"
    elif isinstance(field_type, ZonBoolean):
        return "boolean"
    elif isinstance(field_type, ZonList):
        return "array"
    elif isinstance(field_type, ZonContainer):
        return "object"
    else:
        return "unknown"
