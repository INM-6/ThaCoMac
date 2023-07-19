# self-written public library
def clear_file(file_path):
    with open(file_path, 'w') as f:
        f.truncate()
        f.close()