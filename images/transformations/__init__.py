import importlib
import pkgutil
from pathlib import Path

__path__.append(str(Path(__file__).parent / "transform_classes"))

# Dynamically import every module in this package
for finder, name, ispkg in pkgutil.iter_modules(__path__, __name__ + "."):
    importlib.import_module(name)


from .registry import get_transform_map

TRANSFORM_MAP = get_transform_map()
