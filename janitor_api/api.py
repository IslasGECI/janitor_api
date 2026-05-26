from fastapi import FastAPI, UploadFile

api = FastAPI()


@api.post("/check_traps_ids")
async def check_traps_ids(data_path: UploadFile, initial_parameters_path: UploadFile):
    return {"status": "ok"}
