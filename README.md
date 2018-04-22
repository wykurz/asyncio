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
    return "DONE"

def foo():
    g = bar()
    result = yield from g
     # result == 'DONE'
```
If you are going to use coroutines, it is critically important to not mix programming paradigms together
There are three main uses of yield
* Iteration (a producer of data)
* Receiving messages (a consumer)
* A trap (cooperative multitasking)
Do NOT write generator functions that try to do more than one of these at once
## asyncio
[Python 3 – An Intro to asyncio](https://www.blog.pythonlibrary.org/2016/07/26/python-3-an-intro-to-asyncio/)
[softwaredoug's asncio.md gist](https://gist.github.com/softwaredoug/86fa2abd60ed203b71de)
1. Provides *event loop*
..* An event loop basically says "when event A happens, react with function B"
