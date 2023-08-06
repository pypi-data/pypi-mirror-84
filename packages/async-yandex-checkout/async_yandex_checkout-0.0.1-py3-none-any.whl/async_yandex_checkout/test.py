from async_yandex_checkout.configuration import configuration
from async_yandex_checkout.payment import Payment
import asyncio

configuration.configure("748921", "test_zBBZl3LHniBT4SxxiS4F5OxnF0W8IBAXNsqMYHicyoA")
loop = asyncio.get_event_loop()
payment = Payment()
loop.run_until_complete(
    payment.create(23, "lolkek", "https://yandex.ru")
)

loop.run_until_complete(
    payment.update()
)
print(payment.status)