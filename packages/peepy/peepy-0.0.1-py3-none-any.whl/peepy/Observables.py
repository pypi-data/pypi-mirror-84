class Observable(object):
    def __init__(self, label):
        self._label = label
        self._value = None
        self._observers = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new):
        old = self._value
        self._value = new
        for callback in self._observers:
            callback(self._label, old, new)
            
    def bind_to(self, callback):
        self._observers.append(callback)

    def observer_function(self, func):
        self.bind_to(func)

     
class ObservableDict(dict, Observable):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        Observable.__init__(self, 'ObservableDict')
        
    def __setitem__(self, key, new):
        old = self.get(key, None)
        for callback in self._observers:
            callback(key, old, new)
        super().__setitem__(key, new)
        
def observe_dict(*args):
    def decorator(func):
        for var in args:
            var.bind_to(func)  
    return decorator
    
def observe(*args):
    def decorator(func):
        for var in args:
            var.bind_to(func)
       
    return decorator
