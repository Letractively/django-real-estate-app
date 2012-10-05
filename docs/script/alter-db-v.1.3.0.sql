CREATE TABLE "real_estate_app_property_realtor_fk" (
    "id" serial NOT NULL PRIMARY KEY,
    "property_id" integer NOT NULL,
    "realtor_id" integer NOT NULL REFERENCES "real_estate_app_realtor" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("property_id", "realtor_id")
);

ALTER TABLE "real_estate_app_property_realtor_fk" ADD CONSTRAINT "property_id_refs_id_4e0dee74" FOREIGN KEY ("property_id") REFERENCES "real_estate_app_property" ("id") DEFERRABLE INITIALLY DEFERRED;