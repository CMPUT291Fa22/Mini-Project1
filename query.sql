SELECT *
FROM artists, songs, perform
WHERE songs.title = "Let Me Love You"
AND artists.aid = perform.aid
AND perform.sid = songs.sid