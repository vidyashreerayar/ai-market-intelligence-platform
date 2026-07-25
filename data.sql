--
-- PostgreSQL database dump
--

\restrict JY3ZoFMcybtDY7tDk4elcFRtYYcJDfFiATcFC31V3uMkGoSfQkmmgwM6f8zRhfl

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: news_articles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (2, 'Why are chips packets filled with air? The real reason has nothing to do with fooling customers', 'The Times of India', '2026-07-21 05:55:00', 'https://timesofindia.indiatimes.com/life-style/food-news/why-are-chips-packets-filled-with-air-the-real-reason-has-nothing-to-do-with-fooling-customers/photostory/132527004.cms', 'Few things are as universally disappointing as opening a freshly bought packet of chips and finding it looks only half full. It is a moment that has sparked countless jokes, memes and complaints, with many convinced that snack companies intentionally fill pac…');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (3, 'What do Brits call chips?', 'Lifesciencesworld.com', '2026-07-21 05:30:17', 'https://www.lifesciencesworld.com/what-do-brits-call-chips/', 'What Do Brits Call Chips? Unveiling the Great Potato Divide The answer is simple: In the UK, what Americans call French fries are universally known as chips, while what Americans call chips are known as crisps. The Great Potato Naming Convention: A Transatlan…');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (4, 'Freshco Ontario: McCain Cakes $4.49 After Scene+ Points + Flyer Deals July 23rd – 29th', 'Smartcanucks.ca', '2026-07-21 02:00:13', 'https://smartcanucks.ca/freshco-ontario-mccain-cakes-4-49-after-scene-points-flyer-deals-july-23rd-29th/', 'McCain Deep N'' Delicious cakes are typically well over $5 these days, but from July the 23rd to the 29th you can get them for less at Freshco. Advertised for $4.99, you will receive 50 Scene+ points when you scan your card. After the value of the points the c…');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (5, 'Libre Graphics Meeting 2026', 'Wordpress.com', '2026-07-21 01:18:06', 'https://outsideofinfinity.wordpress.com/2026/07/21/libre-graphics-meeting-2026/', 'Tuesday
I arrived at Nuremberg after a very long travel and nearly no sleep, so I didn’t go to the “warming up” party in the bar, but instead met up with C. and we went to a Balkan restaurant (Balkan Spezialitäten) for dinner. We got Cevapcici sausages with s…');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (6, 'BrightEdge Research: Google AI Cites Facebook in 19.5', 'GlobeNewswire', '2026-07-20 15:03:01', 'https://www.globenewswire.com/news-release/2026/07/20/3329739/0/en/brightedge-research-google-ai-cites-facebook-in-19-5-million-answers-as-social-platforms-become-ai-discovery-sources.html', 'New data from BrightEdge shows Google AI turning to Facebook and Instagram to help answer consumer questions about local businesses, events, entertainment...');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (7, '½ Price: Connoisseur Ice Cream 1 Litre $6.50 @ Woolworths, John West Tuna 95g $1.45 @ Coles + 217 More', 'Ozbargain.com.au', '2026-07-20 09:12:08', 'https://www.ozbargain.com.au/node/968493', 'Back to half price after 10 weeks, stock up while you can. I''m a fan of the honey caramel macadamia! Catalogue Half-Price Report — 2026-07-22 Valid from Wed 22 July to Tue 28 July. Taken …');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (8, 'Food Basics Ontario: Catelli Garden Select Pasta Sauce 99 Cents for Moi Rewards Members', 'Smartcanucks.ca', '2026-07-20 03:06:47', 'https://smartcanucks.ca/food-basics-ontario-catelli-garden-select-pasta-sauce-99-cents-for-moi-rewards-members/', 'Until July the 22nd you can stock up on Catelli Garden Select Pasta Sauce at Food Basics Ontario. If you scan your Moi Rewards app at the checkout you will pay just 99 cents per jar, up to the limit of 6. For non-members and after the limit the price per jar …');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (9, 'Japanese convenience store releases Japanese convenience store-flavor fried chicken', 'SoraNews24', '2026-07-19 19:30:04', 'https://soranews24.com/2026/07/20/japanese-convenience-store-releases-japanese-convenience-store-flavor-fried-chicken/', 'Famima’s newest fried chicken and potato chip flavor is also Famima. For convenience stores in Japan, the ideal situation is to provide customers with both familiar favorites and new eating experiences. Those might seem like opposite objectives, but one way t…');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (10, 'Just how unhealthy are your favourite nostalgic seaside holiday foods? From ring donuts to 99 ice creams and fish and chips - and the snacks that are surprisingly packed full of vitamins', 'Dailymail.com', '2026-07-19 12:26:11', 'https://www.dailymail.com/travel/article-15962533/unhealthy-favourite-nostalgic-seaside-holiday-foods-snacks-surprising.html', 'From ice cream to Cornish pasties, our experts weigh in on how unhealthy everyone''s favourite British seaside treats really are - and which are the guilt-free ones you can guzzle this summer.');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (11, 'The Hidden Risk Of Foodborne Illness During Summer Travel', 'Forbes', '2026-07-19 01:25:38', 'https://www.forbes.com/sites/christopherelliott/2026/07/18/dont-eat-that-the-hidden-risk-of-foodborne-illness-during-summer-travel/', 'Travel disruptions and extreme heat are compromising the food supply chain. Here is how to protect yourself from a gastrointestinal disaster on the road.');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (12, 'Who Knew a $1 Cup of Cheese Could Make These 5 Disney World Snacks 10X Better', 'disneyfoodblog.com', '2026-07-18 23:00:09', 'https://www.disneyfoodblog.com/2026/07/18/who-knew-a-1-cup-of-cheese-could-make-these-5-disney-world-snacks-10x-better/', 'Take these five Disney World snacks to the next level with a $1 cheese upgrade!');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (13, 'Woman Opens Great Value Tortilla Chips From Walmart. Then She Spots Something Shocking: ‘Can Anyone Tell Us What This Is?’', 'BroBible', '2026-07-18 20:00:13', 'https://brobible.com/culture/article/walmart-great-value-tortilla-chips/', 'A mother’s discovery inside a bag of Great Value tortilla chips left her concerned and others online gagging. TikToker Shelby (@weightlossmama) showed off the weird-looking bonus item, which resembles Korg from Guardians of the Galaxy, rather than a salty, di…');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (14, 'The ''most compelling price'' in America revealed by retailers, with shoppers finding it hard to resist when they see it', 'Dailymail.com', '2026-07-18 15:46:23', 'https://www.dailymail.com/yourmoney/article-15979253/price-point-shoppers-love-inflation-economy.html', 'With the constant talk about high gas and grocery prices , it''s no surprise that Americans are spending less frivolously or looking for a better bang for their buck.');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (15, 'The Food Truck Owner’s Guide To SMS Marketing', 'Yeptext.com', '2026-07-18 05:14:47', 'https://blog.yeptext.com/food-truck-owners-sms/', 'Learn how food trucks can use SMS to share locations, menus, specials, and updates that drive repeat customers.');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (16, 'Free 7 Day Healthy Meal Plan (July 20-26)', 'Skinnytaste.com', '2026-07-17 18:11:00', 'https://www.skinnytaste.com/free-7-day-healthy-meal-plan-july-20-26/?adt_ei=*|EMAIL|*', 'A free 7-day, flexible weight loss meal plan including breakfast, lunch and dinner ideas and a shopping list. All recipes include macros and Weight Watchers points. Free 7 Day Healthy Meal Plan (July 20-26) Looking for a simple way to beat the heat? These let…');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (17, 'These 8 Disney World Restaurants Just Got BETTER For A Limited Time!', 'disneyfoodblog.com', '2026-07-17 15:12:10', 'https://www.disneyfoodblog.com/2026/07/17/these-8-disney-world-restaurants-just-got-better-for-a-limited-time/', 'VisitOrlando''s Magical Dining is back, and there are EIGHT Disney World area restaurants on the list!');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (18, 'Food Basics Ontario: Catelli Garden Select Pasta Sauce 99 Cents for Moi Rewards Members July 16th – 22nd', 'Smartcanucks.ca', '2026-07-17 02:24:41', 'https://smartcanucks.ca/food-basics-ontario-catelli-garden-select-pasta-sauce-99-cents-for-moi-rewards-members-july-16th-22nd/', 'Stock up on pasta sauce this week at Food Basics, where Moi Rewards members can get Catelli Garden Select pasta sauce for just 99 cents. To get the offer you can simply scan your app at checkout, and there is a limit of 6 per member. If you are not signed up …');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (19, 'General Mills recalling over 735K Pillsbury bread rolls over potential glass contamination', 'Fox Business', '2026-07-17 00:23:47', 'https://www.foxbusiness.com/lifestyle/general-mills-pulls-more-than-735k-pillsbury-rolls-shelves-possible-glass-contamination', 'The recalled products were distributed to stores across 19 states, according to the FDA.');
INSERT INTO public.news_articles (article_id, title, source, published_at, url, description) VALUES (20, 'Richmond Food News: July 16-22', 'Richmondmagazine.com', '2026-07-16 21:54:00', 'https://richmondmagazine.com/restaurants-in-richmond/food-news/july-16-22-2026/', 'A pizza residency, summer refreshers and more');


--
-- Data for Name: potato_prices; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2000, 6.14);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2001, 6.52);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2002, 8.46);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2003, 9.28);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2004, 7.23);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2005, 6.57);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2006, 16.77);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2007, 18.16);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2008, 12.08);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2009, 11.03);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2010, 15.79);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2011, 19.18);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2012, 13.00);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2013, 24.66);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2014, 15.44);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2015, 12.84);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2016, 19.01);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2017, 16.30);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2018, 16.92);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2019, 24.26);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2020, 18.08);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2021, 12.19);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2022, 23.25);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2023, 32.90);
INSERT INTO public.potato_prices (year, price_eur_per_100kg) VALUES (2024, 31.81);


--
-- Name: news_articles_article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.news_articles_article_id_seq', 21, true);


--
-- PostgreSQL database dump complete
--

\unrestrict JY3ZoFMcybtDY7tDk4elcFRtYYcJDfFiATcFC31V3uMkGoSfQkmmgwM6f8zRhfl

