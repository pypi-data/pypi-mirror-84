"""
Utils module.
"""
def module_name(search_key: str):
    """Returns the module name from search key"""

    return "".join([
        ("_"+i if j> 0 and i.isupper() else i) for j,i in enumerate(
            search_key.replace("Supported","").replace("Types","").replace(
                "-","_"))
        ]).strip().lower()
