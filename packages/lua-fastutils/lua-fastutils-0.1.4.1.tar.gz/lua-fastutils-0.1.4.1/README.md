# lua-fastutils

Collection of simple utils.

## Install

```shell
pip install lua-fastutils
```

## LUA modules

- fastutils.httputils
  - get_request_data
  - header_lines_to_headers_mapping
  - url_path_match
- fastutils.strutils
  - capitalize
  - camel
  - is_in_array
  - startswith
  - endswith
  - is_match_patterns
  - trim
  - ltrim
  - rtrim
  - trim_strings
  - remove_empty_string_from_table
  - split2
  - split
  - is_empty
- fastutils.tableutils
  - concat
- fastutils.typingutils
  - is_string
  - is_number
  - is_boolean
  - is_nil
  - is_function
  - is_table
  - is_list
  - is_map
  - tostring

## Installed Command Utils

- manage-lua-fastutils

## Usage

```shell
Usage: manage-lua-fastutils [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  install  Create a lua package and then install it.
  pack     Create a lua package.
```

## Releases

### v0.1.4-1 2020/11/04

- Add typingutils.
- Add httputils.
- Add tableutils.

### v0.1.0-1 2020/08/27

- First release.
