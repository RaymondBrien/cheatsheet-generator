#!/usr/bin/env python3
"""
CLI interface for the cheatsheet generator.
"""

import argparse
import sys
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).resolve().parent))

from main import main as run_generator

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
        print()
    
    try:
        # Run the generator with topic argument
        run_generator(dry_run=dry_run, topic=args.topic)
        
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