from sl_parser import LogEntry, Unit
from datetime import datetime


def test_parse_from_csv_row():
    csv_row = ["25/02/2022", "14:23:17.075", "3", "5", "code", "description", "0x0000", "Hex", "0", "0xFFADFF2F"]

    units_subunits = {
        3: Unit(
            ini_file="filename_0",
            subunits={
                0: "filename_0",
                1: "filename_1",
                2: "filename_2",
                3: "filename_3",
                4: "filename_4",
                5: "filename_5",
            },
        )
    }
    expected_output = LogEntry(
        timestamp=datetime(2022, 2, 25, 14, 23, 17, 75000),
        unit=3,
        subunit=5,
        unit_subunit_id=-1,
        ini_filename="filename_5",
        code="code",
        description="description",
        value="0x0000",
        type_um="Hex",
        snapshot="0",
        color="0xFFADFF2F",
    )
    assert LogEntry.parse_from_csv_row(csv_row, units_subunits) == expected_output
