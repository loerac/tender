from models import ConnectRequest, RestaurantRequest
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')

@app.get('/')
def home(request: Request):
    """
    Display the homepage with a button to find restaurants
    and to connect to an existing session.
    """

    return templates.TemplateResponse('home.html', {
        "request": request
    })

@app.post('/findRestaurants')
def test(restaurant_req: RestaurantRequest):
    """
    Receive information from user about where and
    what to eat.
    """
    print(restaurant_req)

    return {
        "code": "success",
        "message": "finding restaurants"
    }

@app.post('/connectSession')
def test(connect_req: ConnectRequest):
    """
    Receive code to connect to open session. If session isn't
    found/open, let user know that code is invalid.
    """
    print(connect_req)

    return {
        "code": "success",
        "message": "connecting with others"
    }
