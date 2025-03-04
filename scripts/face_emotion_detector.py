import argparse
import cv2
import sys
import os
from rich.console import Console
from rich.text import Text

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


def detect_emotion(image_path):
    # Dummy function for emotion detection
    console.print(f"Detecting emotion for the image: {image_path}", style="bold cyan")
    return "Happy"


def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Face Emotion Detector")
    parser.add_argument("--face-path", type=str, help="Path to the face image")
    parser.add_argument("--live", action="store_true", help="Start live camera mode")

    args = parser.parse_args()

    if args.face_path:
        emotion = detect_emotion(args.face_path)
        console.print(f"Detected Emotion: {emotion}", style="bold green")
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
