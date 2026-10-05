from pathlib import Path

from postforge.ingest.scanner import scan_repo


def _write(path: Path, data: bytes | str = b"text") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode())


def test_scanner_without_git_skips_excluded_dirs_and_binaries(tmp_path: Path) -> None:
    _write(tmp_path / "README.md", "# focusguard\n")
    _write(tmp_path / "src" / "app.py", "print('hi')\n")
    _write(tmp_path / "bin" / "tool")
    _write(tmp_path / "obj" / "a.dll")
    _write(tmp_path / "node_modules" / "pkg" / "index.js")
    _write(tmp_path / ".venv" / "lib" / "x.py")
    _write(tmp_path / "assets" / "logo.png", b"\x89PNG\r\n\x1a\n\x00\x00binary")

    result = scan_repo(tmp_path, tracked=lambda _root: None)

    assert result == [Path("README.md"), Path("src/app.py")]


def test_scanner_without_git_walks_nested_dirs(tmp_path: Path) -> None:
    _write(tmp_path / "top.txt", "hi\n")
    _write(tmp_path / "a" / "b" / "c.txt", "hello\n")

    result = scan_repo(tmp_path, tracked=lambda _root: None)

    assert result == [Path("a/b/c.txt"), Path("top.txt")]


def test_scanner_uses_tracked_files_when_git_is_present(tmp_path: Path) -> None:
    _write(tmp_path / "README.md")
    _write(tmp_path / "src" / "app.py")
    _write(tmp_path / "bin" / "untracked")

    result = scan_repo(tmp_path, tracked=lambda _root: ["README.md", "src/app.py"])

    assert result == [Path("README.md"), Path("src/app.py")]


def test_scanner_filters_binary_files_even_when_tracked(tmp_path: Path) -> None:
    _write(tmp_path / "data.bin", b"\x00\x01\x02\x03")

    result = scan_repo(tmp_path, tracked=lambda _root: ["data.bin"])

    assert result == []
