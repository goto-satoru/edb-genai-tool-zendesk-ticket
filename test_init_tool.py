#!/usr/bin/env python3

import os
from dotenv import load_dotenv
# from tool import init_tool
from tool_requests import init_tool

# Load environment variables
load_dotenv()

def main():
    print("=" * 70)
    print("Testing tool.py via init_tool()")
    print("=" * 70)
    print()
    
    # Check environment variables
    required_vars = ['ZENDESK_URL', 'ZENDESK_EMAIL', 'ZENDESK_TOKEN']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease create a .env file with:")
        for var in required_vars:
            print(f"  {var}=your_value_here")
        return
    
    print("✓ Environment variables loaded")
    print(f"  ZENDESK_URL: {os.environ.get('ZENDESK_URL')}")
    print(f"  ZENDESK_EMAIL: {os.environ.get('ZENDESK_EMAIL')}")
    print(f"  ZENDESK_TOKEN: {'*' * 20}")
    print()
    
    # Initialize the tool using init_tool()
    print("Calling init_tool()...")
    try:
        zendesk_tool = init_tool()
        print(f"✓ Tool initialized: {zendesk_tool}")
        print(f"  Type: {type(zendesk_tool).__name__}")
        print(f"  Module: {type(zendesk_tool).__module__}")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize tool: {e}")
        import traceback
        print(traceback.format_exc())
        return
    
    # List available activities
    print("-" * 70)
    print("Available Activities")
    print("-" * 70)
    
    activities_found = False
    for attr_name in dir(zendesk_tool):
        attr = getattr(zendesk_tool, attr_name)
        if hasattr(attr, 'is_activity') and attr.is_activity:
            activities_found = True
            print(f"  ✓ {attr_name}")
            if hasattr(attr, 'config'):
                config = attr.config
                if 'description' in config:
                    print(f"      Description: {config['description']}")
                if 'schema' in config:
                    schema_dict = config['schema'].schema
                    print(f"      Required fields:")
                    for key, value in schema_dict.items():
                        print(f"        - {key}: {value.__name__}")
    
    if not activities_found:
        print("  No activities found")
    print()
    
    # Test creating a ticket
    print("-" * 70)
    print("Test: Create Ticket")
    print("-" * 70)
    
    test_params = {
        "values": {
            "requester_name": "Test User via init_tool",
            "requester_email": "test-init@example.com",
            "subject": "Test Ticket from init_tool() Script",
            "description": "This ticket was created by calling init_tool() and then using the new_ticket activity."
        }
    }
    
    print("Creating ticket with:")
    print(f"  Requester: {test_params['values']['requester_name']}")
    print(f"  Email: {test_params['values']['requester_email']}")
    print(f"  Subject: {test_params['values']['subject']}")
    print()
    
    try:
        result = zendesk_tool.new_ticket(test_params)
        print()
        print("=" * 70)
        print("RESULT")
        print("=" * 70)
        print(f"Type: {type(result).__name__}")
        
        if type(result).__name__ == 'ErrorArtifact':
            print("❌ Error occurred:")
            print(f"   {result.value}")
        else:
            print("✅ Success:")
            print(f"   {result.value}")
        print("=" * 70)
    except Exception as e:
        print(f"❌ Failed to create ticket: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
