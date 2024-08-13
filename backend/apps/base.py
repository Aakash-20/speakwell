from apps.v1 import route_blog, route_login, route_index, route_admin, route_image, route_addres
from fastapi import APIRouter


app_router = APIRouter()


app_router.include_router(route_blog.router, include_in_schema=False)
app_router.include_router(route_login.router,include_in_schema=False)
app_router.include_router(route_index.router, include_in_schema=False)
app_router.include_router(route_admin.router, include_in_schema=False)
app_router.include_router(route_image.router, include_in_schema=False)
app_router.include_router(route_addres.router, include_in_schema=False)













