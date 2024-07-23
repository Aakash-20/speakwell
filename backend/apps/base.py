from apps.v1 import route_blog, route_login,route_contactus,route_enquiry
from fastapi import APIRouter

app_router = APIRouter()

app_router.include_router(route_blog.router, prefix="", tags=[""], include_in_schema=False)
app_router.include_router(route_login.router, prefix="/auth", tags=[""], include_in_schema=False)
app_router.include_router(route_contactus.router, prefix="/contactus", tags=["contact Us"],include_in_schema=False)
app_router.include_router(route_enquiry.router, prefix="/enq", tags=["Enquiry"],include_in_schema=False)
