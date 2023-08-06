import itertools as _itertools

import javalang



def __extract_java_identifier_tokens(s):
    try:
        token_stream = javalang.tokenizer.tokenize(s)
    except:
        return []

    return list(
        token.value
        for token in token_stream
        if isinstance(token, javalang.tokenizer.Identifier)
    )

def __extract_code_blobs_from_markdown(s):
    DEFAULT_LANGUAGE = "java"
    return [
        {
            "language": lang or DEFAULT_LANGUAGE,
            "code": md_code_block or md_code_inline2 or md_code_inline1,
        }
        for (lang, md_code_block, md_code_inline2, md_code_inline1) in _re.findall(
            r"```([^\n]*)([^`]*)```|``([^`]*)``|`([^`]*)`",
            s)
    ]

def __extract_java_identifier_tokens_from_markdown(s):

    java_code_blobs = map(lambda blob: blob.get("code"), filter(
        lambda blob: blob.get("language", "").lower() == "java",
        __extract_code_blobs_from_markdown(s)))

    java_identifier_tokens = _itertools.chain(*map(
        __extract_java_identifier_tokens, java_code_blobs))

    return set(java_identifier_tokens)

def extract_variables_from_java_markdown(s):
    return __extract_java_identifier_tokens_from_markdown(s)




def __extract_var_info_from_ast(node):

    is_formal_parameter = isinstance(node, javalang.tree.FormalParameter)
    is_local_variable = isinstance(node, javalang.tree.VariableDeclaration)
    is_field_variable = isinstance(node, javalang.tree.FieldDeclaration)
    is_static_variable = "static" in node.modifiers
    is_array_variable = False

    if node.type and node.type.dimensions and len(node.type.dimensions) > 0:
        is_array_variable = True

    var_kind = None

    if is_formal_parameter:
        var_kind = "parameter"
    elif is_local_variable:
        var_kind = "local"
    elif is_field_variable:
        if is_static_variable:
            var_kind = "constant"
        else:
            var_kind = "instance"

    properties = {
        "type": node.type,
        "kind": var_kind,
        "is_local": is_local_variable,
        "is_field": is_field_variable,
        "is_static": is_static_variable,
        "is_array": is_array_variable,
    }

    def __instantiate(declarator, base_properties=properties):
        is_initialized = declarator.initializer is not None

        properties = {
            "name": declarator.name,
            "is_initialized": is_initialized,
        }

        if isinstance(declarator.initializer, javalang.tree.Literal):
            properties["initial_value"] = declarator.initializer.value
        elif isinstance(declarator.initializer, javalang.tree.MemberReference):
            properties["initial_value"] = declarator.initializer.member
        else:
            properties["initial_node"] = declarator.initializer

        properties.update(base_properties)

        return properties

    if not is_formal_parameter:
        return list(map(__instantiate, node.declarators))

    else:
        properties["name"] = node.name
        return [ properties ]


def extract_variables_from_java_code(code):

    # Parse Java AST
    try:
        tree = javalang.parse.parse(code)
    except javalang.parser.JavaSyntaxError as jse:
        print(code)
        return []
    except AttributeError as ae:
        print(code)
        #raise
        return []

    # Collect all relevant nodes
    nodes = [
        node for path, node in _itertools.chain(
            tree.filter(javalang.tree.FieldDeclaration),
            tree.filter(javalang.tree.VariableDeclaration),
            tree.filter(javalang.tree.FormalParameter))
    ]

    # Transform into variable infos
    var_infos = _itertools.chain(*map(__extract_var_info_from_ast, nodes))

    return list(var_infos)