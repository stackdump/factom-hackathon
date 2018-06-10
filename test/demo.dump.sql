--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4 (Debian 10.4-2.pgdg90+1)
-- Dumped by pg_dump version 10.4 (Ubuntu 10.4-0ubuntu0.18.04)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: counter; Type: SCHEMA; Schema: -; Owner: bitwrap
--

CREATE SCHEMA counter;


ALTER SCHEMA counter OWNER TO bitwrap;

--
-- Name: petchain; Type: SCHEMA; Schema: -; Owner: bitwrap
--

CREATE SCHEMA petchain;


ALTER SCHEMA petchain OWNER TO bitwrap;

--
-- Name: vetchain; Type: SCHEMA; Schema: -; Owner: bitwrap
--

CREATE SCHEMA vetchain;


ALTER SCHEMA vetchain OWNER TO bitwrap;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: token; Type: DOMAIN; Schema: counter; Owner: bitwrap
--

CREATE DOMAIN counter.token AS smallint
	CONSTRAINT token_check CHECK (((VALUE >= 0) AND (VALUE <= 65536)));


ALTER DOMAIN counter.token OWNER TO bitwrap;

--
-- Name: state; Type: TYPE; Schema: counter; Owner: bitwrap
--

CREATE TYPE counter.state AS (
	p0 counter.token,
	p1 counter.token
);


ALTER TYPE counter.state OWNER TO bitwrap;

--
-- Name: current_state; Type: TYPE; Schema: counter; Owner: bitwrap
--

CREATE TYPE counter.current_state AS (
	id character varying(32),
	oid character varying(255),
	action character varying(255),
	rev integer,
	state counter.state,
	payload json,
	modified timestamp without time zone,
	created timestamp without time zone
);


ALTER TYPE counter.current_state OWNER TO bitwrap;

--
-- Name: event; Type: TYPE; Schema: counter; Owner: bitwrap
--

CREATE TYPE counter.event AS (
	id character varying(32),
	oid character varying(255),
	rev integer
);


ALTER TYPE counter.event OWNER TO bitwrap;

--
-- Name: event_payload; Type: TYPE; Schema: counter; Owner: bitwrap
--

CREATE TYPE counter.event_payload AS (
	id character varying(32),
	oid character varying(255),
	seq integer,
	action character varying(255),
	payload json,
	"timestamp" timestamp without time zone
);


ALTER TYPE counter.event_payload OWNER TO bitwrap;

--
-- Name: vector; Type: TYPE; Schema: counter; Owner: bitwrap
--

CREATE TYPE counter.vector AS (
	p0 integer,
	p1 integer
);


ALTER TYPE counter.vector OWNER TO bitwrap;

--
-- Name: token; Type: DOMAIN; Schema: petchain; Owner: bitwrap
--

CREATE DOMAIN petchain.token AS smallint
	CONSTRAINT token_check CHECK (((VALUE >= 0) AND (VALUE <= 65536)));


ALTER DOMAIN petchain.token OWNER TO bitwrap;

--
-- Name: state; Type: TYPE; Schema: petchain; Owner: bitwrap
--

CREATE TYPE petchain.state AS (
	exam petchain.token,
	wait_30_day petchain.token,
	wait_120_day petchain.token,
	rfid_updates petchain.token,
	ready_to_travel petchain.token,
	wait_21_day petchain.token,
	chain_created petchain.token,
	titer_lab_result petchain.token
);


ALTER TYPE petchain.state OWNER TO bitwrap;

--
-- Name: current_state; Type: TYPE; Schema: petchain; Owner: bitwrap
--

CREATE TYPE petchain.current_state AS (
	id character varying(32),
	oid character varying(255),
	action character varying(255),
	rev integer,
	state petchain.state,
	payload json,
	modified timestamp without time zone,
	created timestamp without time zone
);


ALTER TYPE petchain.current_state OWNER TO bitwrap;

--
-- Name: event; Type: TYPE; Schema: petchain; Owner: bitwrap
--

