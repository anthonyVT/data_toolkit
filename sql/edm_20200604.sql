SELECT
    u.name,
    u.email
FROM
    users AS u
WHERE
    lastlogin_at > unix_timestamp('2019-12-01')
    AND lastlogin_at < unix_timestamp('2020-06-01')
    AND u.id NOT IN (
        SELECT
            DISTINCT userid
        FROM
            courses_users_package
    )