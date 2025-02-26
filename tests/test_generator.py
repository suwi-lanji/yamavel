import unittest
import os
import shutil
from yamavel.generator import LaravelYamlGenerator
from yamavel.exceptions import (
    InvalidYAMLError,
    UnsupportedColumnTypeError,
    MissingRequiredKeyError,
)


class TestLaravelYamlGenerator(unittest.TestCase):
    def setUp(self):
        """Set up a test Laravel project directory."""
        self.laravel_root = 'test_laravel_project'
        if os.path.exists(self.laravel_root):
            shutil.rmtree(self.laravel_root)
        os.makedirs(self.laravel_root, exist_ok=True)
        os.makedirs(os.path.join(self.laravel_root, 'database/migrations'), exist_ok=True)
        os.makedirs(os.path.join(self.laravel_root, 'app/Models'), exist_ok=True)
        os.makedirs(os.path.join(self.laravel_root, 'app/Filament/Resources'), exist_ok=True)

        # Create a test YAML schema
        self.yaml_file = 'test_schema.yaml'
        with open(self.yaml_file, 'w') as file:
            file.write("""
User:
  table: users
  columns:
    id:
      type: id
    name:
      type: string
      length: 255
    email:
      type: string
      unique: true
    password:
      type: string
      hidden: true
    timestamps:
      type: timestamps
  relations:
    posts:
      type: hasMany
      model: Post
  filament:
    form:
      fields:
        - name
        - email
        - password
    table:
      columns:
        - id
        - name
        - email
            """)

    def tearDown(self):
        """Clean up the test Laravel project directory."""
        if os.path.exists(self.laravel_root):
            shutil.rmtree(self.laravel_root)
        if os.path.exists(self.yaml_file):
            os.remove(self.yaml_file)

    def test_generate_migrations(self):
        """Test migration generation."""
        generator = LaravelYamlGenerator(self.yaml_file, self.laravel_root)
        generator.generate()

        # Check if migration files were created
        migrations_dir = os.path.join(self.laravel_root, 'database/migrations')
        self.assertTrue(len(os.listdir(migrations_dir)) > 0)

        # Check if the 'users' table migration was created
        users_migration = [f for f in os.listdir(migrations_dir) if 'create_users_table' in f]
        self.assertTrue(len(users_migration) == 1)

    def test_generate_models(self):
        """Test model generation."""
        generator = LaravelYamlGenerator(self.yaml_file, self.laravel_root)
        generator.generate()

        # Check if model files were created
        models_dir = os.path.join(self.laravel_root, 'app/Models')
        self.assertTrue(len(os.listdir(models_dir)) > 0)

        # Check if the 'User' model was created
        user_model_path = os.path.join(models_dir, 'User.php')
        self.assertTrue(os.path.exists(user_model_path))

    def test_generate_filament_resources(self):
        """Test Filament resource generation."""
        generator = LaravelYamlGenerator(self.yaml_file, self.laravel_root)
        generator.generate()

        # Check if Filament resource files were created
        resources_dir = os.path.join(self.laravel_root, 'app/Filament/Resources')
        self.assertTrue(len(os.listdir(resources_dir)) > 0)

        # Check if the 'UserResource' was created
        user_resource_path = os.path.join(resources_dir, 'UserResource.php')
        self.assertTrue(os.path.exists(user_resource_path))

    def test_invalid_yaml(self):
        """Test handling of invalid YAML."""
        invalid_yaml_file = 'invalid_schema.yaml'
        with open(invalid_yaml_file, 'w') as file:
            file.write("Invalid: YAML: Content")

        with self.assertRaises(InvalidYAMLError):
            LaravelYamlGenerator(invalid_yaml_file, self.laravel_root)

        os.remove(invalid_yaml_file)

    def test_missing_required_key(self):
        """Test handling of missing required keys."""
        invalid_yaml_file = 'missing_key_schema.yaml'
        with open(invalid_yaml_file, 'w') as file:
            file.write("""
User:
  table: users
            """)

        with self.assertRaises(MissingRequiredKeyError):
            generator = LaravelYamlGenerator(invalid_yaml_file, self.laravel_root)
            generator.generate()
        os.remove(invalid_yaml_file)

    def test_unsupported_column_type(self):
        """Test handling of unsupported column types."""
        invalid_yaml_file = 'unsupported_column_schema.yaml'
        with open(invalid_yaml_file, 'w') as file:
            file.write("""
User:
  table: users
  columns:
    id:
      type: invalid_type
            """)

        with self.assertRaises(UnsupportedColumnTypeError):
            generator = LaravelYamlGenerator(invalid_yaml_file, self.laravel_root)
            generator.generate()

        os.remove(invalid_yaml_file)


if __name__ == '__main__':
    unittest.main()
