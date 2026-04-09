class OrderService:

    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository

    def _serialize_order(self, order: Order) -> dict:
        return OrderSchema(
            id=order.id,
            user_id=order.user_id,
            address_id=order.address_id,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        ).model_dump(mode="json")

    def create_order(self, order: CreateOrderSchema) -> Order:
        new_order = Order(
        user_id=order.user_id, 
        address_id=order.address_id, 
        status=order.status)
        created_order = self.order_repository.create_order(new_order)
        return self._serialize_order(created_order)

    def get_order_by_id(self, order_id: int) -> Order:
        return self.order_repository.get_order_by_id(order_id)

    def get_all_orders(self) -> List[Order]:
        return self.order_repository.get_all_orders()

    def update_order(self, order: Order) -> Order:
        return self.order_repository.update_order(order)