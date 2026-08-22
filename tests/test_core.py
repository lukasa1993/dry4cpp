from pathlib import Path

from dry4cpp.core import find_duplicates


def test_cross_file_duplicate_is_found(tmp_path: Path) -> None:
    first = tmp_path / ("a_" + 'sample.cpp')
    second = tmp_path / ("b_" + 'sample.cpp')
    first.write_text('class Choice {\npublic:\n  int choose(bool a, bool b) const {\n    if (a && b) { return 1; }\n    return 0;\n  }\n};\n', encoding="utf-8")
    second.write_text('class Selection {\npublic:\n  int decide(bool a, bool b) const {\n    if (a && b) { return 1; }\n    return 0;\n  }\n};\n', encoding="utf-8")
    duplicates = find_duplicates(tmp_path, min_tokens=8)
    assert duplicates


def test_non_overlapping_same_file_duplicate_is_found(tmp_path: Path) -> None:
    path = tmp_path / 'sample.cpp'
    path.write_text('class Choice {\npublic:\n  int choose(bool a, bool b) const {\n    if (a && b) { return 1; }\n    return 0;\n  }\n};\n' + "\n" + 'class Selection {\npublic:\n  int decide(bool a, bool b) const {\n    if (a && b) { return 1; }\n    return 0;\n  }\n};\n', encoding="utf-8")
    duplicates = find_duplicates(tmp_path, min_tokens=8)
    assert any(item.locations[0].file == item.locations[1].file for item in duplicates)
