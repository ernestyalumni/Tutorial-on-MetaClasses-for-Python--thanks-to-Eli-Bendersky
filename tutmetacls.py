# tutmetacls.py
# Based on Eli Bendersky's website Python metaclasses by example
# Shout outs to Eli Bendersky for his excellent website with excellent examples
#
# 20140607
# 
# Fund Science! & Help Ernest finish his Physics Research! : quantum super-A-polynomials - Ernest Yeung
#                                               
# http://igg.me/at/ernestyalumni2014                                                                             
#                                                              
# Facebook     : ernestyalumni  
# github       : ernestyalumni                                                                     
# gmail        : ernestyalumni                                                                     
# linkedin     : ernestyalumni                                                                             
# tumblr       : ernestyalumni                                                               
# twitter      : ernestyalumni                                                             
# youtube      : ernestyalumni                                                                
# indiegogo    : ernestyalumni                                                                        
# 
# Ernest Yeung was supported by Mr. and Mrs. C.W. Yeung, Prof. Robert A. Rosenstone, Michael Drown, Arvid Kingl, Mr. and Mrs. Valerie Cheng, and the Foundation for Polish Sciences, Warsaw University.  
#
# cf. Pro Python (2010).  Marty Alchin
# Chapter 11, Sheets: A CSV Framework
# 
# pp. 246 a base class - since declarative frameworks are all about declaring classes, having a common base class to inherit from gives the frame a place to hook in and process declarations as they're encountered by Python
#
# metaclass - what's a metaclass?
# cf. http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python
# metaclass is the class of a class, like a class defines how an instance of the class behaves, a metaclass defines how a class behaves.  A class is an instance of a metaclass
# To create your own metaclass in Python, you really just want to subclass 'type'
# A metaclass is most commonly used as a class-factory
#
# I didn't understand Alchin's treatment of metaclasses so I went here:
# cf. http://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example/
#
# Metaclass
# wait, create classes with a standard class definition?
# what Python does under the hood is the following
# when it sees a class definition, Python executes it to collect attributes (including methods) into a dictionary
# when class definition is over, Python determines metaclass of the class. Let's call it Meta
# Eventually, Python executes Meta(name, bases, dct), where
# # Meta is metaclass, so this invocation is instantiating it
# # name is name of newly created class
# # bases is tuple of class's base classes
# # dct maps attribute names to objects, listing all of class's attributes

class MyKlass(object):
    foo = 2
# MyKlass has no __metaclass__ attribute, so type is used instead

#
# Metaclass's __new__ and __init__
#

# new - control creation of a new object
# init control initialization of new object after it has been created

class MyMeta(type):
    def __new__(meta, name, bases, dct):
        print '------------------------------------'
        print "Allocating memory for class", name
        print meta  # <class '__main__.MyMeta'>
        print name  # MyKlass
        print bases # (<type 'object'>,)
        print dct   # {'barattr': 2, '__module__': '__main__', 'foo': <function foo at 0x10a5f7f50>, '__metaclass__': <class '__main__.MyMeta'>}
        # notice that dct has all the class attributes, barattr, class modules inside it, foo, and then which metaclass it got inherited from; that's it
        return super(MyMeta, meta).__new__(meta, name, bases, dct)  
# super, see examples, super(MyMeta,meta) is then going to refer to MyMeta's higher guy, which is type
    def __init__(cls, name, bases, dct):
        print '------------------------------------'
        print "Initializing class", name
        print cls
        print bases #(<type 'object'>,) # MyKlass was MyKlass(object) and it is a base
        print dct
        super(MyMeta, cls).__init__(name, bases, dct)

class MyKlass(object):
    __metaclass__ = MyMeta

    def foo(self, param):
        pass

    barattr = 2

# This is all immediately from when Python executes the class definition; it'll immediately do __new__ and then __init__ for MyMeta

#------------------------------------
#Allocating memory for class MyKlass
#<class '__main__.MyMeta'>
#(<type 'object'>,)
#{'barattr': 2, '__module__': '__main__', 'foo': <function foo at 0x10a5f7f50>, '__metaclass__': <class '__main__.MyMeta'>}
#------------------------------------
#Initializing class MyKlass
#<class '__main__.MyKlass'>
#(<type 'object'>,)
#{'barattr': 2, '__module__': '__main__', 'foo': <function foo at 0x10a5f7f50>, '__metaclass__': <class '__main__.MyMeta'>}

# It's important to note here that these print-outs are actually done at class creation time, i.e. when the module containing the class is being imported for the first time.  Keep this detail in mind for later.

# difference between call and init
# cf. http://stackoverflow.com/questions/9663562/what-is-difference-between-init-and-call-in-python

class foo:
    def __init__(self, a , b , c ):
        self.a = a

class boo:
    def __call__(self, a , b, c ):
        self.a = a

x = foo(1,2,3)
x.a

y = boo()
y(1,2,3)
y.a

class MyMeta2(type):
    def __call__(cls, *args, **kwds):
        print '__call__ of ', str(cls)
        print '__call__ *args=', str(args)
        return type.__call__(cls, *args, **kwds)

class MyKlass2(object):
    __metaclass__ = MyMeta2

    def __init__(self, a , b):
        print 'MyKlass object with a=%s, b=%s' % (a, b)

print 'gonna create foo now...'
foo = MyKlass2(1,2)




