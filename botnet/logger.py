debug_mode=True

def success(string):
    message("SUCCESS", string)

def info(string):
    message("INFO", string)

def warning(string):
    message("WARNING", string)

def error(string):
    message("ERROR", string)

def debug(string):
    if debug_mode:
        message("DEBUG", string)

def message(prefix, message):
    print("[" + prefix + "] " + message)
