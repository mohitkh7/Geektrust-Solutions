class Order:
    def __init__(self, fee, programme, quantity):
        self._fee = fee
        self._programme = programme
        self._qty = quantity

    @property
    def quantity(self):
        return self._qty

    @property
    def actual_cost(self) -> float:
        return self._fee.get_actual_cost(self._programme)

    @property
    def membership_discount(self) -> float:
        return self._fee.get_members_discount(self._programme) * self.actual_cost

    @property
    def final_cost(self) -> float:
        return self.actual_cost - self.membership_discount

    @property
    def total_actual_cost(self) -> float:
        return self.actual_cost * self._qty

    @property
    def total_membership_discount(self) -> float:
        return self.membership_discount * self._qty

    @property
    def total_final_cost(self) -> float:
        return self.total_actual_cost - self.total_membership_discount


class OrderContainer:
    def __init__(self, fee):
        self._fee = fee
        self._order_container = []

    def add_programme(self, programme, quantity):   
        self._order_container.append(Order(self._fee, programme, quantity))

    @property
    def total_quantity(self):
        return sum(map(lambda order: order.quantity, self._order_container))

    @property
    def total_final_cost(self):
        return sum(map(lambda order: order.total_final_cost, self._order_container))

    @property
    def total_membership_discount(self):
        return sum(map(lambda order: order.total_membership_discount, self._order_container))

    @property
    def lowest_priced_programme_cost(self) -> float:
        return min(map(lambda order: order.final_cost, self._order_container))
