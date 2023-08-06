import pkgutil
import os
import re
from functools import lru_cache
from pathlib import Path
from robot.libraries import STDLIBS
from docgen import loader, utils

RESOURCES = (".robot", ".resource", ".txt")
INIT_FILES = ("__init__.py", "__init__.robot", "__init__.txt")

KEYWORDS = re.compile(r"^\*+\s*((?:User )?Keywords?)", re.MULTILINE | re.IGNORECASE)
TASKS = re.compile(r"^\*+\s*(Test Cases?|Tasks?)", re.MULTILINE | re.IGNORECASE)


def find_all():
    matches = []
    matches.extend(builtins())
    matches.extend(walk_directory(os.getcwd()))
    matches.extend(walk_modules())
    return [str(match) for match in matches]


def builtins():
    return [name for name in STDLIBS if name not in ("Reserved", "Remote")]


def walk_modules(root=None):
    modules = []
    for module in pkgutil.iter_modules(root):
        if module.name.startswith("_"):
            continue
        elif module.ispkg:
            root = (Path(module.module_finder.path) / module.name).resolve()
            modules.extend(module.name + "." + name for name in walk_modules([root]))
        else:
            modules.append(module.name)
    return modules


def walk_directory(root, libraries=True, resources=True):
    paths, stack = set(), [Path(root)]
    while stack:
        path = stack.pop(0)
        path = path.resolve()

        if path.name.startswith("_"):
            continue
        try:
            if path.is_dir():
                if libraries and is_module_library(path):
                    paths.add(path)
                for child in path.iterdir():
                    stack.append(child)
            elif libraries and is_library_file(path):
                paths.add(path)
            elif resources and is_resource_file(path):
                paths.add(path)
        except Exception:
            utils.debug_traceback()

    return [path.relative_to(root) for path in paths]


def is_module_library(path):
    if not any((path / init).is_file() for init in INIT_FILES):
        return False

    try:
        return bool(loader.load(path).keywords)
    except ImportError:
        return False


def is_library_file(path):
    return path.suffix == ".py" and path.name != "__init__.py"


@lru_cache(maxsize=None)
def is_resource_file(path):
    if path.name in INIT_FILES or path.suffix not in RESOURCES:
        return False

    with open(path, "r", encoding="utf-8", errors="ignore") as infile:
        content = infile.read()

    has_keywords = bool(re.search(KEYWORDS, content))
    has_tasks = bool(re.search(TASKS, content))

    return not has_tasks and has_keywords
