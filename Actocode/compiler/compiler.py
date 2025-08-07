import subprocess
import tempfile
import os

class Compiler:

    def run_subprocess(self, cmd, input_data=None):
        """Executes a subprocess with optional input data"""
        try:
            process = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=5  # Prevent infinite loops
            )
            return {"output": process.stdout if process.returncode == 0 else process.stderr}
        except subprocess.TimeoutExpired:
            return {"output": "Execution timed out"}
        except Exception as e:
            return {"output": f"Error: {str(e)}"}

    def compile_cpp(self, code):
        """Compiles and runs C++ code"""
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as source_file:
            source_file.write(code.encode())
            source_path = source_file.name

        output_binary = source_path.replace(".cpp", "")

        compile_cmd = ["g++", source_path, "-o", output_binary]
        compile_result = self.run_subprocess(compile_cmd)

        if "error" in compile_result["output"]:
            return compile_result

        return self.run_subprocess([output_binary])

    def compile_java(self, code):
        """Compiles and runs Java code"""
        with tempfile.NamedTemporaryFile(suffix=".java", delete=False) as source_file:
            source_file.write(code.encode())
            source_path = source_file.name

        compile_cmd = ["javac", source_path]
        compile_result = self.run_subprocess(compile_cmd)

        if "error" in compile_result["output"]:
            return compile_result

        class_name = os.path.basename(source_path).replace(".java", "")
        return self.run_subprocess(["java", "-cp", os.path.dirname(source_path), class_name])

    def compile_python(self, code):
        """Runs Python code"""
        return self.run_subprocess(["python", "-c", code])
