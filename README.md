# Notes
## *yield* vs. *yield from*:
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
