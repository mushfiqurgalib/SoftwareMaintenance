import os
import difflib

def find_changes_in_solidity_file(file_path1, file_path2):
    try:
        with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()

            differ = difflib.Differ()
            diff = list(differ.compare(lines1, lines2))

            added_lines = []
            deleted_lines = []
            modified_lines = []
            added_lines_count = 0
            deleted_lines_count = 0
            for i, line in enumerate(diff, 1):
                if line.startswith('+ '):
                    added_lines_count += 1 
                    added_lines.append((i, line[2:]))
                elif line.startswith('- '):
                    deleted_lines_count += 1
                    deleted_lines.append((i, line[2:]))
                elif line.startswith('? '):
                    modified_lines.append((i, line[2:]))

            return added_lines, deleted_lines, modified_lines, added_lines_count, deleted_lines_count
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return [], [], [], 0, 0

def count_changes_in_folders(folder_path1, folder_path2):
    changed_files = []
    total_added_lines_count = 0
    total_deleted_lines_count = 0

    for root, _, files in os.walk(folder_path1):
        for file in files:
            file_path1 = os.path.join(root, file)
            file_path2 = os.path.join(folder_path2, file)
            
            if os.path.exists(file_path2):
                added, deleted, modified, added_lines_count, deleted_lines_count = find_changes_in_solidity_file(file_path1, file_path2)
                total_added_lines_count += added_lines_count
                total_deleted_lines_count += deleted_lines_count
                if added or deleted or modified:
                    changed_files.append((file, added, deleted, modified))

    return changed_files, total_added_lines_count, total_deleted_lines_count

# Example usage:
folder_path1 = './solidity-examples - Copy/solidity-examples-master/examples'
folder_path2 = './solidity-examples/solidity-examples-master/examples'
changed_files, total_added_lines, total_deleted_lines = count_changes_in_folders(folder_path1, folder_path2)

for file, added, deleted, modified in changed_files:
    print(f"File: {file}")
   
    if added:
        print("Added Lines:")
        for line_num, line_text in added:
            print(f"Line {line_num}: {line_text}")

    if deleted:
        print("Deleted Lines:")
        for line_num, line_text in deleted:
            print(f"Line {line_num}: {line_text}")

    print()
    
print(f"Total number of added lines in all files: {total_added_lines}")
print(f"Total number of deleted lines in all files: {total_deleted_lines}")
print(f"Total number of changes: {total_added_lines + total_deleted_lines}")
