import numbers
import os
import inspect
from .YellCaller import YellCaller
from .ColorTools import ColorTools
from .Theme import theme


class Yell:
    tools = ColorTools()
    _registry = {}
    custom_class_a = None
    custom_class_b = None
    custom_class_c = None

    custom_color_a = None
    custom_color_b = None
    custom_color_c = None

    def __init__(self, width=80, indent=3):
        self.width = width
        self.indent = ' ' * indent
        self.all_quiet = False
        self.use_theme = True
        self._last = None
        self.load_config()

    def load_config(self):
        def register_modules(the_modules):
            if not the_modules: return
            for key, vals in the_modules.items():
                m = YellCaller(name=key, **vals)
                self._registry[key] = m

        config_dict = {}
        if os.path.exists("yell_config.py"):
            from yell_config import config
            config_dict = config if config else {}
        if not config_dict: return

        self.width = config_dict.get('width', self.width)
        self.indent = config_dict.get('indent', self.indent)
        self.all_quiet = config_dict.get('all_quiet', False)
        self.use_theme = config_dict.get('use_theme', True)
        if not self.use_theme: self.tools.disable_color()

        self.custom_class_a = config_dict.get('custom_class_a')
        self.custom_color_a = config_dict.get('custom_color_a')
        self.custom_class_b = config_dict.get('custom_class_b')
        self.custom_color_b = config_dict.get('custom_color_b')
        self.custom_class_c = config_dict.get('custom_class_c')
        self.custom_color_c = config_dict.get('custom_color_c')

        modules = config_dict.get('modules', {})
        register_modules(modules)

    def tracer(self, lvl=1):
        size = lvl
        h = int(size / 2)
        d = self.tools.dash(theme.dash) * h
        cap = self.tools.pipe(theme.primary)
        return f"{d}{self.tools.pipe(theme.pipe)}{d}{cap}"

    def be_heard(self, *args, **kwargs):
        we_can_yell = not self.all_quiet
        if we_can_yell:
            print(self.tools.timestamp(), *args, **kwargs)

    def wrap(self, user_line, flup_num=0):
        def truncate(text):
            """Truncates text to a specified width while preserving ANSI color codes"""
            visible_length = self.tools.color_text.find_length(text)
            if visible_length <= self.width + len(self.indent):
                return text
            offset = self.tools.color_text.find_ansi_offset(text) + self.width - 1
            text = f"{text:.{offset}}...{self.tools.color_text.ansi.end}"
            return text
        buff = self.tools.flup(theme.flup) * flup_num
        new_line = f"{self.tracer(flup_num)}{buff}{user_line}"
        short = truncate(new_line)
        return short

    def __log(self, things, caller, width=75, corners="sharp", color=theme.primary, label=""):
        width = width if self.width > 75 else self.width
        def color_func(a_thing): return self.tools.color(a_thing, color=color)
        def box_it(*stuff, color_func_=None, align="^", corners_):
            corners_ = self.tools.corners.get(corners_)  # if corners in self.tools.corners.keys() else "sharp"
            top_line = corners_[0] + ("-" * width) + corners_[1]
            bottom_line = corners_[3] + ("-" * width) + corners_[2]

            lines = [f"|{thing:{align}{width}}|" for thing in stuff]
            all_the_stuff = [top_line, *lines, bottom_line]
            all_the_stuff = [color_func_(i) for i in all_the_stuff]
            all_the_stuff = [self.wrap(i, flup_num=caller.lvl) for i in all_the_stuff]
            return all_the_stuff
        def make_call_chain(prefix):
            def white(a_thing):
                return self.tools.color(a_thing).white()

            def bright_white(a_thing):
                return self.tools.color(a_thing).bright_white()

            line_no = f" {bright_white('line')} {white('#')}{bright_white(caller.lineno)}"
            call_chain = [*caller.last_stack, line_no]
            assembled = [prefix, white("stack:")]
            num = len(call_chain) - 1

            for i in call_chain:
                assembled.append(bright_white(i))
                if call_chain.index(i) >= num: continue
                assembled.append(white("=>"))

            almost_done = ' '.join([str(ass) for ass in assembled])
            return self.wrap(almost_done, flup_num=caller.lvl)

        boxed = box_it(*things, color_func_=color_func, corners_=corners)
        chain = make_call_chain(prefix=f"-{color_func(label)}- ")
        self.be_heard(chain, *boxed, sep='\n')

    def success(self, *things, width=75):
        caller = self.handle_caller()
        if not caller.on: return
        self.__log(things, caller, width=width, corners="heavy", color=theme.success, label="SUCCESS")

    def warning(self, *things, width=75):
        caller = self.handle_caller()
        if not caller.on: return
        self.__log(things, caller, width=width, corners="heavy", color=theme.warning, label="WARNING")

    def error(self, *things, width=75):
        caller = self.handle_caller()
        if not caller.on: return
        self.__log(things, caller, width=width, corners="heavy", color=theme.error, label="ERROR")

    def failure(self, *things, width=75):
        caller = self.handle_caller()
        if not caller.on: return
        self.__log(things, caller, width=width, corners="heavy", color=theme.failure, label="FAILURE")

    def info(self, *things, width=75):
        caller = self.handle_caller()
        if not caller.on: return
        self.__log(things, caller, width=width, corners="round", color=theme.info, label="INFO")

    def debug(self, *things, width=75):
        caller = self.handle_caller()
        if not caller.on: return
        self.__log(things, caller, width=width, corners="sharp", color=theme.debug, label="DEBUG")

    def label(self, text, lvl=0):
        caller = self.handle_caller()
        if not caller.on: return
        file = self.tools.color(caller.name, color=theme.primary)
        caller_name = self.tools.color(caller.last_called_func, color=theme.secondary)
        call_count = self.tools.color(caller.get_func_call_count(caller_name), color=theme.failure)
        func_trace = f" {file}.{caller_name}() : {call_count}"
        stuff = self.tools.color(text, color=theme.label)

        line = f"{self.tracer(lvl=lvl)}{self.tools.arrow_right}  -[ {stuff} ]-  {self.tools.arrow_left} {func_trace}"
        thing = self.wrap(line, flup_num=lvl)
        self.be_heard(thing, sep='\n')

    def __user_stuff(self, the_stuff, is_loop=False, lvl=0):
        bucket = []
        def drop_in(drip):
            bucket.append(f"{self.tools.flup(theme.flup) * lvl} {drip}") if is_loop else bucket.append(f" {drip}")

        def make_plunge(plunge_list):
            return ''.join(plunge_list)

        def handle_custom_classes(some_thing):
            colors = self.tools.color_text.ansi
            if self.custom_class_a is not None:
                if isinstance(some_thing, self.custom_class_a) and colors.is_valid(self.custom_color_a):
                    return self.tools.color(some_thing, color=self.custom_color_a)
            if self.custom_class_b is not None:
                if isinstance(some_thing, self.custom_class_b) and colors.is_valid(self.custom_color_b):
                    return self.tools.color(some_thing, color=self.custom_color_b)
            if self.custom_class_c is not None:
                if isinstance(some_thing, self.custom_class_c) and colors.is_valid(self.custom_color_c):
                    return self.tools.color(some_thing, color=self.custom_color_c)
            return some_thing

        def handle_non_iterator(some_thing):
            if isinstance(some_thing, str):
                return self.tools.color(some_thing, color=theme.string)
            elif isinstance(some_thing, bool):
                return self.tools.color(some_thing, color=theme.boolean)
            elif isinstance(some_thing, numbers.Number):
                return self.tools.color(some_thing, color=theme.number)
            elif some_thing is None:
                return self.tools.color("None", color=theme.none)
            else:
                return handle_custom_classes(some_thing)

        def handle_dict(dict_drip, plunger):
            dict_div = self.tools.pipe(color=theme.dict_div)
            plunge = f"{self.indent}{dict_div}"
            plunger.append(plunge)
            squib = f"{make_plunge([*plunger])}{self.tools.dash(theme.dict_div)}"

            def drop_key(some_thing):
                drop_in(f"{squib} {self.tools.color(some_thing, theme.dict_key)} :")

            for pair in dict_drip.items():
                key, val = pair
                if isinstance(val, dict):
                    if not val: val = self.tools.color("{}", theme.dict_div)
                    else:
                        drop_key(key)
                        handle_dict(val, plunger=[*plunger])   
                        continue 
                elif isinstance(val, list):
                    if not val: val = self.tools.color("[]", theme.list_div)
                    else:
                        drop_key(key)
                        handle_list(val, plunger=[*plunger])
                        continue

                drop_in(f"{squib} {self.tools.color(key, theme.dict_key)}: {handle_non_iterator(val)}")
            squib_len = self.tools.color_text.find_length(squib)
            drop_in(f"{squib}{self.tools.div(length=self.width - squib_len, color=theme.dict_div)}")

        def handle_list(user_list, plunger):
            plunge = f"{self.indent}{self.tools.pipe(color=theme.list_div)}"
            plunger.append(plunge)
            my_plunger = [*plunger]
            squib = make_plunge(plunge_list=my_plunger)

            for item in user_list:
                if isinstance(item, list):
                    handle_list(item, plunger=[*plunger])
                elif isinstance(item, dict):
                    handle_dict(item, plunger=[*plunger])
                else:
                    drop_in(f"{squib}{self.tools.dash(theme.list_div)} {handle_non_iterator(item)}")
            squib_len = self.tools.color_text.find_length(squib)
            drop_in(f"{squib}{self.tools.div(length=self.width - squib_len, color=theme.list_div)}")

        def handle_value(value, plunger):
            if isinstance(value, dict):
                handle_dict(value, plunger)
            elif isinstance(value, (list, tuple)):
                handle_list(value, plunger)
            else:
                drop_in(handle_non_iterator(value))

        for thing in the_stuff:
            handle_value(thing, [])

        return [self.wrap(turd) for turd in bucket]

    def handle_caller(self):
        stuff = inspect.stack()
        stack_obj = stuff[2]

        def get_basename(fp):
            fn = os.path.basename(fp)
            return fn
        def get_func(f):
            the_thing = f.function
            if the_thing == "<module>":
                the_thing = get_basename(f.filename)
            else:
                the_thing = f"{the_thing}()"
            return the_thing
        def get_call_chain(fr):
            outers = inspect.getouterframes(fr)
            return [get_func(i) for i in outers]
        def inform_caller(c:YellCaller):
            c.inc_call_count()
            c.last_called_func = stack_obj.function
            c.last_stack = get_call_chain(stack_obj.frame)[::-1]
            c.lineno = stack_obj.lineno
            c.code_context = stack_obj.code_context
            c.log_func(c.last_called_func)
            return c

        filename = get_basename(stack_obj.filename)
        module = filename[:-3]
        caller = self._registry.get(module)
        if caller is None:
            caller = YellCaller(name=module)
            self._registry[module] = caller

        assert isinstance(caller, YellCaller)
        caller = inform_caller(caller)
        return caller

    def __call__(self, *words, is_loop=False, loop_lvl:int=0, title:str=None, **kwargs):
        caller = self.handle_caller()
        if not caller.on: return

        chunk = self.tools.chunk(theme.chunk)
        filename = self.tools.color(f"{caller.name}.py", theme.label)
        basename = self.tools.color(caller.name, theme.primary)
        called_func = self.tools.color(caller.last_called_func, theme.tertiary)
        call_count = self.tools.color(caller.get_func_call_count(caller.last_called_func), theme.failure)

        beginning = f"{self.tracer(caller.lvl)}{chunk} {filename}  {self.tools.pointer_right}  {called_func}(): {call_count} {chunk}"
        end = f"\n{self.tools.div(length=self.width + len(self.indent), color=theme.tertiary)}\n"

        if self._last == caller:
            func_trace = f" {basename}.{called_func}() : {call_count}"
            beginning = f"{self.tracer(caller.lvl)}  {chunk} {title if title else func_trace} {chunk}"
            end = '\n'

        whatever = self.__user_stuff(words, is_loop=is_loop, lvl=caller.lvl)
        whole_thing = [*whatever] if is_loop else [beginning, *whatever]
        self.be_heard(*whole_thing, sep='\n', end=end)
        self._last = caller
