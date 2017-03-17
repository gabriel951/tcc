--select * from bd_unb.student limit 1;

--select * from bd_unb.student where (sex <> 'm' and sex <>'f') limit 10;

--select * from bd_unb.student where course like '%engenharia de compu%' limit 10;

select cod_mat from bd_unb.student where way_out like 'Falecimento' limit 10;