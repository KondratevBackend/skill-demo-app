# Перечисления (ENUM)
Alembic демонстрирует ограниченную совместимость с типом данных ENUM, поэтому при выполнении операций, связанных с перечислениями, необходимо учитывать ряд специфических ситуаций, рассмотренных в последующих разделах.
### 1. Создал? - Не забудь удалить.
В процессе миграции, при создании таблицы с новым типом перечисления, сгенерированная строка в функции upgrade будет выглядеть следующим образом:
```python
sa.Column('column_name', sa.Enum('VALUE1', 'VALUE2', ..., 'VALUEN', name='enumname'), ...)
```
В данной ситуации код функции upgrade корректен. Однако в функции downgrade отсутствует информация о новом типе. Важно отметить, что тип перечисления является независимым объектом и не удаляется автоматически при удалении таблицы. Поэтому в функцию downgrade необходимо добавить следующий код для удаления типа:
```python
sa.Enum(name='enumname').drop(op.get_bind(), checkfirst=False)
```
### 2. Как указать уже существующий ENUM для нового столбца?
При создании новой колонки или изменении типа уже существующей, вместо явного указания перечисления, как в примере:
```python
sa.Enum('VALUE1', 'VALUE2', ..., 'VALUEN', name='enumname')
```
Следует использовать:
```python
postgresql.ENUM(name='enumname', create_type=False)
```
Здесь postgresql импортируется из модуля sqlalchemy.dialects.
### 3. Как заменить тип данных уже существующего столбца на тип данных ENUM?
Пример выполнения миграции для изменения типа столбца на новый тип перечисления:
```python
def upgrade():
    new_type = sa.Enum('VALUE1', 'VALUE2', ..., 'VALUEN', name='enumname')
    new_type.create(op.get_bind(), checkfirst=True)
    op.execute('ALTER TABLE table_name ALTER COLUMN column_name TYPE enumname USING column_name::enumname')

def downgrade():
    op.execute('ALTER TABLE table_name ALTER COLUMN column_name TYPE VARCHAR')
    sa.Enum(name='enumname').drop(op.get_bind(), checkfirst=False)
```
В данном примере выполняется замена типа колонки с текстового значения на перечисление, при этом новый тип перечисления должен содержать все значения, которые ранее присутствовали в изменяемой колонке.
### 4. Как изменить существующий ENUM?
Один из наиболее важных аспектов работы с перечислениями – это изменение значений существующего типа. Пример процедуры:
```python
old_options = ('VALUE1', 'VALUE2', 'VALUE3')
new_options = old_options + ('VALUE4',)

old_type = sa.Enum(*old_options, name='enumname')
new_type = sa.Enum(*new_options, name=old_type.name)
tmp_type = sa.Enum(*new_options, name=f'_{old_type.name}')

table = sa.sql.table('table_name', sa.Column('column_name', new_type, ...))

def upgrade():
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE table_name ALTER COLUMN column_name DROP DEFAULT')
    op.execute(f'ALTER TABLE table_name ALTER COLUMN column_name TYPE {tmp_type.name} USING column_name::text::{tmp_type.name}')
    old_type.drop(op.get_bind(), checkfirst=False)

    new_type.create(op.get_bind(), checkfirst=False)
    op.execute(f'ALTER TABLE table_name ALTER COLUMN column_name TYPE {new_type.name} USING column_name::text::{new_type.name}')
    op.execute('ALTER TABLE table_name ALTER COLUMN column_name SET DEFAULT \'VALUE2\'::enumname')
    tmp_type.drop(op.get_bind(), checkfirst=False)

def downgrade():
    op.execute(table.update().where(table.c.column_name == 'VALUE4').values(column_name='VALUE1'))

    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE table_name ALTER COLUMN column_name DROP DEFAULT')
    op.execute(f'ALTER TABLE table_name ALTER COLUMN column_name TYPE {tmp_type.name} USING column_name::text::{tmp_type.name}')
    new_type.drop(op.get_bind(), checkfirst=False)

    old_type.create(op.get_bind(), checkfirst=False)
    op.execute(f'ALTER TABLE table_name ALTER COLUMN column_name TYPE {old_type.name} USING column_name::text::{old_type.name}')
    op.execute('ALTER TABLE table_name ALTER COLUMN column_name SET DEFAULT \'VALUE2\'::enumname')
    tmp_type.drop(op.get_bind(), checkfirst=False)
```
В данном примере команды DROP DEFAULT и SET DEFAULT можно опустить, если у колонки не было значения по умолчанию. При откате изменений новое значение заменяется на одно из старых.
