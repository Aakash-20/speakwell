from fastapi import APIRouter
from api.v1 import route_user, route_login


api_router = APIRouter()

api_router.include_router(route_user.router, prefix="/users", tags=["users"])
api_router.include_router(route_login.router, prefix="/auth", tags=["token"])