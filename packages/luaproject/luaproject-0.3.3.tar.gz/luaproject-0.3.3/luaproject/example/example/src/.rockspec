package = "package-name"
version = "0.1.0-1"
source = {
    url = "package-name-0.1.0-1.zip"
}
description = {
    summary = "lua plugin package-name",
}
dependencies = {
    "lua >= 5.1, < 5.4",
}
build = {
    type = "builtin",
    modules = {
        ["kong.plugins.package-name.handler"] = "lua/handler.lua",
        ["kong.plugins.package-name.schema"] = "lua/schema.lua",
    }
}