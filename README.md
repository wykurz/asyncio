# Notes

## Coroutines
[A Curious Course on Coroutines and Concurrency](http://dabeaz.com/coroutines/)
Coroutines are similar to generators with a few differences. The main differences are:
* generators are data producers
* coroutines are data consumers

*yield vs. yield from*
[stack overflow link](https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-new-yield-from-syntax-in-python-3)
In summary, its best to think of yield from as a transparent two way channel between the caller and the sub-generator.
A simplistic explanation is to say that\:
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

*yield from vs. await*
[stack overflow link](https://stackoverflow.com/questions/44251045/what-does-the-yield-from-syntax-do-in-asyncio-and-how-is-it-different-from-aw)
* `yield` from is an old way to await for coroutine
* `await` is an modern way to await for coroutine
* Starting python 3.5 `yield from` works only for generators

*@asyncio.coroutine vs async*
[stack overflow link](https://stackoverflow.com/questions/40571786/asyncio-coroutine-vs-async-def)
Main difference is native coroutine objects do not implement `__iter__` and  `__next__` methods. Therefore, they cannot be iterated over or passed to `iter()`, `list()`, `tuple()` and other built-ins. They also cannot be used in a `for..in` loop.

*Summary*
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
..* An event loop basically says "when event A happens, react with function B"

## Resources
[How the heck does async/await work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/)
