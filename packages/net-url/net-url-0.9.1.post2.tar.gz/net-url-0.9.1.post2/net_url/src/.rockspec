package = "net-url"
version = "0.9-1"

source = {
   url = "net-url-0.9-1.zip",
}

description = {
   summary = "URL and Query string parser, builder, normalizer for Lua.",
   detailed = [[
      This small Lua library provides a few functions to parse URL with querystring and build new URL easily.
   ]],
   homepage = "https://github.com/golgote/neturl",
   license = "MIT/X11"
}

dependencies = {
   "lua >= 5.1"
}

build = {
   type = "builtin",
   modules = {
      ["net.url"] = "lua/net/url.lua"
   }
}