from fastapi import APIRouter

router = APIRouter()

'''
    * This is the router for the crypto module
    * This router is mounted on /api/v1/crypto
'''

@router.get("/current")
async def get_current_price(skip: int = 0, limit: int = 10):
    return {"message": "Hello World"}