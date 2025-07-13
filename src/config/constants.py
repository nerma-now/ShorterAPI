from pathlib import Path

ROOT_DIR: Path = Path(__file__).parent.parent
ENV_FILE_PATH: Path = ROOT_DIR.parent.joinpath('.env')

__all__ = ["ROOT_DIR", "ENV_FILE_PATH"]
