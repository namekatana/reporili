from pathlib import Path

from PIL import Image, ImageDraw

assets = Path(r"C:\Users\Vadym\.cursor\projects\c-Users-Vadym-Documents-CodeLegal\assets")
public = Path(r"c:\Users\Vadym\Documents\CodeLegal\frontend\public")

logoSource = assets / "c__Users_Vadym_AppData_Roaming_Cursor_User_workspaceStorage_11f46d4339fc8f2041b9e8bf40462702_images_RL-f0fa9750-dcae-4a10-9cdf-8168863f75b4.png"
faviconSource = assets / "c__Users_Vadym_AppData_Roaming_Cursor_User_workspaceStorage_11f46d4339fc8f2041b9e8bf40462702_images_RL_______2__1_-9d5cee79-f17a-4526-8497-3d041c841ee6.png"


def removeDarkBackground(image: Image.Image, threshold: int = 40) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    for y in range(height):
        for x in range(width):
            red, green, blue, alpha = pixels[x, y]
            if red < threshold and green < threshold and blue < threshold:
                pixels[x, y] = (0, 0, 0, 0)
    return rgba


def trimTransparent(image: Image.Image) -> Image.Image:
    bbox = image.getbbox()
    if not bbox:
        return image
    return image.crop(bbox)


def applyRoundedMask(image: Image.Image, radiusRatio: float = 0.223) -> Image.Image:
    rgba = image.convert("RGBA")
    width, height = rgba.size
    radius = int(min(width, height) * radiusRatio)
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=radius, fill=255)
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    result.paste(rgba, mask=mask)
    return result


def saveLogo() -> None:
    image = Image.open(logoSource)
    image = trimTransparent(removeDarkBackground(image))
    image = image.resize((72, 72), Image.Resampling.LANCZOS)

    pngPath = public / "logo.png"
    webpPath = public / "logo.webp"

    image.save(pngPath, format="PNG", optimize=True)
    image.save(webpPath, format="WEBP", quality=85, method=6)

    print(f"logo.png  {pngPath.stat().st_size} bytes")
    print(f"logo.webp {webpPath.stat().st_size} bytes")


def saveFavicon() -> None:
    image = applyRoundedMask(Image.open(faviconSource))
    sizes = [16, 32, 48]
    icons = [image.resize((size, size), Image.Resampling.LANCZOS) for size in sizes]

    icoPath = public / "favicon.ico"
    icons[1].save(
        icoPath,
        format="ICO",
        sizes=[(size, size) for size in sizes],
        append_images=icons[2:],
    )

    png32Path = public / "favicon.png"
    icons[1].save(png32Path, format="PNG", optimize=True)

    print(f"favicon.ico {icoPath.stat().st_size} bytes")
    print(f"favicon.png {png32Path.stat().st_size} bytes")


if __name__ == "__main__":
    saveLogo()
    saveFavicon()
