-- =========================================================
-- Home Services Marketplace - Core Database Schema
-- =========================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ---------------------------------------------------------
-- USERS (customers, providers, admins - all in one table)
-- ---------------------------------------------------------
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('customer', 'provider', 'admin')),
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ---------------------------------------------------------
-- SERVICE CATEGORIES (painter, plumber, electrician, etc.)
-- ---------------------------------------------------------
CREATE TABLE service_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    base_commission_percent NUMERIC(5,2) DEFAULT 10.00,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ---------------------------------------------------------
-- PROVIDER PROFILES (extra info for role='provider' users)
-- ---------------------------------------------------------
CREATE TABLE provider_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID NOT NULL REFERENCES service_categories(id),
    bio TEXT,
    skill_tags TEXT[],                 -- e.g. {'interior painting','wall repair'}
    pricing_tier VARCHAR(20) CHECK (pricing_tier IN ('budget','standard','premium')),
    hourly_rate NUMERIC(10,2),
    rating_avg NUMERIC(3,2) DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ---------------------------------------------------------
-- BOOKINGS
-- ---------------------------------------------------------
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL REFERENCES users(id),
    provider_id UUID NOT NULL REFERENCES provider_profiles(id),
    category_id UUID NOT NULL REFERENCES service_categories(id),
    scheduled_date DATE,
    scheduled_time TIME,
    address TEXT,
    estimated_price_min NUMERIC(10,2),
    estimated_price_max NUMERIC(10,2),
    final_price NUMERIC(10,2),
    status VARCHAR(20) DEFAULT 'requested'
        CHECK (status IN ('requested','accepted','in_progress','completed','cancelled')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ---------------------------------------------------------
-- REVIEWS
-- ---------------------------------------------------------
CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_id UUID NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    customer_id UUID NOT NULL REFERENCES users(id),
    provider_id UUID NOT NULL REFERENCES provider_profiles(id),
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ---------------------------------------------------------
-- Indexes for faster search/filter
-- ---------------------------------------------------------
CREATE INDEX idx_provider_category ON provider_profiles(category_id);
CREATE INDEX idx_booking_status ON bookings(status);
CREATE INDEX idx_booking_customer ON bookings(customer_id);
CREATE INDEX idx_booking_provider ON bookings(provider_id);

-- ---------------------------------------------------------
-- Sample seed data (for local testing only)
-- ---------------------------------------------------------
INSERT INTO service_categories (name, description) VALUES
('Painter', 'Interior and exterior painting services'),
('Plumber', 'Pipe fitting, leak repair, installations'),
('Electrician', 'Wiring, fixtures, and electrical repair');