CREATE TYPE petchain.event AS (
	id character varying(32),
	oid character varying(255),
	rev integer
);


ALTER TYPE petchain.event OWNER TO bitwrap;

--
-- Name: event_payload; Type: TYPE; Schema: petchain; Owner: bitwrap
--

CREATE TYPE petchain.event_payload AS (
	id character varying(32),
	oid character varying(255),
	seq integer,
	action character varying(255),
	payload json,
	"timestamp" timestamp without time zone
);


ALTER TYPE petchain.event_payload OWNER TO bitwrap;

--
-- Name: vector; Type: TYPE; Schema: petchain; Owner: bitwrap
--

CREATE TYPE petchain.vector AS (
	exam integer,
	wait_30_day integer,
	wait_120_day integer,
	rfid_updates integer,
	ready_to_travel integer,
	wait_21_day integer,
	chain_created integer,
	titer_lab_result integer
);


ALTER TYPE petchain.vector OWNER TO bitwrap;

--
-- Name: token; Type: DOMAIN; Schema: vetchain; Owner: bitwrap
--

CREATE DOMAIN vetchain.token AS smallint
	CONSTRAINT token_check CHECK (((VALUE >= 0) AND (VALUE <= 65536)));


ALTER DOMAIN vetchain.token OWNER TO bitwrap;

--
-- Name: state; Type: TYPE; Schema: vetchain; Owner: bitwrap
--

CREATE TYPE vetchain.state AS (
	vax_count vetchain.token,
	trave_certs_lifetime vetchain.token,
	rfid_updates_lifetime vetchain.token,
	trave_process_inflight vetchain.token,
	booster_count vetchain.token,
	chain_created vetchain.token,
	lab_submission_count vetchain.token,
	titer_count vetchain.token
);


ALTER TYPE vetchain.state OWNER TO bitwrap;

--
-- Name: current_state; Type: TYPE; Schema: vetchain; Owner: bitwrap
--

CREATE TYPE vetchain.current_state AS (
	id character varying(32),
	oid character varying(255),
	action character varying(255),
	rev integer,
	state vetchain.state,
	payload json,
	modified timestamp without time zone,
	created timestamp without time zone
);


ALTER TYPE vetchain.current_state OWNER TO bitwrap;

--
-- Name: event; Type: TYPE; Schema: vetchain; Owner: bitwrap
--

CREATE TYPE vetchain.event AS (
	id character varying(32),
	oid character varying(255),
	rev integer
);


ALTER TYPE vetchain.event OWNER TO bitwrap;

--
-- Name: event_payload; Type: TYPE; Schema: vetchain; Owner: bitwrap
--

CREATE TYPE vetchain.event_payload AS (
	id character varying(32),
	oid character varying(255),
	seq integer,
	action character varying(255),
	payload json,
	"timestamp" timestamp without time zone
);


ALTER TYPE vetchain.event_payload OWNER TO bitwrap;

--
-- Name: vector; Type: TYPE; Schema: vetchain; Owner: bitwrap
--

CREATE TYPE vetchain.vector AS (
	vax_count integer,
	trave_certs_lifetime integer,
	rfid_updates_lifetime integer,
	trave_process_inflight integer,
	booster_count integer,
	chain_created integer,
	lab_submission_count integer,
	titer_count integer
);


ALTER TYPE vetchain.vector OWNER TO bitwrap;

--
-- Name: vclock(); Type: FUNCTION; Schema: counter; Owner: bitwrap
--

CREATE FUNCTION counter.vclock() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        DECLARE
            txn counter.vector;
            revision int4;
        BEGIN
            SELECT
                (vector).* INTO STRICT txn
            FROM
                counter.transitions
            WHERE
                action = NEW.action;

            UPDATE
              counter.states set 
                state = (  (state).P0 + txn.P0, (state).P1 + txn.P1 ),
                rev = rev + 1,
                modified = now()
            WHERE
              oid = NEW.oid
            RETURNING
              rev into STRICT revision;

            NEW.seq = revision;
            NEW.hash = md5(row_to_json(NEW)::TEXT);
            NEW.timestamp = now();

            RETURN NEW;
        END
    $$;


