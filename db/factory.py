import random

import sqlalchemy as sa


def _randint():
    return random.randint(1, 10 ** 9)


_type_to_value = {
    sa.Integer: _randint,
    sa.String: lambda: 'empty',
}


class Factory:
    def __init__(self, engine, declarative_base):
        self._engine = engine
        self._inspector = sa.inspect(engine)

        self._name_to_table = {}
        for table_cls in declarative_base._decl_class_registry.values():
            if not hasattr(table_cls, '__tablename__'):
                continue
            self._name_to_table[table_cls.__tablename__] = table_cls

    def create_model(self, model_cls, session, flexibility_map=None):
        flexibility_map = flexibility_map or {}

        fkeys = self._inspector.get_foreign_keys(model_cls.__tablename__)
        object_kwargs = {}
        for fk in fkeys:
            name = fk['referred_table']
            constrained_column_name, = fk['constrained_columns']
            constrained_column = getattr(model_cls, constrained_column_name)
            if constrained_column.nullable:
                continue

            referred_table = self._name_to_table[name]

            if referred_table not in flexibility_map:
                object_kwargs[name] = self.create_model(referred_table, session, flexibility_map)
            else:
                object_kwargs[name] = flexibility_map[referred_table]

        columns = self._inspector.get_columns(model_cls.__tablename__)
        for column_info in columns:
            name = column_info['name']
            column = getattr(model_cls, name)
            if column.primary_key:
                continue
            if column in flexibility_map:
                object_kwargs[name] = flexibility_map[column]
            else:
                if column.nullable:
                    continue
                column_type = type(column.type)
                object_kwargs[name] = _type_to_value[column_type]()

        obj = model_cls(**object_kwargs)
        session.add(obj)
        return obj

    def _process_fk(self, fk):
        pass
