file_path_to_modify = './result/draw/test_result_T=0.2.txt'

def modify_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace \ta\ with /ta/
    modified_content = content.replace('\\ta', '/ta')

    new_file_path = './result/draw/test_result_T=0.2.txt'
    with open(new_file_path, 'w') as file:
        file.write(modified_content)
    return new_file_path

new_file_path = modify_file(file_path_to_modify)
new_file_path