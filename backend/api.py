from ninja import NinjaAPI, Router

api = NinjaAPI()

v1 = Router()

api.add_router("/v1", v1)


@v1.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
