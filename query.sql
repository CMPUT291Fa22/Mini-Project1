SELECT playlists.pid, plinclude.sid
FROM playlists, plinclude
WHERE playlists.pid = plinclude.pid