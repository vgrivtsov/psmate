


---------JT-ROD-----------------------
UPDATE psmate_jobtitles A
SET jobtitle_rod = jt_rod_create(B.jobtitle)
FROM psmate_jobtitles B
WHERE A.jobtitle_rod IS NULL AND A.id = B.id;

-----------SLUGIFY--------------------

UPDATE psmate_jobtitles A
SET slug = jt_slug_create(B.jobtitle, B.id)
FROM psmate_jobtitles B
WHERE A.slug IS NULL AND A.id = B.id;


---------------------------------
UPDATE psmate_jobtitles A
SET jobtitle_rod = 'четвертого электромеханика'
WHERE jobtitle_rod = 'четвертого эkектромеханика'
--FROM psmate_jobtitles B
--WHERE A.id = B.id;

---------------------------------
UPDATE psmate_jobtitles
SET jobtitle_rod = REPLACE(jobtitle_rod, 'газы', 'газа')
--WHERE jobtitle_rod like 'газы%%'

---------------------------------------------------------------------
--SELECT table_name 
--FROM information_schema.tables  
--WHERE table_name ~ '^psmate_'

TRUNCATE table
psmate_okpdtr,
psmate_educationalreqs,
psmate_eks,
psmate_jobtitles,
psmate_okso,
psmate_okved,
psmate_okz,
psmate_othercharacts,
psmate_reqworkexperiences,
psmate_specialconditions,
psmate_tf_la,
psmate_tf_nk,
psmate_tf_oc,
psmate_tf_rs,
psmate_gtfinfo,
psmate_psinfo,
psmate_tfinfo
CASCADE;

ALTER SEQUENCE psmate_okpdtr_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_educationalreqs_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_eks_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_jobtitles_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_okso_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_okved_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_okz_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_othercharacts_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_reqworkexperiences_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_specialconditions_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_tf_la_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_tf_nk_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_tf_oc_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_tf_rs_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_gtfinfo_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_psinfo_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_tfinfo_id_seq RESTART WITH 1;
ALTER SEQUENCE psmate_offinsts_id_seq RESTART WITH 1;

---------------------------------------------------------------------
UPDATE psmate_gtfinfo
SET    ps_id = psmate_psinfo.id
FROM   psmate_psinfo
WHERE  psmate_psinfo.psregnum = psmate_gtfinfo.psregnum;

UPDATE psmate_tfinfo
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_tfinfo.nameotf;

UPDATE psmate_jobtitles
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_jobtitles.nameotf;

UPDATE psmate_educationalreqs
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_educationalreqs.nameotf;

UPDATE psmate_eks
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_eks.nameotf;

UPDATE psmate_okpdtr
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_okpdtr.nameotf;

UPDATE psmate_okso
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_okso.nameotf;

UPDATE psmate_okved
SET    ps_id = psmate_psinfo.id
FROM   psmate_psinfo
WHERE  psmate_psinfo.psregnum = psmate_okved.psregnum;

UPDATE psmate_okz
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_okz.nameotf;

UPDATE psmate_okz
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_okz.nameotf;

UPDATE psmate_othercharacts
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_othercharacts.nameotf;

UPDATE psmate_reqworkexperiences
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_reqworkexperiences.nameotf;

UPDATE psmate_specialconditions
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_specialconditions.nameotf;

UPDATE psmate_tf_la
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_tf_la.nameotf;

UPDATE psmate_tf_la
SET    tf_id = psmate_tfinfo.id
FROM   psmate_tfinfo
WHERE  psmate_tfinfo.nametf = psmate_tf_la.nametf;

UPDATE psmate_tf_nk
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_tf_nk.nameotf;

UPDATE psmate_tf_nk
SET    tf_id = psmate_tfinfo.id
FROM   psmate_tfinfo
WHERE  psmate_tfinfo.nametf = psmate_tf_nk.nametf;

UPDATE psmate_tf_oc
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_tf_oc.nameotf;

UPDATE psmate_tf_oc
SET    tf_id = psmate_tfinfo.id
FROM   psmate_tfinfo
WHERE  psmate_tfinfo.nametf = psmate_tf_oc.nametf;

UPDATE psmate_tf_rs
SET    ps_id = psmate_gtfinfo.ps_id, gtf_id = psmate_gtfinfo.id 
FROM   psmate_gtfinfo
WHERE  psmate_gtfinfo.nameotf = psmate_tf_rs.nameotf;

UPDATE psmate_tf_rs
SET    tf_id = psmate_tfinfo.id
FROM   psmate_tfinfo
WHERE psmate_tfinfo.nametf = psmate_tf_rs.nametf;
---------------------------------------------------------------------
UPDATE psmate_gtfinfo A
SET    ps_id = B.id
FROM   psmate_psinfo B
WHERE  A.ps_id IS NULL AND B.psregnum = A.psregnum;

UPDATE psmate_tfinfo A
SET ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_jobtitles A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_educationalreqs A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_eks A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_okpdtr A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_okso A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_okved A
SET    ps_id = B.id
FROM   psmate_psinfo B
WHERE  A.ps_id IS NULL AND B.psregnum = A.psregnum;

UPDATE psmate_okz A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_okz A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_othercharacts A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_reqworkexperiences A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_specialconditions A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_tf_la A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_tf_la A
SET    tf_id = B.id
FROM   psmate_tfinfo B
WHERE  A.tf_id IS NULL AND B.nametf = A.nametf;

UPDATE psmate_tf_nk A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_tf_nk A
SET    tf_id = B.id
FROM   psmate_tfinfo B
WHERE  A.tf_id IS NULL AND B.nametf = A.nametf;

UPDATE psmate_tf_oc A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_tf_oc A
SET    tf_id = B.id
FROM   psmate_tfinfo B
WHERE  A.tf_id IS NULL AND B.nametf = A.nametf;

UPDATE psmate_tf_rs A
SET    ps_id = B.ps_id, gtf_id = B.id 
FROM   psmate_gtfinfo B
WHERE  A.ps_id IS NULL AND A.gtf_id IS NULL AND B.nameotf = A.nameotf;

UPDATE psmate_tf_rs A
SET    tf_id = B.id
FROM   psmate_tfinfo B
WHERE  A.tf_id IS NULL AND B.nametf = A.nametf;

----------------------------------------------------------------------

--Find duplicates:

select * from psmate_psinfo A
where (select count(*) from psmate_psinfo B
where B.psregnum = A.psregnum) > 1

select * from psmate_jobtitles A
where (select count(*) from psmate_jobtitles B
where B.jobtitle = A.jobtitle AND B.psregnum = A.psregnum) > 1

