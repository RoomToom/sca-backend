from fastapi import HTTPException

def bad_request(detail: str):
    raise HTTPException(status_code=400, detail=detail)

def not_found(detail: str = "Not found"):
    raise HTTPException(status_code=404, detail=detail)
