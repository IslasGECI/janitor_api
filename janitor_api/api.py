from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import subprocess

api = FastAPI()


@api.post("/check_traps_ids")
async def check_traps_ids(positions_path: UploadFile, mapsource_path: UploadFile):
    await write_internal_file(positions_path)
    await write_internal_file(mapsource_path)

    data_path_filename = positions_path.filename
    mapsource_path_filename = mapsource_path.filename

    command = [
        "Rscript",
        "-e",
        f"readMS::check_traps('{data_path_filename}', '{mapsource_path_filename}')",
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    result_stderr_splitted = result.stderr.splitlines()
    if result.returncode == 0:
        result_message = result_stderr_splitted[0]
    else:
        result_message = result_stderr_splitted[1]
    return JSONResponse(content={"message": result_message})


async def write_internal_file(uploaded_data_path):
    content = await uploaded_data_path.read()
    with open(uploaded_data_path.filename, "wb") as f:
        f.write(content)
