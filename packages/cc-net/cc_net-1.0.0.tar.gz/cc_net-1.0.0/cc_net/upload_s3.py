import subprocess
from pathlib import Path
from typing import Iterable, Sequence


def file_list(dump: str) -> Iterable[Path]:
    root = Path("data/mini_by_segment") / dump
    files_txt = root / "files.txt"
    assert files_txt.exists()
    done = False
    i = 0
    for f in files_txt.read_text().splitlines():
        path = root / f
        if path.name.endswith(".index"):
            continue
        i += 1
        # Hack to resume from previous state
        if path.name == "CC-MAIN-20190216170210-20190216192210-00282.json.gz":
            done = False
        if done:
            continue
        assert path.exists()
        yield path
        print(f"uploaded {i} files")
    yield files_txt


def main(dump: str = "2019-09") -> None:
    s3_folder = f"s3://dl.fbaipublicfiles.com/cc_net/1.0.0/{dump}"
    for f in file_list(dump):
        subprocess.check_call(["fs3cmd", "put", str(f), "/".join((s3_folder, f.name))])


def copy(dump: str = "2019-09") -> None:
    folder = Path("data/mini_by_segment_cleaned") / dump
    folder.mkdir(exist_ok=True, parents=True)
    for f in file_list(dump):
        new = folder / f.name
        if new.is_symlink():
            continue
        new.symlink_to(f.resolve())
    #  fs3cmd sync --follow-symlinks --no-check-md5 --no-preserve data/mini_by_segment__cleaned/2019-09 s3://dl.fbaipublicfiles.com/cc_net/1.0.0/
    subprocess.check_call(
        [
            "fs3cmd",
            "sync",
            "--follow-symlinks",
            "--no-check-md5",
            "--no-preserve",
            str(folder),
            "s3://dl.fbaipublicfiles.com/cc_net/1.0.0/",
        ]
    )


if __name__ == "__main__":
    # main()
    copy()
