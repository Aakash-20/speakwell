from apps.v1 import route_blog, route_login,route_contactus,route_enquiry, route_index , route_gallery
from apps.v1 import route_header, route_footer, route_keyfactor, route_whyus, route_whatsapp, route_aboutus
from fastapi import APIRouter


app_router = APIRouter()

app_router.include_router(route_blog.router, prefix="/blog", tags=[""], include_in_schema=False)
app_router.include_router(route_login.router, prefix="/auth", tags=[""], include_in_schema=False)
app_router.include_router(route_contactus.router,include_in_schema=False)
app_router.include_router(route_enquiry.router, prefix="/enq", tags=["Enquiry"],include_in_schema=False)
app_router.include_router(route_index.router, include_in_schema=False)
app_router.include_router(route_header.router, include_in_schema=False)
app_router.include_router(route_footer.router, include_in_schema=False)
app_router.include_router(route_keyfactor.router, include_in_schema=False)
app_router.include_router(route_whyus.router, include_in_schema=False)
app_router.include_router(route_whatsapp.router, include_in_schema=False)
app_router.include_router(route_gallery.router, include_in_schema=False)
app_router.include_router(route_aboutus.router, include_in_schema=False)














