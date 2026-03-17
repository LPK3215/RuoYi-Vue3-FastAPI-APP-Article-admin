-- --------------------------------------------------------
-- 教程/知识库字典迁移（MySQL）
-- 适用场景：你已初始化过数据库，但缺少 kb_article_type 字典
-- 说明：
-- - 兼容 MySQL 5.7+
-- - 重复执行安全（已存在则跳过）
-- --------------------------------------------------------

-- 1) 字典类型：kb_article_type
set @kb_dict_type_exists := (
  select count(1)
  from sys_dict_type
  where dict_type = 'kb_article_type'
);

set @kb_dict_type_insert_sql := if(
  @kb_dict_type_exists = 0,
  "insert into sys_dict_type(dict_name, dict_type, status, create_by, create_time, update_by, update_time, remark)
   values('教程文章类型', 'kb_article_type', '0', 'admin', sysdate(), '', null, '教程文章类型（教程/笔记/FAQ等）')",
  "select 1"
);

prepare stmt from @kb_dict_type_insert_sql;
execute stmt;
deallocate prepare stmt;

-- 2) 字典数据：tutorial / note / faq
set @kb_dict_data_tutorial_exists := (
  select count(1)
  from sys_dict_data
  where dict_type = 'kb_article_type' and dict_value = 'tutorial'
);
set @kb_dict_data_note_exists := (
  select count(1)
  from sys_dict_data
  where dict_type = 'kb_article_type' and dict_value = 'note'
);
set @kb_dict_data_faq_exists := (
  select count(1)
  from sys_dict_data
  where dict_type = 'kb_article_type' and dict_value = 'faq'
);

set @kb_dict_data_tutorial_sql := if(
  @kb_dict_data_tutorial_exists = 0,
  "insert into sys_dict_data(dict_sort, dict_label, dict_value, dict_type, css_class, list_class, is_default, status, create_by, create_time, update_by, update_time, remark)
   values(1, '教程', 'tutorial', 'kb_article_type', '', 'primary', 'Y', '0', 'admin', sysdate(), '', null, '教程文章')",
  "select 1"
);

set @kb_dict_data_note_sql := if(
  @kb_dict_data_note_exists = 0,
  "insert into sys_dict_data(dict_sort, dict_label, dict_value, dict_type, css_class, list_class, is_default, status, create_by, create_time, update_by, update_time, remark)
   values(2, '笔记', 'note', 'kb_article_type', '', 'info', 'N', '0', 'admin', sysdate(), '', null, '随手笔记')",
  "select 1"
);

set @kb_dict_data_faq_sql := if(
  @kb_dict_data_faq_exists = 0,
  "insert into sys_dict_data(dict_sort, dict_label, dict_value, dict_type, css_class, list_class, is_default, status, create_by, create_time, update_by, update_time, remark)
   values(3, 'FAQ', 'faq', 'kb_article_type', '', 'warning', 'N', '0', 'admin', sysdate(), '', null, '常见问题')",
  "select 1"
);

prepare stmt2 from @kb_dict_data_tutorial_sql;
execute stmt2;
deallocate prepare stmt2;

prepare stmt3 from @kb_dict_data_note_sql;
execute stmt3;
deallocate prepare stmt3;

prepare stmt4 from @kb_dict_data_faq_sql;
execute stmt4;
deallocate prepare stmt4;

-- 3) 可能历史数据字符集不正确：强制把 kb_article_type 的 dict_label 修正为中文
update sys_dict_data
set dict_label = case dict_value
  when 'tutorial' then '教程'
  when 'note' then '笔记'
  when 'faq' then 'FAQ'
  else dict_label
end
where dict_type = 'kb_article_type';
