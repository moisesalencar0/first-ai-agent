import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        listed_dir = directory
        if directory == ".":
            listed_dir = "current"
        print(f"Result for {listed_dir} directory:")

        # PATH VALIDATION
        valid_target_dir = (  # Will be True or False
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return (
                f'Error: Cannot list "{directory}"'
                'as it is outside the permitted working directory'
            )
        
        if not os.path.isdir(target_dir): 
            return f'Error: "{directory}" is not a directory'

        # LEGACY: return f'Success: "{directory}" is within the working directory'

        dir_items = os.listdir(target_dir)

        item_info_list = []
        for item in dir_items:
            abs_item_path = os.path.join(target_dir, item)
            item_info_list.append(
                f'- {item}: file_size={os.path.getsize(abs_item_path)} bytes, is_dir={os.path.isdir(abs_item_path)}'
            )
        return "\n".join(item_info_list)
    
    except Exception as e:
        return f"Error:{e}"