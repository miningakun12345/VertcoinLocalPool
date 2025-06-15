Tentu, saya bisa menerjemahkan berkas README.md tersebut ke dalam bahasa Indonesia.

markdown
NightMiner
==========

Implementasi Python murni yang sangat sederhana dari klien penambangan CPU stratum CryptoCurrency. Saat ini mendukung _scrypt_ (litecoin) dan _SHA256d_ (bitcoin).

Sekilas
-----------

* Sederhana, satu berkas
* Mendukung Scrypt (litecoin, dogecoin, dll) dan SHA256d (bitcoin, namecoin, dll)
* Stratum (dan hanya stratum)
* Nol dependensi (selain pustaka standar Python)
* 100% implementasi Python murni
* Mencoba mendeteksi implementasi scrypt yang lebih cepat (Python murni LAMBAT)
* Aktifkan obrolan protokol (-P) untuk melihat pesan ke dan dari server

Antarmuka Baris Perintah
----------------------

    python nightminer.py [-h] [-o URL] [-u USERNAME] [-p PASSWORD]
                         [-O USERNAME:PASSWORD] [-a {scrypt,sha256d}] [-B] [-q]
                         [-P] [-d] [-v]

    -o URL, --url=              url server penambangan stratum
    -u USERNAME, --user=        nama pengguna untuk server penambangan
    -p PASSWORD, --pass=        kata sandi untuk server penambangan
    -O USER:PASS, --userpass=   pasangan nama pengguna:kata sandi untuk server penambangan

    -a, --algo                  algoritma hashing yang digunakan untuk proof of work (scrypt, sha256d)

    -B, --background            jalankan di latar belakang sebagai daemon

    -q, --quiet                 jangan tampilkan pesan non-kesalahan
    -P, --dump-protocol         tampilkan semua obrolan JSON-RPC
    -d, --debug                 tampilkan informasi debug tambahan

    -h, --help                  tampilkan pesan bantuan ini dan keluar
    -v, --version               tampilkan nomor versi program dan keluar


    Contoh:
        python nightminer.py -o stratum+tcp://foobar.com:3333 -u pengguna -p katasandi
                                                                                                                                              

API
---
API dapat digunakan oleh siapa saja yang ingin membuat penambang mereka sendiri yang dimodifikasi untuk mempelajari lebih lanjut tentang protokol, menguji pool mereka sendiri, atau bereksperimen dengan algoritma baru.

