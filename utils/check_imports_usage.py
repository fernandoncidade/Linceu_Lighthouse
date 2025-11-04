import os
import ast

def get_imports_and_usage(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    imports = set()
    used = set()

    class ImportVisitor(ast.NodeVisitor):
        def visit_Import(self, node):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])

        def visit_ImportFrom(self, node):
            if node.module:
                imports.add(node.module.split('.')[0])

    class UsageVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            used.add(node.id)

    ImportVisitor().visit(tree)
    UsageVisitor().visit(tree)
    return imports, used

def analyze_project(root_dir):
    results = {}
    exclude_dirs = {'.venv', 'venv', '__pycache__'}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                try:
                    imports, used = get_imports_and_usage(filepath)
                    used_imports = imports & used
                    unused_imports = imports - used
                    results[filepath] = {
                        "imports": imports,
                        "used_imports": used_imports,
                        "unused_imports": unused_imports
                    }

                except SyntaxError:
                    print(f"Arquivo ignorado por erro de sintaxe: {filepath}")

    return results

if __name__ == "__main__":
    project_path = r"C:\Users\ferna\WORK\Projetos_Python\File-Folder-Manager\Panoptes_Patrol"
    report = analyze_project(project_path)

    all_used_imports = set()
    for data in report.values():
        all_used_imports.update(data['used_imports'])

    with open("requirements_detected.txt", "w", encoding="utf-8") as req_file:
        for lib in sorted(all_used_imports):
            req_file.write(f"{lib}\n")

    print("Arquivo requirements_detected.txt gerado com sucesso.")
