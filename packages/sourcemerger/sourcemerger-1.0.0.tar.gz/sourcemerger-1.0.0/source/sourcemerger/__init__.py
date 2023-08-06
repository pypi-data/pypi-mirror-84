# Explanation of ".sourcemerger":
# - to the left of the dot should go the package name (i.e. the name of the
#   folder that contains this file), which in this case should be 'sourcemerger',
#   but it can be left implicit;
# - to the right of the dot goes a module name, i.e. a Python file name,
#   which in this case is 'sourcemerger'; if there were other modules in folder
#   'sourcemerger' then their names could go after the dot as well, e.g. '.newmodule';
#
# A '#noqa' comment tells Flake8 to ignore any warnings caused by the line;
# this is needed because, while the statements below allow external Python code
# (for example the unit tests) to simply write 'import sourcemerger' and
# get sourcemerger's functions with proper scope (like "sourcemerger.fetch_filenames()"),
# Flake8 will warn that, in this file ('__init__.py'), 'fetch_filenames' and
# the other functions are imported but not used.

from .sourcemerger import _cmdline_tool_main # noqa
from .sourcemerger import _fetch_filenames # noqa
from .sourcemerger import merge_files # noqa
from .sourcemerger import _parse_cmdline_arguments # noqa
from .sourcemerger import _remove_include_guard # noqa
from .sourcemerger import _remove_firstparty_includes # noqa
from .sourcemerger import _version # noqa
