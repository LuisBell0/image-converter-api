import importlib
import pkgutil

# Dynamically import every module in this package
for finder, name, ispkg in pkgutil.iter_modules(__path__, __name__ + "."):
    importlib.import_module(name)


from .registry import get_transform_map

TRANSFORM_MAP = get_transform_map()
