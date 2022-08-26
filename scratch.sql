SELECT 
    g.id, 
    g.title,
    AVG(r.rating) AS AvgRating
FROM raterapp_game g
JOIN raterapp_rating r ON r.game_id = g.id
GROUP BY r.game_id
ORDER BY AvgRating DESC
LIMIT 5;

SELECT 
    g.id, 
    g.title,
    COUNT(r.id) AS TimesRated
FROM raterapp_game g
JOIN raterapp_rating r ON r.game_id = g.id
GROUP BY r.game_id
ORDER BY TimesRated DESC
LIMIT 1;

SELECT 
    u.first_name|| ' ' || u.last_name AS Name,
    COUNT(r.id) AS TimesReviewed
FROM raterapp_review r 
JOIN raterapp_player p ON p.id = r.player_id
JOIN auth_user u ON u.id = p.user_id
GROUP BY r.player_id
ORDER BY TimesReviewed DESC
LIMIT 3;

SELECT 
    c.id,
    c.name,
    COUNT(g.id) AS number
FROM raterapp_game g
JOIN raterapp_gamecategories gc ON gc.game_id = g.id
JOIN raterapp_category c ON c.id = gc.category_id
GROUP BY gc.category_id
ORDER BY c.name;


SELECT 
    g.id,
    g.title,
    g.number_of_players
FROM raterapp_game g
WHERE g.number_of_players > 5;


WITH NoPic AS (
    SELECT
        u.id,
        u.first_name|| ' ' || u.last_name AS Name,
        COUNT(g.player_id) AS GamesFromPlayer
    FROM raterapp_game g
    JOIN raterapp_player p ON p.id = g.player_id
    JOIN auth_user u ON u.id = p.user_id
    GROUP BY player_id
    )

SELECT 
    Name
FROM Most
WHERE GamesFromPlayer = (
    SELECT
        MAX(GamesFromPlayer)
    FROM Most
);

SELECT 
    g.id,
    g.title,
    g.rec_age
FROM raterapp_game g
WHERE g.rec_age < 8;


WITH NoPic AS (
    SELECT 
        g.id,
        g.title,
        COUNT(p.id) AS num
    FROM raterapp_game g
    LEFT JOIN raterapp_picture p ON p.game_id = g.id
    GROUP BY g.id
    )

SELECT 
    COUNT(*)
FROM NoPic
WHERE num = 0;
