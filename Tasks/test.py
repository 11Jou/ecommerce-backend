from Core.CeleryApp import celery_app

@celery_app.task
def test(x: int, y: int):
    print(f"Test task executed with {x} and {y}")
    print(f"Result: {x + y}")