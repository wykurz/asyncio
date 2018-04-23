import asyncio
from functools import partial

@asyncio.coroutine
def legacy_coroutine():
    yield 1

async def async_coroutine():
    yield 2

def yield_generator(coroutine):
    yield coroutine()

def yield_from_generator(coroutine):
    yield from coroutine()

# Raises syntax error:
#
# @asyncio.coroutine
# def legacy_coroutine_await(coroutine):
#     await coroutine()

async def await_coroutine_await(coroutine):
    await coroutine()

def wrap(func, argfunc):
    try:
        return func(argfunc())
    except Exception as exc:
        return str(exc)

for f in [legacy_coroutine, async_coroutine]:
    try:
        print(f.__name__)
        print('  - calling next:', wrap(next, f))
        print('  - calling next on yield_generator:', wrap(next, partial(yield_generator, f)))
        print('  - calling yield_from_generator:', wrap(yield_from_generator, f))
        print('  - calling await_coroutine_await:', wrap(await_coroutine_await, f))
    except Exception as exc:
        print(exc)

# Output:
#
# legacy_coroutine
#   - calling next: 1
#   - calling next on yield_generator: <generator object legacy_coroutine at 0x7fd5a7435200>
#   - calling yield_from_generator: <generator object yield_from_generator at 0x7fd5a74351a8>
#   - calling await_coroutine_await: <coroutine object await_coroutine_await at 0x7fd5a7435200>
# sandbox.py:38: RuntimeWarning: coroutine 'await_coroutine_await' was never awaited
#   print('  - calling await_coroutine_await:', wrap(await_coroutine_await, f))
# async_coroutine
#   - calling next: 'async_generator' object is not an iterator
#   - calling next on yield_generator: <async_generator object async_coroutine at 0x7fd5a7901ba8>
#   - calling yield_from_generator: <generator object yield_from_generator at 0x7fd5a7435200>
#   - calling await_coroutine_await: <coroutine object await_coroutine_await at 0x7fd5a7435200>

async def foo():
    asyncio.Task.current_task().print_stack()
    return 42

async def bar():
    return await foo()

async def baz():
    return await bar()

loop = asyncio.get_event_loop()
task = asyncio.ensure_future(baz())
task.add_done_callback(lambda _res: loop.stop())
try:
    loop.run_forever()
finally:
    loop.close()

print('Done!')
