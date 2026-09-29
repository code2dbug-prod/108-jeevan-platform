# Domain model

## Customer
Authenticated person who owns one or more birth profiles and can view published readings.

## Birth profile
Immutable inputs should be versioned in production when corrected. Required: name, DOB, birthplace, coordinates, timezone, and birth-time precision. Exact/approximate times require a time; unknown forbids one.

## Chart snapshot
A reproducible deterministic result keyed by calculation version and settings. Never overwrite old snapshots after engine upgrades.

## Reading session
The container for one question/read. Links chart, current astrology, spread, card draws, evidence, reader notes and final report.

## Evidence
Every synthesized statement should be traceable to one or more evidence records: natal placement, Dasha, transit, card, card combination, source note or reader note.
