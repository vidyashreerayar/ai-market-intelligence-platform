INSERT INTO brands (brand_name, parent_company, positioning, target_consumer)
VALUES
('Chio', 'Intersnack', 'Classic potato chips and snacks', 'General consumers'),
('funny-frisch', 'Intersnack', 'Fun everyday snacks', 'Families'),
('Pom-Bär', 'Intersnack', 'Children''s potato snacks', 'Children'),
('Tyrrells', 'Intersnack', 'Premium hand-cooked crisps', 'Premium consumers'),
('KP Snacks', 'Intersnack', 'Nuts and savory snacks', 'General consumers'),

('Lay''s', 'PepsiCo', 'Global potato chips', 'General consumers'),
('Doritos', 'PepsiCo', 'Bold flavored tortilla chips', 'Young adults'),
('Cheetos', 'PepsiCo', 'Cheese snacks', 'Young consumers'),
('Pringles', 'Kellanova', 'Stackable potato crisps', 'General consumers'),
('Kettle Chips', 'Campbell Soup Company', 'Premium kettle cooked chips', 'Premium consumers');

SELECT * FROM brands;

INSERT INTO products (
    brand_id,
    product_name,
    category,
    sub_category,
    flavor,
    is_active
)
VALUES
-- Chio
(1,'Chio Paprika','Potato Chips','Classic','Paprika',TRUE),
(1,'Chio Ready Salted','Potato Chips','Classic','Salted',TRUE),
(1,'Chio Sour Cream & Onion','Potato Chips','Classic','Sour Cream & Onion',TRUE),

-- funny-frisch
(2,'funny-frisch Ungarisch','Potato Chips','Classic','Hungarian',TRUE),
(2,'funny-frisch Chipsfrisch Oriental','Potato Chips','Classic','Oriental',TRUE),
(2,'funny-frisch Kessel Chips Sea Salt','Potato Chips','Kettle','Sea Salt',TRUE),

-- Pom-Bär
(3,'Pom-Bär Original','Potato Snacks','Kids','Original',TRUE),
(3,'Pom-Bär Ketchup Style','Potato Snacks','Kids','Ketchup',TRUE),

-- Tyrrells
(4,'Tyrrells Sea Salt','Potato Chips','Kettle','Sea Salt',TRUE),
(4,'Tyrrells Mature Cheddar & Chive','Potato Chips','Kettle','Cheddar & Chive',TRUE),
(4,'Tyrrells Sweet Chilli','Potato Chips','Kettle','Sweet Chilli',TRUE),

-- KP Snacks
(5,'KP Dry Roasted Peanuts','Nuts','Peanuts','Dry Roasted',TRUE),
(5,'KP Salted Peanuts','Nuts','Peanuts','Salted',TRUE),
(5,'KP Original Nuts','Mixed Nuts','Mixed','Original',TRUE),

-- Lay's
(6,'Lay''s Classic','Potato Chips','Classic','Salted',TRUE),
(6,'Lay''s Barbecue','Potato Chips','Classic','Barbecue',TRUE),
(6,'Lay''s Sour Cream & Onion','Potato Chips','Classic','Sour Cream & Onion',TRUE),

-- Doritos
(7,'Doritos Nacho Cheese','Tortilla Chips','Corn','Nacho Cheese',TRUE),
(7,'Doritos Cool Ranch','Tortilla Chips','Corn','Cool Ranch',TRUE),

-- Cheetos
(8,'Cheetos Crunchy','Cheese Snacks','Corn','Cheese',TRUE),
(8,'Cheetos Puffs','Cheese Snacks','Corn','Cheese',TRUE),

-- Pringles
(9,'Pringles Original','Potato Crisps','Stacked','Original',TRUE),
(9,'Pringles Sour Cream & Onion','Potato Crisps','Stacked','Sour Cream & Onion',TRUE),
(9,'Pringles Paprika','Potato Crisps','Stacked','Paprika',TRUE),

-- Kettle Chips
(10,'Kettle Sea Salt','Potato Chips','Kettle','Sea Salt',TRUE),
(10,'Kettle Sea Salt & Vinegar','Potato Chips','Kettle','Salt & Vinegar',TRUE),
(10,'Kettle Sweet Chilli','Potato Chips','Kettle','Sweet Chilli',TRUE);

SELECT * FROM products;

