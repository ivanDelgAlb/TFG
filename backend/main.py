
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import predictionCalibration
from routers import predictionError
from routers import historical

app = FastAPI()

# Permite el acceso de cualquier origen (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargamos las rutas desde el archivo routers/prediction.py
app.include_router(predictionError.router, prefix="/predictError")
app.include_router(predictionCalibration.router, prefix="/predictCalibration")
app.include_router(historical.router, prefix="/historical")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
