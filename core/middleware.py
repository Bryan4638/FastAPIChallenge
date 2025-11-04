from fastapi import Request
import time
from datetime import datetime


async def timing_middleware(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    process_time_ms = round(process_time * 1000, 2)

    print(f"{datetime.now().isoformat()} - {request.method} {request.url.path} - Tiempo: {process_time_ms}ms - Status: {response.status_code}")

    return response