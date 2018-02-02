

def keymap_replace(string: str, mappings: dict, lower_keys=False, lower_values=False, lower_string=False) -> str:
    """Replace parts of a string based on a dictionary.
    Keyword arguments:
    string       -- The string to replace characters in.
    mappings     -- A dictionary of replacement mappings.
    lower_keys   -- Whether or not to lower the keys in mappings.
    lower_values -- Whether or not to lower the values in mappings.
    lower_string -- Whether or not to lower the input string.
    """
    replaced_string = string.lower() if lower_string else string
    for character, replacement in mappings.items():
        character = '{' + character + '}'
        replaced_string = replaced_string.replace(
            str(character).lower() if lower_keys else str(character),
            str(replacement).lower() if lower_values else str(replacement)
        )
    return replaced_string
