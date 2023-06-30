from aiohttp import web

from utils.database import create_tables
from views.advertisement_detail_view import AdvertisementDetail
from views.index_view import Index
from views.user_login_view import UserLogin
from views.user_logout_view import UserLogout
from views.user_registration_view import UserRegistration

app = web.Application()
app.on_startup.append(create_tables)
app.add_routes(
    [
        web.view("/advertisements/", Index),
        web.view("/advertisements/{id:\d+}/", AdvertisementDetail),
        web.view("/users/register/", UserRegistration),
        web.view("/users/login/", UserLogin),
        web.view("/users/logout/", UserLogout),
    ]
)

if __name__ == "__main__":
    web.run_app(app, port=5000, host="0.0.0.0")
