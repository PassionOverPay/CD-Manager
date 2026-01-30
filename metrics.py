import ast
import os
import csv
from collections import Counter

def analyze_project_to_csv(project_path, output_file="metrics_report.csv"):
    # --- CONFIGURATION ---
    # Folders to completely ignore
    IGNORE_DIRS = {
        'env', 'venv', '.venv', '__pycache__', '.git', '.idea', 
        'build', 'dist', 'node_modules', 'anaconda3', 'site-packages', 'lib'
    }

    # DATA STORAGE
    # Stores where classes are defined: {'ClassName': {'file': '...', 'if_impl': 0, 'dep_out': 0}}
    class_definitions = {}
    
    # Stores how many times a name is CALLED (instantiated/used) globally: {'ClassName': count}
    global_call_counts = Counter()

    print(f"Scanning project: {project_path} ...")
    
    # --- PASS 1: SCAN ALL FILES ---
    for root, dirs, files in os.walk(project_path):
        # Filter directories to avoid scanning libraries
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and "anaconda" not in d.lower()]
        
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, project_path)
                
                try:
                    with open(full_path, "r", encoding="utf-8") as source:
                        tree = ast.parse(source.read())
                    
                    # 1. Calculate Dep_Out (Imports) for this file
                    # We count 'Import' and 'ImportFrom' nodes
                    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
                    file_dep_out = len(imports)
                    
                    # 2. Walk the file to find Classes and Function Calls
                    for node in ast.walk(tree):
                        
                        # Found a Class Definition
                        if isinstance(node, ast.ClassDef):
                            class_definitions[node.name] = {
                                'file': rel_path,
                                'if_impl': len(node.bases), # Parents count
                                'dep_out': file_dep_out     # Based on file imports
                            }
                        
                        # Found a Function/Class Call (e.g. MyClass())
                        elif isinstance(node, ast.Call):
                            if isinstance(node.func, ast.Name):
                                global_call_counts[node.func.id] += 1
                                
                except Exception:
                    # Skip files that fail to parse
                    pass

    # --- PASS 2: WRITE TO CSV ---
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            # Write Header
            writer.writerow(['Class Name', 'File Location', 'IFImpl (Parents)', 'Dep_Out (Imports)', 'InstSpec (Usage)'])
            
            # Write Data (Sorted by Class Name)
            sorted_classes = sorted(class_definitions.keys())

            for class_name in sorted_classes:
                data = class_definitions[class_name]
                inst_spec = global_call_counts[class_name]
                
                writer.writerow([
                    class_name, 
                    data['file'], 
                    data['if_impl'], 
                    data['dep_out'], 
                    inst_spec
                ])
                
        print(f"\nSuccess! Metrics saved to: {os.path.abspath(output_file)}")
        
    except PermissionError:
        print(f"\nError: Could not write to {output_file}. Is the file open in Excel?")

if __name__ == "__main__":
    # --- TARGET PATH ---
    target_path = r"F:\repo\MSIC_CD-Tracker"
    
    if os.path.exists(target_path):
        analyze_project_to_csv(target_path)
    else:
        print(f"Error: Path not found: {target_path}")