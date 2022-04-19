from pathlib import Path

import pytest

from unblob.file_utils import File
from unblob.handlers.filesystem.romfs import get_string, is_safe_path, valid_checksum


@pytest.mark.parametrize(
    "content, expected",
    (
        (b"\x00\x00\x00\x00", b""),
        (b"AAAAAAAAAAAAAAAA\x00", b"AAAAAAAAAAAAAAAA"),
        (b"AAAAAAAAAAAAAAA\x00", b"AAAAAAAAAAAAAAA"),
        (b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00", b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
        (b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00", b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
    ),
)
def test_get_string(content, expected):

    f = File.from_bytes(content)
    assert get_string(f) == expected


@pytest.mark.parametrize(
    "content, valid",
    (
        (b"\x00\x00\x00\x00", True),
        (b"\x00\x00\x00\x00\x00\x00\x00\x00", True),
        (b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", True),
        (b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", True),
        (b"\x00\x00\x00", False),
        (b"\x00\x00\x00\x00\x00\x00\x00", False),
        (b"\x00\x00\x00\x00\x00\x00\x00\x00\x00", False),
        (b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", False),
        (
            b"""-rom1fs-\x00\x00\x11\xb0h("arom 61de9f79\x00\x00\x00\x00\x00\x00\x00I\x00\x00\x00 \x00\x00\x00\x00\xd1\xff\xff\x97.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00 \x00\x00\x00\x00\xd1\xd1\xff\x80..\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x92\x00\x00\x00\x00\x00\x00\x00\x07\xf84b\x9ahlink_3_4\x00\x00\x00\x00\x00\x00\x00file34\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd3\x00\x00\x00\x00\x00\x00\x00\x1c\xef4cDslink_2_2\x00\x00\x00\x00\x00\x00\x00/tmp/fruits/dir_2/file_2.txt\x00\x00\x00\x00\x00\x00\x01\x13\x00\x00\x00\x00\x00\x00\x00\x1c\xf04c\x04slink_2_1\x00\x00\x00\x00\x00\x00\x00/tmp/fruits/dir_2/file_1.txt\x00\x00\x00\x00\x00\x00\x02i\x00\x00\x010\x00\x00\x00\x00i\x96\x8a\x08dir_2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01b\x00\x00\x00\x00\x00\x00\x00\x07\xc1\xeec\xbefile_4.txt\x00\x00\x00\x00\x00\x00file24\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x92\x00\x00\x00\x00\x00\x00\x00\x07\xc1\xedc\x8efile_5.txt\x00\x00\x00\x00\x00\x00file25\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc2\x00\x00\x00\x00\x00\x00\x00\x07\xc1\xf1c^file_1.txt\x00\x00\x00\x00\x00\x00file21\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xe0\x00\x00\x01\x10\x00\x00\x00\x00\xd1\xff\xfd\x10.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00 \x00\x00\x00\x00\xd1\xd1\xfd\xe0..\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00""",
            True,
        ),
        (
            b"""-rom1fs-\x01\x00\x11\xb0h("arom 61de9f79\x00\x00\x00\x00\x00\x00\x00I\x00\x00\x00 \x00\x00\x00\x00\xd1\xff\xff\x97.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00 \x00\x00\x00\x00\xd1\xd1\xff\x80..\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x92\x00\x00\x00\x00\x00\x00\x00\x07\xf84b\x9ahlink_3_4\x00\x00\x00\x00\x00\x00\x00file34\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd3\x00\x00\x00\x00\x00\x00\x00\x1c\xef4cDslink_2_2\x00\x00\x00\x00\x00\x00\x00/tmp/fruits/dir_2/file_2.txt\x00\x00\x00\x00\x00\x00\x01\x13\x00\x00\x00\x00\x00\x00\x00\x1c\xf04c\x04slink_2_1\x00\x00\x00\x00\x00\x00\x00/tmp/fruits/dir_2/file_1.txt\x00\x00\x00\x00\x00\x00\x02i\x00\x00\x010\x00\x00\x00\x00i\x96\x8a\x08dir_2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01b\x00\x00\x00\x00\x00\x00\x00\x07\xc1\xeec\xbefile_4.txt\x00\x00\x00\x00\x00\x00file24\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x92\x00\x00\x00\x00\x00\x00\x00\x07\xc1\xedc\x8efile_5.txt\x00\x00\x00\x00\x00\x00file25\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc2\x00\x00\x00\x00\x00\x00\x00\x07\xc1\xf1c^file_1.txt\x00\x00\x00\x00\x00\x00file21\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xe0\x00\x00\x01\x10\x00\x00\x00\x00\xd1\xff\xfd\x10.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00 \x00\x00\x00\x00\xd1\xd1\xfd\xe0..\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00""",
            False,
        ),
    ),
)
def test_valid_checksum(content, valid):
    assert valid_checksum(content) == valid


@pytest.mark.parametrize(
    "basedir, path, expected",
    (
        ("/tmp/out", "/tmp/out/file", True),
        ("/tmp/out", "file", True),
        ("/tmp/out", "dir/file", True),
        ("/tmp/out", "some/dir/file", True),
        ("/tmp/out", "some/dir/../file", True),
        ("/tmp/out", "some/dir/../../file", True),
        ("/tmp/out", "some/dir/../../../file", False),
        ("/tmp/out", "some/dir/../../../", False),
        ("/tmp/out", "some/dir/../../..", False),
        ("/tmp/out", "../file", False),
        ("/tmp/out", "/tmp/out/../file", False),
    ),
)
def test_is_safe_path(basedir, path, expected):
    assert is_safe_path(Path(basedir), Path(path)) is expected