from marshmallow import Schema, fields


class EnemySchema(Schema):
    id = fields.Int()
    breed = fields.Str()
    type = fields.Str()
    to_kill = fields.Str()
    data = fields.Str()
    nemesis = fields.Str()
