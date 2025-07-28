package {{ package }};

import org.apache.ibatis.annotations.Mapper;
import com.example.domain.{{ class_name }};

@Mapper
public interface {{ class_name }}Mapper extends BaseMapper<{{ class_name }}> {

    int completeAll() throws Exception;
    int deleteAll() throws Exception;
}
