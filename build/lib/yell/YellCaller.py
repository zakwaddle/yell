
class YellCaller:

    def __init__(self, name, on=True, lvl=1):
        self.name = name
        self.on = on
        self.lvl = lvl
        self.func_registry = {}
        self.call_count = 0
        self.last_called_func = None
        self.last_stack = []
        self.code_context = None
        self.lineno = None

    def set_last_stack(self, stack_stuff):
        self.last_stack = stack_stuff

    def log_func(self, func_name):
        if not self.on:
            return None
        caller = func_name
        caller_count = self.func_registry.get(caller)
        if caller_count is None:
            self.func_registry[caller] = 1
        elif caller_count >= 1:
            self.func_registry[caller] = caller_count + 1
        self.set_last_called_func(func_name)
        return self.func_registry[caller]

    def inc_call_count(self):
        self.call_count += 1

    def get_module_call_count(self):
        return self.call_count

    def get_func_call_count(self, func_name):
        return self.func_registry.get(func_name)

    def set_last_called_func(self, func_name):
        self.last_called_func = func_name
