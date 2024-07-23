from apps.v1 import route_blog, route_login,route_contactus,route_enquiry,header,footer,index,whyus,keyfactor
from fastapi import APIRouter

app_router = APIRouter()

app_router.include_router(route_blog.router, prefix="/blog", tags=[""], include_in_schema=False)
app_router.include_router(route_login.router, prefix="/auth", tags=[""], include_in_schema=False)
app_router.include_router(route_contactus.router, prefix="/contactus", tags=["contact Us"],include_in_schema=False)
app_router.include_router(route_enquiry.router, prefix="/enq", tags=["Enquiry"],include_in_schema=False)
app_router.include_router(header.router, prefix="", tags=[""],include_in_schema=False)
app_router.include_router(footer.router, prefix="", tags=[""],include_in_schema=False)
app_router.include_router(index.router, prefix="", tags=[""],include_in_schema=False)
app_router.include_router(keyfactor.router, prefix="", tags=[""],include_in_schema=False)
app_router.include_router(whyus.router, prefix="", tags=[""],include_in_schema=False)






