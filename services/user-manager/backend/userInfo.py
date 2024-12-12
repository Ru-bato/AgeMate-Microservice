#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Developed by AlecNi @ 2024/12/12
# Description:
#   the UserInfo entity and related manager
# Solved:
# Unsolved:
#   1.userInfo Struct
#   2.post method
#   else

from pydantic import BaseModel, Depends, File, UploadFile


# TODO: refine the UserInfo class & create post method

class UserInfo(BaseModel):
    username: str
    email: str

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = 0.0

class ResponseModel(BaseModel):
    item_id: int
    name: str
    description: str = None

def common_parameters(q: str = None, limit: int = 10):
    return {"q": q, "limit": limit}

@app.get("/search/")
async def search(params: dict = Depends(common_parameters)):
    return params


@app.get("/items/{item_id}", response_model=ResponseModel)
async def get_item(item_id: int):
    return {"item_id": item_id, "name": "Example Item", "description": "This is an example"}


@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "total_price": item.price + item.tax}

if __name__ == "__main__":
    print("userInfo.py test")
    print("test list:")
else:
    print("userInfo.py imported")
    print("userInfo initialized")