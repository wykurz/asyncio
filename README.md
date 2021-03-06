# Coroutines
[A Curious Course on Coroutines and Concurrency](http://dabeaz.com/coroutines/)

Coroutines are similar to generators with a few differences. The main differences are:
* generators are data producers
* coroutines are data consumers

[Tasks and coroutines](https://docs.python.org/3/library/asyncio-task.html)

The word "coroutine", like the word "generator", is used for two different (though related) concepts:
* The function that defines a coroutine (a function definition using async def or decorated with @asyncio.coroutine). If disambiguation is needed we will call this a coroutine function (iscoroutinefunction() returns True)
* The object obtained by calling a coroutine function. This object represents a computation or an I/O operation (usually a combination) that will complete eventually. If disambiguation is needed we will call it a coroutine object (iscoroutine() returns True)

Things a coroutine can do:
* `result = await future` or `result = yield from future` – suspends the coroutine until the future is done, then returns the future's result, or raises an exception, which will be propagated. (If the future is cancelled, it will raise a `CancelledError` exception.) Note that tasks are futures, and everything said about futures also applies to tasks
* `result = await coroutine` or `result = yield from coroutine` - wait for another coroutine to produce a result (or raise an exception, which will be propagated). The coroutine expression must be a call to another coroutine
* `return expression` - produce a result to the coroutine that is waiting for this one using await or yield from
* `raise exception` - raise an exception in the coroutine that is waiting for this one using await or yield from

Calling a coroutine does not start its code running - the coroutine object returned by the call doesn't do anything until you schedule its execution. There are two basic ways to start it running: call await coroutine or yield from coroutine from another coroutine (assuming the other coroutine is already running!), or schedule its execution using the `ensure_future()` function or the `AbstractEventLoop.create_task()` method. A nice discussion about differences between `ensure_future()` and `create_task()` [here](https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine).

Coroutines (and tasks) can only run when the event loop is running.

# asyncio
## Event Loop
The event loop is the central execution device provided by asyncio. It provides multiple facilities, including:
* Registering, executing and cancelling delayed calls (timeouts)
* Creating client and server transports for various kinds of communication
* Launching subprocesses and the associated transports for communication with an external program
* Delegating costly function calls to a pool of threads

### Methods
* [run_forever](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.run_forever)
* [run_until_complete](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.run_until_complete)
* [is_running](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.is_running)
* [stop](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.stop)
* [is_closed](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.is_closed)
* [close](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.close)
* [shutdown_asyncgens](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.shutdown_asyncgens)


## Future
[asyncio.Future](https://docs.python.org/3/library/asyncio-task.html#asyncio.Future)

From [wikipedia](https://en.wikipedia.org/wiki/Futures_and_promises) article: "... a future is a read-only placeholder view of a variable, while a promise is a writable, single assignment container which sets the value of the future ..."

Futures can be used to chain result of a coroutines with callbacks:
```
import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

def got_result(future):
    print(future.result())
    loop.stop()

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
future.add_done_callback(got_result)
try:
    loop.run_forever()
finally:
    loop.close()
```

## Task
[asynctio.Task](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task)

A task is responsible for executing a coroutine object in an event loop. If the wrapped coroutine yields from a future, the task suspends the execution of the wrapped coroutine and waits for the completion of the future. When the future is done, the execution of the wrapped coroutine restarts with the result or the exception of the future.

Don't directly create Task instances: use the `ensure_future()` function or the `AbstractEventLoop.create_task()` method.

```
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        await asyncio.sleep(1)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    factorial("A", 2),
    factorial("B", 3),
    factorial("C", 4),
))
loop.close()
```

Output:
```
Task A: Compute factorial(2)...
Task B: Compute factorial(2)...
Task C: Compute factorial(2)...
Task A: factorial(2) = 2
Task B: Compute factorial(3)...
Task C: Compute factorial(3)...
Task B: factorial(3) = 6
Task C: Compute factorial(4)...
Task C: factorial(4) = 24
```

## Functions
A selection of asyncio task functions, full list [here](https://docs.python.org/3/library/asyncio-task.html#task-functions).

* [asyncio.ensure_future](https://docs.python.org/3/library/asyncio-task.html#asyncio.ensure_future)
* [asynctio.gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)
* [asyncio.iscoroutine](https://docs.python.org/3/library/asyncio-task.html#asyncio.iscoroutine)
* [asyncio.iscoroutinefunction](https://docs.python.org/3/library/asyncio-task.html#asyncio.iscoroutinefunction)
* [asyncio.run_coroutine_threadsafe](https://docs.python.org/3/library/asyncio-task.html#asyncio.run_coroutine_threadsafe)
* [asyncio.sleep](https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep)
* [asyncio.shield](https://docs.python.org/3/library/asyncio-task.html#asyncio.shield)
* [asyncio.wait](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait)
* [asyncio.wait_for](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for)

## Various thoughts
### yield vs. yield from
[stack overflow link](https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-new-yield-from-syntax-in-python-3)

In summary, its best to think of yield from as a transparent two way channel between the caller and the sub-generator.
A simplistic explanation is to say that:
```
yield from g
# is equivalent to:
for v in g:
    yield v
```

But that doesn't capture the full essence, as `yield from` handles `send`, pushing exceptions and other [corner cases](https://www.python.org/dev/peps/pep-0380/#id13).

Another interesting tidbit is that `yield from` returns whatever the underlying generator returns, e.g.:
```
def bar():
    for i in range(0, 5)
        rcvd = yield i
    return 'DONE'

def foo():
    g = bar()
    result = yield from g
     # result == 'DONE'
 ```

### yield from vs. await
[stack overflow link](https://stackoverflow.com/questions/44251045/what-does-the-yield-from-syntax-do-in-asyncio-and-how-is-it-different-from-aw)

* `yield` from is an old way to await for coroutine
* `await` is an modern way to await for coroutine
* Starting python 3.5 `yield from` works only for generators

### @asyncio.coroutine vs async
[stack overflow link](https://stackoverflow.com/questions/40571786/asyncio-coroutine-vs-async-def)

Main difference is native coroutine objects do not implement `__iter__` and  `__next__` methods. Therefore, they cannot be iterated over or passed to `iter()`, `list()`, `tuple()` and other built-ins. They also cannot be used in a `for..in` loop.

### asynchronous generator
From [documeentation](https://docs.python.org/3/glossary.html#term-asynchronous-generator): A function which returns an asynchronous generator iterator. It looks like a coroutine function defined with async def except that it contains yield expressions for producing a series of values usable in an async for loop.

### async for
From [documentation](https://docs.python.org/3/reference/compound_stmts.html#async-for): the async for statement allows convenient iteration over asynchronous iterators.

The following code:
```
async for TARGET in ITER:
    BLOCK
else:
    BLOCK2
```

Is semantically equivalent to:
```
iter = (ITER)
iter = type(iter).__aiter__(iter)
running = True
while running:
    try:
        TARGET = await type(iter).__anext__(iter)
    except StopAsyncIteration:
        running = False
    else:
        BLOCK
else:
    BLOCK2
```

See also:
* [__aiter__](https://docs.python.org/3/reference/datamodel.html#object.__aiter__)
* [__anext__](https://docs.python.org/3/reference/datamodel.html#object.__anext__)

### async with
From [documentation](https://docs.python.org/3/reference/compound_stmts.html#async-with): an asynchronous context manager is a context manager that is able to suspend execution in its enter and exit methods.

The following code:
```
async with EXPR as VAR:
    BLOCK
```

Is semantically equivalent to:
```
mgr = (EXPR)
aexit = type(mgr).__aexit__
aenter = type(mgr).__aenter__(mgr)

VAR = await aenter
try:
    BLOCK
except:
    if not await aexit(mgr, *sys.exc_info()):
        raise
else:
    await aexit(mgr, None, None, None)
```

See also:
* [__aenter__](https://docs.python.org/3/reference/datamodel.html#object.__aenter__)
* [__aexit__](https://docs.python.org/3/reference/datamodel.html#object.__aexit__)

# Development
From [documentation](https://docs.python.org/3/library/asyncio-dev.html): to enable all debug checks for an application:

* Enable the asyncio debug mode globally by setting the environment variable `PYTHONASYNCIODEBUG` to 1, or by calling `AbstractEventLoop.set_debug()`
* Set the log level of the asyncio logger to `logging.DEBUG`. For example, call `logging.basicConfig(level=logging.DEBUG)` at startup
* Configure the warnings module to display `ResourceWarning` warnings. For example, use the `-Wdefault` command line option of Python to display them

Example debug checks:
* Log coroutines defined but never "yielded from"
* `call_soon()` and `call_at()` methods raise an exception if they are called from the wrong thread
* Log the execution time of the selector
* Log callbacks taking more than 100 ms to be executed. The `AbstractEventLoop.slow_callback_duration` attribute is the minimum duration in seconds of "slow" callbacks
* `ResourceWarning` warnings are emitted when transports and event loops are not closed explicitly

# Summary
If you are going to use coroutines, it is critically important to not mix programming paradigms together.

There are three main uses of yield:
* Iteration (a producer of data)
* Receiving messages (a consumer)
* A trap (cooperative multitasking)

Do NOT write generator functions that try to do more than one of these at once

# Resources
* [Python 3.6 Glossary](https://docs.python.org/3/glossary.html)
* [How the heck does async/await work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/)
