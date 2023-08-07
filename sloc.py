def count_lines_solidity_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            line_count = sum(1 for line in lines if line.strip() and not line.strip().startswith('//'))
            return line_count
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return 0

# Example usage:
file_path = './sample.sol'
line_count = count_lines_solidity_file(file_path)
print(f"SLOC: {line_count}")
