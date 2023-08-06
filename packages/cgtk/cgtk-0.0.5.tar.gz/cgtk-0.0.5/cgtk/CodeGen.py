import ast
import os
import sys

def find_files(pattern):
    import os, glob
    return [fn for fn in glob.iglob(pattern, recursive=True)
            if not os.path.isdir(fn)]

class Pushd():
    def __init__(self, new_dir):
        self.new_dir = new_dir
    def __enter__(self):
        self.previous_dir = os.getcwd()
        os.chdir(self.new_dir)
    def __exit__(self, type, value, traceback):
        os.chdir(self.previous_dir)

class PushPath():
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        sys.path.insert(0, self.path)
    def __exit__(self, type, value, traceback):
        sys.path.remove(self.path)

class CodeGen():
    def __init__(self, filename, ctx, verbose=False):
        self.filename = os.path.abspath(filename)
        self.ctx = ctx
        self.verbose = verbose
    def debug(self, msg):
        if self.verbose:
            print("[DEBUG]", "[%s]" % self.filename, msg)
    def info(self, msg):
        print("[INFO]", "[%s]" % self.filename, msg)
    def error(self, msg):
        print("[ERROR]", "[{}:{}]".format(self.filename, self.lineid + 1), msg)
        exit(1)
    def run_block_code(self, lines):
        try:
            tree = ast.parse("\n".join(lines), self.filename)
        except SyntaxError as e:
            e.text = lines[e.lineno - 1]
            e.lineno += self.lineid
            raise e
        tree = ast.increment_lineno(tree, self.lineid)
        code = compile(tree, self.filename, "exec")
        ctx = self.ctx()
        path = os.path.dirname(self.filename)
        with Pushd(path):
            with PushPath(path):
                gd = {"ctx": ctx, "__file__": self.filename}
                exec(code, gd)
        return ctx.lines
    def generate_code(self):
        # read file
        try:
            with open(self.filename) as f:
                file_content = f.read()
        except UnicodeDecodeError:
            self.debug("binary file, skipped.")
            return
        except:
            self.debug("cannot read, skipped.")
            return
        lines = file_content.split('\n')
        # process
        new_lines = []
        self.lineid = 0
        has_cg_block = False
        while self.lineid < len(lines):
            line = lines[self.lineid]
            if line.endswith('[codegen]'):
                has_cg_block = True
                lcg = self.lineid
                lb = lcg
                while not lines[lb].endswith('[begin]'):
                    lb += 1
                    if lb == len(lines) or lines[lb].endswith('[codegen]'):
                        self.error("[codegen] block without [begin]")
                le = lb
                while not lines[le].endswith('[end]'):
                    le += 1
                    if le == len(lines):
                        self.error("codegen block without [end]")
                new_lines += lines[lcg:lb+1]
                new_lines += self.run_block_code(lines[lcg+1:lb])
                new_lines.append(lines[le])
                self.lineid = le + 1
            else:
                new_lines.append(line)
                self.lineid += 1
        if not has_cg_block:
            self.debug("no codegen block can be found")
        else:
            # write back if differs
            write_content = '\n'.join(new_lines)
            if write_content != file_content:
                self.info("file modified!")
                with open(self.filename, "w") as f:
                    f.write(write_content)
            else:
                self.info("file unchanged.")