INSERT INTO nutrition (
    product_id,
    serving_size_g,
    calories_kcal,
    protein_g,
    fat_g,
    carbohydrates_g,
    sugar_g,
    salt_g
)
VALUES
(1,100,535,6.5,34.5,52.0,1.2,1.3),
(2,100,530,6.2,33.8,53.0,0.8,1.2),
(3,100,532,6.4,34.0,52.5,2.0,1.4),
(4,100,528,6.1,33.5,53.2,1.5,1.3),
(5,100,531,6.3,34.2,52.1,1.8,1.2),
(6,100,540,6.8,35.5,50.8,0.9,1.1),
(7,100,510,5.8,28.0,60.0,2.1,1.0),
(8,100,515,5.7,28.5,59.2,4.0,1.2),
(9,100,545,6.0,36.5,49.8,0.7,1.4),
(10,100,548,6.4,36.8,49.2,1.1,1.5),
(11,100,550,6.2,37.0,48.9,2.2,1.3),
(12,100,610,26.0,49.0,16.0,4.5,1.0),
(13,100,615,25.8,50.0,15.2,3.8,1.1),
(14,100,600,21.5,48.0,19.5,3.0,0.9),
(15,100,536,6.4,34.0,52.4,0.5,1.2),
(16,100,540,6.6,35.0,51.0,4.2,1.3),
(17,100,538,6.3,34.7,51.8,2.1,1.3),
(18,100,500,7.0,25.0,63.0,2.5,1.6),
(19,100,502,7.1,25.2,62.8,2.4,1.5),
(20,100,560,7.5,35.0,54.0,1.8,1.7),
(21,100,562,7.3,35.5,53.5,2.0,1.6),
(22,100,530,4.8,33.0,56.0,1.0,1.2),
(23,100,532,4.9,33.5,55.8,2.0,1.2),
(24,100,534,4.8,33.8,55.2,1.5,1.2),
(25,100,545,6.1,36.2,50.0,0.6,1.3),
(26,100,548,6.2,36.8,49.3,1.8,1.4),
(27,100,547,6.0,36.5,49.7,2.1,1.3);

SELECT * FROM nutrition;

INSERT INTO health_claims (claim_name)
VALUES
('Vegan'),
('Gluten Free'),
('High Protein'),
('Low Salt'),
('Organic'),
('No Artificial Flavours'),
('High Fibre');

INSERT INTO product_health_claims (product_id, claim_id)
VALUES
-- Pom-Bär
(7,6),
(8,6),

-- KP Snacks
(12,3),
(13,3),
(14,3),

-- Tyrrells
(9,6),
(10,6),
(11,6),

-- Kettle Chips
(25,6),
(26,6),
(27,6),

-- Lay's
(15,2),
(16,2),

-- Pringles
(22,2),
(23,2),
(24,2);

SELECT * FROM health_claims;

SELECT * FROM product_health_claims;

SELECT
    p.product_name,
    h.claim_name
FROM product_health_claims ph
JOIN products p
    ON ph.product_id = p.product_id
JOIN health_claims h
    ON ph.claim_id = h.claim_id
ORDER BY p.product_name;

INSERT INTO ingredients (product_id, ingredient_name)
VALUES
(1,'Potatoes'),
(1,'Sunflower Oil'),
(1,'Paprika Seasoning'),

(2,'Potatoes'),
(2,'Sunflower Oil'),
(2,'Salt'),

(3,'Potatoes'),
(3,'Sunflower Oil'),
(3,'Sour Cream & Onion Seasoning'),

(12,'Peanuts'),
(12,'Salt'),

(15,'Potatoes'),
(15,'Vegetable Oil'),
(15,'Salt'),

(18,'Corn'),
(18,'Vegetable Oil'),
(18,'Nacho Cheese Seasoning'),

(22,'Potato Flakes'),
(22,'Vegetable Oil'),
(22,'Salt');

SELECT * FROM ingredients;

INSERT INTO competitors (
    company_name,
    headquarters,
    market_share
)
VALUES
('PepsiCo','USA',22.5),
('Kellanova','USA',12.8),
('Campbell Soup Company','USA',6.5),
('Mondelez International','USA',10.4);

INSERT INTO retailers (retailer_name,country)
VALUES
('REWE','Germany'),
('EDEKA','Germany'),
('Kaufland','Germany'),
('Amazon','Germany'),
('Tesco','United Kingdom');

