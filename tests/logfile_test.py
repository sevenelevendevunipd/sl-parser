from datetime import datetime

import pytest

from sl_parser.logfile import LogFile


@pytest.fixture
def sample_log() -> list[str]:
    return (
        "PC DateTime: 25.02.2022 14:23:21\n"
        "UPS DateTime: 25.02.2022 14:23:20\n"
        "INI File name :  unit.ini; Unit=0 - SubUnit=0\n"
        "INI File name :  unit.ini; Unit=1 - SubUnit=0\n"
        "INI File name :  module.ini; Unit=1 - SubUnit=1\n"
        "INI File name :  module.ini; Unit=1 - SubUnit=2\n"
        "INI File name :  module.ini; Unit=1 - SubUnit=3\n"
        "INI File name :  bypass.ini; Unit=1 - SubUnit=14\n"
        "Date ; Time ; Unit  ; SubUnit ; Code ; Description ; Value ; Type/UM ; Snapshot ; Color\n"
        "25/02/2022 ; 14:23:17.075 ; 1 ; 0 ; code1 ; code1 ; 0x0000 ; Hex ; 0 ; 0xFFADFF2F\n"
        "25/02/2022 ; 14:23:17.075 ; 1 ; 0 ; code2 ; code2 ; 112 ; [-] ; 0 ; 0xFFADFF2F\n"
        "25/02/2022 ; 14:23:17.075 ; 1 ; 0 ; code3 ; code3 ; 0 ; [-] ; 0 ; 0xFFADFF2F\n"
        "25/02/2022 ; 14:23:12.375 ; 1 ; 0 ; code4 ; In Service mode ; OFF ; BIN ; 0 ; 0xFFE0FFFF\n"
        "25/02/2022 ; 14:23:12.275 ; 1 ; 0 ; code5 ; [-] ; Service Mode OFF ; [-] ; 0 ; 0xFFADFF2F\n"
        "25/02/2022 ; 14:23:04.557 ; 1 ; 0 ; code4 ; In Service mode ; ON ; BIN ; 0 ; 0xFFE0FFFF\n"
        "25/02/2022 ; 14:23:04.457 ; 1 ; 0 ; code5 ; [-] ; Service Mode On ; [-] ; 0 ; 0xFFADFF2F\n"
        "25/02/2022 ; 14:22:45.258 ; 1 ; 0 ; code4 ; In Service mode ; OFF ; BIN ; 0 ; 0xFFE0FFFF\n"
        "25/02/2022 ; 14:22:45.158 ; 1 ; 0 ; code5 ; [-] ; Service Mode OFF ; [-] ; 0 ; 0xFFADFF2F\n"
        "25/02/2022 ; 14:22:40.558 ; 1 ; 0 ; code5 ; [-] ; lol ; [-] ; 0 ; 0xFFADFF2F\n"
        "25/02/2022 ; 14:22:22.259 ; 1 ; 0 ; code6 ; Reset History Log ; ON ; BIN ; 0 ; 0xFFD3D3D3\n"
    )


def test_parse_log(sample_log: list[str]) -> None:
    filename = "test_log.log"
    log_file = LogFile.parse_log(filename, sample_log)
    assert log_file.filename == filename
    assert log_file.pc_datetime == datetime(2022, 2, 25, 14, 23, 21)
    assert log_file.ups_datetime == datetime(2022, 2, 25, 14, 23, 20)
    assert len(log_file.units_subunits) == 2  # noqa: PLR2004
    assert log_file.units_subunits[0].ini_file == "unit.ini"
    assert log_file.units_subunits[0].subunits == {0: "unit.ini"}
    assert log_file.units_subunits[1].ini_file == "unit.ini"
    assert log_file.units_subunits[1].subunits == {
        0: "unit.ini",
        1: "module.ini",
        2: "module.ini",
        3: "module.ini",
        14: "bypass.ini",
    }

    assert len(log_file.log_entries) == 11  # noqa: PLR2004
