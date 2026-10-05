"""Schema validation for Day 6."""

def validate_arguments(arguments, schema):

    # -----------------------------------------------------
    # 1. Arguments must be an object
    # -----------------------------------------------------

    if not isinstance(arguments, dict):
        return "Expected a JSON object."


    properties = schema.get("properties", {})


    # -----------------------------------------------------
    # 2. Missing required arguments
    # -----------------------------------------------------

    for required in schema.get("required", []):

        if required not in arguments:
            return (
                f"Missing required argument '{required}'. "
                f"Expected one of: {', '.join(properties)}."
            )


    # -----------------------------------------------------
    # 3. Invented arguments
    # -----------------------------------------------------

    if schema.get("additionalProperties") is False:

        for key in arguments:

            if key not in properties:

                return (
                    f"Invented argument '{key}'. "
                    f"Allowed arguments: {', '.join(properties)}."
                )


    # -----------------------------------------------------
    # 4. Type and enum validation
    # -----------------------------------------------------

    for key, value in arguments.items():

        if key not in properties:
            continue

        rule = properties[key]

        expected_type = rule.get("type")


        # Wrong type
        if expected_type == "string" and not isinstance(value, str):

            return (
                f"Wrong type for '{key}'. "
                f"Expected string but received {type(value).__name__}."
            )


        # Enum validation
        if "enum" in rule:

            if value not in rule["enum"]:

                return (
                    f"Invalid value '{value}' for '{key}'. "
                    f"Expected one of: {', '.join(rule['enum'])}."
                )


    return None