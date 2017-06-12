import lxifc


class MyOnIdleVisitor(lxifc.Visitor):
    def __init__(self, todo_function, *args, **kwargs):
        self.todo_function = todo_function
        self.args = args
        self.kwargs = kwargs
        self.reset()

    def reset(self):
        self._armed = False

    def arm(self):
        if not self._armed:
            self._armed = True
            return True
        return False

    def vis_Evaluate(self):
        if self._armed:
            self.todo_function(*self.args, **self.kwargs)
        self.reset()
