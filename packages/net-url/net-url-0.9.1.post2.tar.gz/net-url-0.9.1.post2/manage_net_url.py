import os
from luaproject import LuaProjectManager
import net_url

application_root = os.path.abspath(os.path.dirname(net_url.__file__))
manager = LuaProjectManager(application_root).get_manager()

if __name__ == "__main__":
    manager()
