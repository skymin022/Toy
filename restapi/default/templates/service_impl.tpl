package {{ package }};

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.domain.{{ class_name }};
import {{ mapper_package }}.{{ class_name }}Mapper;
import com.github.pagehelper.PageInfo;

@Service
public class {{ class_name }}ServiceImpl implements {{ class_name }}Service {

    @Autowired
    private {{ class_name }}Mapper {{ class_name|lower }}Mapper;

    @Override
    public List<{{ class_name }}> list() {
        return {{ class_name|lower }}Mapper.list();
    }

    @Override
    public PageInfo<{{ class_name }}> list(int page, int size) {
        // PageHelper 사용 예시 (필요에 따라 import, 의존 추가 필요)
        com.github.pagehelper.PageHelper.startPage(page, size);
        List<{{ class_name }}> list = {{ class_name|lower }}Mapper.list();
        return new PageInfo<>(list);
    }

    @Override
    public {{ class_name }} select(Long no) {
        return {{ class_name|lower }}Mapper.select(no);
    }

    @Override
    public {{ class_name }} selectById(String id) {
        return {{ class_name|lower }}Mapper.selectById(id);
    }

    @Override
    public boolean insert({{ class_name }} entity) {
        return {{ class_name|lower }}Mapper.insert(entity) > 0;
    }

    @Override
    public boolean update({{ class_name }} entity) {
        return {{ class_name|lower }}Mapper.update(entity) > 0;
    }

    @Override
    public boolean updateById({{ class_name }} entity) {
        return {{ class_name|lower }}Mapper.updateById(entity) > 0;
    }

    @Override
    public boolean delete(Long no) {
        return {{ class_name|lower }}Mapper.delete(no) > 0;
    }

    @Override
    public boolean deleteById(String id) {
        return {{ class_name|lower }}Mapper.deleteById(id) > 0;
    }

    {% if 'status' in fields|map(attribute='name') %}
    @Override
    public boolean completeAll() throws Exception {
        return {{ class_name|lower }}Mapper.completeAll() > 0;
    }
    {% endif %}

    @Override
    public boolean deleteAll() throws Exception {
        return {{ class_name|lower }}Mapper.deleteAll() > 0;
    }
}
