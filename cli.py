import argparse

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="CLI for interacting with the Anthropic API.")
    
    parser.add_argument(
        "--model", 
        type=str, 
        help="The model to use for the request."
    )
    
    parser.add_argument(
        "--role", 
        type=str, 
        choices=["user", "assistant"], 
        default="user", 
        help="The role of the message sender."
    )
    
    parser.add_argument(
        "--content", 
        type=str, 
        required=True, 
        help="The content of the message."
    )
    
    parser.add_argument(
        "--dry-run",
        action='store_true',
        help="If set, the script will not send any requests to the API, just print the parameters and prompt content."
    )

    return parser.parse_args()