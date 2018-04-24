---
presentation:
  # theme: "solarized.css"
  # theme: "league.css"
  # theme: "serif.css"
  # theme: "white"
  theme: "serif.css"
  width: 1200
  height: 1200

  # Factor of the display size that should remain empty around the content
  margin: 0.1
  # Display the page number of the current slide
  slideNumber: true
  # Vertical centering of slides
  # center: false
  transition: slide
  enableSpeakerNotes: true
---

<!-- slide -->
# Special method
__snail__

2018-04-01

<!-- slide -->
## Overview

1. New-style and classic classes - function and method
2. What is special method ?
3. When to use special method ?
4. SHOW ME THE CODE
5. References


<!-- slide class="new-style classes" -->
### New-style and classic classes
* new-style classes were introduced to unify the concepts of `class` and `type`
* old-style classes are removed in Python 3, leaving only new-style classes

```python
class A: pass

a = A()
print dir(A) # ['__doc__', '__module__']
print a.__class__ # <class __main__.A at 0x1005833f8>
print type(a) # <type 'instance'>
```

```python
class A(object): pass

a = A()
print dir(A) # ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
print a.__class__ # <class '__main__.A'>
print type(a) # <class '__main__.A'>
```

<!-- slide class="new-style classes" vertical="true" -->
### function vs method

* function can be called by name
* method called by the instance - bound vs unbound
```python
def func(): pass
print type(func) # type 'function'>
```

```python
class A(object):
    def a(self): pass
print type(A.a) # <type 'instancemethod'>
print A.a       # <unbound method A.a>
print A.a()     # TypeError: unbound method a() must be called with A instance as first argument (got nothing instead)
print A().a     # <bound method A.a of <__main__.A object at 0x100599a90>>
print A().a()   # no TypeError
```

<!-- slide class="what-special-method" -->
## What is special method ?
```python
#!/usr/bin/env python

class RedEnvelopPersonError(Exception):
    pass

class RedEnvelope(object):

    def __init__(self, person, amount):
        self.person = person
        self.amount = amount

    def __repr__(self):
        return 'RedEnvelop({!r}) RMB'.format((self.person, self.amount))

    def __str__(self):
        return '{0}\'s red envelope {1} RMB'.format(self.person, self.amount)

    def __add__(self, other):
        if not isinstance(other, RedEnvelope):
            raise TypeError
        if other.person != self.person:
            raise RedEnvelopPersonError
        return RedEnvelope(self.person, self.amount + other.amount)

if __name__ == '__main__':
    s_one = RedEnvelope('snail', 5)
    l_one = RedEnvelope('leslie', 10)
    s_two = RedEnvelope('snail', 15)
    print s_one             # snail's red envelope 5 RMB
    print repr(l_one)       # RedEnvelop(('leslie', 10)) RMB
    # print s_one + l_one   # Error
    print s_one + s_two     # snail's red envelope 20 RMB
```
<!-- slide class="what-special-method" vertical="true" -->
## What is special method ?

* classes method with special syntax (`__x__`)
* **operator overloading** , allowing classes to define their own behavior with respect to language operators.
* both in old-style and new-style classes
*  behavior ->  `__method__`
    * x + y    ->  `__add__`
    * repr(x)  ->  `__repr__`
    * str(x)   ->  `__str__`
    * init()   ->  `__init__`
    * len(x)   ->  `__len__`
    * a()      ->  `__call__`

<!-- slide class="when-special-method" -->
## when ?
1. **create instance** [**more**]
2. **customizing attribute access**
    * implementing descriptors [**more**]
    * `__slots__`
3. **customizing class creation** - `__metaclass__`
4. **customizing instance and subclass checks**
5. **emulating callable objects** [**more**]
6. **emulating container types** - `__len__`,`__getitem__`,`__reversed__`
7. **emulating sequence types** - `__getslice__`,`__setslice__`
8. **emulating numeric types** - `__add__`,`__mod__`
10. **with statement context managers** [**more**]
11. **represent instance** - `__repr__`,`__str__`
12. **compare instance** - `__equals__`,`__lt__`
...

