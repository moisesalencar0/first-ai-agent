import os, subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes (run) a python file",
        "parameters": {
            "type": "object",
            "properties":{
                "file_path": {
                    "type": "string",
                    "description": "Relative path of the file to be writen, from the working directory",
                },
                "args":{
                    "type": "string",
                    "description": "Aditional arguments for the subprocess creation"
                }
            },
            "required": ["file_path"]
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # PATH VALIDATION
        valid_target_file = (  # Will be True or False
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return (
                f'Error: Cannot execute "{file_path}"'
                ' as it is outside the permited working directory'
            )
        
        if not os.path.isfile(target_file): 
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        

        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        parts = []
        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}")
        if result.stderr == "" and result.stdout == "":
            parts.append("No output produced")
        else:
            parts.append(f"STDERR:{result.stderr}")
            parts.append(f"STDOUT:{result.stdout}")

        return "\n".join(parts)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"