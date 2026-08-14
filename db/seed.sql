-- =========================================================
-- Sample / Dummy Data — for local testing only
-- Run this AFTER schema.sql has created the tables.
-- =========================================================

-- ---------------------------------------------------------
-- 1. USERS (2 customers + 6 providers)
--    password_hash values below are placeholders (NOT real
--    hashes) — fine for local testing until auth is built.
-- ---------------------------------------------------------
INSERT INTO users (id, full_name, email, phone, password_hash, role, city) VALUES
('a1111111-0000-0000-0000-000000000001', 'Ayesha Khan',    'ayesha.customer@example.com', '03001234561', 'placeholder_hash', 'customer', 'Rawalpindi'),
('a1111111-0000-0000-0000-000000000002', 'Bilal Ahmed',    'bilal.customer@example.com',  '03001234562', 'placeholder_hash', 'customer', 'Islamabad'),

('b2222222-0000-0000-0000-000000000001', 'Usman Tariq',    'usman.painter@example.com',   '03011234561', 'placeholder_hash', 'provider', 'Rawalpindi'),
('b2222222-0000-0000-0000-000000000002', 'Farhan Sheikh',  'farhan.painter@example.com',  '03011234562', 'placeholder_hash', 'provider', 'Islamabad'),
('b2222222-0000-0000-0000-000000000003', 'Imran Baig',     'imran.plumber@example.com',   '03011234563', 'placeholder_hash', 'provider', 'Rawalpindi'),
('b2222222-0000-0000-0000-000000000004', 'Kashif Rana',    'kashif.plumber@example.com',  '03011234564', 'placeholder_hash', 'provider', 'Islamabad'),
('b2222222-0000-0000-0000-000000000005', 'Adnan Malik',    'adnan.electrician@example.com','03011234565', 'placeholder_hash', 'provider', 'Rawalpindi'),
('b2222222-0000-0000-0000-000000000006', 'Waqas Iqbal',    'waqas.electrician@example.com','03011234566', 'placeholder_hash', 'provider', 'Islamabad');

-- ---------------------------------------------------------
-- 2. PROVIDER PROFILES
--    (category_id looked up by name from service_categories,
--     which is already seeded in schema.sql)
-- ---------------------------------------------------------
INSERT INTO provider_profiles (user_id, category_id, bio, skill_tags, pricing_tier, hourly_rate, rating_avg, is_verified, is_available) VALUES
('b2222222-0000-0000-0000-000000000001',
 (SELECT id FROM service_categories WHERE name = 'Painter'),
 'Professional painter with 8 years of experience in residential interior and exterior painting.',
 ARRAY['interior painting','exterior painting','wall texture'],
 'standard', 800.00, 4.50, TRUE, TRUE),

('b2222222-0000-0000-0000-000000000002',
 (SELECT id FROM service_categories WHERE name = 'Painter'),
 'Budget-friendly painting services, specializing in quick single-room touch-ups.',
 ARRAY['interior painting','wall repair','putty work'],
 'budget', 500.00, 4.10, TRUE, TRUE),

('b2222222-0000-0000-0000-000000000003',
 (SELECT id FROM service_categories WHERE name = 'Plumber'),
 'Licensed plumber handling leak repairs, pipe fitting, and bathroom installations.',
 ARRAY['leak repair','pipe fitting','bathroom installation'],
 'standard', 700.00, 4.70, TRUE, TRUE),

('b2222222-0000-0000-0000-000000000004',
 (SELECT id FROM service_categories WHERE name = 'Plumber'),
 'Premium plumbing service with same-day emergency response.',
 ARRAY['emergency repair','water heater install','pipe fitting'],
 'premium', 1200.00, 4.90, TRUE, TRUE),

('b2222222-0000-0000-0000-000000000005',
 (SELECT id FROM service_categories WHERE name = 'Electrician'),
 'Certified electrician for wiring, fixture installation, and safety inspections.',
 ARRAY['wiring','fixture installation','safety inspection'],
 'standard', 900.00, 4.60, TRUE, TRUE),

('b2222222-0000-0000-0000-000000000006',
 (SELECT id FROM service_categories WHERE name = 'Electrician'),
 'Affordable electrical repair and appliance installation services.',
 ARRAY['appliance installation','minor repair','switchboard fitting'],
 'budget', 600.00, 4.00, TRUE, FALSE);

-- ---------------------------------------------------------
-- 3. BOOKINGS (a few sample requests in different states)
-- ---------------------------------------------------------
INSERT INTO bookings (customer_id, provider_id, category_id, scheduled_date, scheduled_time, address, estimated_price_min, estimated_price_max, final_price, status) VALUES
('a1111111-0000-0000-0000-000000000001',
 (SELECT id FROM provider_profiles WHERE user_id = 'b2222222-0000-0000-0000-000000000001'),
 (SELECT id FROM service_categories WHERE name = 'Painter'),
 CURRENT_DATE + INTERVAL '3 days', '10:00:00',
 'House 12, Street 4, Bahria Town, Rawalpindi',
 6000.00, 9000.00, NULL, 'requested'),

('a1111111-0000-0000-0000-000000000002',
 (SELECT id FROM provider_profiles WHERE user_id = 'b2222222-0000-0000-0000-000000000003'),
 (SELECT id FROM service_categories WHERE name = 'Plumber'),
 CURRENT_DATE - INTERVAL '2 days', '14:00:00',
 'Flat 5B, F-10 Markaz, Islamabad',
 1500.00, 2500.00, 2000.00, 'completed'),

('a1111111-0000-0000-0000-000000000001',
 (SELECT id FROM provider_profiles WHERE user_id = 'b2222222-0000-0000-0000-000000000005'),
 (SELECT id FROM service_categories WHERE name = 'Electrician'),
 CURRENT_DATE + INTERVAL '1 day', '11:30:00',
 'House 12, Street 4, Bahria Town, Rawalpindi',
 1000.00, 1800.00, NULL, 'accepted');

-- ---------------------------------------------------------
-- 4. REVIEWS (only for the completed booking)
-- ---------------------------------------------------------
INSERT INTO reviews (booking_id, customer_id, provider_id, rating, comment)
SELECT b.id, b.customer_id, b.provider_id, 5, 'Fixed the leak quickly and cleaned up after. Very professional.'
FROM bookings b
WHERE b.status = 'completed'
LIMIT 1;
