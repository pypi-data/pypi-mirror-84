from fastapi import Request

body_scope_name = 'body'


async def inject_body(request: Request):
    request.scope[body_scope_name] = await request.body()


async def get_injected_body(request: Request) -> bytes:
    return request.scope[body_scope_name]
