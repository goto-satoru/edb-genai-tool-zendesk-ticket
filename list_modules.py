import subprocess
import sys
import json

def list_installed_modules():
    """
    Runs the 'pip list' command and returns the output in OpenAPI-friendly JSON format.
    """
    try:
        # Use subprocess.run to execute the 'pip list --format=json' command
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--format=json'],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse the JSON output
        packages = json.loads(result.stdout)
        
        # Format for OpenAPI response
        response = {
            "status": "success",
            "total_packages": len(packages),
            "packages": packages
        }
        
        return json.dumps(response, indent=2)

    except subprocess.CalledProcessError as e:
        error_response = {
            "status": "error",
            "error": f"Error executing pip list: {e}",
            "stderr": e.stderr
        }
        return json.dumps(error_response, indent=2)
    except FileNotFoundError:
        error_response = {
            "status": "error",
            "error": "The 'python' or 'pip' executable was not found."
        }
        return json.dumps(error_response, indent=2)
    except Exception as e:
        error_response = {
            "status": "error",
            "error": f"An unexpected error occurred: {str(e)}"
        }
        return json.dumps(error_response, indent=2)

if __name__ == "__main__":
    result = list_installed_modules()
    print(result)
