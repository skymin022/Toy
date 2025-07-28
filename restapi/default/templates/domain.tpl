package com.example.domain;

import java.util.Date;
import java.util.UUID;
import lombok.Data;

@Data
public class {{ class_name }} {

{% for field in fields %}
    private {{ field.java_type }} {{ field.name }}; {% if field.comment %}// {{ field.comment }}{% endif %}
{% endfor %}

    public {{ class_name }}() {
        this.id = UUID.randomUUID().toString();
    }
}
