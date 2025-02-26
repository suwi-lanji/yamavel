import os

def read_file(file_path):
    """Read the contents of a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as file:
        return file.read()


def write_file(file_path, content):
    """Write content to a file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(content)


def check_table_exists(laravel_root, table_name):
    """Check if a table exists in the Laravel project."""
    migrations_dir = os.path.join(laravel_root, 'database/migrations')
    if not os.path.exists(migrations_dir):
        return False
    for filename in os.listdir(migrations_dir):
        if f"create_{table_name}_table" in filename:
            return True
    return False


def check_column_exists(laravel_root, table_name, column_name):
    """Check if a column exists in a table."""
    migrations_dir = os.path.join(laravel_root, 'database/migrations')
    if not os.path.exists(migrations_dir):
        return False
    for filename in os.listdir(migrations_dir):
        if f"create_{table_name}_table" in filename:
            migration_content = read_file(os.path.join(migrations_dir, filename))
            if f"$table->" in migration_content and f"'{column_name}'" in migration_content:
                return True
    return False