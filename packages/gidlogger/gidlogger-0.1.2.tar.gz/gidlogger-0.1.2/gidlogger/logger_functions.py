
# region [Imports]

# * Standard Library Imports -->
import os
import sys
import logging
from logging import handlers
from functools import wraps

# endregion [Imports]

# region [TOC]


# endregion [TOC]


# region [Constants]

__updated__ = '2020-11-01 21:25:58'


# endregion [Constants]

# region[Global_Functions]

def pathmaker(first_segment, *in_path_segments, rev=False):
    """
    Normalizes input path or path fragments, replaces '\\\\' with '/' and combines fragments.

    Parameters
    ----------
    first_segment : str
        first path segment, if it is 'cwd' gets replaced by 'os.getcwd()'
    rev : bool, optional
        If 'True' reverts path back to Windows default, by default None

    Returns
    -------
    str
        New path from segments and normalized.
    """
    _first = os.getcwd() if first_segment == 'cwd' else first_segment
    _path = os.path.join(_first, *in_path_segments)
    _path = _path.replace('\\\\', '/')
    _path = _path.replace('\\', '/')
    if rev is True:
        _path = _path.replace('/', '\\')

    return _path.strip()
# endregion[Global_Functions]

# region [Logging_Messages]


def imported(in_name):
    return (f"succesfully imported [-{in_name}-]")


def DEPRECATED(in_alternative=None):
    if in_alternative is None:
        _msg = "!!!!!!!!!DEPRECATED FUNCTION!!!!!!!!!, stop using it!"
    else:
        _msg = f"!!!!!!!!!DEPRECATED FUNCTION!!!!!!!!!, use [{in_alternative}] instead!"
    return _msg


def NEWRUN():
    return "# " + "*-$-" * 6 + "* --> NEW_RUN <-- " + "*-?-" * 6 + "* #"


def class_initiated(in_class, use=None):
    if use == 'repr':
        _string = repr(in_class)
    elif use == 'str':
        _string = str(in_class)
    else:
        _string = in_class.__class__.__name__
    return f"finished initiating {_string} class"


def called(function_name):
    return f"{function_name} was called"


def completed(function_name):
    return f"{function_name} completed"

# endregion [Logging_Messages]


# region [Logging_Settings]


def aux_logger(in_name):
    return logging.getLogger('main').getChild(in_name)


def main_logger(in_file_name, in_level, in_back_up=2):

    _out = logging.getLogger('main')
    _out.setLevel(getattr(logging, in_level.upper()))
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(lineno)s : %(funcName)s : %(message)s')
    should_roll_over = os.path.isfile(in_file_name)
    handler = handlers.RotatingFileHandler(in_file_name, mode='a', backupCount=in_back_up)
    handler.namer = std_namer
    if should_roll_over:
        handler.doRollover()
    handler.setFormatter(formatter)
    _out.addHandler(handler)

    return _out


def main_logger_stdout(in_level, message_sep: int = 10):

    _out = logging.getLogger('main')
    _out.setLevel(getattr(logging, in_level.upper()))
    formatter = logging.Formatter(fmt='[{levelname}][{funcName}] --> ' + ' ' * message_sep + '{message}', style='{')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    _out.addHandler(handler)

    return _out

# endregion [Logging_Settings]


# region [Logging_Functions]


def std_namer(name):
    _nameparts = name.split('.')
    _path, _basename = _nameparts[0].rsplit('\\', 1)
    return pathmaker(_path, 'old_logs', f'{_basename}_{_nameparts[2]}.{_nameparts[1]}')


def log_folderer(in_log_file_name, in_main_log_folder='logs', in_log_folder_directory=None):
    _cwd = pathmaker(os.getcwd()) if in_log_folder_directory is None else pathmaker(in_log_folder_directory)
    _path_to_old_folder = pathmaker(_cwd, in_main_log_folder, 'old_logs')
    if os.path.exists(_path_to_old_folder) is False:
        os.makedirs(_path_to_old_folder)
    return pathmaker(_cwd, in_main_log_folder, in_log_file_name + ".log")


def log_args(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        _log = logging.getLogger('main')
        _log.debug('started executing %s: --> %s <--, with arguments: %s, %s %s', type(function).__name__, function.__name__, ', '.join(map(str, args)), ', '.join([f"{str(key)}={str(value)}" for key, value in kwargs.items()]), '-' * 50)
        return function(*args, **kwargs)
    return wrapper


# endregion [Logging_Functions]


# region [Logging_Class_1]


# endregion [Logging_Class_1]
if __name__ == "__main__":
    pass
