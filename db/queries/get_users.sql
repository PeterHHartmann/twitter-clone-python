SELECT 
    user_details.user_name, 
    user_details.display_name,
    profile_pictures.image_name AS pfp_image_name, 
    banners.image_name AS banner_image_name,
    users.user_email
FROM user_details 
JOIN profile_pictures ON profile_pictures.user_name = user_details.user_name
JOIN banners ON banners.user_name = user_details.user_name
JOIN users ON users.user_name = user_details.user_name
LEFT JOIN email_validations ON email_validations.user_email = users.user_email
WHERE NOT user_details.user_name="Tom"
AND NOT user_details.user_name="admin"
AND email_validations.user_email IS NULL
ORDER BY joined_date DESC 
LIMIT 10;

SELECT * FROM follows;

SELECT u.user_name
FROM users u
LEFT JOIN follows f
ON f.user_name = u.user_name
WHERE NOT u.user_name IN (
    SELECT ff.follows_user
    FROM users uu
    LEFT JOIN follows ff
    ON ff.user_name = uu.user_name
    WHERE uu.user_name = "barackobama"
);



-- WHERE NOT u.user_name = "barackobama";
