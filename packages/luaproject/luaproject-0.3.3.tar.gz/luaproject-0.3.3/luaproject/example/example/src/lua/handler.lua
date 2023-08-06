


local BasePlugin = require("kong.plugins.base_plugin")
local PackageClassNameHandler = BasePlugin:extend()
local kong = kong


function PackageClassNameHandler:access(config)
    PackageClassNameHandler.super.access(self)
-- add process logic below

-- add process logic above
end


return PackageClassNameHandler
