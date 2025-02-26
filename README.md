# Yamavel: Laravel YAML Generator

**Yamavel** is a powerful Python package that automates the generation of **Laravel migrations**, **Eloquent models**, and **Filament resources** from a simple YAML schema. Whether you're building a new Laravel application or extending an existing one, Yamavel saves you time by eliminating repetitive boilerplate code.

With Yamavel, you can:

- Define your database schema and relationships in a clean, human-readable YAML file.
- Automatically generate **migrations** to create or update database tables.
- Generate **Eloquent models** with relationships and configurations.
- Create **Filament resources** with forms and tables for easy CRUD management.

---

## Features

- **YAML Schema**: Define your database schema, relationships, and Filament configurations in a single YAML file.
- **Migrations**: Automatically generate Laravel migrations with proper column types, indexes, and foreign keys.
- **Models**: Generate Eloquent models with relationships like `hasMany`, `belongsTo`, and more.
- **Filament Resources**: Create Filament resources with forms and tables for seamless admin panel integration.
- **Error Handling**: Robust error handling with custom exceptions for invalid YAML, missing keys, and unsupported configurations.
- **Extensible**: Easily extend Yamavel to support custom column types, relationships, or Filament components.

---

## Installation

### Prerequisites

- Python 3.7 or higher
- Laravel project (for generating migrations, models, and resources)

### Install via Pip

```bash
pip install yamavel
```

### Install from Source

1. Clone the repository:

   ```bash
   git clone https://github.com/suwi-lanji/yamavel.git
   cd yamavel
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

---

## Usage

### Step 1: Define Your YAML Schema

Create a `schema.yaml` file in your Laravel project root. Here's an example:

```yaml
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

Post:
  table: posts
  columns:
    id:
      type: id
    title:
      type: string
    content:
      type: text
    user_id:
      type: unsignedBigInteger
      foreign: users.id
    timestamps:
      type: timestamps
  relations:
    user:
      type: belongsTo
      model: User
  filament:
    form:
      fields:
        - title
        - content
        - user_id
    table:
      columns:
        - id
        - title
        - user_id
```

### Step 2: Run Yamavel

Run the `yamavel` command to generate migrations, models, and Filament resources:

```bash
yamavel --yaml schema.yaml --laravel-root /path/to/your/laravel-project
```

### Step 3: Verify Generated Files

1. **Migrations**:

   - Check the `database/migrations/` directory for migration files like `2024_10_01_123456_create_users_table.php`.

2. **Models**:

   - Check the `app/Models/` directory for model files like `User.php` and `Post.php`.

3. **Filament Resources**:
   - Check the `app/Filament/Resources/` directory for resource files like `UserResource.php` and `PostResource.php`.

### Step 4: Run Migrations

Run the generated migrations to create the tables in your database:

```bash
php artisan migrate
```

### Step 5: Use Filament Resources

Access the Filament admin panel in your Laravel project. You should see the generated resources (e.g., Users, Posts) in the sidebar. Use the forms and tables to manage your data.

## Note: Filament Resource generation still a working progress

## Example YAML Schema

Here’s a more complex example with multiple models and relationships:

```yaml
User:
  table: users
  columns:
    id:
      type: id
    name:
      type: string
    email:
      type: string
      unique: true
    password:
      type: string
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

Post:
  table: posts
  columns:
    id:
      type: id
    title:
      type: string
    content:
      type: text
    user_id:
      type: unsignedBigInteger
      foreign: users.id
    timestamps:
      type: timestamps
  relations:
    user:
      type: belongsTo
      model: User
    comments:
      type: hasMany
      model: Comment
  filament:
    form:
      fields:
        - title
        - content
        - user_id
    table:
      columns:
        - id
        - title
        - user_id

Comment:
  table: comments
  columns:
    id:
      type: id
    content:
      type: text
    post_id:
      type: unsignedBigInteger
      foreign: posts.id
    user_id:
      type: unsignedBigInteger
      foreign: users.id
    timestamps:
      type: timestamps
  relations:
    post:
      type: belongsTo
      model: Post
    user:
      type: belongsTo
      model: User
  filament:
    form:
      fields:
        - content
        - post_id
        - user_id
    table:
      columns:
        - id
        - content
        - post_id
        - user_id
```

---

## Customization

### Supported Column Types

- `id`
- `string`
- `text`
- `integer`
- `timestamps`
- `unsignedBigInteger`

### Supported Relationships

- `hasMany`
- `belongsTo`
- `hasOne`
- `belongsToMany`

### Filament Configuration

- Define form fields and table columns for each model in the `filament` section of the YAML schema.

---

## Contributing

We welcome contributions! Here’s how you can help:

1. **Report Issues**: Found a bug? Open an issue on GitHub.
2. **Suggest Features**: Have an idea for a new feature? Let us know!
3. **Submit Pull Requests**: Fix a bug or add a feature? Submit a PR.

### Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/suwi-lanji/yamavel.git
   cd yamavel
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run tests:
   ```bash
   python -m unittest tests/test_generator.py
   ```

---

## License

Yamavel is open-source software licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Why Yamavel?

- **Save Time**: Automate repetitive tasks and focus on building your application.
- **Consistency**: Ensure consistent naming conventions and configurations across your project.
- **Flexibility**: Easily extend Yamavel to fit your specific needs.

---

## Get Started Today!

Install Yamavel and start generating Laravel migrations, models, and Filament resources in minutes. Say goodbye to boilerplate code and hello to productivity!

```bash
pip install yamavel
```

---

Let me know what you think! Share your feedback, report issues, or contribute to the project on [GitHub](https://github.com/suwi-lanji/yamavel). Happy coding! 🚀
