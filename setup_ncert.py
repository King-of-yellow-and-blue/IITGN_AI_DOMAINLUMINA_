<<<<<<< HEAD

import ncert_manager
import time

def main():
    print("Initialize NCERT Bulk Download...")
    results = ncert_manager.download_all_class_10_science()
    
    print("\n--- Download Report ---")
    for res in results:
        print(res)
    print("\nAll tasks completed.")

if __name__ == "__main__":
    main()
=======

import ncert_manager
import time

def main():
    print("Initialize NCERT Bulk Download...")
    results = ncert_manager.download_all_class_10_science()
    
    print("\n--- Download Report ---")
    for res in results:
        print(res)
    print("\nAll tasks completed.")

if __name__ == "__main__":
    main()
>>>>>>> 7a16fead81d78061ecb1a77ea6528f87c946d5f5
