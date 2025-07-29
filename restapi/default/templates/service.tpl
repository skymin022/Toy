package {{ package }};

import com.example.domain.{{ class_name }};
import java.util.List;

public interface {{ class_name }}Service extends BaseService<{{ class_name }}> {

    {% set field_names = fields|map(attribute='name')|map('lower') %}
    {% if 'status' in field_names %}
    boolean completeAll() throws Exception;
    {% endif %}
    boolean deleteAll() throws Exception;
}
