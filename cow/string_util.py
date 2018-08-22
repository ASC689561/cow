def keymap_replace(string: str, mappings: dict) -> str:
    """Replace parts of a string based on a dictionary.
    Keyword arguments:
    string       -- The string to replace characters in.
    mappings     -- A dictionary of replacement mappings.
    """
    replaced_string = string
    for character, replacement in mappings.items():
        character = '{' + character + '}'
        replaced_string = replaced_string.replace(str(character), str(replacement)
                                                  )
    return replaced_string
