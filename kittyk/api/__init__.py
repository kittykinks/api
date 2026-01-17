from fastapi import APIRouter

from kittyk.api.auth import router as router_auth
from kittyk.api.users import router as router_users
from kittyk.api.kinks import router as router_kinks
from kittyk.api.sites import router as router_sites
from kittyk.api.files import router as router_files


router = APIRouter()


router.include_router(router_auth)
router.include_router(router_users)
router.include_router(router_kinks)
router.include_router(router_sites)
router.include_router(router_files)