### **Conclusion: Useful!**

<!-- slide -->
## SHOW ME THE CODE

<!-- slide class='when-special-method' vertical="true" -->
### create instance
SHOW ME THE CODE `__new__` : **singleton class**
```python {cmd="/usr/bin/python"}
#!/usr/bin/env python

class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class DBConnection(Singleton):
    def __init__(self, db_settings):
        if not hasattr(self, 'db_settings'):
            self.db_settings = db_settings

if __name__ == '__main__':
    connection = DBConnection("db_settings")
    print id(connection), connection.db_settings # 4302936400 db_settings
    conn = DBConnection("new_db_settings")
    print id(conn), conn.db_setting              # 4302936400 db_settings
```


<!-- slide class='when-special-method' vertical="true" -->
### customizing attribute access
SHOW ME THE CODE: **descriptors**
```python {cmd="/usr/bin/python"}
#!/usr/bin/env python

class CoWorkerName(object):

    def __init__(self):
        self._name = ''

    def __get__(self, obj, objtype):
        print 'Getting: {0}'.format(self._name)
        return self._name

    def __set__(self, obj, value):
        print 'Setting: {0}'.format(value)
        self._name = value.title()

    def __delete__(self, obj):
        print 'Deleting: {0}'.format(self._name)
        del self._name

class ServerCoWorker(object):
    name = CoWorkerName()

if __name__ == '__main__':
    author = ServerCoWorker()
    author.name = 'snail'
    print author.name
    del author.name
```


<!-- slide class='when-special-method' vertical="true" -->
### callable objects
SHOW ME THE CODE: `__call__`
```python
class Callable(object):

    def __call__(self):
        return 'invoking __call__ from Callable object: {0}'.format(id(self))

if __name__ == '__main__':
    c = Callable()
    print c() # invoking __call__ from Callable object: 4302848592
```
<!-- slide class='when-special-method' vertical="true" -->
### callable objects
ONE MORE THING:
```python {cmd="/usr/bin/python"}
class Callable(object):

    def __call__(self):
        return 'invoking __call__ from Callable object: {0}'.format(id(self))

def call():
    return 'invoking __call__ from function'

if __name__ == '__main__':
    c = Callable()
    print c.__call__()
    print c()
    # print type(c.__call__) # <type 'instancemethod'>
    c.__call__ = call
    # print type(c.__call__) # <type 'function'>
    print c.__call__()
    print c()   # implicit invocations
    print Callable.__call__(c)
```
**special method VS instance dictionary**
> For new-style classes, implicit invocations of special methods are only guaranteed to work correctly if defined on an object's type, not in the object's instance dictionary

<!-- slide class='when-special-method' vertical="true" -->
### context manager
SHOW ME THE CODE: **context manager class**
```python
#!/usr/bin/env python

import socket

class TCPSocketClient(object):
    HOST = '127.0.0.1'
    PORT = 8080
    BUFFER_SIZE = 1024

    def __init__(self, host=None, port=None):
        self.address = (host or self.HOST, port or self.PORT)

    def __enter__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(self.address)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.close()

    def send(self, data):
        self._client.send(data)

    def receive(self, buffer_size=None):
        buffer_size = buffer_size or TCPSocketClient.BUFFER_SIZE
        return self._client.recv(buffer_size)

if __name__ == '__main__':
    with TCPSocketClient() as client:
        client.send('hi')
        print client.receive()   # [Sun Apr  1 22:41:28 2018], hi
```


<!-- slide class="reference" -->
## References
* [Python Documentation](https://docs.python.org/2.7/reference/datamodel.html)
* [Python魔术方法指南](http://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/a-guide-to-pythons-magic-methods.html#id20)
* [video] - [What Does It Take To Be An Expert At Python?](https://www.youtube.com/watch?v=7lmCu8wz8ro&t=598s)

<!-- slide -->
### THANK YOU FOR YOUR TIME

### Q&A
