<!-- this_file: WORK.md -->

## Unreleased — 2026-11-01

Merged the retained PyQt4 QStyleOptionFrameV3 alias fix. The Qt5-style public
QStyleOptionFrame now exposes frameShape on the PyQt4 route. The existing
QStyleOptionViewItem alias is preserved.

Verification: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 uv run --no-project --python
cpython-3.11-macos-aarch64-none --with pytest python -B -m pytest -q
-p no:cacheprovider tests/test_frame_alias.py`: baseline exit1, merged exit0
(one regression). It executes the actual PyQt4 adapter block with owned binding
sentinels; real PyQt4 and the full binding matrix were not available.
Qt reference: https://doc.qt.io/Archives/qt-4.7/qstyleoptionframev3.html .
