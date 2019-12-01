from PIL import Image
ASSET_LOCATION = "..\assets"

def main():
    print("Hello World")
    im = Image.open(ASSET_LOCATION + "\ball_left.png");
    print("Done.")


if __name__ == "__main__":
    main()