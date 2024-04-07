-- 7 Знайти оцінки студентів у окремій групі з певного предмета --
select  s."name" as student, 
		g2."name" as  group_name, 
		s2."name" as subject, 
		g.grade , g.grade_date 
from grades g 
join students s on s.id = g.student_id
join subjects s2 on s2.id = g.subject_id
join "groups" g2 on g2.id = s.group_id
where g2.id = 2 and s2."name" = 'Philosophy'