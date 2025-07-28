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
    id, name, seq)
    VALUES (
    #{id}, #{name}, #{seq})
  </insert>

  <update id="update">
    UPDATE {{ table_name }}
    <set>
      <if test="name != null">name = #{name},</if>
      <if test="status != null">status = #{status},</if>
      <if test="seq != null">seq = #{seq},</if>
      updated_at = now()
    </set>
    WHERE no = #{no}
  </update>

  <delete id="delete">
    DELETE FROM {{ table_name }} WHERE no = #{no}
  </delete>

  <update id="completeAll">
    UPDATE {{ table_name }} SET status = true
  </update>

  <delete id="deleteAll">
    DELETE FROM {{ table_name }}
  </delete>

</mapper>
