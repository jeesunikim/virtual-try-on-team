from ninja import NinjaAPI
from try_on.api import router as try_on_router


api = NinjaAPI()

api.add_router("/try_on", try_on_router)
