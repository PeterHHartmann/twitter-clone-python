SELECT 
    u.user_name, 
    ud.display_name,
    pp.image_name AS pfp_image_name, 
    b.image_name AS banner_image_name
FROM users u, user_details ud, profile_pictures pp, banners b
WHERE NOT ud.user_name = "Tom"
AND NOT ud.user_name = "admin"
AND ud.user_name = u.user_name
AND pp.user_name = u.user_name
AND b.user_name = u.user_name
AND NOT u.user_name IN (
    SELECT f.follows_user 
    FROM follows f
    WHERE f.user_name = "Tom"
)
AND NOT u.user_email IN (
    SELECT e.user_email
    FROM email_validations e
    WHERE e.user_email = u.user_email
)
ORDER BY joined_date DESC 
LIMIT 10;