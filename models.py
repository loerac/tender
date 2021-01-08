from pydantic import BaseModel

class RestaurantRequest(BaseModel):
    location: str
    restaurants: dict
    cost: dict
    distance: float

class ConnectRequest(BaseModel):
    connect_code: str
