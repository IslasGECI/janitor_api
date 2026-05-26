from janitor_api.api import api

import io
from fastapi.testclient import TestClient

client = TestClient(api)


def test_api_check_traps_ids():
    traps_positions_path = "tests/data/IG_POSICION_TRAMPAS_24MAY2026.xlsx"
    mapsource_path = "tests/data/IG_MAPSOURCE_TRAMPA_24MAY2026.txt"

    with open(traps_positions_path, "rb") as f:
        file_like_traps_positions = io.BytesIO(f.read())

    with open(mapsource_path, "rb") as f:
        file_like_mapsource = io.BytesIO(f.read())

    remote_traps_positions_path = "IG_POSICION_TRAMPAS_24MAY2026.xlsx"
    remote_mapsource_path = "IG_MAPSOURCE_TRAMPA_24MAY2026.txt"

    request = {
        "url": "/check_traps_ids",
        "files": {
            "data_path": (
                remote_traps_positions_path,
                file_like_traps_positions,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            "initial_parameters_path": (
                remote_mapsource_path,
                file_like_mapsource,
                "text/tab-separated-values",
            ),
        },
    }

    response = client.post(**request)
    print(response.json())
    assert response.status_code == 200
    assert "💚 La revisión de trampas es correcta 💚" == response.json()["message"]

    mapsource_path_with_missing_trap = (
        "tests/data/IG_MAPSOURCE_TRAMPA_24MAY2026_with_missing_traps.txt"
    )

    with open(traps_positions_path, "rb") as f:
        file_like_traps_positions = io.BytesIO(f.read())

    with open(mapsource_path_with_missing_trap, "rb") as f:
        file_like_mapsource = io.BytesIO(f.read())

    remote_traps_positions_path = "IG_POSICION_TRAMPAS_24MAY2026.xlsx"
    remote_mapsource_path = "IG_MAPSOURCE_TRAMPA_24MAY2026.txt"

    request = {
        "url": "/check_traps_ids",
        "files": {
            "data_path": (
                remote_traps_positions_path,
                file_like_traps_positions,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            "initial_parameters_path": (
                remote_mapsource_path,
                file_like_mapsource,
                "text/tab-separated-values",
            ),
        },
    }

    response = client.post(**request)
    print(response.json())
    assert response.status_code == 200
    assert "TC-01-056-JA" in response.json()["message"]
