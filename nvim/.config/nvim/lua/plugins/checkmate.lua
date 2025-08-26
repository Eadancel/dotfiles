return {
    "bngarren/checkmate.nvim",
    ft = "markdown", -- Lazy loads for Markdown files matching patterns in 'files'
    opts = {
        -- your configuration here
        -- or leave empty to use defaults
        -- metadata
        metadata = {
            due={
                style = function(context)
                    dateStr = context.value:lower() 
                    local year, month, day = dateStr:match("(%d+)-(%d+)-(%d+)")
                    local targetDate = os.time({year = tonumber(year), month = tonumber(month), day = tonumber(day)})
                    local currentDate = os.time()
                    diff = os.difftime(targetDate, currentDate) / (24 * 60 * 60)
                    local days_diff = math.floor(diff + 0.5)
                    
                    if days_diff < 1 then
                        return { fg = "#ff5555", bold = true }
                    elseif days_diff < 2 then
                        return { fg = "#ffb86c" }
                    elseif days_diff < 5 then
                        return { fg = "#8be9fd" }
                    else -- fallback
                        return { fg = "#8be9fd" }
                    end
                end,
                get_value = function()
                        local currentTime = os.time()
                        local futureTime = currentTime + (12 * 24 * 60 * 60) -- 12 days in the future
                        local futureDateStr = os.date("%Y-%m-%d", futureTime)
                        return futureDateStr -- Default due time 
                    end,
                key = "<leader>Tq",
                sort_order = 10,
                jump_to_on_insert = "value",
                select_on_insert = true,
            },
            done = {
                aliases = { "completed", "finished" },
                style = { fg = "#96de7a" },
                get_value = function()
                    return tostring(os.date("%Y-%m-%d %H:%M"))
                end,
                key = "<leader>Td",
                on_add = function(todo_item)
                    require("checkmate").set_todo_item(todo_item, "checked")
                end,
                on_remove = function(todo_item)
                    require("checkmate").set_todo_item(todo_item, "unchecked")
                end,
                sort_order = 30,
            },
            status = {
                get_value = function()
                    return "backlog"
                end,
                choices = { "backlog", "in-progress", "blocked", "review", "done" },
                key = "<leader>Ta",
                style = { fg = "#ffb86c"},
                jump_to_on_insert = "value",
            }
        }
    },

}
