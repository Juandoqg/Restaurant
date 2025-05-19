from PIL import Image

# Compatibilidad con Pillow nueva y vieja
try:
    resample_filter = Image.Resampling.LANCZOS
except AttributeError:
    resample_filter = Image.ANTIALIAS

def comprimir_webp(ruta_entrada, ruta_salida, max_ancho=1200, calidad=80):
    with Image.open(ruta_entrada) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        ancho_original, alto_original = img.size

        if ancho_original <= max_ancho:
            img.save(ruta_salida, format='WEBP', quality=calidad)
            print(f"Imagen guardada sin redimensionar: {ruta_salida}")
            return

        escala = max_ancho / float(ancho_original)
        nuevo_alto = int(alto_original * escala)
        img = img.resize((max_ancho, nuevo_alto), resample_filter)

        img.save(ruta_salida, format='WEBP', quality=calidad)
        print(f"✅ Imagen redimensionada a {max_ancho}x{nuevo_alto} y guardada como WebP.")
if __name__ == "__main__":
    comprimir_webp("Salchipapa.webp", "Salchipapa2.webp", max_ancho=1200, calidad=75)