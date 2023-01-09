# debug mode
debug_mode=True

# success message
def success(string):
    message("SUCCESS", string)

# info message
def info(string):
    message("INFO", string)

# warning message
def warning(string):
    message("WARNING", string)

# error message
def error(string):
    message("ERROR", string)

# debug message
def debug(string):
    if debug_mode:
        message("DEBUG", string)

# default log message method
def message(prefix, message):
    print("[" + prefix + "] " + message)
