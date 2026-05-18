from PIL import Image
import os

INPUT_DIR = "images"
OUTPUT_DIR = "images_aframe"

TARGET_SIZE = (4096, 2048)
JPEG_QUALITY = 85

os.makedirs(OUTPUT_DIR, exist_ok=True)

valid_extensions = (".jpg", ".jpeg", ".png", ".webp")

converted = 0
skipped = 0

for filename in os.listdir(INPUT_DIR):
    filename_lower = filename.lower()

    # Só converte panoramas do CloudPano
    if not filename_lower.startswith("scene-"):
        print(f"Ignorado (não é scene): {filename}")
        skipped += 1
        continue

    if not filename_lower.endswith(valid_extensions):
        print(f"Ignorado (extensão inválida): {filename}")
        skipped += 1
        continue

    input_path = os.path.join(INPUT_DIR, filename)

    base_name = os.path.splitext(filename)[0]
    output_filename = base_name + ".jpg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        with Image.open(input_path) as img:
            original_size = img.size

            # Segurança extra: só converte imagens próximas de proporção 2:1
            ratio = original_size[0] / original_size[1]

            if not (1.9 <= ratio <= 2.1):
                print(f"Ignorado (não parece panorama 2:1): {filename} | tamanho: {original_size}")
                skipped += 1
                continue

            img = img.convert("RGB")
            img = img.resize(TARGET_SIZE, Image.LANCZOS)

            img.save(
                output_path,
                "JPEG",
                quality=JPEG_QUALITY,
                optimize=True
            )

            print(f"Convertido: {filename} | {original_size} -> {TARGET_SIZE}")

            converted += 1

    except Exception as e:
        print(f"Erro ao converter {filename}: {e}")

print("\nFinalizado.")
print(f"Convertidas: {converted}")
print(f"Ignoradas: {skipped}")