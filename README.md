# Static Site Generator

A simple Python-based static site generator that converts Markdown files into a fully-functional HTML website.

## Features

- **Markdown to HTML**: Converts recursive directories of Markdown files.
- **Template System**: Uses a central `template.html` for consistent styling.
- **Static Asset Handling**: Automatically copies CSS and images to the build directory.
- **Live Preview**: Includes a shell script to build and serve the site locally.

## Project Structure

- `src/`: The Python source code for parsing and generation.
- `content/`: Where you write your Markdown files.
- `static/`: Static assets (CSS, images) to be included in the build.
- `template.html`: The HTML shell for your site.
- `docs/` / `public/`: The output directories for the generated site.

## How to Use

1. **Build and Serve**:
   Run the following command to generate the site and start a local development server:
   ```bash
   ./main.sh
   ```

2. **Run Tests**:
   To ensure everything is working correctly:
   ```bash
   ./test.sh
   ```

## Requirements

- Python 3.x
