start cmd /k "ngrok http --url=muskox-direct-walleye.ngrok-free.app 8000"
start cmd /k "C:\Users\shasoka\Projects\eQueue\backend\venv\Scripts\activate && cd eQueue && python -m uvicorn main:app --reload"