package {{ package }};

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.domain.{{ class_name }};
import {{ mapper_package }}.{{ class_name }}Mapper;

@Service
public class {{ class_name }}ServiceImpl implements {{ class_name }}Service {

    @Autowired
    private {{ class_name }}Mapper {{ class_name|lower }}Mapper;

    @Override
    public List<{{ class_name }}> list() {
        return {{ class_name|lower }}Mapper.list();
    }

    @Override
    public boolean completeAll() throws Exception {
        return {{ class_name|lower }}Mapper.completeAll() > 0;
    }

    @Override
    public boolean deleteAll() throws Exception {
        return {{ class_name|lower }}Mapper.deleteAll() > 0;
    }
}
