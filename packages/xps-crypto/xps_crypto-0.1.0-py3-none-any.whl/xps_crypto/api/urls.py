from fastapi import APIRouter

from xps_crypto.api.wallets.views import router as wallets_router

root_router = APIRouter()
root_router.include_router(wallets_router, prefix='/wallets')
