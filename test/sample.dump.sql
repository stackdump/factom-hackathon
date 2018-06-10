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
my_pet_uuid	1	create_chain	{}	6554ac66b53c391bc6484ad139531c2a	2018-06-10 01:39:15.963688
my_pet_uuid	2	update_rfid	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	18c05de241a6eadef0426650a3076a26	2018-06-10 01:39:15.978441
my_pet_uuid	3	new_travel_process	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	89b701d600b96ae6a2ce2fa8c1dd53cc	2018-06-10 01:39:15.993914
my_pet_uuid	4	vaccine	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	966601cecdb9ada11f968749a672ce02	2018-06-10 01:39:16.006809
my_pet_uuid	5	booster	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	d962b2e7951f2cc9d6c4800404fd6c02	2018-06-10 01:39:16.020397
my_pet_uuid	6	titer_test	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	0381a21c9ffa1c5536d537b8d49970f1	2018-06-10 01:39:16.033615
my_pet_uuid	7	submit_lab_work	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	ebd31331d8cf96494262381a2fe500a4	2018-06-10 01:39:16.046556
my_pet_uuid	8	verified_complete	{"rfid": "123.456789999999", "vetchain": "dr_chery_york_dvm"}	d5941f5b70e5818620c51d4f96ee58c8	2018-06-10 01:39:16.060603
1528595045159	1	create_chain	{}	1561a9b9b37ed154537ebee0ee6ce161	2018-06-10 01:44:05.218406
1528595066957	1	create_chain	{}	dbfa4c0e185dfdcba54eab88c7d52d93	2018-06-10 01:44:27.00342
1528596301409	1	create_chain	{"chain_id": "f0ec1ecb5cd6be2d5d68355e956ee8d77b52e9ef52a026222ab7f3f7bcc436da", "entry_hash": "d6e14e13723503a8b8f517a09b20bcc3cf2703fe0dbd3491ec6447c351429049"}	aea5f995323a2203548067d6ef77cc70	2018-06-10 02:05:02.08485
1528596301409	2	update_rfid	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	5550e04b0c770f73a133e5dd06444422	2018-06-10 02:30:26.066568
1528596301409	3	update_rfid	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	37a2e415a532a68d503b8b102590ffab	2018-06-10 02:37:40.125202
1528596301409	4	update_rfid	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	daddbba4480c4a10ba1481c66ea73cb8	2018-06-10 02:38:33.492222
1528596301409	5	update_rfid	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	2e0a3f92f7be699e55200078bba96e84	2018-06-10 02:39:26.546257
1528596301409	6	update_rfid	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	c16cbcf520fbbcdbd37d0d11b4c6000b	2018-06-10 02:40:19.370588
testmy_pet_uuid	1	create_chain	{"chain_id": "2fda5eb156f12821453d7783422c702f295035fadcd59fa52cd20508c279575b", "entry_hash": "8aa1fe7922a554612ce053388a48aa62671ef3e866142fef6d2d0092af30b702"}	dbbc56105d31fdad59d54b35887848af	2018-06-10 02:41:56.339949
testmy_pet_uuid	2	update_rfid	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	32efa36fb7a8eee6251b5ce2265118eb	2018-06-10 02:41:56.918659
testmy_pet_uuid	3	new_travel_process	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	08c370854c12257defa3cb354361a1e3	2018-06-10 02:41:58.037474
testmy_pet_uuid	4	vaccine	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	721db099eae468c31b6a617f85ae3cdb	2018-06-10 02:41:59.180047
testmy_pet_uuid	5	booster	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	b9866f6e3111e0289bbfac63b5c5cee5	2018-06-10 02:42:00.319537
testmy_pet_uuid	6	titer_test	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	e7ee5f214edad6a6382c2ecec0dfdfbd	2018-06-10 02:42:01.451587
testmy_pet_uuid	7	submit_lab_work	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	b34d390a0534a391c7c7b33bb0bb0ca1	2018-06-10 02:42:02.594257
testmy_pet_uuid	8	verified_complete	{"rfid": "123.456789999999", "vetchain": "testdr_chery_york_dvm"}	32ed47af69125c84a0f98b67d38814a4	2018-06-10 02:42:03.721464
\.


--
-- Data for Name: states; Type: TABLE DATA; Schema: petchain; Owner: bitwrap
--

