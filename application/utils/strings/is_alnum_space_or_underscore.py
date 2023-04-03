

def is_alpha_num_space_or_underscore(s: str) -> bool:
    for char in s:
        if not (char.isalnum() or char == " " or char == "_"):
            return False
    return True
