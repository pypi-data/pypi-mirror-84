"""
This file contains the transformation class.
"""


class HL7Transform:
    """
    The transformation class that applies an :class:`HL7Mapping` to
    an :class:`HL7Message`.
    """
    def __init__(self, mapping):
        """
        :param mapping: A dictionary that contains field mappings.
        """
        self.mapping = mapping

    def execute(self, message):
        from warnings import warn
        warn("This function is deprecated. Use __call__ instead.")
        return self(message)

    def __call__(self, message):
        """
        Applies the transformation to an HL7 message and outputs the
        transformed message both as the return value and
        by modifying the input message.

        :param message: Applies the transformation to this message.
        :return: The transformed copy of the input message.
        """
        for mapping in self.mapping:
            for target_field, operation in mapping.items():
                try:
                    message[target_field] = operation(message)
                except (IndexError, KeyError) as e:
                    print(message.to_string())
                    raise RuntimeError("Error occurred during processing of {}. Reason: {}".format(target_field, str(e)))
        return message
