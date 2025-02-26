class LaravelYamlGeneratorError(Exception):
    """Base exception for all Laravel YAML Generator errors."""
    pass


class InvalidYAMLError(LaravelYamlGeneratorError):
    """Raised when the YAML schema is invalid or cannot be parsed."""
    def __init__(self, message="Invalid YAML schema provided."):
        self.message = message
        super().__init__(self.message)


class MissingYAMLFileError(LaravelYamlGeneratorError):
    """Raised when the specified YAML file does not exist."""
    def __init__(self, file_path):
        self.message = f"The YAML file '{file_path}' does not exist."
        super().__init__(self.message)


class UnsupportedColumnTypeError(LaravelYamlGeneratorError):
    """Raised when an unsupported column type is specified in the YAML schema."""
    def __init__(self, column_type):
        self.message = f"Unsupported column type: '{column_type}'."
        super().__init__(self.message)


class MissingRequiredKeyError(LaravelYamlGeneratorError):
    """Raised when a required key is missing in the YAML schema."""
    def __init__(self, key):
        self.message = f"Missing required key: '{key}'."
        super().__init__(self.message)


class TableAlreadyExistsError(LaravelYamlGeneratorError):
    """Raised when attempting to create a table that already exists."""
    def __init__(self, table_name):
        self.message = f"The table '{table_name}' already exists."
        super().__init__(self.message)


class ColumnAlreadyExistsError(LaravelYamlGeneratorError):
    """Raised when attempting to add a column that already exists in a table."""
    def __init__(self, column_name, table_name):
        self.message = f"The column '{column_name}' already exists in the table '{table_name}'."
        super().__init__(self.message)


class InvalidRelationError(LaravelYamlGeneratorError):
    """Raised when an invalid relationship type is specified in the YAML schema."""
    def __init__(self, relation_type):
        self.message = f"Invalid relationship type: '{relation_type}'."
        super().__init__(self.message)


class FileWriteError(LaravelYamlGeneratorError):
    """Raised when there is an error writing to a file."""
    def __init__(self, file_path):
        self.message = f"Failed to write to file: '{file_path}'."
        super().__init__(self.message)


class FileReadError(LaravelYamlGeneratorError):
    """Raised when there is an error reading a file."""
    def __init__(self, file_path):
        self.message = f"Failed to read file: '{file_path}'."
        super().__init__(self.message)
