from PIL import Image
from pathlib import Path

images_dir = Path(__file__).parent.parent / "static" / "images"

for path in images_dir.glob("*"):
    if path.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        continue
    img = Image.open(path)
    has_transparency = img.mode in ("RGBA", "LA") and img.convert("RGBA").getchannel("A").getextrema()[0] < 255
    img = img.convert("RGBA") if has_transparency else img.convert("RGB")
    img.thumbnail((1000, 1000))
    out_path = path.with_suffix(".webp")
    img.save(out_path, "WEBP", quality=80)
    print(f"{path.name} -> {out_path.name}  ({out_path.stat().st_size // 1024} KB)")