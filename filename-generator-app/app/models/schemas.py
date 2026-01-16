from marshmallow import Schema, fields

class FileNameSchema(Schema):
    prefix = fields.Str(required=True, description="The prefix for the file name")
    suffix = fields.Str(required=False, description="The suffix for the file name")
    extension = fields.Str(required=False, default="txt", description="The file extension")