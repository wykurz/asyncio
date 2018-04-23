# Notes

## Coroutines
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

Calling a coroutine does not start its code running - the coroutine object returned by the call doesn't do anything until you schedule its execution. There are two basic ways to start it running: call await coroutine or yield from coroutine from another coroutine (assuming the other coroutine is already running!), or schedule its execution using the `ensure_future()` function or the `AbstractEventLoop.create_task()` method.

Coroutines (and tasks) can only run when the event loop is running.

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

### Summary
If you are going to use coroutines, it is critically important to not mix programming paradigms together.

There are three main uses of yield:
* Iteration (a producer of data)
* Receiving messages (a consumer)
* A trap (cooperative multitasking)

Do NOT write generator functions that try to do more than one of these at once

## asyncio
[Python 3 – An Intro to asyncio](https://www.blog.pythonlibrary.org/2016/07/26/python-3-an-intro-to-asyncio/)

[softwaredoug's asncio.md gist](https://gist.github.com/softwaredoug/86fa2abd60ed203b71de)

1. Provides *event loop*
    * An event loop basically says "when event A happens, react with function B"

### Future
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

### Task
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

## Resources
[How the heck does async/await work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/)
