project_root/
├── table_parser/             # SQL 테이블 파서 모듈
│   ├── __init__.py
│   ├── parser.py             # SQL 파싱 및 테이블 메타정보 추출
│   └── utils.py              # 타입 변환 등 유틸 함수
│
├── code_generator/           # 코드 생성 모듈
│   ├── __init__.py
│   ├── domain_generator.py   # Domain.java 생성기
│   ├── mapper_generator.py   # Mapper.java 생성기
│   ├── service_generator.py  # Service.java 생성기
│   ├── service_impl_generator.py # ServiceImpl.java 생성기
│   └── xml_generator.py      # Mapper.xml 생성기
│
├── templates/                # 코드 템플릿 (Jinja2 등)
│   ├── domain.tpl
│   ├── mapper_java.tpl
│   ├── service.tpl
│   ├── service_impl.tpl
│   └── mapper_xml.tpl
│
├── views.py                  # 사용자 입력 받아 파싱 및 파일 생성 뷰
├── urls.py
└── settings.py
