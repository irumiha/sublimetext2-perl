import sublime, sublime_plugin, re, commands

class PerldocForWordCommand(sublime_plugin.TextCommand):
  def showdoc(self,name,doctext):
    help_view, _id = self.view_in_tab("Perldoc: "+name,doctext)
    help_view.set_read_only(_id)

  def view_in_tab(self, title, text):
    '''Helper function to display information in a tab.
    '''
    tab = self.view.window().new_file()
    tab.set_name(title)
    _id = tab.buffer_id()
    tab.set_scratch(_id)
    tab.settings().set("gutter", True)
    tab.settings().set("line_numbers", False)
    tab.set_syntax_file("Packages/Markdown/Markdown.tmLanguage")
    ed = tab.begin_edit()
    tab.insert(ed, 0, text)
    tab.end_edit(ed)
    return tab, _id

  def run(self, edit):
    funclist = ["abs", "accept", "alarm", "atan2", "bind", "binmode", 
                "bless", "break", "caller", "chdir", "chmod", "chomp", 
                "chop", "chown", "chr", "chroot", "close", "closedir", 
                "connect", "continue", "cos", "crypt", "dbmclose", "dbmopen", 
                "defined", "delete", "die", "do", "dump", "each", "endgrent", 
                "endhostent", "endnetent", "endprotoent", "endpwent", 
                "endservent", "eof", "eval", "exec", "exists", "exit", "exp", 
                "fcntl", "fileno", "flock", "fork", "format", "formline", 
                "getc", "getgrent", "getgrgid", "getgrnam", "gethostbyaddr", 
                "gethostbyname", "gethostent", "getlogin", "getnetbyaddr", 
                "getnetbyname", "getnetent", "getpeername", "getpgrp", 
                "getppid", "getpriority", "getprotobyname", "getprotobynumber", 
                "getprotoent", "getpwent", "getpwnam", "getpwuid", 
                "getservbyname", "getservbyport", "getservent", "getsockname", 
                "getsockopt", "glob", "gmtime", "goto", "grep", "hex", "import", 
                "index", "int", "ioctl", "join", "keys", "kill", "last", "lc", 
                "lcfirst", "length", "link", "listen", "local", "localtime", 
                "lock", "log", "lstat", "m", "map", "mkdir", "msgctl", "msgget", 
                "msgrcv", "msgsnd", "my", "next", "no", "oct", "open", "opendir", 
                "ord", "our", "pack", "package", "pipe", "pop", "pos", "print", 
                "printf", "prototype", "push", "q", "qq", "qr", "quotemeta", 
                "qw", "qx", "rand", "read", "readdir", "readline", "readlink", 
                "readpipe", "recv", "redo", "ref", "rename", "require", "reset",
                "return", "reverse", "rewinddir", "rindex", "rmdir", "s", "say",
                "scalar", "seek", "seekdir", "select", "semctl", "semget", 
                "semop", "send", "setgrent", "sethostent", "setnetent", 
                "setpgrp", "setpriority", "setprotoent", "setpwent", "setservent",
                "setsockopt", "shift", "shmctl", "shmget", "shmread", 
                "shmwrite", "shutdown", "sin", "sleep", "socket", 
                "socketpair", "sort", "splice", "split", "sprintf", "sqrt", 
                "srand", "stat", "state", "study", "sub", "substr", 
                "symlink", "syscall", "sysopen", "sysread", "sysseek", 
                "system", "syswrite", "tell", "telldir", "tie", "tied", 
                "time", "times", "tr", "truncate", "uc", "ucfirst", "umask", 
                "undef", "unlink", "unpack", "unshift", "untie", "use", 
                "utime", "values", "vec", "wait", "waitpid", "wantarray", 
                "warn", "write", "-X", "y"]
    for region in self.view.sel():
      if region.empty():
        p = region.begin()
        s = self.view.substr(self.view.word(p))
      else:
        s = self.view.substr(region)    
      r = ""
      if s in funclist:
        r = commands.getoutput("perldoc -u -f %s | pod2markdown" % s)
      else:
        r = commands.getoutput("perldoc -u %s | pod2markdown" % s)
      self.showdoc(s,r.decode("utf-8"))
