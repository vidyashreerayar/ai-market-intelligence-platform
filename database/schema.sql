CREATE TABLE brands(
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(50) NOT NULL,
    parent_company VARCHAR(50),
    positioning TEXT,
    target_consumer VARCHAR(50)
)

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    sub_category VARCHAR(50),
    flavor VARCHAR(100),
    launch_date DATE,
    is_active BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
);

CREATE TABLE nutrition (
    nutrition_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    serving_size_g DECIMAL(5,2),
    calories_kcal DECIMAL(6,2),
    protein_g DECIMAL(5,2),
    fat_g DECIMAL(5,2),
    carbohydrates_g DECIMAL(5,2),
    sugar_g DECIMAL(5,2),
    salt_g DECIMAL(5,2),

    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE health_claims (
    claim_id SERIAL PRIMARY KEY,
    claim_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE product_health_claims (
    product_id INTEGER NOT NULL,
    claim_id INTEGER NOT NULL,

    PRIMARY KEY (product_id, claim_id),

    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (claim_id) REFERENCES health_claims(claim_id)
);

-- ==========================
-- PRODUCT HEALTH CLAIMS
-- ==========================
CREATE TABLE IF NOT EXISTS product_health_claims (

    product_id INTEGER,
    claim_id INTEGER,

    PRIMARY KEY(product_id, claim_id),

    FOREIGN KEY(product_id)
        REFERENCES products(product_id),

    FOREIGN KEY(claim_id)
        REFERENCES health_claims(claim_id)
);

-- ==========================
-- INGREDIENTS
-- ==========================
CREATE TABLE IF NOT EXISTS ingredients (

    ingredient_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    ingredient_name VARCHAR(150) NOT NULL,

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);

-- ==========================
-- COMPETITORS
-- ==========================
CREATE TABLE IF NOT EXISTS competitors (

    competitor_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    headquarters VARCHAR(100),
    market_share DECIMAL(5,2)
);

-- ==========================
-- RETAILERS
-- ==========================
CREATE TABLE IF NOT EXISTS retailers (

    retailer_id SERIAL PRIMARY KEY,
    retailer_name VARCHAR(100) NOT NULL,
    country VARCHAR(100)
);

-- ==========================
-- PRICES
-- ==========================
CREATE TABLE IF NOT EXISTS prices (

    price_id SERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,
    retailer_id INTEGER NOT NULL,

    price DECIMAL(6,2),
    currency VARCHAR(10),
    date_recorded DATE,

    FOREIGN KEY(product_id)
        REFERENCES products(product_id),

    FOREIGN KEY(retailer_id)
        REFERENCES retailers(retailer_id)
);

-- ==========================
-- CONSUMER REVIEWS
-- ==========================
CREATE TABLE IF NOT EXISTS consumer_reviews (

    review_id SERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,

    rating DECIMAL(2,1),

    review_title VARCHAR(255),

    review_text TEXT,

    review_date DATE,

    source VARCHAR(100),

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);

-- ==========================
-- MARKET TRENDS
-- ==========================
CREATE TABLE IF NOT EXISTS market_trends (

    trend_id SERIAL PRIMARY KEY,

    category VARCHAR(100),

    country VARCHAR(100),

    trend_score DECIMAL(6,2),

    trend_date DATE
);

-- ==========================
-- FORECASTS
-- ==========================
CREATE TABLE IF NOT EXISTS forecasts (

    forecast_id SERIAL PRIMARY KEY,

    product_id INTEGER,

    forecast_date DATE,

    predicted_demand DECIMAL(10,2),

    confidence_score DECIMAL(5,2),

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;


CREATE TABLE news_articles (
    article_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    source VARCHAR(255),
    published_at TIMESTAMP,
    url TEXT UNIQUE,
    description TEXT
);

SELECT * FROM news_articles;

CREATE TABLE IF NOT EXISTS potato_prices (
    year INTEGER PRIMARY KEY,
    price_eur_per_100kg DECIMAL(10,2)
);