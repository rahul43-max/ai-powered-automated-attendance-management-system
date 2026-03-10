import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.recognition import probe_recognition


if __name__ == "__main__":
    out = probe_recognition()
    print(out)
