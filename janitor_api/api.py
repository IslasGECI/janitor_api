from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import subprocess

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    result_message = format_check_traps_ids_message(result)
    return JSONResponse(content={"message": result_message})


def format_check_traps_ids_message(result):
    result_stderr_splitted = result.stderr.splitlines()
    index_of_message = result.returncode
    return result_stderr_splitted[index_of_message]


async def write_internal_file(uploaded_data_path):
    content = await uploaded_data_path.read()
    with open(uploaded_data_path.filename, "wb") as f:
        f.write(content)
