import difflib
import os.path


def assert_schema(result_schema, expected_schema_filename):
    expected_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), expected_schema_filename
    )
    with open(expected_file) as f:
        expected_schema = f.read()

    diff = difflib.unified_diff(
        expected_schema.splitlines(True),
        result_schema.splitlines(True),
    )
    diff = "".join(diff)
    assert expected_schema == result_schema and not diff, diff
