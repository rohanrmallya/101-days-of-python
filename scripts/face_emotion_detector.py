import argparse
import cv2
import sys
import os
from rich.console import Console
from rich.text import Text
import base64
import mimetypes

console = Console()


def print_banner():
    banner = Text(
        """
    ***************************************
    *    Face Emotion Detector Program    *
    ***************************************
    """,
        style="bold magenta",
    )
    console.print(banner)

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def detect_emotion(base64_image):
    return {
        "model": "claude-3-7-sonnet-latest",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is the emotion of the person in this image?"},
                    {"type": "image", "source": base64_image}
                ]
            }
        ]
    }

def detect_media_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and mime_type.startswith("image/"):
        return mime_type
    return "unknown"

def print_emotion(emotion):
    console.print(f"Detected Emotion: {emotion}", style="bold green")

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Face Emotion Detector")
    parser.add_argument("--face-path", type=str, help="Path to the face image")
    parser.add_argument("--live", action="store_true", help="Start live camera mode")

    args = parser.parse_args()

    if args.face_path:
        emotion = detect_emotion(args.face_path)
        console.print(print_emotion(emotion))
    elif args.live:
        cap = cv2.VideoCapture(0)
        console.print("Press 'Enter' to capture an image.", style="bold yellow")
        while True:
            ret, frame = cap.read()
            cv2.imshow("Live Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord("\r"):
                image_path = "captured_image.jpg"
                cv2.imwrite(image_path, frame)
                console.print(
                    f"Image captured and saved to {image_path}", style="bold cyan"
                )
                emotion = detect_emotion(image_path)
                console.print(f"Detected Emotion: {emotion}", style="bold green")
                os.remove(image_path)
                console.print(
                    f"Temporary image {image_path} deleted.", style="bold red"
                )
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        console.print(
            "Please provide either --face-path or --live option.", style="bold red"
        )
        sys.exit(1)
    


if __name__ == "__main__":
    main()



        