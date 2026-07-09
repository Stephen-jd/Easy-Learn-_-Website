import sys
from PIL import Image

def remove_white_background(input_path, output_path, threshold=200):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        # Check if the pixel is close to white
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            # Change all white-ish pixels to transparent
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Saved transparent image to {output_path}")

if __name__ == "__main__":
    remove_white_background(sys.argv[1], sys.argv[2])
