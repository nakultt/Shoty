"""PixelPipe - Main Entry Point.

Run this script to process screenshots through the vision pipeline.
"""

import os
import json

from agent import graph


def main():
    """Main execution loop for PixelPipe."""
    image_file = input("Enter screenshot filename: ").strip('"')  # Strips quotes if drag-dropped
    
    if not os.path.exists(image_file):
        print("❌ File not found.")
        return
    
    thread = {"configurable": {"thread_id": "session_v1"}}
    
    print("=" * 50)
    print("🚀 STARTING PIXELPIPE")
    print("=" * 50)
    
    # Phase 1: Run until Human Review (interrupt_before is set in graph compilation)
    for event in graph.stream({"image_path": image_file}, config=thread):
        pass
    
    # Phase 2: Check State
    current_state = graph.get_state(thread)
    if not current_state.values:
        print("❌ Workflow failed before reaching checkpoint.")
        return
    
    cls = current_state.values.get('classification')
    data = current_state.values.get('extracted_data')
    
    if cls == "UNKNOWN" or not data:
        print("\n❌ Could not classify image. Try a clearer screenshot.")
        return
    
    print(f"\n🔍 [CHECKPOINT] extracted ({cls}):")
    print(json.dumps(data, indent=2))
    
    # Phase 3: User Input
    choice = input("\n👉 Type 'APPROVED' to execute action, or press Enter to cancel: ")
    
    if choice.strip().upper() == "APPROVED":
        graph.update_state(thread, {"user_feedback": "APPROVED"})
        print("\n🟢 Resuming...")
        for event in graph.stream(None, config=thread):
            pass
        print("\n✅ PIXELPIPE COMPLETE")
    else:
        print("🔴 Action Cancelled.")


if __name__ == "__main__":
    main()
