from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=120)
    parser.add_argument("--output", default="calibration/refs")
    parser.add_argument("--input", default="calibration/refs")
    parser.add_argument("--scenes", default="config/scenes.yaml")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    print(f"Tool executed with args: {args}")


if __name__ == "__main__":
    main()
