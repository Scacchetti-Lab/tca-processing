CREATE EXTENSION vector;

CREATE TABLE "user" (
  "us_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "us_fullname" VARCHAR(255) NOT NULL,
  "us_username" VARCHAR(255) UNIQUE NOT NULL,
  "us_cpf" CHAR(11) UNIQUE NOT NULL,
  "us_mobilephone" VARCHAR(255),
  "us_birthdate" DATE NOT NULL,
  "us_email" VARCHAR(255) NOT NULL,
  "us_password" VARCHAR(255) NOT NULL,
  "us_profilephoto" VARCHAR(255),
  "us_address_id" UUID NOT NULL,
  "us_score" INTEGER DEFAULT 0,
  "us_score_type" VARCHAR(255) CHECK ("us_score_type" IN ('PERFORMANCE', 'STRATEGIC')),
  "us_ai_token_used" INTEGER DEFAULT 0,
  "us_status" VARCHAR(255) NOT NULL CHECK ("us_status" IN ('FORCE_CHANGE_PASSWORD', 'VERIFIED', 'WAITING_VERIFY', 'BANNED', 'ACTIVE', 'INACTIVE')),
  "us_is_deleted" BOOLEAN NOT NULL DEFAULT false,
  "us_modified_on" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  "us_created_by" UUID,
  "us_created_on" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  PRIMARY KEY ("us_id")
);

CREATE TABLE "address" (
  "ad_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "ad_postalcode" CHAR(8) NOT NULL,
  "ad_number" VARCHAR(20) NOT NULL,
  "ad_name" VARCHAR(255) NOT NULL,
  "ad_complement" VARCHAR(255),
  "ad_state" VARCHAR(255) NOT NULL,
  "ad_uf" CHAR(2) NOT NULL,
  "ad_neighborhood" VARCHAR(255) NOT NULL,
  PRIMARY KEY ("ad_id")
);

CREATE TABLE "profile" (
  "pf_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "pf_name" VARCHAR(255) NOT NULL,
  "pf_avg_salary" DECIMAL(8,2),
  "pf_is_admin" BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY ("pf_id")
);

CREATE TABLE "user_profile" (
  "up_user_id" UUID NOT NULL,
  "up_profile_id" UUID NOT NULL,
  PRIMARY KEY ("up_user_id", "up_profile_id")
);

CREATE TABLE "salesperson" (
  "sp_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "sp_user_id" UUID UNIQUE NOT NULL,
  "sp_total_leads" INTEGER,
  "sp_performance_pp" SMALLINT,
  "sp_engagement_pp" SMALLINT,
  "sp_communication_quality_pp" SMALLINT,
  "sp_opportunities_seized_pp" SMALLINT,
  "sp_objection_handling_pp" SMALLINT,
  "sp_total_meetings" INTEGER NOT NULL DEFAULT 0,
  "sp_need_training" BOOLEAN NOT NULL DEFAULT false,
  "sp_squad_id" UUID NOT NULL,
  PRIMARY KEY ("sp_id")
);

CREATE TABLE "squad" (
  "sq_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "sq_name" VARCHAR(255) NOT NULL,
  "fk_sq_manager_id" UUID NOT NULL,
  "sq_description" VARCHAR(255) NOT NULL,
  "sq_performance_avg" SMALLINT NOT NULL DEFAULT 0,
  PRIMARY KEY ("sq_id")
);

CREATE TABLE "manager" (
  "mg_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "mg_user_id" UUID UNIQUE NOT NULL,
  "mg_total_meetings" INTEGER NOT NULL DEFAULT 0,
  "mg_performance_pp" SMALLINT,
  "mg_total_squads" SMALLINT NOT NULL DEFAULT 0,
  "mg_unit" VARCHAR(255),
  "mg_score_goal" SMALLINT,
  "mg_created_by" UUID NOT NULL,
  "mg_created_on" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  "mg_modified_on" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  PRIMARY KEY ("mg_id")
);

