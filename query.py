tableCreateSql = """
            CREATE SCHEMA IF NOT EXISTS decanaria;

            DROP TABLE IF EXISTS decanaria.raw_table;

            CREATE TABLE IF NOT EXISTS decanaria.raw_table
        (
            id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
            title text COLLATE pg_catalog."default",
            description text COLLATE pg_catalog."default",
            slug text COLLATE pg_catalog."default",
            language text COLLATE pg_catalog."default",
            languages text[] COLLATE pg_catalog."default",
            req_id text COLLATE pg_catalog."default",
            street_address text COLLATE pg_catalog."default",
            city text COLLATE pg_catalog."default",
            state text COLLATE pg_catalog."default",
            country_code text COLLATE pg_catalog."default",
            postal_code text COLLATE pg_catalog."default",
            location_type text COLLATE pg_catalog."default",
            latitude numeric,
            longitude numeric,
            categories jsonb[],
            brand text COLLATE pg_catalog."default",
            department text COLLATE pg_catalog."default",
            recruiter_id text COLLATE pg_catalog."default",
            promotion_value numeric,
            salary_value numeric,
            salary_min_value numeric,
            salary_max_value numeric,
            employment_type text COLLATE pg_catalog."default",
            source text COLLATE pg_catalog."default",
            posted_date text COLLATE pg_catalog."default",
            posting_expiry_date text COLLATE pg_catalog."default",
            apply_url text COLLATE pg_catalog."default",
            is_internal boolean,
            is_searchable boolean,
            is_applyable boolean,
            is_li_easy_applyable boolean,
            ats_code text COLLATE pg_catalog."default",
            meta_data jsonb,
            create_date date,
            update_date date,
            category text[] COLLATE pg_catalog."default",
            full_location text COLLATE pg_catalog."default",
            short_location text COLLATE pg_catalog."default",
            CONSTRAINT raw_table_pkey PRIMARY KEY (id)
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS decanaria.raw_table
            OWNER to postgres;

"""

insertSql = """
                INSERT INTO
                    decanaria.raw_table (slug, language, languages, req_id, title, description, street_address, city, state,
                                         country_code, postal_code, location_type, latitude, longitude, categories,
                                         brand, department, recruiter_id, promotion_value, salary_value, salary_min_value,
                                         salary_max_value, employment_type, source, posted_date, posting_expiry_date, apply_url,
                                         is_internal, is_searchable, is_applyable, is_li_easy_applyable, ats_code,
                                         meta_data, update_date, create_date, category, full_location, short_location)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, 
                     %s, %s, %s, %s, %s, %s::jsonb[], 
                     %s, %s, %s, %s, %s, %s, 
                     %s, %s, %s, %s, %s, %s, 
                     %s, %s, %s, %s, %s, 
                     %s, %s, %s, %s, %s, %s);
            """