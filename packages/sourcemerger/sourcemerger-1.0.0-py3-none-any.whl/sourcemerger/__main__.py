# '.sourcemerger' is actually 'sourcemerger.sourcemerger',
# with the first one being left implicit
from .sourcemerger import _cmdline_tool_main

# This code is executed if sourcemerger is called from the
# command line as a module, i.e. via 'python -m sourcemerger'
if __name__ == '__main__':
    _cmdline_tool_main()
