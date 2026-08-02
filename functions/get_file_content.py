import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the contents of a text file, truncated to 10,000 characters.",
        "parameters": {
            "type": "object",
            "file_path": {
                "type": "string",
                "description": "Relative path of the file to be writen, from the working directory",
            },
            "required": ["file_path"]
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # PATH VALIDATION
        valid_target_file = (  # Will be True or False
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return (
                f'Error: Cannot list "{file_path}"'
                'as it is outside the permitted working directory'
            )
        
        if not os.path.isfile(target_file): 
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{target_file}" truncated at {MAX_CHARS} characters]'

        # After reading the first MAX_CHARS...
        return file_content_string
    
    except Exception as e:
        return f"Error:{e}"