
import ncert_manager

print("Starting Bulk Download for Class 11 & 12 PCMB...")
r11 = ncert_manager.download_class_11_pcmb()
r12 = ncert_manager.download_class_12_pcmb()

print("\n--- Download Summary ---")
for r in r11 + r12:
    print(r)
