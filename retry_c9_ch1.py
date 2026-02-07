
import ncert_manager
import time

# Try alternate book code if iesc1 fails? 
# Sometimes Class 9 Science is just 'iesc1'
# Let's try downloading with the standard code first, but maybe from a different mirror if possible? 
# Actually, ncert website is the only source.
# Let's add a small sleep to be nice.

print("Attempting to download Class 9 Chapter 1...")
path, msg = ncert_manager.download_ncert_pdf("9", "Science", "1")
print(f"Status: {msg}")

if path:
    import os
    size = os.path.getsize(path)
    print(f"File Size: {size} bytes")
    if size < 1000:
        print("Warning: File seems too small (corrupt/empty).")
