<<<<<<< HEAD

import ncert_manager

print("Starting Bulk Download for Class 11 & 12 PCMB...")
r11 = ncert_manager.download_class_11_pcmb()
r12 = ncert_manager.download_class_12_pcmb()

print("\n--- Download Summary ---")
for r in r11 + r12:
    print(r)
=======

import ncert_manager

print("Starting Bulk Download for Class 11 & 12 PCMB...")
r11 = ncert_manager.download_class_11_pcmb()
r12 = ncert_manager.download_class_12_pcmb()

print("\n--- Download Summary ---")
for r in r11 + r12:
    print(r)
>>>>>>> 7a16fead81d78061ecb1a77ea6528f87c946d5f5
