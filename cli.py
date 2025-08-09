#!/usr/bin/env python3
"""
CLI interface for the cheatsheet generator.
"""
# Add the project root to the path
sys.path.append(str(Path(__file__).resolve().parent))

import argparse
import re
import sys
import yaml
from pathlib import Path
from main import main as run_generator

CHEATSHEET_DIR = Path.cwd() / "cheatsheets"  # assumes this file is in root

def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate technical cheatsheets using Claude AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --topic bash --dry-run              # Test prompt without API call
  python cli.py --topic bash --live                 # Make actual API call
  python cli.py --topic python --verbose            # Verbose output
  python cli.py --help                              # Show this help message
        """
    )
    
    parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="Topic for cheatsheet generation (e.g., bash, python, git)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Run in dry-run mode to validate prompt (default: True)"
    )
    
    parser.add_argument(
        "--live",
        action="store_true",
        help="Make actual API call (overrides --dry-run)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser


def save_cheatsheet(response: str, topic: str, CHEATSHEET_DIR: Path, *args, **kwargs):
# Fix the directory path
CHEATSHEET_DIR = Path.cwd() / "outputs" / "cheatsheets"

# Fix the save_cheatsheet function
def save_cheatsheet(response: str, topic: str, cheatsheet_dir: Path):
    """Save the generated cheatsheet to a YAML file."""
    # Ensure directory exists
    cheatsheet_dir.mkdir(parents=True, exist_ok=True)

    # Create filename with .yml extension
    filename = f"{topic}_cheatsheet.yml"
    filepath = cheatsheet_dir / filename

    try:
        # Extract YAML content if response contains it
        yaml_match = re.search(r'```yaml\s*(.*?)\s*```', response, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            # Validate YAML
            parsed_yaml = yaml.safe_load(yaml_content)
            # Save formatted YAML
            with open(filepath, 'w') as f:
                yaml.dump(parsed_yaml, f, default_flow_style=False, sort_keys=False)
        else:
            # If no YAML found, save the raw response
            with open(filepath, 'w') as f:
                f.write(response)

        print(f"✅ Cheatsheet saved successfully: {filepath}")

    except Exception as e:
        raise RuntimeError(f"Failed to save cheatsheet: {e}")

def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Determine if we should run in dry-run mode
    dry_run = not args.live
    
    if args.verbose:
        print(f"🔧 CLI Arguments:")
        print(f"   Dry run: {dry_run}")
        print(f"   Topic: {args.topic}")
        print(f"   Verbose: {args.verbose}")
    
    try:
        # Run the generator with topic argument
        response: str = run_generator(dry_run=dry_run, topic=args.topic)
        print(response)

        if not response:
            print("❌ No response generated. Exiting.")
            raise RuntimeError("No response generated")
        if not dry_run:
            save_cheatsheet(response, args.topic, CHEATSHEET_DIR)

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()