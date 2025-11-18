"""
Test script for the emergency contact dialog
"""

import sys
import os

# Add current directory to path so we can import splash_screen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from splash_screen import show_emergency_contact_dialog
    
    print("Testing Emergency Contact Dialog...")
    print("A dialog window should appear asking for emergency contact information.")
    
    # Show the dialog
    result = show_emergency_contact_dialog()
    
    if result:
        print("\n[SUCCESS] Emergency Contact Setup Complete!")
        print(f"Contact: {result['contact']}")
        print(f"WhatsApp Preference: {result['whatsapp_preference']}")
    else:
        print("\n[CANCELLED] Emergency Contact Setup was cancelled.")
    
    print("\nDialog test completed!")
    
except ImportError as e:
    print(f"Error importing splash_screen module: {e}")
except Exception as e:
    print(f"Error running emergency contact dialog: {e}")
    import traceback
    traceback.print_exc()
