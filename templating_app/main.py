"""
Markdown Templating App for Programming Cheatsheets and Music Theory Resources
A scalable system for generating professional PDF and HTML documents from markdown templates
"""

import os
import yaml
import jinja2
import subprocess
from markdown import Markdown
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import doctest
import shutil

# --------- Music specific imports ---------
try:
    from music21 import interval, note, stream
    MUSIC_SUPPORT = True
except ImportError:
    MUSIC_SUPPORT = False
# -------------------------------------------

from config.lib_config import CHEATSHEET_DIR, TOPIC_DIR, APP_NAME, DEFAULT_DIR, TEMPLATE_DIR

@dataclass  # TODO add to utils
class Utils:
    date: datetime = str(datetime.now().year)
    last_checked: datetime = str(datetime.now())


class TemplatingApp:
    """Main application for processing markdown templates into PDFs and HTML"""
    
    def __init__(self, project_root: str = "."):  # TODO project root not configured correctly, needs work
        self.project_root = Path(project_root)
        self.setup_directories()
        self.setup_jinja_environment()
        self.config = self.load_global_config()
        self.markdown_processor = Markdown(extensions=['codehilite', 'toc'])
        
    def setup_directories(self):
        """Create project directory structure"""
        directories = [
            "templates/base",
            "templates/styles", 
            "content/",
            "output/pdf",
            "output/html",
            "tests",
            "config"
        ]
        
        for directory in directories:
            (self.project_root / directory).mkdir(parents=True, exist_ok=True)
    
    def setup_jinja_environment(self):
        """Configure Jinja2 environment with custom functions"""
        template_dir = self.project_root / "templates"
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom functions to templates
        self.jinja_env.globals.update({
            'current_year': lambda: datetime.now().year,
            'current_date': lambda fmt='%Y-%m-%d': datetime.now().strftime(fmt),
            'copyright_notice': self.generate_copyright
        })
    
    def load_global_config(self) -> Dict:
        """Load global configuration settings"""
        config_file = self.project_root / "config" / "global.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        return self.create_default_config()
    
    def create_default_config(self) -> Dict:
        """Create default configuration"""
        config = {
            'author': 'Your Name',
            'organization': 'Your Organization',
            'copyright_start_year': 2024,
            'pandoc': {
                'pdf_engine': 'xelatex',
                'template': 'templates/styles/custom.latex',
                'variables': {
                    'geometry': 'margin=1in',
                    'fontfamily': 'libertine',
                    'colorlinks': True
                }
            },
            'output_formats': ['pdf', 'html']
        }
        
        # Save default config
        config_file = self.project_root / "config" / "global.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        return config
    
    def generate_copyright(self) -> str:
        """Generate copyright notice with dynamic year range"""
        start_year = self.config.get('copyright_start_year', 2024)
        current_year = datetime.now().year
        
        if start_year == current_year:
            year_range = str(current_year)
        else:
            year_range = f"{start_year}-{current_year}"
            
        return f"© {year_range} {self.config.get('author', 'Author')}"
    
    def load_content_config(self, content_dir: Path) -> Dict:
        """Load content-specific configuration"""
        config_file = content_dir / "config.yaml"
        if not config_file.exists():
            raise FileNotFoundError(f"No config.yaml found in {content_dir}")
        
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def render_template(self, template_name: str, context: Dict) -> str:
        """Render Jinja2 template with given context"""
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except jinja2.TemplateError as e:
            raise RuntimeError(f"Template rendering error: {e}")
    
    def validate_markdown(self, markdown_file: Path) -> bool:
        """Validate markdown file structure and content"""
        # TODO: Implement markdownlint integration
        # For now, basic validation
        if not markdown_file.exists():
            return False
        
        # Check file is not empty
        if markdown_file.stat().st_size == 0:
            return False
            
        # TODO: Add spell checking with pyspellchecker
        # TODO: Add custom validation rules
        return True
    
    def run_doctest(self, markdown_content: str) -> bool:
        """Run doctest on code blocks in markdown content"""
        # Extract Python code blocks and run doctests
        # This is a simplified version - you'd want more robust extraction
        try:
            # TODO: Extract Python code blocks and run doctest.testmod()
            return True
        except Exception as e:
            print(f"Doctest failed: {e}")
            return False
    
    def compile_templates(self, content_dir: Path) -> str:
        """Compile multiple template sections into single markdown document"""
        content_config = self.load_content_config(content_dir)
        
        # Load content data
        content_file = content_dir / "content.yaml"
        if content_file.exists():
            with open(content_file, 'r') as f:
                content_data = yaml.safe_load(f)
        else:
            content_data = {}
        
        # Merge global config with content-specific config
        context = {
            **self.config,
            **content_config,
            **content_data
        }
        
        # Determine template to use
        template_name = content_config.get('template', 'base/default.md.j2')
        
        # Render the template
        markdown_content = self.render_template(template_name, context)
        
        return markdown_content

    def convert_to_pdf(self, markdown_content: str, output_file: Path):
        """Dead simple PDF conversion"""
        temp_md = self.project_root / "temp.md"
        with open(temp_md, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        try:
            # Minimal pandoc command - no custom template
            cmd = ['pandoc', str(temp_md), '-o', str(output_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Pandoc error: {result.stderr}")
                raise RuntimeError(f"Pandoc failed: {result.stderr}")

        finally:
            if temp_md.exists():
                temp_md.unlink()



    #     try:
    #         # Build pandoc command
    #         cmd = [
    #             'pandoc',
    #             '-s',
    #             str(temp_md),
    #             '-o', str(output_file),
    #             '--pdf-engine', self.config['pandoc']['pdf_engine'],
    #             # '--no-highlight',
    #             '--listings'
    #         ]
            
    #         # Add template if exists
    #         template_file = self.project_root / self.config['pandoc']['template']
    #         if template_file.exists():
    #             cmd.extend(['--template', str(template_file)])
            
    #         # Add variables
    #         for var, value in self.config['pandoc']['variables'].items():
    #             cmd.extend(['-V', f"{var}={value}"])
            
    #         # Run pandoc
    #         result = subprocess.run(cmd, capture_output=True, text=True)
    #         if result.returncode != 0:
    #             raise RuntimeError(f"Pandoc error: {result.stderr}")
                
    #     finally:
    #         # Clean up temp file
    #         if temp_md.exists():
    #             temp_md.unlink()
    
    def convert_to_html(self, markdown_content: str, output_file: Path):
        """Convert markdown to HTML using pandoc"""
        temp_md = self.project_root / "temp.md"
        with open(temp_md, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        try:
            cmd = [
                'pandoc',
                str(temp_md),
                '-o', str(output_file),
                '--standalone',
                '--self-contained'
            ]
            
            # Add CSS if exists
            css_file = self.project_root / "templates/styles/main.css"
            if css_file.exists():
                cmd.extend(['--css', str(css_file)])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Pandoc HTML error: {result.stderr}")
                
        finally:
            if temp_md.exists():
                temp_md.unlink()
    
    def process_single_document(self, content_dir: Path):
        """Process a single document from content directory"""
        print(f"Processing: {content_dir.name}")
        # Compile templates
        markdown_content = self.compile_templates(content_dir)
        
        # Validate
        temp_md = self.project_root / "temp_validation.md"
        with open(temp_md, 'w') as f:
            f.write(markdown_content)
        
        if not self.validate_markdown(temp_md):
            print(f"Validation failed for {content_dir.name}")
            return False
        
        # Run doctests if enabled
        if self.config.get('run_doctests', True):
            if not self.run_doctest(markdown_content):
                print(f"Doctest failed for {content_dir.name}")
        
        # Generate outputs
        output_name = content_dir.name
        
        for format_type in self.config['output_formats']:
            if format_type == 'pdf':
                output_file = self.project_root / "output/pdf" / f"{output_name}.pdf"
                self.convert_to_pdf(markdown_content, output_file)
                print(f"  ✓ PDF: {output_file}")
                
            elif format_type == 'html':
                output_file = self.project_root / "output/html" / f"{output_name}.html"
                self.convert_to_html(markdown_content, output_file)
                print(f"  ✓ HTML: {output_file}")
        
        # Cleanup
        if temp_md.exists():
            temp_md.unlink()
        
        return True
    
    def batch_process(self):
        """Process all documents in content directory"""
        content_dir = self.project_root / "content"
        
        if not content_dir.exists():
            print("No content directory found")
            return
        
        processed_count = 0
        failed_count = 0
        
        # Process each subdirectory in content/
        for item in content_dir.iterdir():
            if item.is_dir():
                try:
                    if self.process_single_document(item):
                        processed_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    print(f"Error processing {item.name}: {e}")
                    failed_count += 1
        
        print(f"\nBatch processing complete:")
        print(f"  ✓ Processed: {processed_count}")
        print(f"  ✗ Failed: {failed_count}")


def main():
    """Main entry point"""
    # breakpoint()
    app = TemplatingApp()
    
    # Example usage
    if len(os.sys.argv) > 1:
        command = os.sys.argv[1]
        if command == "batch":
            app.batch_process()
        elif command == "single" and len(os.sys.argv) > 2:
            content_path = Path(os.sys.argv[2])
            app.process_single_document(content_path)
        else:
            print("Usage: python templating_app.py [batch|single <content_dir>]")
    else:
        print("Running batch process...")
        app.batch_process()


if __name__ == "__main__":
    main()
