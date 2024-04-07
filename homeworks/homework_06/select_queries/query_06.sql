-- 6 Знайти список студентів у певній групі --
select  s."name" as student, 
		g."name" as group_name
from "groups" g
join students s on s.group_id = g.id 
where g.id = 2