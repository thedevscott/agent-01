import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    Validates that the requested directory (relative to working_directory) is
    inside the permitted working directory.
    """
    #==========================================================================
    # Validate requested directory
    #==========================================================================
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = ( os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs )
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # return f'Success: "{directory}" is within the working directory'

    #==========================================================================
    # List files
    #==========================================================================
        lines = []
        entries = os.listdir(target_dir)
        for name in entries:
            item_path = os.path.join(target_dir, name)
            is_dir = os.path.isdir(item_path)
            stat = os.stat(item_path)
            file_size = stat.st_size
            lines.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")
        
        if directory == ".":
            header = "Result for current directory:"
        else:
            header = f"Result for {directory} directory:"
        
        return header + "\n "+ "\n ".join(lines) if lines else header

    except Exception as e:
        return f"ErrorL {e}"
    
   
