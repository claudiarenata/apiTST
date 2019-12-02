# Tugas Besar TST

Spy - Cari Video dan Lagu Kesukaanmu. Aplikasi ini memungkinkan user untuk membuat playlist yang terdiri atas beberapa lagu kesukaan user. Tiap lagu bisa dimunculkan video youtube terkait dan lagu yang akan didengarkan lewat spotify. 

## API Usage 

1. Youtube API - Claudia Renata Maharani 18217048 
2. Spotify API - Zalikha Adiera Gambetta 18217027



## Akses Aplikasi 

``` 
http://54.164.251.124:6004 

```
## Cara Menggunakan Aplikasi 
1. Klik daftar Playlist di menu Search Playlist untuk menampilkan playlist yang sudah pernah dibuat
2. Ketik nama playlist yang ingin dilihat isinya pada kolom search 
3. Klik button youtube atau spotify untuk melihat lagu maupun video 
4. Untuk membuat Playlist baru, klik menu add Playlist, tuliskan nama playlist yang diinginkan
5. Klik Add More untuk menambahkan lagu dan penyanyi yang diinginkan
6. Klik Submit untuk menambah playlist baru 


## Dokumentasi API 
| Method | Deskripsi | Akses|
| :---: | :---: | :---: |
GET |Menampilkan informasi video berdasarkan keyword ​ tertentu | http://54.164.251.124:6003/api/youtubesearch?=keyword 
GET| Menampilkan nama ​playlist| http://54.164.251.124:6003/api/allplaylist
GET| Menampilkan seluruh lagu dalam ​playlist | http://54.164.251.124:6003/api/playlist?playlistName= 
POST | Menambahkan ​playlist ​ ke dalam ​database |http://54.164.251.124:6003/api/playlist 
