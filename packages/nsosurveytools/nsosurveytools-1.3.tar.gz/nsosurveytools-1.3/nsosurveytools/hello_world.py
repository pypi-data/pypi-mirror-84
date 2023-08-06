import tkinter as tk
import sys

class ExampleApp(tk.Tk):
    def __init__(self, **options):
        tk.Tk.__init__(self)
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")
        b1 = tk.Button(self, text="print to stdout", command=self.print_stdout)
        b2 = tk.Button(self, text="print to stderr", command=self.print_stderr)
        b1.pack(in_=toolbar, side="left")
        b2.pack(in_=toolbar, side="left")
        self.text = tk.Text(self, wrap="word")
        self.text.pack(side="top", fill="both", expand=True)
        self.text.tag_configure("stderr", foreground="#b22222")

        self.re_stdout = options.get('stdout')
        self.re_stderr = options.get('stderr')

        if self.re_stderr or self.re_stderr:
            tk.Button(self, text='Start redirect', command=self.start_redirect).pack(in_=toolbar, side="left")
            tk.Button(self, text='Stop redirect', command=self.stop_redirect).pack(in_=toolbar, side="left")

    def start_redirect(self):
        self.re_stdout.start(TextRedirector(self.text, "stdout").write) if self.re_stdout else ...
        self.re_stderr.start(TextRedirector(self.text, "stderr").write) if self.re_stderr else ...

    def stop_redirect(self):
        self.re_stdout.stop() if self.re_stdout else ...
        self.re_stderr.stop() if self.re_stderr else ...

    @staticmethod
    def print_stdout():
        """Illustrate that using 'print' writes to stdout"""
        print("this is stdout")

    @staticmethod
    def print_stderr():
        """Illustrate that we can write directly to stderr"""
        sys.stderr.write("this is stderr\n")


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, msg):
        self.widget.configure(state="normal")
        self.widget.insert("end", msg, (self.tag,))
        self.widget.configure(state="disabled")
        
        
def test_tk_without_stop_btn():
    app = ExampleApp()
    with RedirectStdMsg(sys.stdout)(TextRedirector(app.text, "stdout").write), \
            RedirectStdMsg(sys.stderr)(TextRedirector(app.text, "stderr").write):
        app.mainloop()


def test_tk_have_stop_btn():
    director_out = RedirectStdMsg(sys.stdout)
    director_err = RedirectStdMsg(sys.stderr)
    app = ExampleApp(stdout=director_out, stderr=director_err)
    app.mainloop()


def test_to_file():

    # stdout test
    with open('temp.stdout.log', 'w') as file_obj:
        with RedirectStdMsg(sys.stdout)(file_obj.write):
            print('stdout to file')
    print('stdout to console')


    # stderr test
    with open('temp.stderr.log', 'w') as file_obj:
        with RedirectStdMsg(sys.stderr)(file_obj.write):
            sys.stderr.write('stderr to file')
    sys.stderr.write('stderr to console')

    # another way
    cs_stdout = RedirectStdMsg(sys.stdout)
    cs_stdout.start(open('temp.stdout.log', 'a').write)
    print('stdout to file 2')
    ...
    cs_stdout.stop()
    print('stdout to console 2')


if __name__ == '__main__':
    test_to_file()
    test_tk_without_stop_btn()
    test_tk_have_stop_btn()