from docparse.latex2png import tex2pil

import os

def generate_images_from_text(dir_path):
    for filename in os.listdir(dir_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as file:
                text = file.read()
                image = tex2pil(text)[0]
                
                # Save the image in the same directory with .jpg extension
                image_save_path = os.path.join(dir_path, f"{os.path.splitext(filename)[0]}.jpg")
                image.save(image_save_path)

if __name__ == "__main__":
    generate_images_from_text('./')
