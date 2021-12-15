import os
import time

script_name = 'main.py'
index = 141244


for param in range(50, 501, 50):
        start_time = time.time()
        os.system(f"python {script_name} {index}_{param}.txt")
        end_time = time.time()
        print(f'{index} \t {param} \t {(end_time - start_time)*1000}')
