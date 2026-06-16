from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from Modules.Order.Services.CartService import CartService, get_cart_service
from Modules.Auth.CheckAuth import get_current_user
from Modules.Auth.Models import User
from Utils.Response import success_response
from Modules.Order.Schemas import *
from Modules.Order.Mappers.CartMapper import to_cart_dict
from Modules.Order.Services.OrderService import OrderService, get_order_service
from Modules.Order.Mappers.OrderMapper import to_order_dict

router = APIRouter(prefix="/order", tags=["order"])






