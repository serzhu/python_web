-- 5 Знайти які курси читає певний викладач --
select  s."name" as subject, 
		t."name" as teacher
from subjects s
join teachers t  on t.id = s.teacher_id
where t.id  = 4