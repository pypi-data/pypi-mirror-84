from flask_restful import reqparse
from flask import request


class ArgsMixin(object):
    """
    Helpers to retrieve parameters from GET or POST queries.
    """

    def get_args(self, descriptors):
        parser = reqparse.RequestParser()
        for descriptor in descriptors:
            action = None

            if len(descriptor) == 4:
                (name, default, required, action) = descriptor
            else:
                (name, default, required) = descriptor

            parser.add_argument(
                name, required=required, default=default, action=action
            )

        return parser.parse_args()

    def clear_empty_fields(self, data):
        """
        Remove fiels set to None from data dict.
        """
        for key in list(data.keys()):
            if data[key] is None:
                del data[key]
        return data

    def get_page(self):
        """
        Returns page requested by the user.
        """
        options = request.args
        return int(options.get("page", "-1"))

    def get_force(self):
        """
        Returns force parameter.
        """
        options = request.args
        return options.get("force", "false") == "true"

    def get_relations(self):
        """
        Returns force parameter.
        """
        options = request.args
        return options.get("relations", "false") == "true"

    def get_episode_id(self):
        """
        Returns episode ID parameter.
        """
        options = request.args
        return options.get("episode_id", None)