CREATE TABLE "meeting" (
  "mt_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "mt_totvs_id" INTEGER UNIQUE NOT NULL,
  "mt_transcript_id" UUID UNIQUE NOT NULL,
  "mt_title" VARCHAR(255) NOT NULL,
  "mt_summary" TEXT NOT NULL,
  "mt_scheduled" TIMESTAMPTZ NOT NULL,
  "mt_duration_min" INTEGER,
  "mt_type" VARCHAR(50) NOT NULL CHECK ("mt_type" IN ('SALESPERSON', 'DIRECTOR')),
  "mt_status" VARCHAR(50) NOT NULL CHECK ("mt_status" IN ('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
  "mt_performance_avg" SMALLINT,
  "mt_feedback" TEXT NOT NULL,
  "mt_priority" VARCHAR(50) CHECK ("mt_priority" IN ('HIGH', 'MEDIUM', 'LOW')),
  "mt_client_id" UUID NOT NULL,
  "mt_is_deleted" BOOLEAN NOT NULL DEFAULT false,
  "mt_embeddings" VECTOR(384),
  PRIMARY KEY ("mt_id")
);

CREATE TABLE "meeting_employee" (
  "me_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "me_meeting_id" UUID NOT NULL,
  "me_user_profile_id" UUID NOT NULL,
  "me_feedback_tip" TEXT NOT NULL,
  PRIMARY KEY ("me_id")
);

CREATE TABLE "client" (
  "cl_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "cl_name" VARCHAR(255) NOT NULL,
  "cl_fantasy_name" VARCHAR(255) NOT NULL,
  "cl_cnpj" CHAR(14) UNIQUE NOT NULL,
  "cl_address_id" UUID NOT NULL,
  "cl_revenue" DECIMAL(15,2) NOT NULL DEFAULT 0,
  "cl_status" VARCHAR(255) NOT NULL CHECK ("cl_status" IN ('CRITIC', 'BAD', 'OK', 'GOOD')),
  "cl_embeddings" VECTOR(384),
  PRIMARY KEY ("cl_id")
);

CREATE TABLE "client_analyse" (
  "ca_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "ca_client_id" UUID UNIQUE NOT NULL,
  "ca_performance" SMALLINT NOT NULL,
  "ca_closing_probability" SMALLINT NOT NULL,
  "ca_problem_understanding" SMALLINT NOT NULL,
  "ca_risk" SMALLINT NOT NULL,
  "ca_finacial_impact" DECIMAL(8,2) NOT NULL,
  "ca_finacial_status" VARCHAR(255) NOT NULL CHECK ("ca_finacial_status" IN ('MINIMAL', 'LOW', 'MEDIUM', 'HIGH', 'SEVERAL')),
  PRIMARY KEY ("ca_id")
);

CREATE TABLE "transcript" (
  "tr_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "tr_raw_transcript" TEXT NOT NULL,
  "tr_resume" TEXT NOT NULL,
  "tr_status" VARCHAR(255) NOT NULL CHECK ("tr_status" IN ('NOT_STARTED', 'IN_PROGRESS', 'DONE', 'ERROR', 'CANCELLED')),
  PRIMARY KEY ("tr_id")
);

CREATE TABLE "session" (
  "ss_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "ss_title" VARCHAR(255) NOT NULL,
  "ss_last_activity" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  "ss_created_on" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  "ss_user_id" UUID NOT NULL,
  "ss_model_used" VARCHAR(255) NOT NULL CHECK ("ss_model_used" IN ('FAST', 'PRO')),
  "ss_last_interaction_id" VARCHAR(255),
  PRIMARY KEY ("ss_id")
);

CREATE TABLE "message" (
  "ms_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "ms_session_id" UUID NOT NULL,
  "ms_role" VARCHAR(255) NOT NULL CHECK ("ms_role" IN ('SALESPERSON', 'MANAGER', 'TOTVS_AI')),
  "ms_content" TEXT NOT NULL,
  "ms_created_on" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  PRIMARY KEY ("ms_id")
);

CREATE TABLE "configuration" (
  "cf_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "cf_key" VARCHAR(255) UNIQUE NOT NULL,
  "cf_type" VARCHAR(255) NOT NULL CHECK ("cf_type" IN ('STRING', 'INTEGER', 'DOUBLE', 'BOOLEAN')),
  "cf_content" TEXT NOT NULL,
  PRIMARY KEY ("cf_id")
);

CREATE TABLE "transcript_chunks" (
  "tc_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "tc_transcript_id" UUID NOT NULL,
  "tc_chunk_text" TEXT NOT NULL,
  "tc_embedding" VECTOR(384) NOT NULL,
  "tc_created_at" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  PRIMARY KEY ("tc_id")
);

CREATE TABLE "audit" (
  "au_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "au_entity_name" VARCHAR(255) NOT NULL,
  "au_user_id" UUID,
  "au_created_at" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  "au_previous" JSONB NOT NULL,
  "au_new" JSONB NOT NULL,
  PRIMARY KEY ("au_id")
);

CREATE TABLE "meeting_strategic_analyse" (
  "sa_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "sa_meeting_id" UUID UNIQUE NOT NULL,
  "sa_client_id" UUID NOT NULL,
  "sa_employees_performance" NUMERIC(4,2) NOT NULL,
  "sa_company_status" VARCHAR(50) NOT NULL,
  "sa_company_performance" NUMERIC(4,2) NOT NULL,
  "sa_closing_probability" NUMERIC(4,2) NOT NULL,
  "sa_problem_understanding" NUMERIC(4,2) NOT NULL,
  "sa_risk" NUMERIC(4,2) NOT NULL,
  "sa_financial_impact" NUMERIC(4,2) NOT NULL,
  "sa_financial_impact_status" VARCHAR(50) NOT NULL,
  "sa_created_at" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  PRIMARY KEY ("sa_id")
);

CREATE TABLE "meeting_performance_analyse" (
  "pa_id" UUID NOT NULL DEFAULT (gen_random_uuid()),
  "pa_meeting_id" UUID UNIQUE NOT NULL,
  "pa_engagement" NUMERIC(4,2) NOT NULL,
  "pa_opportunities_seized" NUMERIC(4,2) NOT NULL,
  "pa_communication_quality" NUMERIC(4,2) NOT NULL,
  "pa_objection_handling" NUMERIC(4,2) NOT NULL,
  "pa_converted_potencials" NUMERIC(4,2) NOT NULL,
  "pa_leads_converted" INTEGER NOT NULL,
  "pa_tips" TEXT NOT NULL,
  "pa_created_at" TIMESTAMPTZ NOT NULL DEFAULT (now()),
  PRIMARY KEY ("pa_id")
);

CREATE UNIQUE INDEX "user_unique_0" ON "user" ("us_cpf", "us_username");

CREATE INDEX "user_us_cpf_index" ON "user" ("us_cpf");

CREATE UNIQUE INDEX "address_unique_0" ON "address" ("ad_postalcode", "ad_number", "ad_complement");

CREATE UNIQUE INDEX "user_profile_unique_0" ON "user_profile" ("up_user_id", "up_profile_id");

CREATE INDEX "squad_fk_sq_manager_id_index" ON "squad" ("fk_sq_manager_id");

CREATE UNIQUE INDEX "meeting_employee_unique_participant" ON "meeting_employee" ("me_meeting_id", "me_user_profile_id");

CREATE INDEX "meeting_employee_me_meeting_id_index" ON "meeting_employee" ("me_meeting_id");

CREATE INDEX "message_ms_session_id_index" ON "message" ("ms_session_id");

CREATE INDEX "message_ms_created_on_index" ON "message" ("ms_created_on");

CREATE INDEX ON "transcript_chunks" USING HNSW ("tc_embedding" vector_cosine_ops);

COMMENT ON COLUMN "user"."us_modified_on" IS 'ATUALIZA QUANDO QUALQUER OPERACAO CRUD OCORRER (EXCETO READ)';

COMMENT ON COLUMN "user"."us_created_on" IS 'DATA DE HOJE EM CASO DE NULO';

COMMENT ON COLUMN "salesperson"."sp_performance_pp" IS 'Porcentagem do desempenho do vendedor';

COMMENT ON COLUMN "salesperson"."sp_engagement_pp" IS 'Porcentagem do engajamento do vendedor';

COMMENT ON COLUMN "salesperson"."sp_communication_quality_pp" IS 'Porcentagem da qualidade de comunicação do vendedor';

COMMENT ON COLUMN "salesperson"."sp_opportunities_seized_pp" IS 'Porcentagem de aproveitamento de oportunidades do vendedor';

COMMENT ON COLUMN "salesperson"."sp_objection_handling_pp" IS 'Porcentagem de tratamento de objeções do vendedor';

COMMENT ON COLUMN "salesperson"."sp_total_meetings" IS 'total de reuniões participadas no último mês';

COMMENT ON COLUMN "manager"."mg_total_meetings" IS 'total de reuniões do gerente e da sua equipe';

COMMENT ON COLUMN "manager"."mg_performance_pp" IS 'porcentagem de desempenho agregado da equipe';

COMMENT ON COLUMN "manager"."mg_total_squads" IS 'total de squads geridas por esse gerente';

COMMENT ON COLUMN "manager"."mg_unit" IS 'unidade/filial do gerente';

COMMENT ON COLUMN "manager"."mg_score_goal" IS 'meta de score definida para a equipe';

COMMENT ON COLUMN "manager"."mg_created_by" IS 'usuário (admin) que criou este registro de gerente';

COMMENT ON COLUMN "meeting"."mt_scheduled" IS 'Data e hora em que a reunião foi agendada';

COMMENT ON COLUMN "meeting"."mt_duration_min" IS 'Duração da reunião em minutos';

COMMENT ON COLUMN "meeting"."mt_type" IS 'Define qual tabela de analytic aplica: SALESPERSON -> meeting_performance_analyse, DIRECTOR -> meeting_strategic_analyse';

COMMENT ON COLUMN "client"."cl_revenue" IS 'faturamento mensal';

COMMENT ON COLUMN "transcript_chunks"."tc_transcript_id" IS 'Identificador da transcrição';

COMMENT ON COLUMN "transcript_chunks"."tc_embedding" IS 'Vetor de embedding gerado pelo modelo local (384 dimensões)';

COMMENT ON COLUMN "audit"."au_entity_name" IS 'Nome da entidade do banco de dados';

COMMENT ON COLUMN "audit"."au_user_id" IS 'Usuário que realizou a alteração';

COMMENT ON COLUMN "audit"."au_created_at" IS 'Data de criação';

COMMENT ON COLUMN "audit"."au_previous" IS 'último valor antes da modificação';

COMMENT ON COLUMN "audit"."au_new" IS 'novo valor após a modificação';

COMMENT ON COLUMN "meeting_strategic_analyse"."sa_client_id" IS 'Desnormalizado de meeting.mt_client_id para evitar join -- mantido em sincronia pela aplicação';

ALTER TABLE "meeting_employee" ADD FOREIGN KEY ("me_user_profile_id") REFERENCES "user_profile" ("up_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "meeting_employee" ADD FOREIGN KEY ("me_meeting_id") REFERENCES "meeting" ("mt_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "session" ADD FOREIGN KEY ("ss_user_id") REFERENCES "user" ("us_uid") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "salesperson" ADD FOREIGN KEY ("sp_user_id") REFERENCES "user" ("us_uid") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "client" ADD FOREIGN KEY ("cl_address_id") REFERENCES "address" ("ad_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "meeting" ADD FOREIGN KEY ("mt_client_id") REFERENCES "client" ("cl_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "squad" ADD FOREIGN KEY ("fk_sq_manager_id") REFERENCES "manager" ("mg_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "user_profile" ADD FOREIGN KEY ("up_user_id") REFERENCES "user" ("us_uid") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "meeting" ADD FOREIGN KEY ("mt_transcript_id") REFERENCES "transcript" ("tr_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "user" ADD FOREIGN KEY ("us_address_id") REFERENCES "address" ("ad_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "client_analyse" ADD FOREIGN KEY ("ca_client_id") REFERENCES "client" ("cl_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "manager" ADD FOREIGN KEY ("mg_user_id") REFERENCES "user" ("us_uid") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "manager" ADD FOREIGN KEY ("mg_created_by") REFERENCES "user" ("us_uid") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "user" ADD FOREIGN KEY ("us_created_by") REFERENCES "user" ("us_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "message" ADD FOREIGN KEY ("ms_session_id") REFERENCES "session" ("ss_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "salesperson" ADD FOREIGN KEY ("sp_squad_id") REFERENCES "squad" ("sq_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "user_profile" ADD FOREIGN KEY ("up_profile_id") REFERENCES "profile" ("pf_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "transcript_chunks" ADD FOREIGN KEY ("tc_transcript_id") REFERENCES "transcript" ("tr_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "meeting_performance_analyse" ADD FOREIGN KEY ("pa_meeting_id") REFERENCES "meeting" ("mt_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "meeting_strategic_analyse" ADD FOREIGN KEY ("sa_meeting_id") REFERENCES "meeting" ("mt_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "meeting_strategic_analyse" ADD FOREIGN KEY ("sa_client_id") REFERENCES "client" ("cl_id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "audit" ADD FOREIGN KEY ("au_user_id") REFERENCES "user" ("us_uid") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY IMMEDIATE;

CREATE ROLE ai_role;

GRANT USAGE ON SCHEMA public TO ai_role;

GRANT SELECT ON
  "user",
  client,
  client_analyse,
  meeting,
  manager,
  meeting_employee,
  meeting_performance_analyse,
  meeting_strategic_analyse,
  salesperson,
  transcript,
  session,
  message
TO ai_role;

GRANT SELECT, INSERT, DELETE ON transcript_chunks TO ai_role;

GRANT UPDATE (mt_embeddings) ON meeting TO ai_role;
GRANT UPDATE (cl_embeddings) ON client TO ai_role;

CREATE ROLE totvsai LOGIN PASSWORD 'totvsai' IN ROLE ai_role;
