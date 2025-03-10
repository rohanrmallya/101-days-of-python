import argparse
import os
from dataclasses import dataclass
from typing import Optional, Tuple
from PIL import Image
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


@dataclass
class ImageConfig:
    file_path: str
    target_size: int
    output_path: Optional[str] = None
    verbose: bool = False


class Logger:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.console = Console()

    def print_banner(self):
        text = Text()
        text.append("Image Resizer", style="bold magenta")
        text.append(" - by Aditya Patange", style="italic")
        self.console.print(Panel(text, border_style="bright_black"))

    def info(self, message: str):
        if self.verbose:
            self.console.log(message)

    def success(self, message: str):
        self.console.print(f"[bold green]{message}[/bold green]")

    def error(self, message: str):
        self.console.print(f"[bold red]Error:[/bold red] {message}")


class ImageProcessor:
    def __init__(self, config: ImageConfig, logger: Logger):
        self.config = config
        self.logger = logger
        self.size_tolerance = 0.1  # 10% tolerance

    def process(self) -> Optional[str]:
        try:
            img = Image.open(self.config.file_path)
            output_path = self._get_output_path()

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Get baseline size
            img.save(output_path, optimize=True)
            current_size = os.path.getsize(output_path) / 1024
            target_size = self.config.target_size

            self.logger.info(f"Original size: {current_size:.1f}KB")
            self.logger.info(f"Target size: {target_size:.1f}KB")

            # Calculate initial scale based on size ratio
            scale = (target_size / current_size) ** 0.5
            new_size = tuple(int(dim * scale) for dim in img.size)
            scaled_img = img.resize(new_size, Image.LANCZOS)

            # Binary search for optimal quality
            min_quality = 5
            max_quality = 95
            best_result = (current_size, 95, scaled_img)

            while min_quality <= max_quality:
                quality = (min_quality + max_quality) // 2
                scaled_img.save(output_path, quality=quality, optimize=True)
                new_size = os.path.getsize(output_path) / 1024

                self.logger.info(
                    f"Scale: {scale:.2f}, Quality: {quality}, Size: {new_size:.1f}KB"
                )

                if abs(new_size - target_size) < abs(best_result[0] - target_size):
                    best_result = (new_size, quality, scaled_img)

                if abs(new_size - target_size) <= self.size_tolerance * target_size:
                    break

                if new_size > target_size:
                    max_quality = quality - 1
                else:
                    min_quality = quality + 1

            # Save best result
            _, quality, best_img = best_result
            best_img.save(output_path, quality=quality, optimize=True)

            return output_path

        except Exception as e:
            self.logger.error(str(e))
            return None

    def _get_output_path(self) -> str:
        if self.config.output_path:
            return os.path.abspath(self.config.output_path)
        base, ext = os.path.splitext(self.config.file_path)
        return f"{base}_output{ext}"


def main():
    parser = argparse.ArgumentParser(
        description="Resize an image to specified file size."
    )
    parser.add_argument(
        "-f", "--file", required=True, help="Path to image file (jpeg/png)"
    )
    parser.add_argument(
        "-s", "--size", required=True, type=int, help="Target file size in KB"
    )
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    config = ImageConfig(
        file_path=os.path.abspath(args.file),
        target_size=args.size,
        output_path=args.output,
        verbose=args.verbose,
    )

    logger = Logger(verbose=args.verbose)
    logger.print_banner()

    processor = ImageProcessor(config, logger)
    if output_path := processor.process():
        logger.success(f"Image resized successfully: {output_path}")
    else:
        logger.error("Failed to resize image")


if __name__ == "__main__":
    main()