ALTER FUNCTION counter.vclock() OWNER TO bitwrap;

--
-- Name: vclock(); Type: FUNCTION; Schema: petchain; Owner: bitwrap
--

CREATE FUNCTION petchain.vclock() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        DECLARE
            txn petchain.vector;
            revision int4;
        BEGIN
            SELECT
                (vector).* INTO STRICT txn
            FROM
                petchain.transitions
            WHERE
                action = NEW.action;

            UPDATE
              petchain.states set 
                state = (  (state).exam + txn.exam, (state).wait_30_day + txn.wait_30_day, (state).wait_120_day + txn.wait_120_day, (state).rfid_updates + txn.rfid_updates, (state).ready_to_travel + txn.ready_to_travel, (state).wait_21_day + txn.wait_21_day, (state).chain_created + txn.chain_created, (state).titer_lab_result + txn.titer_lab_result ),
                rev = rev + 1,
                modified = now()
            WHERE
              oid = NEW.oid
            RETURNING
              rev into STRICT revision;

            NEW.seq = revision;
            NEW.hash = md5(row_to_json(NEW)::TEXT);
            NEW.timestamp = now();

            RETURN NEW;
        END
    $$;


ALTER FUNCTION petchain.vclock() OWNER TO bitwrap;

--
-- Name: vclock(); Type: FUNCTION; Schema: vetchain; Owner: bitwrap
--

CREATE FUNCTION vetchain.vclock() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        DECLARE
            txn vetchain.vector;
            revision int4;
        BEGIN
            SELECT
                (vector).* INTO STRICT txn
            FROM
                vetchain.transitions
            WHERE
                action = NEW.action;

            UPDATE
              vetchain.states set 
                state = (  (state).vax_count + txn.vax_count, (state).trave_certs_lifetime + txn.trave_certs_lifetime, (state).rfid_updates_lifetime + txn.rfid_updates_lifetime, (state).trave_process_inflight + txn.trave_process_inflight, (state).booster_count + txn.booster_count, (state).chain_created + txn.chain_created, (state).lab_submission_count + txn.lab_submission_count, (state).titer_count + txn.titer_count ),
                rev = rev + 1,
                modified = now()
            WHERE
              oid = NEW.oid
            RETURNING
              rev into STRICT revision;

            NEW.seq = revision;
            NEW.hash = md5(row_to_json(NEW)::TEXT);
            NEW.timestamp = now();

            RETURN NEW;
        END
    $$;


ALTER FUNCTION vetchain.vclock() OWNER TO bitwrap;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: events; Type: TABLE; Schema: counter; Owner: bitwrap
--

