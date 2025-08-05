import re

def parse_create_table(sql: str) -> dict:
    """
    SQL CREATE TABLE 문에서 테이블명, 컬럼정보 추출
    컬럼정보: 이름, 타입, 제약조건, 코멘트 등
    """
    table_info = {
        'table_name': '',
        'columns': []
    }

    # 테이블명 추출 (IF NOT EXISTS 있을 경우도 포함, 백틱 포함 가능)
    table_name_match = re.search(r"CREATE TABLE\s+(IF NOT EXISTS\s+)?`?(\w+)`?\s*\(", sql, re.IGNORECASE)
    if table_name_match:
        table_info['table_name'] = table_name_match.group(2)
    else:
        raise ValueError("테이블명을 찾을 수 없습니다.")



    # 컬럼 추출 (간단히 괄호 내부 줄 단위로)
    columns_str = re.search(r"\((.*)\)", sql, re.DOTALL).group(1).strip()
    columns_lines = [line.strip().rstrip(',') for line in columns_str.splitlines() if line.strip()]

    for col_line in columns_lines:
        # 컬럼명, 데이터타입, 옵션, 주석 분리 (대략적 분리)
        # 예: `no` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'PK',
        col_parts = re.split(r'\s+', col_line, maxsplit=3)
        if len(col_parts) < 2:
            continue
        col_name = col_parts[0].strip('`')
        sql_type = col_parts[1]
        rest = col_parts[2] if len(col_parts) > 2 else ''
        comment_match = re.search(r"COMMENT\s+'([^']*)'", col_line)
        comment = comment_match.group(1) if comment_match else ''

        table_info['columns'].append({
            'name': col_name,
            'sql_type': sql_type,
            'options': rest,
            'comment': comment
        })

    return table_info