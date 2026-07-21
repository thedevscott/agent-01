import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = ( os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs )
        
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
            
        command = ["python", target_path]
        if args:
            command.extend(args)

        completed = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""

        if completed.returncode != 0:
            error_code_msg = f"Process exited with code {completed.returncode}"
        else:
            error_code_msg = ""
        
        if not stdout and not stderr:
            output_msg = "No output produced"
        else:
            parts = []
            if stdout:
                parts.append(f"STDOUT: {stdout}")
            if stderr:
                parts.append(f"STDERR: {stderr}")
            output_msg = "\n".join(parts)
        return "\n".join([p for p in [error_code_msg, output_msg] if p])

    except Exception as e:
        return f"Error: executing Python file: {e}"