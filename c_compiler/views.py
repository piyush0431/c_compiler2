# c_compiler/views.py
from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import logging
import os

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def compile_and_run_c_program(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')

        try:
            # Save the C code to a temporary file
            with open('temp.c', 'w') as file:
                file.write(code)

            # Log the received code
            logger.info("Code received: %s", code)

            # Run the compilation command
            compile_command = ['gcc', 'temp.c', '-o', 'temp']
            logger.info("Compile command: %s", ' '.join(compile_command))
            compile_result = subprocess.run(compile_command, capture_output=True, text=True, cwd=os.getcwd())

            # Check the compilation result
            if compile_result.returncode == 0:
                # Run the compiled program
                run_command = ['./temp']
                logger.info("Run command: %s", ' '.join(run_command))
                run_result = subprocess.run(run_command, capture_output=True, text=True, cwd=os.getcwd())

                # Check the execution result
                if run_result.returncode == 0:
                    return JsonResponse({'output': run_result.stdout})
                else:
                    return JsonResponse({'error': f'Execution failed. Error message:\n{run_result.stderr}'}, status=500)
            else:
                return JsonResponse({'error': f'Compilation failed. Error message:\n{compile_result.stderr}'}, status=500)

        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': f'Command failed with return code {e.returncode}. Output:\n{e.output.decode()}'}, status=500)
        except Exception as e:
            logger.exception("Error during compilation and execution:")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)