CREATE TABLE counter.events (
    oid character varying(255) NOT NULL,
    seq integer NOT NULL,
    action character varying(255) NOT NULL,
    payload jsonb DEFAULT '{}'::jsonb,
    hash character varying(32) NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE counter.events OWNER TO bitwrap;

--
-- Name: events_seq_seq; Type: SEQUENCE; Schema: counter; Owner: bitwrap
--

CREATE SEQUENCE counter.events_seq_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE counter.events_seq_seq OWNER TO bitwrap;

--
-- Name: events_seq_seq; Type: SEQUENCE OWNED BY; Schema: counter; Owner: bitwrap
--

ALTER SEQUENCE counter.events_seq_seq OWNED BY counter.events.seq;


--
-- Name: states; Type: TABLE; Schema: counter; Owner: bitwrap
--

CREATE TABLE counter.states (
    oid character varying(256) NOT NULL,
    rev integer DEFAULT 0,
    state counter.state DEFAULT ROW((2)::counter.token, (0)::counter.token)::counter.state,
    created timestamp without time zone DEFAULT now(),
    modified timestamp without time zone DEFAULT now()
);


ALTER TABLE counter.states OWNER TO bitwrap;

--
-- Name: transitions; Type: TABLE; Schema: counter; Owner: bitwrap
--

CREATE TABLE counter.transitions (
    action character varying(255) NOT NULL,
    vector counter.vector
);


ALTER TABLE counter.transitions OWNER TO bitwrap;

--
-- Name: events; Type: TABLE; Schema: petchain; Owner: bitwrap
--

CREATE TABLE petchain.events (
    oid character varying(255) NOT NULL,
    seq integer NOT NULL,
    action character varying(255) NOT NULL,
    payload jsonb DEFAULT '{}'::jsonb,
    hash character varying(32) NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE petchain.events OWNER TO bitwrap;

--
-- Name: events_seq_seq; Type: SEQUENCE; Schema: petchain; Owner: bitwrap
--

CREATE SEQUENCE petchain.events_seq_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE petchain.events_seq_seq OWNER TO bitwrap;

--
-- Name: events_seq_seq; Type: SEQUENCE OWNED BY; Schema: petchain; Owner: bitwrap
--

ALTER SEQUENCE petchain.events_seq_seq OWNED BY petchain.events.seq;


--
-- Name: states; Type: TABLE; Schema: petchain; Owner: bitwrap
--

CREATE TABLE petchain.states (
    oid character varying(256) NOT NULL,
    rev integer DEFAULT 0,
    state petchain.state DEFAULT ROW((0)::petchain.token, (0)::petchain.token, (0)::petchain.token, (0)::petchain.token, (0)::petchain.token, (0)::petchain.token, (0)::petchain.token, (0)::petchain.token)::petchain.state,
    created timestamp without time zone DEFAULT now(),
    modified timestamp without time zone DEFAULT now()
);


ALTER TABLE petchain.states OWNER TO bitwrap;

--
-- Name: transitions; Type: TABLE; Schema: petchain; Owner: bitwrap
--

CREATE TABLE petchain.transitions (
    action character varying(255) NOT NULL,
    vector petchain.vector
);


ALTER TABLE petchain.transitions OWNER TO bitwrap;

--
-- Name: events; Type: TABLE; Schema: vetchain; Owner: bitwrap
--

CREATE TABLE vetchain.events (
    oid character varying(255) NOT NULL,
    seq integer NOT NULL,
    action character varying(255) NOT NULL,
    payload jsonb DEFAULT '{}'::jsonb,
    hash character varying(32) NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE vetchain.events OWNER TO bitwrap;

--
-- Name: events_seq_seq; Type: SEQUENCE; Schema: vetchain; Owner: bitwrap
--

CREATE SEQUENCE vetchain.events_seq_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE vetchain.events_seq_seq OWNER TO bitwrap;

--
-- Name: events_seq_seq; Type: SEQUENCE OWNED BY; Schema: vetchain; Owner: bitwrap
--

ALTER SEQUENCE vetchain.events_seq_seq OWNED BY vetchain.events.seq;


--
-- Name: states; Type: TABLE; Schema: vetchain; Owner: bitwrap
--

CREATE TABLE vetchain.states (
    oid character varying(256) NOT NULL,
    rev integer DEFAULT 0,
    state vetchain.state DEFAULT ROW((0)::vetchain.token, (0)::vetchain.token, (0)::vetchain.token, (0)::vetchain.token, (0)::vetchain.token, (0)::vetchain.token, (0)::vetchain.token, (0)::vetchain.token)::vetchain.state,
    created timestamp without time zone DEFAULT now(),
    modified timestamp without time zone DEFAULT now()
);


ALTER TABLE vetchain.states OWNER TO bitwrap;

--
-- Name: transitions; Type: TABLE; Schema: vetchain; Owner: bitwrap
--

CREATE TABLE vetchain.transitions (
    action character varying(255) NOT NULL,
    vector vetchain.vector
);


ALTER TABLE vetchain.transitions OWNER TO bitwrap;

--
-- Name: events seq; Type: DEFAULT; Schema: counter; Owner: bitwrap
--

ALTER TABLE ONLY counter.events ALTER COLUMN seq SET DEFAULT nextval('counter.events_seq_seq'::regclass);


--
-- Name: events seq; Type: DEFAULT; Schema: petchain; Owner: bitwrap
--

ALTER TABLE ONLY petchain.events ALTER COLUMN seq SET DEFAULT nextval('petchain.events_seq_seq'::regclass);


--
-- Name: events seq; Type: DEFAULT; Schema: vetchain; Owner: bitwrap
--

ALTER TABLE ONLY vetchain.events ALTER COLUMN seq SET DEFAULT nextval('vetchain.events_seq_seq'::regclass);


--
-- Data for Name: events; Type: TABLE DATA; Schema: counter; Owner: bitwrap
--

COPY counter.events (oid, seq, action, payload, hash, "timestamp") FROM stdin;
1528596702421	1	INC_0	{}	14ed17d48ff00b7833dd196614a4b84c	2018-06-10 02:11:43.373061
1528596702421	2	INC_0	{}	fc3657047b674908ccb46ef012a4b561	2018-06-10 02:11:45.181653
\.


--
-- Data for Name: states; Type: TABLE DATA; Schema: counter; Owner: bitwrap
--

COPY counter.states (oid, rev, state, created, modified) FROM stdin;
1528595037206	0	(2,0)	2018-06-10 01:43:57.228825	2018-06-10 01:43:57.228825
1528596702421	2	(4,0)	2018-06-10 02:11:42.454313	2018-06-10 02:11:45.181653
\.


--
-- Data for Name: transitions; Type: TABLE DATA; Schema: counter; Owner: bitwrap
--

COPY counter.transitions (action, vector) FROM stdin;
INC_0	(1,0)
INC_1	(0,1)
DEC_1	(0,-1)
DEC_0	(-1,0)
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: petchain; Owner: bitwrap
--

COPY petchain.events (oid, seq, action, payload, hash, "timestamp") FROM stdin;
my_pet_uuid	1	create_chain	{"chain_id": "850c0ca65b9f980e551a0b2e84860d86159d5c47c56a84e0016bdc9762657175", "entry_hash": "22eef4bd6f1ca69d95643be07678ec8412990800cd3228a91da7a5a15f850e70"}	033d28beef224b933814234f4889b7a9	2018-06-10 02:45:49.087013
my_pet_uuid	2	update_rfid	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	18c05de241a6eadef0426650a3076a26	2018-06-10 02:45:49.657718
my_pet_uuid	3	new_travel_process	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	89b701d600b96ae6a2ce2fa8c1dd53cc	2018-06-10 02:45:50.767169
my_pet_uuid	4	vaccine	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	966601cecdb9ada11f968749a672ce02	2018-06-10 02:45:51.883146
my_pet_uuid	5	booster	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	d962b2e7951f2cc9d6c4800404fd6c02	2018-06-10 02:45:53.003383
my_pet_uuid	6	titer_test	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	0381a21c9ffa1c5536d537b8d49970f1	2018-06-10 02:45:54.115458
my_pet_uuid	7	submit_lab_work	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	ebd31331d8cf96494262381a2fe500a4	2018-06-10 02:45:55.229368
my_pet_uuid	8	verified_complete	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	d5941f5b70e5818620c51d4f96ee58c8	2018-06-10 02:45:56.352524
\.


--
-- Data for Name: states; Type: TABLE DATA; Schema: petchain; Owner: bitwrap
--

COPY petchain.states (oid, rev, state, created, modified) FROM stdin;
my_pet_uuid	8	(0,0,0,1,1,0,1,0)	2018-06-10 02:45:48.536414	2018-06-10 02:45:56.352524
\.


--
-- Data for Name: transitions; Type: TABLE DATA; Schema: petchain; Owner: bitwrap
--

COPY petchain.transitions (action, vector) FROM stdin;
vaccine	(-1,1,0,0,0,0,0,0)
update_rfid	(0,0,0,1,0,0,0,0)
submit_lab_work	(0,0,1,0,0,0,0,-1)
titer_test	(0,0,0,0,0,-1,0,1)
new_travel_process	(1,0,0,0,0,0,0,0)
verified_complete	(0,0,-1,0,1,0,0,0)
booster	(0,-1,0,0,0,1,0,0)
create_chain	(0,0,0,0,0,0,1,0)
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: vetchain; Owner: bitwrap
--

COPY vetchain.events (oid, seq, action, payload, hash, "timestamp") FROM stdin;
dr_chery_york_dvm	1	create_chain	{"chain_id": "7c227bd5d3b80ae298ab707e87693db5d613332fe9d9abc6691106fb7566edfa", "entry_hash": "d4227f5032f5dfa9e91a682d14d0247319af5fad356c937fa94562754711efba"}	9580b01645091d95e47cf659f30c9e51	2018-06-10 02:45:48.511674
dr_chery_york_dvm	2	update_rfid	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	b30645ed024df52dba146cb527dd1f1c	2018-06-10 02:45:49.111657
dr_chery_york_dvm	3	new_travel_process	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	e9c5ae608ca0227e4f3f4751736c07bf	2018-06-10 02:45:50.225802
dr_chery_york_dvm	4	vaccine	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	ce7ff8a59cdf4f45fdcced106ee9fd32	2018-06-10 02:45:51.33392
dr_chery_york_dvm	5	booster	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	f88f7bd3278e4bf6aeb9b60453ed49b3	2018-06-10 02:45:52.448608
dr_chery_york_dvm	6	titer_test	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	4857e0376762aba25b0910237f0d4ddf	2018-06-10 02:45:53.564009
dr_chery_york_dvm	7	submit_lab_work	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	3e1ad33520b0faf0ca2ab2e51f9f6054	2018-06-10 02:45:54.679034
dr_chery_york_dvm	8	verified_complete	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	313ae920d9e98dcebe06636e3326a0f9	2018-06-10 02:45:55.795116
\.


--
-- Data for Name: states; Type: TABLE DATA; Schema: vetchain; Owner: bitwrap
--

COPY vetchain.states (oid, rev, state, created, modified) FROM stdin;
dr_chery_york_dvm	8	(1,1,1,0,1,1,1,1)	2018-06-10 02:45:47.962361	2018-06-10 02:45:55.795116
\.


--
-- Data for Name: transitions; Type: TABLE DATA; Schema: vetchain; Owner: bitwrap
--

COPY vetchain.transitions (action, vector) FROM stdin;
vaccine	(1,0,0,0,0,0,0,0)
update_rfid	(0,0,1,0,0,0,0,0)
submit_lab_work	(0,0,0,0,0,0,1,0)
titer_test	(0,0,0,0,0,0,0,1)
new_travel_process	(0,0,0,1,0,0,0,0)
verified_complete	(0,1,0,-1,0,0,0,0)
booster	(0,0,0,0,1,0,0,0)
create_chain	(0,0,0,0,0,1,0,0)
\.


--
-- Name: events_seq_seq; Type: SEQUENCE SET; Schema: counter; Owner: bitwrap
--

SELECT pg_catalog.setval('counter.events_seq_seq', 2, true);


--
-- Name: events_seq_seq; Type: SEQUENCE SET; Schema: petchain; Owner: bitwrap
--

SELECT pg_catalog.setval('petchain.events_seq_seq', 8, true);


--
-- Name: events_seq_seq; Type: SEQUENCE SET; Schema: vetchain; Owner: bitwrap
--

SELECT pg_catalog.setval('vetchain.events_seq_seq', 8, true);


--
-- Name: events oid_seq_pkey; Type: CONSTRAINT; Schema: counter; Owner: bitwrap
--

ALTER TABLE ONLY counter.events
    ADD CONSTRAINT oid_seq_pkey PRIMARY KEY (oid, seq);


--
-- Name: states states_pkey; Type: CONSTRAINT; Schema: counter; Owner: bitwrap
--

ALTER TABLE ONLY counter.states
    ADD CONSTRAINT states_pkey PRIMARY KEY (oid);


--
-- Name: transitions transitions_pkey; Type: CONSTRAINT; Schema: counter; Owner: bitwrap
--

ALTER TABLE ONLY counter.transitions
    ADD CONSTRAINT transitions_pkey PRIMARY KEY (action);


--
-- Name: events oid_seq_pkey; Type: CONSTRAINT; Schema: petchain; Owner: bitwrap
--

ALTER TABLE ONLY petchain.events
    ADD CONSTRAINT oid_seq_pkey PRIMARY KEY (oid, seq);


--
-- Name: states states_pkey; Type: CONSTRAINT; Schema: petchain; Owner: bitwrap
--

ALTER TABLE ONLY petchain.states
    ADD CONSTRAINT states_pkey PRIMARY KEY (oid);


--
-- Name: transitions transitions_pkey; Type: CONSTRAINT; Schema: petchain; Owner: bitwrap
--

ALTER TABLE ONLY petchain.transitions
    ADD CONSTRAINT transitions_pkey PRIMARY KEY (action);


--
-- Name: events oid_seq_pkey; Type: CONSTRAINT; Schema: vetchain; Owner: bitwrap
--

ALTER TABLE ONLY vetchain.events
    ADD CONSTRAINT oid_seq_pkey PRIMARY KEY (oid, seq);


--
-- Name: states states_pkey; Type: CONSTRAINT; Schema: vetchain; Owner: bitwrap
--

ALTER TABLE ONLY vetchain.states
    ADD CONSTRAINT states_pkey PRIMARY KEY (oid);


--
-- Name: transitions transitions_pkey; Type: CONSTRAINT; Schema: vetchain; Owner: bitwrap
--

ALTER TABLE ONLY vetchain.transitions
    ADD CONSTRAINT transitions_pkey PRIMARY KEY (action);


--
-- Name: hash_idx; Type: INDEX; Schema: counter; Owner: bitwrap
--

CREATE INDEX hash_idx ON counter.events USING btree (hash);


--
-- Name: hash_idx; Type: INDEX; Schema: petchain; Owner: bitwrap
--

CREATE INDEX hash_idx ON petchain.events USING btree (hash);


--
-- Name: hash_idx; Type: INDEX; Schema: vetchain; Owner: bitwrap
--

CREATE INDEX hash_idx ON vetchain.events USING btree (hash);


--
-- Name: events counter_dispatch; Type: TRIGGER; Schema: counter; Owner: bitwrap
--

CREATE TRIGGER counter_dispatch BEFORE INSERT ON counter.events FOR EACH ROW EXECUTE PROCEDURE counter.vclock();


--
-- Name: events petchain_dispatch; Type: TRIGGER; Schema: petchain; Owner: bitwrap
--

CREATE TRIGGER petchain_dispatch BEFORE INSERT ON petchain.events FOR EACH ROW EXECUTE PROCEDURE petchain.vclock();


--
-- Name: events vetchain_dispatch; Type: TRIGGER; Schema: vetchain; Owner: bitwrap
--

CREATE TRIGGER vetchain_dispatch BEFORE INSERT ON vetchain.events FOR EACH ROW EXECUTE PROCEDURE vetchain.vclock();


--
-- Name: events events_oid_fkey; Type: FK CONSTRAINT; Schema: counter; Owner: bitwrap
--

ALTER TABLE ONLY counter.events
    ADD CONSTRAINT events_oid_fkey FOREIGN KEY (oid) REFERENCES counter.states(oid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: events events_oid_fkey; Type: FK CONSTRAINT; Schema: petchain; Owner: bitwrap
--

ALTER TABLE ONLY petchain.events
    ADD CONSTRAINT events_oid_fkey FOREIGN KEY (oid) REFERENCES petchain.states(oid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: events events_oid_fkey; Type: FK CONSTRAINT; Schema: vetchain; Owner: bitwrap
--

ALTER TABLE ONLY vetchain.events
    ADD CONSTRAINT events_oid_fkey FOREIGN KEY (oid) REFERENCES vetchain.states(oid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

