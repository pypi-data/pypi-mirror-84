import importlib
import sys
from typing import Any, Dict, Optional, Tuple, Union, cast

try:
    from .__version__ import __version__, __version_info__  # noqa
except Exception:
    pass


__author__ = "Carl Oscar Aaro"  # noqa
__email__ = "hello@carloscar.com"  # noqa

__asahi_module = sys.modules["asahi"]
__available_defs: Dict[str, Union[Tuple[str], Tuple[str, Optional[str]]]] = {
    "extras": ("asahi.extras", None),
}
__imported_modules: Dict[str, Any] = {"asahi": __asahi_module}
__cached_defs: Dict[str, Any] = {}


def __getattr__(name: str) -> Any:
    if name in __cached_defs:
        return __cached_defs[name]

    if name in __available_defs:
        real_name: Optional[str] = name

        adfs = __available_defs[name]
        if len(adfs) == 2:
            module_name, real_name = cast(Tuple[str, Optional[str]], adfs)
        else:
            (module_name,) = cast(Tuple[str], adfs)

        if not __imported_modules.get(module_name):
            try:
                __imported_modules[module_name] = importlib.import_module(module_name)
            except ModuleNotFoundError as e:
                missing_module_name = str(getattr(e, "name", None) or "")
                if missing_module_name and missing_module_name == "asahi.extras":
                    raise ModuleNotFoundError("module 'asahi.extras' not found - install package 'asahi-extras' first")
                raise
            except Exception:  # pragma: no cover
                raise

        module = __imported_modules.get(module_name)

        if real_name is not None:
            __cached_defs[name] = getattr(module, real_name)
        else:
            __cached_defs[name] = module

        return __cached_defs[name]

    raise AttributeError("module 'asahi' has no attribute '{}'".format(name))


__all__ = [
    "__version__",
    "__version_info__",
    "__author__",
    "__email__",
    "extras",
]
