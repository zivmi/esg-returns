--
-- PostgreSQL database dump
--

-- Dumped from database version 13.13
-- Dumped by pg_dump version 13.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: test_esg_data; Type: TABLE; Schema: public; Owner: macbook
--

CREATE TABLE public.test_esg_data (
    date date,
    adj_close_a double precision,
    adj_close_aa double precision,
    adj_close_aal double precision,
    adj_close_aap double precision,
    adj_close_aapl double precision,
    adj_close_abbv double precision,
    adj_close_abk double precision,
    adj_close_abmd double precision,
    adj_close_abnb double precision,
    adj_close_abs double precision
);


ALTER TABLE public.test_esg_data OWNER TO macbook;

--
-- Data for Name: test_esg_data; Type: TABLE DATA; Schema: public; Owner: macbook
--

COPY public.test_esg_data (date, adj_close_a, adj_close_aa, adj_close_aal, adj_close_aap, adj_close_aapl, adj_close_abbv, adj_close_abk, adj_close_abmd, adj_close_abnb, adj_close_abs) FROM stdin;
\N	43.75773620605469	70.69157409667969	NaN	NaN	0.8472068905830383	NaN	0.10516999661922455	18.25	NaN	NaN
\N	40.415138244628906	71.01907348632812	NaN	NaN	0.7757785320281982	NaN	0.10516999661922455	17.812999725341797	NaN	NaN
\N	37.90818786621094	75.11319732666016	NaN	NaN	0.7871308922767639	NaN	0.1036899983882904	18	NaN	NaN
\N	36.46479797363281	74.13062286376953	NaN	NaN	0.7190139293670654	NaN	0.1036899983882904	18.031999588012695	NaN	NaN
\N	39.50351333618164	73.91230010986328	NaN	NaN	0.7530726790428162	NaN	0.1036899983882904	17.937999725341797	NaN	NaN
\N	41.89652633666992	73.69392395019531	NaN	NaN	0.7398278117179871	NaN	0.1036899983882904	20.5	NaN	NaN
\N	41.326751708984375	73.2572021484375	NaN	NaN	0.7019848823547363	NaN	0.1036899983882904	19.812999725341797	NaN	NaN
\N	40.491111755371094	72.60218048095703	NaN	NaN	0.6598851680755615	NaN	0.1036899983882904	19.5939998626709	NaN	NaN
\N	41.0988655090332	71.29203033447266	NaN	NaN	0.7322590351104736	NaN	0.1036899983882904	21	NaN	NaN
\N	41.5546760559082	69.87275695800781	NaN	NaN	0.76016765832901	NaN	0.1036899983882904	21.375	NaN	NaN
\.


--
-- PostgreSQL database dump complete
--

