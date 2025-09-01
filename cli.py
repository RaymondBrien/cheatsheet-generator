#!/usr/bin/env python3
"""
CLI interface for the cheatsheet generator.
"""
# Add the project root to the path
# sys.path.append(str(Path(__file__).resolve().parent))

import argparse
import re
import sys
from pathlib import Path

import yaml

from config.lib_config import CHEATSHEET_DIR
from main import main as run_generator
from utils.file_management import (save_cheatsheet, save_response_data,
                                   save_voiceover_script)
from utils.general_utils import make_version
from utils.voiceover import generate_dry_run_voiceover, generate_voiceover

# ============ CLI ARGUMENTS =================

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
  python cli.py --topic bash --dry-run --voiceover  # Dry run with voiceover recording
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
    
    parser.add_argument(
        "--voiceover",
        action="store_true",
        help="Generate voiceover recording during dry run"
    )
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Determine if we should run in dry-run mode
    dry_run = not args.live
    
    if args.verbose:
        print("🔧 CLI Arguments:")
        print(f"   Dry run: {dry_run}")
        print(f"   Topic: {args.topic}")
        print(f"   Verbose: {args.verbose}")
        print(f"   Voiceover: {args.voiceover}")
    
    try:
        # Run the generator with topic argument
        response: str = run_generator(dry_run=dry_run, topic=args.topic)
        print(response)

        if not response:
            raise RuntimeError("No response generated, exited")
            
        # Generate voiceover during dry run if requested
        if dry_run and args.voiceover:
            print("\n🎵 Generating voiceover recording for dry run...")
            try:
                # Get prompt text from the response for voiceover generation
                prompt_text = response if isinstance(response, str) else str(response)
                voiceover_file = generate_dry_run_voiceover(args.topic, prompt_text)
                print(f"🎤 Voiceover recording completed: {voiceover_file}")
            except Exception as e:
                print(f"⚠️  Voiceover generation failed: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
        
        if not dry_run:
            saved_files = save_response_data(response, args.topic)
            if args.voiceover:
                # Generate voiceover script if not in dry run mode
                voiceover_file = generate_voiceover(response, args.topic)
                saved_files.append(voiceover_file)
            if len(saved_files) == 2 and saved_files[1]:
                print("✅ Saved both cheatsheet and voiceover script")
            else:
                print("✅ Saved cheatsheet only")

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