INSERT INTO prices (
    product_id,
    retailer_id,
    price,
    currency,
    date_recorded
)
VALUES
(1,1,2.49,'EUR','2026-07-22'),
(2,1,2.39,'EUR','2026-07-22'),
(3,2,2.59,'EUR','2026-07-22'),
(4,2,2.29,'EUR','2026-07-22'),
(5,3,2.69,'EUR','2026-07-22'),
(6,3,2.99,'EUR','2026-07-22'),
(7,1,1.99,'EUR','2026-07-22'),
(8,1,1.99,'EUR','2026-07-22'),
(9,2,3.29,'EUR','2026-07-22'),
(10,2,3.49,'EUR','2026-07-22'),
(11,3,3.39,'EUR','2026-07-22'),
(12,4,2.99,'EUR','2026-07-22'),
(13,4,2.89,'EUR','2026-07-22'),
(14,5,3.19,'GBP','2026-07-22'),
(15,1,2.49,'EUR','2026-07-22'),
(16,2,2.59,'EUR','2026-07-22'),
(17,3,2.69,'EUR','2026-07-22'),
(18,4,3.29,'EUR','2026-07-22'),
(19,5,3.49,'GBP','2026-07-22'),
(20,1,2.79,'EUR','2026-07-22'),
(21,2,2.89,'EUR','2026-07-22'),
(22,3,2.99,'EUR','2026-07-22'),
(23,4,3.09,'EUR','2026-07-22'),
(24,5,3.19,'GBP','2026-07-22'),
(25,1,3.29,'EUR','2026-07-22'),
(26,2,3.39,'EUR','2026-07-22'),
(27,3,3.49,'EUR','2026-07-22');

SELECT * FROM prices;

INSERT INTO consumer_reviews (
    product_id,
    rating,
    review_title,
    review_text,
    review_date,
    source
)
VALUES
(1,4.5,'Great flavor','Really enjoyed the paprika seasoning.','2026-07-20','Amazon'),
(2,4.2,'Classic chips','Simple and tasty.','2026-07-18','REWE'),
(4,4.7,'Family favorite','Always fresh and crunchy.','2026-07-15','Amazon'),
(9,4.8,'Premium quality','Excellent taste and texture.','2026-07-16','Tesco'),
(12,4.6,'Healthy snack','Great protein content.','2026-07-19','Amazon'),
(15,4.3,'Good value','Classic chips at a fair price.','2026-07-17','EDEKA'),
(18,4.9,'Best tortilla chips','Perfect with salsa.','2026-07-21','Amazon'),
(22,4.1,'Crispy','Very addictive.','2026-07-20','Kaufland'),
(25,4.7,'Excellent kettle chips','Very crunchy and flavorful.','2026-07-19','Amazon');

INSERT INTO market_trends (
    category,
    country,
    trend_score,
    trend_date
)
VALUES
('High Protein Snacks','Germany',89.5,'2026-07-22'),
('Healthy Chips','Germany',84.2,'2026-07-22'),
('Plant-Based Snacks','Germany',91.0,'2026-07-22'),
('Low Salt Snacks','Germany',72.4,'2026-07-22'),
('Premium Chips','United Kingdom',78.6,'2026-07-22'),
('Tortilla Chips','Germany',80.5,'2026-07-22');

INSERT INTO forecasts (
    product_id,
    forecast_date,
    predicted_demand,
    confidence_score
)
VALUES
(1,'2026-08-01',1200,92.5),
(4,'2026-08-01',980,90.2),
(9,'2026-08-01',860,94.1),
(12,'2026-08-01',1450,95.3),
(15,'2026-08-01',1700,91.4),
(18,'2026-08-01',1550,93.8),
(22,'2026-08-01',1320,89.7),
(25,'2026-08-01',910,92.0);

SELECT
    p.product_name,
    b.brand_name
FROM products p
JOIN brands b
ON p.brand_id = b.brand_id;

SELECT
    p.product_name,
    n.calories_kcal,
    n.protein_g
FROM products p
JOIN nutrition n
ON p.product_id = n.product_id;

SELECT
    p.product_name,
    h.claim_name
FROM products p
JOIN product_health_claims ph
ON p.product_id = ph.product_id
JOIN health_claims h
ON ph.claim_id = h.claim_id;

SELECT
    p.product_name,
    r.retailer_name,
    pr.price,
    pr.currency
FROM prices pr
JOIN products p
ON pr.product_id = p.product_id
JOIN retailers r
ON pr.retailer_id = r.retailer_id;

SELECT
    p.product_name,
    c.rating,
    c.review_title
FROM consumer_reviews c
JOIN products p
ON c.product_id = p.product_id;

SELECT * FROM news_articles;

DELETE FROM news_articles
WHERE title = 'Test Article';

SELECT COUNT(*) FROM news_articles;

SELECT * FROM news_articles;

SELECT
'INSERT INTO news_articles (article_id, title, source, published_at, url, description) VALUES (' ||
article_id || ', ' ||
quote_literal(title) || ', ' ||
quote_literal(source) || ', ' ||
quote_literal(published_at) || ', ' ||
quote_literal(url) || ', ' ||
quote_literal(description) || ');'
FROM news_articles;