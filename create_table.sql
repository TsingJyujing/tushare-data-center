-- Table: public.stock_5min_tick

-- DROP TABLE public.stock_5min_tick;

CREATE TABLE public.stock_5min_tick
(
  code character varying(10) NOT NULL, -- 股票代码
  tick timestamp without time zone NOT NULL, -- 采样日期
  volume double precision,
  open double precision,
  close double precision,
  high double precision,
  low double precision,
  CONSTRAINT stock_5min_tick_pkey PRIMARY KEY (code, tick)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.stock_5min_tick
  OWNER TO postgres;
COMMENT ON COLUMN public.stock_5min_tick.code IS '股票代码';
COMMENT ON COLUMN public.stock_5min_tick.tick IS '采样日期';

-- Table: public.stock_daily_tick

-- DROP TABLE public.stock_daily_tick;

CREATE TABLE public.stock_daily_tick
(
  code character varying(10) NOT NULL, -- 股票代码
  tick timestamp without time zone NOT NULL, -- 采样日期
  volume double precision,
  open double precision,
  close double precision,
  high double precision,
  low double precision,
  CONSTRAINT stock_daily_tick_pkey PRIMARY KEY (code, tick)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.stock_daily_tick
  OWNER TO postgres;
COMMENT ON COLUMN public.stock_daily_tick.code IS '股票代码';
COMMENT ON COLUMN public.stock_daily_tick.tick IS '采样日期';

