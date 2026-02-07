
import ncert_manager

def test_mapping():
    print("Testing Chapter Mapping...")
    chapters = ncert_manager.get_class_10_science_chapters()
    print(f"Total Chapters: {len(chapters)}")
    
    first = chapters[0]
    num = ncert_manager.CLASS_10_SCIENCE_CHAPTERS[first]
    print(f"First Chapter: {first} -> {num}")
    
    if num == 1:
        print("Mapping Verified!")
    else:
        print("Mapping Failed.")

if __name__ == "__main__":
    test_mapping()