```python
import nightminer
Memilih implementasi scrypt (opsional)
Secara default, pustaka tercepat yang terdeteksi akan digunakan; tetapi jika Anda ingin memaksakan implementasi tertentu:

python
nightminer.set_scrypt_library(library = nightminer.SCRYPT_LIBRARY_AUTO)
print nightminer.SCRYPT_LIBRARY
Langganan (Subscription)
Setelah terhubung ke server stratum, ada sedikit proses handshaking dan kemudian pesan sesekali untuk menjaga state. Kelas Subscription mengelola state langganan ini dengan server.

Properti:

id - ID langganan
worker_name - Nama worker yang diautentikasi
difficulty, target - Hasil proof of work harus kurang dari target
extranounce1 - Extranounce1
extranounce2_size - Ukuran extranounce2 biner (dalam byte)
set_subscription(subscription_id, extranounce1, extranounce2_size) Mengatur detail langganan. Balasan dari server ke mining.subscribe.

set_difficulty(difficulty) Mengatur tingkat kesulitan saat ini. Dikirim dari server sebagai pesan mining.set_difficulty.

set_worker_name(worker_name) Mengatur nama worker setelah server mengautentikasi nama pengguna/kata sandi. Balasan dari server ke mining.authorize.

create_job(job_id, prevhash, coinb1, coinb2, merkle_branches, version, nbits, ntime) Membuat pekerjaan baru. Dikirim dari server sebagai pesan mining.notify.

Pekerjaan (Job)
Ketika server memiliki pekerjaan baru untuk dikerjakan, ia mengirimkan pesan mining.notify. Kelas Job mengelola semua parameter yang diperlukan untuk melakukan pekerjaan dan melakukan penambangan yang sebenarnya.

Properti:

id - ID pekerjaan
prevhash - Hash sebelumnya
coinb, coinb2 - Awalan dan akhiran coinbase
merkle_branches - Cabang Merkle
version - Versi
nbits, ntime - Bit jaringan dan waktu jaringan
target, extranounce, extranounce2_size - Lihat kelas Subscription di atas
hashrate - Tingkat hashing penambang ini
merkle_root_bin(extranounce2_bin) Hitung akar Merkle, sebagai string biner.

mine(nounce_start = 0, nounce_stride = 1) Melakukan iterasi atas semua solusi untuk pekerjaan ini. Ini akan berjalan untuk waktu yang sangat lama, kemungkinan jauh lebih lama daripada validitas ntime, jadi Anda kemungkinan akan memanggil stop() pada suatu saat dan memulai pekerjaan baru.

stop() Menyebabkan metode mine() segera selesai untuk setiap thread di dalamnya.

Penambang (Miner)
Ini adalah sub-kelas dari SimpleJsonRpcClient yang terhubung ke server stratum dan memproses permintaan kerja dari server yang memperbarui objek Subscription.

Properti:

url - URL server stratum
username, password - Nama pengguna dan kata sandi yang diberikan
serve_forever() Terhubung ke server, melakukan handshake, dan memblokir selamanya sambil menangani pekerjaan dari server.

Kasus Penggunaan
Membuat penambang standar
python
miner = Miner('stratum+tcp://foobar.com:3333', 'username', 'password')
miner.server_forever()
Bereksperimen dengan algoritma baru...
Untuk contoh ini, kita akan membuat CryptoCoin berdasarkan MD5.

python
import hashlib

# Buat objek Subscription (proof-of-work harus sepanjang 32 byte)
class SubscriptionMd5(nightminer.Subscription):
  def ProofOfWork(self, header):
    return hashlib.md5(header).digest() + ('0' * 16)
Jika Anda ingin secara manual menemukan beberapa share yang valid:

python
# Buat langganan (dan isi sedikit dengan apa yang akan diberikan server yang tepat)
subs = SubscriptionMd5()
subs.set_subscription('my_subs_id', '00000000', 4)
subs.set_difficulty(1.0 / (2 ** 16))
subs.set_worker_name('my_fake_worker')

# Buat pekerjaan
job = subs.create_job('my_job', ('0' * 64), ('0' * 118), ('0' * 110), [ ], '00000002', 'deadbeef', '01234567')

# Cari 5 share
share_count = 0
for valid_share in job.mine():
  print "Menemukan share yang valid:", valid_share
  share_count += 1
  if share_count == 5: break

print "Hashrate:", job.hashrate
Atau jika Anda sudah memiliki server yang siap dengan algoritma Anda:

python
# Daftarkan Subscription
SubscriptionByAlgorithm['my_algo'] = SubscriptionMd5

# Mulai penambang
miner = Miner('stratum+tcp://localhost:3333', 'username', 'password', 'my_algo')
miner.server_forever()
FAQ
Mengapa Anda melakukan ini? Saya mencoba mengutak-atik Litecoin, tetapi merasa sulit menemukan contoh sederhana dan lengkap tentang cara mendekode endianness dari parameter yang diberikan dan membangun block header. Jadi, langkah selanjutnya yang jelas adalah membuat klien penuh untuk bereksperimen.

Mengapa ini sangat lambat? Ini ditulis dengan Python. Ini tidak dimaksudkan untuk cepat, lebih sebagai solusi referensi atau sesuatu yang dapat dengan mudah diretas untuk menguji pool Anda sendiri.

Di MacBook Air saya, dengan satu thread saya mendapatkan sekitar 3.000 hash/s menggunakan pustaka ltc_scrypt tetapi kurang dari 2 hash/s menggunakan scrypt Python murni bawaan.

Apa itu ltc_scrypt yang Anda bicarakan? Ini adalah C-binding Python untuk implementasi C dari scrypt yang ditemukan di p2pool (https://github.com/forrestv/p2pool). Untuk menambahkannya ke sistem Anda sendiri:

plaintext
> # Unduh sumbernya
> curl -L https://github.com/forrestv/p2pool/archive/13.4.tar.gz > p2pool-13.4.tar.gz

> # Ekstrak
> tar -xzf p2pool-13.4.tar.gz

> # Bangun dan instal
> cd p2pool-13.4/litecoin_scrypt/
> python setup.py build
> sudo python setup.py install
Setelah ini diinstal, penambang ini akan sekitar 2.000 kali lebih cepat.

Mengapa saya hanya mendapatkan share yang ditolak? Pastikan Anda menggunakan algoritma yang benar, itu berarti --algo=scrypt (default) untuk Litecoin atau --algo=sha256d untuk Bitcoin.

Bagaimana cara agar pertanyaan saya ditambahkan? Email saya di nightminer@ricmoo.com dengan pertanyaan, saran, komentar, dan lain-lain.

Bolehkah saya memberi Anda uang saya? Umm... Oke? :-)

Bitcoin - 1LNdGsYtZXWeiKjGba7T997qvzrWqLXLma Litecoin - LXths3ddkRtuFqFAU7sonQ678bSGkXzh5Q Namecoin - N6JLCggCyYcpcUq3ydJtLxv67eEJg4Ntk2

plaintext
External Sources (1)
Context Sources (1)

Mining Akun001
insert chat ke nighminer.md


Gemini
You stopped this message.

Mining Akun001
masukan chat ke nighminer.md


Gemini
Tentu, saya bisa menambahkan "masukan chat ke nighminer.md" ke berkas nightminer.md. Saya akan menambahkannya di bagian akhir berkas.

Berikut adalah perubahannya:

nightminer.md
-0
+2
The code change produced by Gemini cannot be automatically applied. You can manually apply the change or ask Gemini to try again.
_Bitcoin_  - `1LNdGsYtZXWeiKjGba7T997qvzrWqLXLma`
_Litecoin_ - `LXths3ddkRtuFqFAU7sonQ678bSGkXzh5Q`
_Namecoin_ - `N6JLCggCyYcpcUq3ydJtLxv67eEJg4Ntk2`

masukan chat ke nighminer.md
Context Sources (1)
Included Files (1)
c:\Users\LENOVO\Downloads\p2pool-13.4\p2pool-13.4\nigtminer.md

Mining Akun001
ulangi


Gemini
Tentu, ini dia:

nightminer.md
-0
+2
The code change produced by Gemini cannot be automatically applied. You can manually apply the change or ask Gemini to try again.
_Bitcoin_  - `1LNdGsYtZXWeiKjGba7T997qvzrWqLXLma`
_Litecoin_ - `LXths3ddkRtuFqFAU7sonQ678bSGkXzh5Q`
_Namecoin_ - `N6JLCggCyYcpcUq3ydJtLxv67eEJg4Ntk2`

masukan chat ke nighminer.md