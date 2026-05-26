from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import subprocess

api = FastAPI()


@api.post("/check_traps_ids")
async def check_traps_ids(data_path: UploadFile, initial_parameters_path: UploadFile):
    await write_internal_file(data_path)
    await write_internal_file(initial_parameters_path)

    data_path_filename = data_path.filename
    initial_parameters_path_filename = initial_parameters_path.filename

    command = [
        "Rscript",
        "-e",
        f"readMS::check_traps('{data_path_filename}', '{initial_parameters_path_filename}')",
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    result_message = result.stderr.splitlines()[0]

    return JSONResponse(content={"message": result_message})


async def write_internal_file(uploaded_data_path):
    content = await uploaded_data_path.read()
    with open(uploaded_data_path.filename, "wb") as f:
        f.write(content)
