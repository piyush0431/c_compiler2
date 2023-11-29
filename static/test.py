import subprocess

def compile_and_run_c_program(source_code, output_filename='output'):
    # Save the C code to a temporary file
    with open('temp.c', 'w') as file:
        file.write(source_code)

    # Run the compilation command
    compile_command = ['gcc', 'temp.c', '-o', output_filename]
    compile_result = subprocess.run(compile_command, capture_output=True, text=True)

    # Check the compilation result
    if compile_result.returncode == 0:
        # Run the compiled program
        run_command = [f'./{output_filename}']
        run_result = subprocess.run(run_command, capture_output=True, text=True)

        # Check the execution result
        if run_result.returncode == 0:
            return f"Compilation and execution successful. Output:\n{run_result.stdout}"
        else:
            return f"Compilation successful, but execution failed. Error message:\n{run_result.stderr}"
    else:
        return f"Compilation failed. Error message:\n{compile_result.stderr}"

# Example C code
c_code = """
#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}
"""

# Compile and run the C program
result_message = compile_and_run_c_program(c_code)

# Print the result
print(result_message)
