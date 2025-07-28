def sql_type_to_java_type(sql_type: str) -> str:
    sql_type = sql_type.upper()
    if 'BIGINT' in sql_type:
        return 'Long'
    elif 'VARCHAR' in sql_type or 'TEXT' in sql_type or 'CHAR' in sql_type:
        return 'String'
    elif 'BOOLEAN' in sql_type or 'TINYINT(1)' in sql_type:
        return 'Boolean'
    elif 'INT' in sql_type:
        return 'Integer'
    elif 'TIMESTAMP' in sql_type or 'DATETIME' in sql_type or 'DATE' in sql_type:
        return 'Date'
    else:
        return 'String'  # 기본 타입
