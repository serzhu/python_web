-- 3 Знайти середній бал у групах з певного предмета --
select  g2."name" as group_name, 
		s2."name" as subject, 
		round(avg(g.grade),2) as avg_grade
from grades g 
join students s on s.id = g.student_id
join "groups" g2 on g2.id = s.group_id 
join subjects s2 on s2.id = g.subject_id
where s2."name"  = 'Physics'
group by g2."name", s2."name" 
order by g2."name" 