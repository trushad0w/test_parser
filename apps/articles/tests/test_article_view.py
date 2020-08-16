import pytest

from apps.articles.dto.article import OrderEnum, OrderDirectionEnum


@pytest.mark.parametrize("limit", (0, 10, 100, 500, None))
@pytest.mark.parametrize("offset", (0, 1, 10, 1000, None))
@pytest.mark.parametrize("order", list(OrderEnum.__members__.values()) + ["1", "asd", 3, None])
@pytest.mark.parametrize(
    "order_direction", list(OrderDirectionEnum.__members__.values()) + ["1", "asd", 2, None]
)
def test_articles_get(db, client, limit, offset, order, order_direction):
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if order is not None:
        if isinstance(order, OrderEnum):
            order = order.value
        params["order"] = order
    if order_direction is not None:
        if isinstance(order_direction, OrderDirectionEnum):
            order_direction = order_direction.value
        params["order_direction"] = order_direction

    response = client.get("/posts", data=params,)
    valid_condition = (
        (limit is None or limit <= 100)
        and (order is None or order in OrderEnum.__members__.values())
        and (order_direction is None or order_direction in OrderDirectionEnum.__members__.values())
    )
    print(response.json())
    if valid_condition:
        assert response.status_code == 200
    else:
        assert response.status_code == 400
