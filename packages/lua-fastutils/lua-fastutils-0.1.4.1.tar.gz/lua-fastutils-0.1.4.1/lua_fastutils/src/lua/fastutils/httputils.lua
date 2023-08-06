local httputils = {}


function httputils.get_request_data(name, queries, body, headers)
    local value = nil

    if headers == nil then
        headers = {}
    end
    if body == nil then
        body = {}
    end
    if queries == nil then
        queries = {}
    end

    value = headers[name]
    if value ~= nil then
        return value
    end

    value = body[name]
    if value ~= nil then
        return value
    end

    value = queries[name]
    if value ~= nil then
        return value
    end

    return nil
end


function httputils.header_lines_to_headers_mapping(header_lines)
    local strutils = require("fastutils.strutils")
    local headers = {}
    for _, header_line in pairs(header_lines) do
        local k, v = strutils.split2(header_line, ":")
        if k ~= nil and v ~= nil then
            k = strutils.trim(k)
            v = strutils.trim(v)
            headers[k] = v
        end
    end
    return headers
end

function httputils.url_path_match(url, path)
    local strutils = require("fastutils.strutils")
    local schema, left = strutils.split2(url, "://")
    local host, left = strutils.split2(left, "/")
    local url_path, params = strutils.split2(left, "?")
    if url_path == nil then
        url_path = params
    end
    local url_path = "/" .. url_path
    if url_path == path then
        return true
    else
        return false
    end
end

return httputils
