from marshmallow import Schema, fields


class EnemySchema(Schema):
    id = fields.Int()
    breed = fields.Str()
    type = fields.Str()
    task = fields.Str()
    data = fields.Str()
    nemesis = fields.Str()
    selected_by = fields.Str(default="")
