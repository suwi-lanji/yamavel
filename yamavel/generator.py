import os
import yaml
import argparse
from datetime import datetime
from inflection import tableize
from .utils import check_column_exists, read_file, write_file, check_table_exists
from .exceptions import (
    InvalidYAMLError,
    MissingYAMLFileError,
    UnsupportedColumnTypeError,
    MissingRequiredKeyError,
    InvalidRelationError,
    FileWriteError,
    FileReadError,
)


class LaravelYamlGenerator:
    def __init__(self, yaml_file, laravel_root):
        """
        Initialize the Laravel YAML Generator.

        Args:
            yaml_file (str): Path to the YAML schema file.
            laravel_root (str): Path to the root of the Laravel project.
        """
        self.yaml_file = yaml_file
        self.laravel_root = laravel_root
        self.schema = self._load_schema()

    def _load_schema(self):
        """
        Load the YAML schema file.

        Returns:
            dict: Parsed YAML schema.

        Raises:
            MissingYAMLFileError: If the YAML file does not exist.
            InvalidYAMLError: If the YAML file is invalid.
        """
        if not os.path.exists(self.yaml_file):
            raise MissingYAMLFileError(self.yaml_file)

        try:
            with open(self.yaml_file, 'r') as file:
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise InvalidYAMLError(f"Error parsing YAML file: {e}")

    def generate(self):
        """
        Generate migrations, models, and Filament resources based on the YAML schema.
        """
        for model_name, config in self.schema.items():
            self._generate_migration(model_name, config)
            self._generate_model(model_name, config)
            self._generate_filament_resource(model_name, config)

    def _generate_migration(self, model_name, config):
        """
        Generate a migration file for the given model.

        Args:
            model_name (str): Name of the model.
            config (dict): Configuration for the model.

        Raises:
            MissingRequiredKeyError: If the 'columns' key is missing.
            TableAlreadyExistsError: If the table already exists.
            FileReadError: If there is an error reading the migration stub.
            FileWriteError: If there is an error writing the migration file.
        """
        table_name = config.get('table', tableize(model_name))
        columns = config.get('columns', {})

        if not columns:
            raise MissingRequiredKeyError('columns')

        if check_table_exists(self.laravel_root, table_name):
            self._generate_update_migration(table_name, columns)
        else:
            self._create_new_migration(table_name, columns)

    def _create_new_migration(self, table_name, columns):
        """
        Create a new migration file for a table that does not exist.

        Args:
            table_name (str): Name of the table.
            columns (dict): Column configurations.

        Raises:
            FileReadError: If there is an error reading the migration stub.
            FileWriteError: If there is an error writing the migration file.
        """
        try:
            migration_stub = read_file(os.path.join(os.path.dirname(__file__), 'stubs/migration.stub'))
        except Exception:
            raise FileReadError("Failed to read migration stub.")

        column_definitions = self._generate_column_definitions(columns)
        stub = migration_stub.replace('{{table}}', table_name)
        stub = stub.replace('{{columns}}', column_definitions)

        timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')
        filename = f"{timestamp}_create_{table_name}_table.php"
        file_path = os.path.join(self.laravel_root, 'database/migrations', filename)

        try:
            write_file(file_path, stub)
        except Exception:
            raise FileWriteError(file_path)

    def _generate_update_migration(self, table_name, columns):
        """
        Generate an update migration file for an existing table.

        Args:
            table_name (str): Name of the table.
            columns (dict): Column configurations.

        Raises:
            FileReadError: If there is an error reading the migration stub.
            FileWriteError: If there is an error writing the migration file.
        """
        try:
            migration_stub = read_file(os.path.join(os.path.dirname(__file__), 'stubs/update_migration.stub'))
        except Exception:
            raise FileReadError("Failed to read update migration stub.")

        column_definitions = self._generate_update_column_definitions(table_name, columns)
        stub = migration_stub.replace('{{table}}', table_name)
        stub = stub.replace('{{columns}}', column_definitions)

        timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')
        filename = f"{timestamp}_update_{table_name}_table.php"
        file_path = os.path.join(self.laravel_root, 'database/migrations', filename)

        try:
            write_file(file_path, stub)
        except Exception:
            raise FileWriteError(file_path)

    def _generate_update_column_definitions(self, table_name, columns):
        """
        Generate column definitions for an update migration.

        Args:
            table_name (str): Name of the table.
            columns (dict): Column configurations.

        Returns:
            str: Column definitions as a string.
        """
        definitions = []
        for column_name, column_config in columns.items():
            if not check_column_exists(self.laravel_root, table_name, column_name):
                column_type = column_config.get('type', 'string')
                if column_type not in ['id', 'string', 'text', 'integer', 'timestamps', 'unsignedBigInteger']:
                    raise UnsupportedColumnTypeError(column_type)

                definition = f"$table->{column_type}('{column_name}')"
                if column_config.get('unique'):
                    definition += '->unique()'
                if column_config.get('foreign'):
                    definition += f"->foreign('{column_name}')->references('id')->on('{column_config['foreign']}')"
                definitions.append(definition + ";")  # Add semicolon to each definition

        return "\n            ".join(definitions)

    def _generate_column_definitions(self, columns):
        """
        Generate column definitions for migrations.

        Args:
            columns (dict): Column configurations.

        Returns:
            str: Column definitions as a string.

        Raises:
            UnsupportedColumnTypeError: If an unsupported column type is specified.
        """
        definitions = []
        for column_name, column_config in columns.items():
            column_type = column_config.get('type', 'string')
            if column_type not in ['id', 'string', 'text', 'integer', 'timestamps', 'unsignedBigInteger']:
                raise UnsupportedColumnTypeError(column_type)

            definition = f"$table->{column_type}('{column_name}')"
            if column_config.get('unique'):
                definition += '->unique()'
            if column_config.get('foreign'):
                definition += f"->foreign('{column_name}')->references('id')->on('{column_config['foreign']}')"
            definitions.append(definition + ";")  # Add semicolon to each definition

        return "\n            ".join(definitions)

    def _generate_model(self, model_name, config):
        """
        Generate a model file for the given model.

        Args:
            model_name (str): Name of the model.
            config (dict): Configuration for the model.

        Raises:
            FileReadError: If there is an error reading the model stub.
            FileWriteError: If there is an error writing the model file.
        """
        try:
            model_stub = read_file(os.path.join(os.path.dirname(__file__), 'stubs/model.stub'))
        except Exception:
            raise FileReadError("Failed to read model stub.")

        model_stub = model_stub.replace('{{model}}', model_name)
        model_stub = model_stub.replace('{{table}}', config.get('table', tableize(model_name)))

        relations = self._generate_relations(config.get('relations', {}))
        model_stub = model_stub.replace('{{relations}}', relations)

        model_path = os.path.join(self.laravel_root, 'app/Models', f"{model_name}.php")
        if not os.path.exists(model_path):
            try:
                write_file(model_path, model_stub)
            except Exception:
                raise FileWriteError(model_path)
        else:
            print(f"Model {model_name} already exists. Skipping...")

    def _generate_relations(self, relations):
        """
        Generate relationship methods for the model.

        Args:
            relations (dict): Relationship configurations.

        Returns:
            str: Relationship methods as a string.

        Raises:
            InvalidRelationError: If an invalid relationship type is specified.
        """
        relation_methods = []
        for relation_name, relation_config in relations.items():
            relation_type = relation_config.get('type')
            if relation_type not in ['hasMany', 'belongsTo', 'hasOne', 'belongsToMany']:
                raise InvalidRelationError(relation_type)

            related_model = relation_config.get('model')
            relation_methods.append(
                f"public function {relation_name}() {{\n"
                f"    return $this->{relation_type}({related_model}::class);\n"
                f"}}"
            )
        return "\n\n".join(relation_methods)

    def _generate_filament_resource(self, model_name, config):
        """
        Generate a Filament resource file for the given model.

        Args:
            model_name (str): Name of the model.
            config (dict): Configuration for the model.

        Raises:
            FileReadError: If there is an error reading the Filament resource stub.
            FileWriteError: If there is an error writing the Filament resource file.
        """
        try:
            resource_stub = read_file(os.path.join(os.path.dirname(__file__), 'stubs/filament_resource.stub'))
        except Exception as e:
            raise FileReadError(f"Failed to read Filament resource stub: {e}")

        resource_stub = resource_stub.replace('{{model}}', model_name)

        form_fields = self._generate_form_fields(config.get('filament', {}).get('form', {}).get('fields', []))
        table_columns = self._generate_table_columns(config.get('filament', {}).get('table', {}).get('columns', []))

        resource_stub = resource_stub.replace('{{formFields}}', form_fields)
        resource_stub = resource_stub.replace('{{tableColumns}}', table_columns)

        resource_path = os.path.join(self.laravel_root, 'app/Filament/Resources', f"{model_name}Resource.php")
        if not os.path.exists(resource_path):
            try:
                write_file(resource_path, resource_stub)
            except Exception:
                raise FileWriteError(resource_path)
        else:
            print(f"Filament resource for {model_name} already exists. Skipping...")

    def _generate_form_fields(self, fields):
        """
        Generate form fields for Filament resources.

        Args:
            fields (list): List of form fields.

        Returns:
            str: Form fields as a string.
        """
        return ",\n                ".join([fr"Forms\Components\TextInput::make('{field}')" for field in fields])

    def _generate_table_columns(self, columns):
        """
        Generate table columns for Filament resources.

        Args:
            columns (list): List of table columns.

        Returns:
            str: Table columns as a string.
        """
        return ",\n                ".join([fr"Tables\Columns\TextColumn::make('{column}')" for column in columns])


def main():
    """Entry point for the yamavel command-line tool."""
    parser = argparse.ArgumentParser(description="Generate Laravel migrations, models, and Filament resources from YAML.")
    parser.add_argument('--yaml', required=True, help="Path to the YAML schema file.")
    parser.add_argument('--laravel-root', required=True, help="Path to the Laravel project root.")
    args = parser.parse_args()

    try:
        generator = LaravelYamlGenerator(args.yaml, args.laravel_root)
        generator.generate()
        print("YAML schema processed successfully!")
    except (InvalidYAMLError, MissingYAMLFileError) as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
