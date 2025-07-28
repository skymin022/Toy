package {{ package }};

import com.example.domain.{{ class_name }};
import java.util.List;

public interface {{ class_name }}Service extends BaseService<{{ class_name }}> {
    boolean completeAll() throws Exception;
    boolean deleteAll() throws Exception;
}
