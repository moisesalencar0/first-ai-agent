import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes on a text file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative path of the file to be writen, from the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "What to write on the file",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # PATH VALIDATION
        valid_target_file = (  # Will be True or False
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return (
                f'Error: Cannot write to "{file_path}"'
                'as it is outside the permitted working directory'
            )
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # If there's no parent directory for the file, creates it
        parent_directory = os.path.dirname(target_file)
        os.makedirs(parent_directory, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        # After reading the first MAX_CHARS...
        final_string = f'   Successfully wrote to "{file_path}" ({len(content)} characters written)'
        print(final_string)
        return final_string
    
    except Exception as e:
        return f"Error:{e}"