BEGIN;

-- Bulk load this batch into staging first.

INSERT INTO candles (...)
SELECT DISTINCT ON (
    exchange, symbol, timeframe, open_time
)
    exchange, symbol, timeframe, open_time,
    open, high, low, close, volume
FROM candles_staging
ORDER BY
    exchange, symbol, timeframe, open_time,
    received_at DESC
ON CONFLICT (exchange, symbol, timeframe, open_time)
DO UPDATE SET
    open   = EXCLUDED.open,
    high   = EXCLUDED.high,
    low    = EXCLUDED.low,
    close  = EXCLUDED.close,
    volume = EXCLUDED.volume;

-- Update the ingestion checkpoint here, in the same transaction.

COMMIT;


CREATE TABLE ingestion_jobs (
    id UUID PRIMARY KEY,
    symbol TEXT NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE outbox_events (
    id UUID PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at TIMESTAMPTZ,
    attempts INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX idx_outbox_pending
    ON outbox_events (created_at)
    WHERE published_at IS NULL;

from uuid import uuid4
from datetime import datetime, timezone


def create_ingestion_job(db, symbol, start_time, end_time):
    job_id = uuid4()
    event_id = uuid4()

    with db.begin():
        db.execute(
            """
            INSERT INTO ingestion_jobs (
                id, symbol, start_time, end_time
            )
            VALUES (:id, :symbol, :start, :end)
            """,
            {
                "id": job_id,
                "symbol": symbol,
                "start": start_time,
                "end": end_time,
            },
        )

        db.execute(
            """
            INSERT INTO outbox_events (
                id, aggregate_id, event_type, payload
            )
            VALUES (
                :event_id, :job_id, :event_type, CAST(:payload AS jsonb)
            )
            """,
            {
                "event_id": event_id,
                "job_id": job_id,
                "event_type": "ingestion.job_created",
                "payload": (
                    '{"job_id": "' + str(job_id) + '", '
                    '"symbol": "' + symbol + '"}'
                ),
            },
        )

    return job_id

