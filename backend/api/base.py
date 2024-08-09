from fastapi import APIRouter
from api.v1 import route_user
from api.v1 import route_blog, route_login, route_image


api_router = APIRouter()

api_router.include_router(route_user.router, prefix="/users", tags=["users"])
api_router.include_router(route_blog.router, prefix="/blogs", tags=["blogs"])
api_router.include_router(route_login.router, prefix="/auth", tags=["token"])
api_router.include_router(route_image.router, prefix="/image", tags=["image"])

# api_router.include_router(route_review.router, prefix="/review", tags=["review"])
