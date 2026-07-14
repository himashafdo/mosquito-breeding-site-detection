from ultralytics import YOLO
import sys

# Load your new 6-class model weights
model = YOLO("best.pt")

# Loop through all images passed as command-line arguments
for img in sys.argv[1:]:
    r = model.predict(img, conf=0.1, save=True)
    boxes = r[0].boxes
    print(f"\n=== {img} ===")

    if len(boxes) == 0:
        print("  no breeding-site objects detected")
    else:
        counts = {}
        for b in boxes:
            name = model.names[int(b.cls[0])]
            counts[name] = counts.get(name, 0) + 1
            print(f"  {name}: {float(b.conf[0]):.0%}")
            
        # FIXED: Fixed the unpacking variable order (name, count)
        # FIXED: Indented properly to stay inside the 'else' block
        summary = ", ".join(f"{count} {name}" for name, count in counts.items())
        print(f"  --> yard contains: {summary}")
        
    print(f"  annotated image saved in: {r[0].save_dir}")