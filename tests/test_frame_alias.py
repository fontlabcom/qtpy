# this_file: tests/test_frame_alias.py
"""Check the actual PyQt4 alias block with owned Qt-name sentinels."""
import ast
from pathlib import Path
import sys
from types import ModuleType


def test_pyqt4_frame_alias_exposes_v3_without_removing_view_item_alias(monkeypatch):
    source = Path(__file__).parents[1] / "qtpy/QtWidgets.py"
    tree = ast.parse(source.read_text())
    branch = next(node for node in ast.walk(tree)
                  if isinstance(node, ast.If) and isinstance(node.test, ast.Name)
                  and node.test.id == "PYQT4")
    gui = ModuleType("PyQt4.QtGui")
    for node in ast.walk(branch):
        if isinstance(node, ast.Name):
            setattr(gui, node.id, object())
    gui.QStyleOptionFrame = object()
    gui.QStyleOptionFrameV3 = object()
    parent = ModuleType("PyQt4")
    parent.QtGui = gui
    monkeypatch.setitem(sys.modules, "PyQt4", parent)
    monkeypatch.setitem(sys.modules, "PyQt4.QtGui", gui)
    gui.patch_qcombobox = lambda widget: None
    gui.introduce_renamed_methods_qheaderview = lambda widget: None
    namespace = {}
    exec(compile(ast.Module(body=branch.body, type_ignores=[]), str(source), "exec"), namespace)
    assert namespace["QStyleOptionFrame"] is gui.QStyleOptionFrameV3
    assert "QStyleOptionFrameV3" not in namespace
    assert namespace["QStyleOptionViewItem"] is gui.QStyleOptionViewItemV4
    assert "QStyleOptionViewItemV4" not in namespace
