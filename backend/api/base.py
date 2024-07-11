from fastapi import APIRouter
from api.v1 import route_user
from api.v1 import route_blog
from api.v1 import route_login
from api.v1 import route_enquiry
from api.v1 import route_contactus

api_router = APIRouter()

api_router.include_router(route_user.router, prefix="/users", tags=["users"])
api_router.include_router(route_blog.router, prefix="/blogs", tags=["blogs"])
api_router.include_router(route_login.router, prefix="/auth", tags=["login"])
api_router.include_router(route_enquiry.router, prefix="/enquiry", tags=["enquiry"])
api_router.include_router(route_contactus.router, prefix="/contactus", tags=["contact-us"])
