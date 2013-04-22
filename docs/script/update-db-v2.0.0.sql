--insert into real_estate_app_apps_propretys_position_of_sun select id, position, logical_exclude from real_estate_app_positionofsun
--insert into real_estate_app_apps_propretys_aditionalthings select id, name, logical_exclude from real_estate_app_aditionalthings;
--insert into real_estate_app_apps_propretys_proprety_aditionalthings_fk select id, property_id, aditionalthings_id from real_estate_app_property_aditionalthings_fk; 
--insert into real_estate_app_apps_propretys_classification select id, classification, logical_exclude from real_estate_app_classification; 
--insert into real_estate_app_apps_propretys_district select id,district, logical_exclude, state from real_estate_app_district;
--insert into real_estate_app_apps_propretys_status_proprety SELECT id, statusproperty, logical_exclude FROM real_estate_app_statusproperty; 
--insert into real_estate_app_apps_propretys_proprety select id, address, slug, zip_code, price, district_fk_id, condominio, iptu, classification_fk_id, statusproperty_fk_id, state,rooms, baths, garage, elevator,  furnishing, featured,  under_contruction, private_area,  position_of_sun_id,date_init, date_end, description,enable_publish,gmap_point_x,gmap_point_y, code_property,'2013-04-05' from real_estate_app_property; 
--insert into real_estate_app_apps_propretys_proprety_domain select id, property_id, site_id from real_estate_app_property_domain;
--insert into real_estate_app_apps_photos_photo select id , album_id, photo,  width, height, slug, description, pub_date, is_published, image_destaque from real_estate_app_photo;
--insert into real_estate_app_apps_newspapers_news select id,title,slug,content,link, pub_date, enable_publish from real_estate_app_news;
--INSERT INTO real_estate_app_apps_real_estate_files_files SELECT id,title, slug,pub_date,files FROM real_estate_app_files;
/*FALTA MIGRAR 
   - PORTLET: este deve ser o mais complicado devido aos tipos.
   - PORTLETPROPAGANDAIMAGE: migrar para portlet e migrar para marketing caso exista
   - Avisar que o images deixou de ser suportado por conta do real_estate_files.*/
SELECT setval('real_estate_app_apps_photos_photo_id_seq', (select max(id)+1 from real_estate_app_apps_photos_photo));
SELECT setval('real_estate_app_apps_portlets_portlet_id_seq', (select max(id)+1 from real_estate_app_apps_portlets_portlet));
SELECT setval('real_estate_app_apps_propretys_classification_id_seq', (select max(id)+1 from real_estate_app_apps_propretys_classification));
SELECT setval('real_estate_app_apps_propretys_district_id_seq',(select max(id)+1 from real_estate_app_apps_propretys_district));
SELECT setval('real_estate_app_apps_propretys_position_of_sun_id_seq',(select max(id)+1 from real_estate_app_apps_propretys_position_of_sun));
SELECT setval('real_estate_app_apps_propretys_proprety_domain_id_seq',(select max(id)+1 from real_estate_app_apps_propretys_proprety_domain));
SELECT setval('real_estate_app_apps_propretys_proprety_id_seq',(select max(id)+1 from real_estate_app_apps_propretys_proprety));
SELECT setval('real_estate_app_apps_propretys_proprety_realtor_fk_id_seq',(select max(id)+1 from real_estate_app_apps_propretys_proprety_realtor_fk));
SELECT setval('real_estate_app_apps_propretys_status_proprety_id_seq',(select max(id)+1 from real_estate_app_apps_propretys_status_proprety));
SELECT setval('real_estate_app_apps_realtors_realtor_id_seq',(select max(id)+1 from real_estate_app_apps_realtors_realtor));
SELECT setval('real_estate_files_files_id_seq',(select max(id)+1 from real_estate_files_files));
SELECT setval('real_estate_app_apps_propretys_aditionalthings_id_seq', (select max(id)+1 from real_estate_app_apps_propretys_aditionalthings));