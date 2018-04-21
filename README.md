# Notes
* *yield* vs. *yield from*: [[https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-new-yield-from-syntax-in-python-3][stack overflow link]]
** In summary, its best to think of yield from as a transparent two way channel between the caller and the sub-generator.
** ```for v in g:
    yield v```
** test
