<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper
  PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="{{ package }}.{{ class_name }}Mapper">

  <select id="list" resultType="{{ class_name }}">
    SELECT * FROM {{ table_name }}
  </select>

  <insert id="insert">
    INSERT INTO {{ table_name }}(
      {%- for field in fields %}
        {{ field.name }}{% if not loop.last %}, {% endif %}
      {%- endfor %}
    )
    VALUES (
      {%- for field in fields %}
        #{ {{ field.name }} }{% if not loop.last %}, {% endif %}
      {%- endfor %}
    )
  </insert>

  <update id="update">
    UPDATE {{ table_name }}
    <set>
      {%- for field in fields if field.name not in ['id', 'created_at', 'no'] %}
        <if test="{{ field.name }} != null">{{ field.name }} = #{{ '{' }}{{ field.name }}{{ '}' }},{% if not loop.last %}\n      {% endif %}</if>
      {%- endfor %}
      updated_at = now()
    </set>
    WHERE {% if 'no' in fields|map(attribute='name') %}no = #{no}{% elif 'id' in fields|map(attribute='name') %}id = #{id}{% else %}-- key 지정 필요{% endif %}
  </update>

  <delete id="delete">
    DELETE FROM {{ table_name }} WHERE {% if 'no' in fields|map(attribute='name') %}no = #{no}{% elif 'id' in fields|map(attribute='name') %}id = #{id}{% else %}-- key 지정 필요{% endif %}
  </delete>

  <update id="completeAll">
    UPDATE {{ table_name }} SET {% if 'status' in fields|map(attribute='name') %}status = true{% else %}-- 수정필드 없음{% endif %}
  </update>

  <delete id="deleteAll">
    DELETE FROM {{ table_name }}
  </delete>
</mapper>
