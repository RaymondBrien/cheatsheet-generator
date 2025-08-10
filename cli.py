#!/usr/bin/env python3
"""
CLI interface for the cheatsheet generator.
"""
# Add the project root to the path
# sys.path.append(str(Path(__file__).resolve().parent))

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
        "-t", "--topic",
        type=str,
        required=True,
        help="Topic for cheatsheet generation (e.g., bash, python, git)"
    )
    
    parser.add_argument(
        "-dr", "--dry-run",
        action="store_true",
        default=True,
        help="Run in dry-run mode to validate prompt (default: True)"
    )
    
    parser.add_argument(
        "-l", "--live",
        action="store_true",
        help="Make actual API call (overrides --dry-run)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser


def make_version() -> str:
    """Generate a version string based on the current date."""
    from datetime import datetime
    return str(datetime.now().strftime("%Y%m%d_%H%M%S"))

CHEATSHEET_DIR = Path.cwd() / "outputs" / "cheatsheets"

def save_cheatsheet(response: str, topic: str):
    """Save the generated cheatsheet to a YAML file."""
    # Ensure directory exists
    CHEATSHEET_DIR.mkdir(parents=True, exist_ok=True)
    version =  make_version()
    # Create filename with .yml extension
    filename = f"{topic}_cheatsheet_{version}.yml"
    filepath = CHEATSHEET_DIR / filename

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

        # check file made successfully
        if not filepath.exists():
            raise RuntimeError(f"Failed to create cheatsheet file: {filepath}")
        print(f"✅ Cheatsheet saved successfully: {filepath}")

        return filepath
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
            save_cheatsheet(response, args.topic)

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