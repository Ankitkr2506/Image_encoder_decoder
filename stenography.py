from PIL import Image

def text_to_binary(text):
    return ''.join([format(ord(i), '08b') for i in text])

def binary_to_text(binary_data):
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    return ''.join([chr(int(byte, 2)) for byte in all_bytes])

def encode(image_path, message, output_path):
    img = Image.open(image_path)
    binary_message = text_to_binary(message) + '1111111111111110'  # EOF marker

    if img.mode != 'RGB':
        raise ValueError("Image mode needs to be RGB")

    encoded = img.copy()
    width, height = img.size
    data_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for n in range(3):  # RGB
                if data_index < len(binary_message):
                    pixel[n] = pixel[n] & ~1 | int(binary_message[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    encoded.save(output_path)
    print(f"✅ Message encoded and saved to {output_path}")

def decode(image_path):
    img = Image.open(image_path)
    binary_data = ''
    if img.mode != 'RGB':
        raise ValueError("Image mode needs to be RGB")

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixel = img.getpixel((x, y))
            for n in range(3):  # RGB
                binary_data += str(pixel[n] & 1)

    end_marker = '1111111111111110'
    if end_marker in binary_data:
        binary_data = binary_data[:binary_data.index(end_marker)]
        decoded_text = binary_to_text(binary_data)
        print("🕵️ Hidden Message:")
        print(decoded_text)
    else:
        print("❌ No hidden message found.")

# Example usage
if __name__ == "__main__":
    print("1. Encode\n2. Decode")
    choice = input("Choose option: ")

    if choice == "1":
        image_path = input("Enter input image path: ")
        message = input("Enter secret message to hide: ")
        output_path = input("Enter output image path (e.g., output_image.png): ")
        encode(image_path, message, output_path)
    elif choice == "2":
        image_path = input("Enter image path to decode: ")
        decode(image_path)
    else:
        print("Invalid choice.")
