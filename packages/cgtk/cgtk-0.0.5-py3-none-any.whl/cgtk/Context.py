class CodeGenCtx():
    def __init__(self):
        self.lines = []
        self.buffer = ""
        self.indent = []
    def push_indent(self, s = "  "):
        self.indent.append(s)
    def pop_indent(self):
        self.indent.pop()
    def write(self, content):
        self.buffer += content
    def flush(self):
        for line in self.buffer.split("\n"):
            self.lines.append("".join(self.indent) + line)
        self.buffer = ""
    def writeline(self, content):
        self.write(content)
        self.flush()
    def make_scope(self, indent="    ", start="", end=""):
        return Scope(self, indent, start, end)

class Scope():
    def __init__(self, ctx, indent, start="", end=""):
        self.ctx = ctx
        self.indent = indent
        self.start = start
        self.end = end
    def __enter__(self):
        if self.start:
            self.ctx.writeline(self.start)
        self.ctx.push_indent(self.indent)
    def __exit__(self, type, value, traceback):
        self.ctx.pop_indent()
        if self.end:
            self.ctx.writeline(self.end)