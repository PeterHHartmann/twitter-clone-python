SELECT 
    t.tweet_id, 
    t.tweet_text, 
    t.tweet_timestamp,
    ti.image_name,
    ud.user_name,
    ud.display_name, 
    pp.image_name AS pfp_image_name
FROM 
    tweets t
JOIN user_details ud ON ud.user_name = t.user_name
LEFT JOIN profile_pictures pp ON pp.user_name = t.user_name
LEFT JOIN tweet_images ti ON ti.tweet_id = t.tweet_id
WHERE t.user_name = "Tom"
ORDER BY t.tweet_timestamp DESC
LIMIT 10;