COPY petchain.states (oid, rev, state, created, modified) FROM stdin;
my_pet_uuid	8	(0,0,0,1,1,0,1,0)	2018-06-10 01:39:15.962098	2018-06-10 01:39:16.060603
1528595045159	1	(0,0,0,0,0,0,1,0)	2018-06-10 01:44:05.208979	2018-06-10 01:44:05.218406
1528595066957	1	(0,0,0,0,0,0,1,0)	2018-06-10 01:44:26.999681	2018-06-10 01:44:27.00342
1528596301409	6	(0,0,0,5,0,0,1,0)	2018-06-10 02:05:01.470658	2018-06-10 02:40:19.370588
testmy_pet_uuid	8	(0,0,0,1,1,0,1,0)	2018-06-10 02:41:55.7908	2018-06-10 02:42:03.721464
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
dr_chery_york_dvm	1	create_chain	{}	f52afac61223312ce397ef9854af0924	2018-06-10 01:39:15.941588
dr_chery_york_dvm	2	update_rfid	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	b30645ed024df52dba146cb527dd1f1c	2018-06-10 01:39:15.977017
dr_chery_york_dvm	3	new_travel_process	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	e9c5ae608ca0227e4f3f4751736c07bf	2018-06-10 01:39:15.99247
dr_chery_york_dvm	4	vaccine	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	ce7ff8a59cdf4f45fdcced106ee9fd32	2018-06-10 01:39:16.00454
dr_chery_york_dvm	5	booster	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	f88f7bd3278e4bf6aeb9b60453ed49b3	2018-06-10 01:39:16.018959
dr_chery_york_dvm	6	titer_test	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	4857e0376762aba25b0910237f0d4ddf	2018-06-10 01:39:16.032089
dr_chery_york_dvm	7	submit_lab_work	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	3e1ad33520b0faf0ca2ab2e51f9f6054	2018-06-10 01:39:16.044491
dr_chery_york_dvm	8	verified_complete	{"rfid": "123.456789999999", "petchain": "my_pet_uuid"}	313ae920d9e98dcebe06636e3326a0f9	2018-06-10 01:39:16.059249
1528595953438	1	create_chain	{}	34421168394ba3515f358fbee22f2921	2018-06-10 01:59:18.202726
1528596059185	1	create_chain	{}	87e5a1ade010451e550ce55256012e77	2018-06-10 02:01:02.694972
testdr_chery_york_dvm	1	create_chain	{"chain_id": "c9c6927f56c18bd50c314b2d3482135e3f620917d03ca848dffc6a0162211060", "entry_hash": "aab344acb05d877a58ef680a2fa9dcc39ae126937606b7b2a736a8edf38b7f8f"}	96c98ea7ce6665884aecc1c0a274902d	2018-06-10 02:41:55.75939
testdr_chery_york_dvm	2	update_rfid	{"rfid": "123.456789999999", "petchain": "testmy_pet_uuid"}	6620261146cd433efb8cc1669ae72a12	2018-06-10 02:41:56.368766
testdr_chery_york_dvm	3	new_travel_process	{"rfid": "123.456789999999", "petchain": "testmy_pet_uuid"}	7f453a4c94cb6423a93e40e55a481cd3	2018-06-10 02:41:57.486346
testdr_chery_york_dvm	4	vaccine	{"rfid": "123.456789999999", "petchain": "testmy_pet_uuid"}	3234799f4ebc92a4d0d88a73bd75a2de	2018-06-10 02:41:58.615859
testdr_chery_york_dvm	5	booster	{"rfid": "123.456789999999", "petchain": "testmy_pet_uuid"}	dea2eb1b36015924c4dc329a37861adb	2018-06-10 02:41:59.75734
testdr_chery_york_dvm	6	titer_test	{"rfid": "123.456789999999", "petchain": "testmy_pet_uuid"}	8ce1d884574999556c90f96f7463be20	2018-06-10 02:42:00.893169
testdr_chery_york_dvm	7	submit_lab_work	{"rfid": "123.456789999999", "petchain": "testmy_pet_uuid"}	9b989d62e7d45b212b69d310e91fc983	2018-06-10 02:42:02.032274
testdr_chery_york_dvm	8	verified_complete	{"rfid": "123.456789999999", "petchain": "testmy_pet_uuid"}	7b27457e07bae71ddfe684360d56e7fe	2018-06-10 02:42:03.168532
\.


--
-- Data for Name: states; Type: TABLE DATA; Schema: vetchain; Owner: bitwrap
--

COPY vetchain.states (oid, rev, state, created, modified) FROM stdin;
dr_chery_york_dvm	8	(1,1,1,0,1,1,1,1)	2018-06-10 01:39:15.9393	2018-06-10 01:39:16.059249
1528595747101	0	(0,0,0,0,0,0,0,0)	2018-06-10 01:55:47.179277	2018-06-10 01:55:47.179277
1528595900455	0	(0,0,0,0,0,0,0,0)	2018-06-10 01:58:20.523333	2018-06-10 01:58:20.523333
1528595953438	1	(0,0,0,0,0,1,0,0)	2018-06-10 01:59:13.491174	2018-06-10 01:59:18.202726
1528596059185	1	(0,0,0,0,0,1,0,0)	2018-06-10 02:00:59.234201	2018-06-10 02:01:02.694972
1528596216997	0	(0,0,0,0,0,0,0,0)	2018-06-10 02:03:37.051448	2018-06-10 02:03:37.051448
1528596279973	0	(0,0,0,0,0,0,0,0)	2018-06-10 02:04:40.030884	2018-06-10 02:04:40.030884
testdr_chery_york_dvm	8	(1,1,1,0,1,1,1,1)	2018-06-10 02:41:55.191639	2018-06-10 02:42:03.168532
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

SELECT pg_catalog.setval('petchain.events_seq_seq', 24, true);


--
-- Name: events_seq_seq; Type: SEQUENCE SET; Schema: vetchain; Owner: bitwrap
--

SELECT pg_catalog.setval('vetchain.events_seq_seq', 32, true);


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

