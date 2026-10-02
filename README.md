# Portfolio Website - Tugas 1, 2, 3, 4 & 5 PBP

Nama: Michelle Yuyun Margarethy Aritonang

NPM: 2506656961

Kelas: PBP C

## Deskripsi Proyek

Website portofolio pribadi yang dibuat sebagai bagian dari mata kuliah Pemrograman Berbasis Platform. Website ini menampilkan informasi pribadi, profil singkat, pendidikan, pengalaman organisasi/kepanitiaan, skills, serta projects yang pernah dikerjakan.

Pada Tugas 1, website dibuat menggunakan HTML5 dan CSS3 dengan desain responsive. Pada Tugas 2, website dikembangkan menggunakan Django dengan menambahkan bagian Projects yang datanya disimpan di database dan ditampilkan secara dinamis. Pada Tugas 3, website dikembangkan lebih lanjut dengan menambahkan penggunaan ModelForm, fitur pengelolaan data Experience, flash messages, serta penyediaan data dalam format JSON dan XML.

## Teknologi yang Dipakai

- HTML5
- CSS3
- Python
- Django
- Git & GitHub

## Fitur Website

- About Me / Profile
- Education
- Experience / Organizational Activities
- Programming Skills
- Software Skills
- Projects dengan data yang disimpan di database
- Menambahkan data Experience melalui form
- Mengubah data Experience melalui form
- Menghapus data Experience
- Flash messages untuk memberikan notifikasi setelah pengelolaan data
- Penyediaan data Experience dalam format JSON
- Penyediaan data Projects dalam format JSON dan XML
- Responsive layout
- Link menuju GitHub, LinkedIn, dan Email
- Navigasi antar halaman menggunakan Django URL

## Setup / Instalasi

Untuk menjalankan website secara lokal:

1. Clone repository GitHub.
2. Masuk ke folder project.
3. Buat dan aktifkan virtual environment.
4. Install dependencies yang diperlukan.
5. Jalankan migration database.
6. Jalankan Django development server.
7. Buka website melalui browser pada alamat `http://127.0.0.1:8000/`.

Perintah utama yang digunakan:

```bash
python manage.py migrate
python manage.py runserver
```

---

## Tugas 1

### Pertanyaan Reflektif

#### 1. Penggunaan Elemen Semantik HTML5

Pada perancangan struktur HTML website portofolio ini, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>`. Elemen-elemen tersebut membantu saya mengorganisasi struktur halaman berdasarkan fungsi dan kontennya. Misalnya, `<header>` digunakan untuk bagian navigasi, `<main>` menjadi bagian utama website, `<section>` digunakan untuk mengelompokkan bagian seperti About Me, Education, dan Skills, sedangkan `<article>` digunakan untuk setiap informasi pendidikan dan pengalaman yang berdiri sebagai satu kesatuan.

Penggunaan elemen semantik membuat struktur HTML lebih terorganisasi, mudah dibaca, dan lebih mudah dikembangkan ketika website bertambah kompleks. Selain itu, struktur tersebut membantu saya memahami hubungan antara struktur konten HTML dengan tampilan yang kemudian diatur menggunakan CSS.

#### 2. Tantangan Desain Responsive

Tantangan utama ketika membuat website responsive adalah memastikan tata letak dan ukuran elemen tetap nyaman digunakan pada berbagai ukuran layar. Pada tampilan desktop, informasi dapat ditampilkan dalam beberapa kolom, seperti bagian About Me dan foto profil yang diletakkan berdampingan serta Education dan Skills yang ditampilkan dalam dua kolom.

Namun, pada ukuran layar yang lebih kecil, tata letak tersebut dapat menjadi terlalu sempit dan menyebabkan teks atau elemen visual terlihat tidak nyaman. Untuk mengatasinya, saya menggunakan media query pada CSS untuk mengubah beberapa layout menjadi satu kolom dan menyesuaikan ukuran font serta spacing agar website tetap mudah dibaca pada perangkat dengan ukuran layar yang berbeda.

#### 3. Rencana Pengembangan Fitur

Jika diberikan kesempatan untuk mengembangkan website portofolio ini lebih lanjut, saya ingin menambahkan beberapa fitur seperti halaman detail untuk setiap project, filter berdasarkan kategori project atau pengalaman, serta form untuk menambahkan data secara dinamis.

Pengembangan tersebut akan membuat website tidak hanya berfungsi sebagai halaman portofolio statis, tetapi juga dapat digunakan untuk mengelola dan menampilkan informasi secara lebih dinamis.

---

## Tugas 2

### Pertanyaan Reflektif

#### 1. Implementasi MVT pada Website

Pada Tugas 2, saya menggunakan konsep Model-View-Template (MVT) pada Django. Model digunakan untuk mendefinisikan struktur data yang disimpan di database, View digunakan untuk mengatur logika aplikasi dan mengambil data dari database, sedangkan Template digunakan untuk menampilkan data kepada pengguna.

Pada website portofolio ini, model `Project` digunakan untuk menyimpan informasi project seperti judul, deskripsi, teknologi yang digunakan, dan URL project. View kemudian mengambil data tersebut dan mengirimkannya ke template `projects.html` untuk ditampilkan pada halaman website.

#### 2. Peran Model dalam Penyimpanan Data

Model Django membantu saya mendefinisikan struktur data dengan lebih teratur. Setiap field pada model memiliki tipe data dan aturan tertentu, seperti `CharField` untuk teks pendek, `TextField` untuk deskripsi, dan `URLField` untuk URL project.

Dengan menggunakan model, data project dapat disimpan di database sehingga informasi tidak perlu ditulis secara langsung di dalam file HTML. Hal ini membuat website lebih mudah dikembangkan karena data dapat ditambah atau diubah tanpa harus mengubah struktur HTML secara manual.

#### 3. Perbedaan Makemigrations dan Migrate

`makemigrations` digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada model Django. File tersebut berisi instruksi mengenai perubahan struktur database yang perlu diterapkan.

Sementara itu, `migrate` digunakan untuk menerapkan migration tersebut ke database. Jadi, `makemigrations` dapat dianggap sebagai proses membuat catatan perubahan struktur database, sedangkan `migrate` menjalankan perubahan tersebut pada database.

Contoh perintah yang digunakan:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Tugas 3

### Pertanyaan Reflektif

#### 1. Mengapa Menggunakan ModelForm Dibandingkan Membuat Form HTML Secara Manual? Apa Keuntungan Menggunakan ModelForm?

Saya menggunakan `ModelForm` karena form dapat dibuat berdasarkan model Django yang sudah ada. Dengan `ModelForm`, field pada form dapat disesuaikan dengan field yang terdapat pada model tanpa perlu membuat setiap input HTML secara manual.

Keuntungan lainnya adalah validasi dasar dari field model dapat digunakan kembali oleh form. Hal ini membantu mengurangi kode yang perlu ditulis dan membuat proses pengelolaan data menjadi lebih terstruktur.

Pada Tugas 3, saya menggunakan `ExperienceForm` yang dibuat berdasarkan model `Experience`. Form tersebut digunakan untuk menambahkan dan mengubah data pengalaman.

#### Mengapa Kita Perlu Menggunakan `{% csrf_token %}` pada Form Django?

`{% csrf_token %}` digunakan untuk memberikan perlindungan terhadap serangan Cross-Site Request Forgery (CSRF). Token tersebut memastikan bahwa request POST yang dikirim melalui form berasal dari halaman aplikasi yang valid.

Karena form yang digunakan untuk membuat, mengubah, dan menghapus data menggunakan method POST, maka `{% csrf_token %}` diperlukan agar Django dapat memverifikasi request tersebut.

#### 2. Mengapa JSON Lebih Populer Digunakan untuk Pertukaran Data Dibandingkan XML?

JSON banyak digunakan untuk pertukaran data karena struktur sintaksnya relatif sederhana dan mudah dibaca oleh manusia maupun program. JSON juga memiliki struktur yang dekat dengan struktur data yang umum digunakan dalam pemrograman, seperti object dan array.

Dibandingkan XML, JSON memiliki format yang lebih ringkas karena tidak membutuhkan tag pembuka dan penutup untuk setiap data. Hal tersebut membuat JSON lebih praktis digunakan untuk pertukaran data antara aplikasi atau API.

Namun, XML juga memiliki kelebihan tertentu, seperti kemampuan menggunakan atribut dan struktur dokumen yang lebih kompleks. Oleh karena itu, penggunaan JSON atau XML tetap bergantung pada kebutuhan aplikasi.

#### 3. Jelaskan Fungsi dari View yang Mengembalikan Data dalam Format JSON

View yang mengembalikan data dalam format JSON digunakan untuk menyediakan data dari database agar dapat diakses dalam format yang dapat dipertukarkan oleh aplikasi.

Pada implementasi Tugas 3, prosesnya dimulai dengan mengambil data `Experience` dari database menggunakan:

```python
Experience.objects.all()
```

Data tersebut kemudian diubah menjadi JSON menggunakan serializer Django:

```python
serializers.serialize("json", raw_data)
```

Setelah menjadi JSON, data tersebut kemudian di-deserialize kembali untuk digunakan pada halaman `experience.html`:

```python
experience_list = [
    item.object
    for item in serializers.deserialize("json", data_json)
]
```

Hasil deserialisasi tersebut kemudian dikirim melalui context ke template agar data pengalaman dapat ditampilkan pada halaman website.

Serializer diperlukan karena objek QuerySet Django tidak dapat langsung dikirim dalam format JSON. Serializer mengubah objek atau QuerySet Django menjadi format data yang dapat direpresentasikan sebagai JSON. Sebaliknya, deserializer digunakan untuk mengubah kembali data JSON menjadi objek Django yang dapat digunakan oleh aplikasi.

---

## AI Disclosure

Dalam pengerjaan Tugas 1, Tugas 2, dan Tugas 3, saya menggunakan ChatGPT sebagai alat bantu dalam proses pembelajaran dan pengembangan website.

### Penggunaan AI

ChatGPT digunakan untuk memberikan saran, alternatif implementasi, membantu memahami konsep Django, serta membantu melakukan pengecekan terhadap struktur kode dan requirement tugas. Saya tidak menggunakan AI untuk menggantikan seluruh proses pengerjaan, melainkan menggunakan hasil diskusi sebagai referensi yang kemudian saya sesuaikan dengan kebutuhan project.

### Strategi Prompting

Saya memberikan konteks mengenai struktur project, requirement tugas, kode yang sedang digunakan, serta error yang ditemukan. Setelah mendapatkan penjelasan atau alternatif solusi, saya memeriksa kembali hasilnya dan menyesuaikannya dengan implementasi project saya.

### Bagian yang Dibantu AI

Beberapa bagian yang dibantu melalui diskusi dengan AI antara lain:

- Memahami struktur HTML5 dan penggunaan semantic elements pada Tugas 1.
- Mendapatkan saran mengenai responsive design menggunakan CSS.
- Memahami konsep MVT pada Django.
- Memahami penggunaan Model, View, dan Template.
- Membantu memahami migration dan database Django.
- Membantu memahami penggunaan ModelForm pada Tugas 3.
- Membantu memahami proses serialization dan deserialization JSON.
- Membantu mengecek struktur URL, view, form, dan template.
- Membantu mencari penyebab error berdasarkan pesan yang muncul pada terminal.

### Verifikasi Hasil AI

Setiap saran dari AI tetap saya periksa dan sesuaikan dengan requirement tugas serta struktur project yang saya gunakan. Saya juga melakukan perubahan pada kode dan menguji website secara langsung untuk memastikan fitur dapat berjalan sesuai kebutuhan.

### Chat/Log Penggunaan AI

Percakapan dengan AI digunakan sebagai dokumentasi proses diskusi selama pengerjaan tugas. Penggunaan AI terutama dilakukan untuk memahami konsep, mencari alternatif solusi, dan melakukan debugging ketika menemukan masalah dalam implementasi.

---

## Weekly Progress

### Week 1

Membuat website portofolio statis menggunakan HTML5 dan CSS3. Pada tahap ini saya membuat struktur halaman, navigation bar, bagian About Me, Education, Skills, Experience, serta menyesuaikan tampilan website agar responsive pada berbagai ukuran layar.

### Week 2

Mengimplementasikan Django dan konsep MVT. Data project mulai disimpan menggunakan database melalui model Django. Saya juga membuat halaman Projects yang mengambil data dari database serta mengimplementasikan routing dan template inheritance.

### Week 3

Menambahkan fitur pengelolaan data menggunakan ModelForm. Pada bagian Experience, pengguna dapat menambahkan, mengubah, dan menghapus data pengalaman melalui form. Saya juga mengimplementasikan penyediaan data dalam format JSON serta proses serialization dan deserialization untuk menampilkan data pada halaman Experience.

---

## Tutorial 04: Autentikasi, Session, dan Cookie

Implementasi memakai `User` bawaan Django, `UserCreationForm` untuk registrasi,
serta `AuthenticationForm(request, data=...)` untuk login. Registrasi menyimpan
password dalam bentuk hash, menampilkan error validasi, dan mengarahkan pengguna
ke login dengan pesan sukses. Registrasi tidak langsung login dan tidak memberi
hak staff, Editor, atau superuser. Nama pemilik portofolio tetap Michelle Yuyun
Margarethy Aritonang; username di navbar adalah akun pengunjung yang sedang login.

`login()` membuat session Django. Cookie `sessionid` mengidentifikasi session di
server; cookie `last_login` hanya menampilkan waktu login dalam zona Asia/Jakarta,
bukan sumber hak akses. Cookie ini menggunakan `HttpOnly` dan `SameSite=Lax`.
Logout memakai form **POST dengan CSRF**, mengakhiri session, menghapus
`last_login`, lalu kembali ke profil. GET `/logout/` menghasilkan 405 dan tidak
mengubah session. Ini penyesuaian keamanan terhadap contoh tautan GET di tutorial.

Semua form mutasi memakai `{% csrf_token %}` dan `CsrfViewMiddleware` tetap aktif.
Form kosong maupun kredensial salah menampilkan error. Tidak ada `csrf_exempt`
dan tidak ada AJAX tambahan karena aplikasi memakai form HTML biasa.

Project tetap dapat dibaca publik dan dicari berdasarkan judul. Create/delete
Project hanya untuk superuser: pengunjung diarahkan ke `/login/`, pengguna biasa
maupun Editor mendapat 403. Tombol create/delete hanya tampil untuk superuser.
Semua pengguna login dapat Star/Unstar melalui POST; satu pengguna maksimal satu
star per Project. GET endpoint star menghasilkan 405 bagi pengguna login.

`/api/projects/`, `/json/`, `/json/<uuid>/`, `/xml/`, dan `/xml/<uuid>/` tetap
tersedia. Relasi star memakai natural key User, sehingga JSON menampilkan
`[["username"]]`, bukan ID database pengguna. Password dan data session tidak
ikut diserialisasi. Username pemberi star merupakan informasi publik.

### Hasil audit Tutorial 04

- Sudah tersedia: konfigurasi auth/session/messages/CSRF, form auth bawaan,
  navbar, last_login, otorisasi Project, relasi star, dan API Project utama.
- Diperbaiki: logout via GET, POST kosong yang sebelumnya tidak menampilkan error,
  error form Project yang tidak dirender, serta ID User numerik pada API lama.
- Konfigurasi secret dipindahkan dari kode ke environment; wildcard host dihapus.
- `.gitignore` dilengkapi `.venv/` dan `.env*`. Tidak ada `.env`, database,
  virtualenv, bytecode, atau hasil collectstatic yang dilacak pada hasil audit.
- Skrip Selenium kini memvalidasi akun uji yang sudah ada, tanpa membuat,
  mengganti password, atau mempromosikan akun secara otomatis.

## Tugas 4: Hak Akses Experience

Model pilihan dari Tugas 3 adalah **Experience**. Relasi
`starred_by = ManyToManyField(User, related_name="starred_experiences", blank=True)`
dan migrasi `0004_experience_starred_by` sudah ada di working tree saat audit dan
sudah diterapkan pada database lokal. Perubahan tersebut dipertahankan dan
kemudian di-commit bersama backend; tidak dibuat migrasi duplikat.

| Peran | Baca | Star/Unstar | Create | Edit | Delete |
| --- | --- | --- | --- | --- | --- |
| Pengunjung | Ya | Login dahulu | Login dahulu | Login dahulu | Login dahulu |
| Pengguna biasa | Ya | Ya | 403 | 403 | 403 |
| Editor | Ya | Ya | 403 | Ya | 403 |
| Superuser | Ya | Ya | Ya | Ya | Ya |

`@login_required` memeriksa autentikasi sebelum pemeriksaan role. Helper
`is_editor(user)` memeriksa keanggotaan **Group bernama persis `Editor`**; username
atau atribut staff saja tidak cukup. Editor pada aplikasi ini boleh mengedit
Experience, tetapi tidak diberi hak pemilik pada Project. Semua pemeriksaan
berlaku di view, termasuk jika URL diakses langsung.

Template menampilkan create/delete hanya untuk superuser dan edit untuk
superuser atau Editor. Form star tetap dapat dilihat pengunjung, tetapi POST-nya
akan diarahkan ke login. Setelah login, pengguna kembali ke profil dan dapat
membuka Experience untuk memberi star; aksi POST tidak diulang otomatis.

Endpoint `experience/<uuid>/star/` hanya menerima POST untuk pengguna login.
Tombol menampilkan Star/Unstar, jumlah star, dan status aksesibilitas
`aria-pressed`. Relasi ManyToMany mencegah pasangan pengguna/Experience ganda.
Create/edit memvalidasi `ExperienceForm`; delete hanya menghapus pada POST.
GET delete tidak menghapus data.

API publik `/api/experience/` dan `/api/experience/<uuid>/` tetap memakai format
serializer Django dan `use_natural_foreign_keys=True`. Field Experience lama
tetap tersedia; `starred_by` berisi natural key username. Alur
serialization/deserialization halaman dari Tugas 3 tetap dipertahankan.

### Setup lokal dan migrasi

Dari direktori yang berisi `manage.py`:

```bash
python -m venv env
source env/bin/activate  # macOS/Linux; Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

CSS berada di `main/static/css/style.css` dan ditemukan melalui app static
finder. Tidak perlu menambahkan direktori yang sama ke `STATICFILES_DIRS`.
Untuk deployment, jalankan `python manage.py collectstatic --noinput` setelah
perubahan CSS; hasil `staticfiles/` tidak boleh di-commit. Jika browser masih
menampilkan stylesheet lama, lakukan hard refresh.

Konfigurasi menggunakan environment proses:

- `DJANGO_DEBUG` default `true` untuk pengembangan lokal; set `false` saat deploy.
- `DJANGO_SECRET_KEY`: gunakan secret acak yang stabil di environment deployment.
  Saat debug mati, server menolak startup jika nilai ini tidak disediakan.
- Tanpa secret pada mode lokal, Django menggunakan secret acak per proses,
  sehingga session lama tidak bertahan setelah restart. Untuk session lokal yang
  stabil selama terminal yang sama, jalankan sebelum server:

```bash
export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
```

Settings aplikasi tidak otomatis membaca `.env`; gunakan environment terminal
atau konfigurasi platform deployment. `.env` hanya dibaca skrip Selenium.
Pada deployment HTTPS (`DJANGO_DEBUG=false`), session dan CSRF cookie memakai
`Secure`. Host localhost dan domain PWS proyek tetap diizinkan secara eksplisit.
Secret lama pernah berada di kode Git; penghapusan dari settings tidak menghapus
riwayat. Gunakan secret baru di deployment, jangan gunakan kembali nilai lama.

### Menetapkan Editor melalui Django Admin

1. Jalankan `python manage.py createsuperuser` jika belum memiliki akun pemilik,
   lalu `python manage.py runserver`.
2. Login ke `http://127.0.0.1:8000/admin/` dengan superuser.
3. Pada **Authentication and Authorization → Groups**, buat grup **Editor**
   jika belum ada. Simpan; tidak perlu memberi izin create/delete.
4. Buka **Users**, pilih akun pengguna biasa, tambahkan grup **Editor**, dan simpan.
5. Login sebagai akun tersebut pada aplikasi. Pastikan Edit Experience tampil,
   sedangkan Tambah/Hapus tidak tampil dan akses langsung create/delete mendapat 403.

Keanggotaan grup ini diperiksa oleh aplikasi portofolio. Akun Editor tidak perlu
`is_staff` atau akses Django Admin. Jangan otomatis menambahkan akun registrasi
ke grup atau mengubahnya menjadi superuser. Audit tidak mengubah role akun lokal.

### Pengujian

```bash
python manage.py check
python manage.py test
python manage.py showmigrations
python manage.py makemigrations --check --dry-run
```

27 tes Django mencakup tes lama, registrasi/hash password, invalid form, login,
navbar, session, last_login, logout, empat role Experience, perubahan data,
star/unstar dan duplikasi, template sesuai role, API JSON/XML lama, serta CSRF
menggunakan `Client(enforce_csrf_checks=True)`. Setiap tes memakai database tes
terpisah, bukan menghapus data portofolio lokal.

Audit menjalankan tes pada virtualenv yang terpasang (Django 6.1) dan salinan
sementara Django 5.2 sesuai `requirements.txt`; virtualenv pengguna tidak diganti.
Semua migrasi hingga `main.0004` sudah diterapkan dan tidak ada perubahan model
yang memerlukan migrasi tambahan.

Selenium bersifat opsional. Untuk mengulang pengujian lokal:

```bash
pip install selenium python-dotenv
python manage.py runserver 127.0.0.1:8000
# Pada terminal kedua, dengan virtualenv aktif:
python test_e2e.py --headless
```

Siapkan Chrome serta akun lokal `burhan_test` (biasa, tanpa grup) dan `admin_test`
(superuser) secara eksplisit. Isi `.env` lokal dengan `E2E_USER_PASSWORD` dan
`E2E_ADMIN_PASSWORD` yang cocok; jangan commit atau membagikan nilainya. Skrip
berhenti jika akun/password/peran tidak cocok dan hanya menargetkan
`http://127.0.0.1:8000`. Selenium memverifikasi CSRF form, login/cookie, penolakan
Project untuk pengguna biasa, akses superuser, dan logout. Alur ini lulus saat
audit. Role Editor diuji melalui database tes Django; ulangi dengan akun Editor
pilihanmu pada browser untuk memeriksa pengalaman pengguna nyata.

Burp Suite adalah latihan manual opsional dan tidak menjadi dependency aplikasi.

### AI Disclosure Tutorial 04 dan Tugas 4

**OpenAI Codex** digunakan dalam sesi audit dan implementasi ini. Penggunaan
**ChatGPT** pada tugas sebelumnya sudah dijelaskan di bagian disclosure terdahulu.
Bantuan Codex meliputi membaca persyaratan PDF Tutorial 04/Tugas 4, audit
kode autentikasi/session/cookie, evaluasi desain otorisasi, penyelesaian role
Editor dan fitur star, debugging, perencanaan serta implementasi tes, review
perubahan kode, dan penyusunan dokumentasi.

Strategi prompting adalah memberi konteks repository yang sudah berjalan,
menentukan Experience sebagai model tugas, meminta audit Tutorial 04 selesai
lebih dahulu, mempertahankan desain cream/burgundy dan endpoint lama, lalu
mewajibkan tes dan commit berdasarkan tahap teknis nyata tanpa push otomatis.

Catatan prompt nyata dari sesi ini (kutipan singkat):

> FIRST audit and verify my existing Tutorial 04 implementation against the tutorial requirements.

> Do NOT create duplicate migrations.

> Do NOT push automatically.

Hasil AI diperiksa terhadap persyaratan tugas dan kode repository, disesuaikan
untuk route/template/desain proyek, serta diuji otomatis melalui Django dan
Selenium. Contoh penyesuaian: mempertahankan migrasi 0004 yang sudah ada,
memperbaiki logout menjadi POST, mempertahankan alur Tugas 3, serta membatasi
Editor pada Experience tanpa memperluas otorisasi Project.

Keterbatasan AI: hasil tes lokal tidak membuktikan konfigurasi deployment benar;
contoh kode tutorial juga tetap perlu dinilai keamanannya. Kode frontend yang
menyembunyikan tombol tidak menggantikan pemeriksaan server. Pemilik proyek
perlu membaca perubahan, memahami alasan implementasi, memilih akun Editor,
dan memverifikasi environment deployment. Tidak ada klaim bahwa review manual
pemilik sudah selesai. **Tidak ada tautan chat/log eksternal yang disertakan**;
catatan prompt di atas adalah ringkasan/kutipan sesi nyata, bukan percakapan buatan.

### Weekly Progress: Week 4

Mengaudit Tutorial 04 terlebih dahulu, memperbaiki auth/form/API dan konfigurasi,
menjalankan tes serta Selenium, kemudian menyelesaikan backend dan UI empat role
Experience dengan menggunakan perubahan lokal yang sudah ada. Pekerjaan
tersimpan sebagai commit terpisah sesuai tahap yang benar-benar selesai.
Dokumentasi minggu sebelumnya tetap dipertahankan.

### Sebelum push dan pengumpulan

```bash
git status
python manage.py check
python manage.py test
python manage.py showmigrations
git diff --check
git log --oneline -10
```

Belum ada push otomatis. Setelah review dan persetujuan pemilik, push dapat
dilakukan secara eksplisit. Dokumen tugas meminta tautan **commit GitHub** hasil
akhir untuk submisi, bukan hanya tautan repository. Proses push/submisi tetap
merupakan langkah terpisah yang dilakukan pemilik.

---

## Tutorial 05: Web Interactivity with JavaScript

Tutorial 05 melanjutkan fitur autentikasi dan otorisasi Tutorial 04. Precheck pada
awal pengerjaan: working tree bersih, 27 tes sebelumnya lulus, system check bersih,
dan seluruh migrasi sudah diterapkan. Tidak ditemukan bug prasyarat yang
menghalangi Tutorial 05. Identitas Michelle, isi portofolio, desain cream/burgundy,
dan fitur Experience/Editor dari Tugas 4 tetap dipertahankan.

### Toast yang dapat dipakai ulang

`components/toast.html` disertakan oleh `base.html` setelah footer dan memuat
`main/static/js/toast.js`. Fungsi global
`showToast(title, message, type = 'normal', duration = 3000)` menampilkan popover
manual di kanan bawah, dengan tipe normal/success/error. Isi memakai `textContent`,
bukan HTML. Timer lama dibatalkan ketika notifikasi baru datang, termasuk saat
animasi keluar sedang berjalan. Toast memiliki live region untuk pembaca layar
serta mengikuti preferensi reduced motion. Tidak ada tombol tes permanen.

### Daftar dan pencarian Project melalui AJAX

`show_projects` merender kerangka `projects.html`, nama pemilik, nilai pencarian,
dan `ProjectForm()` untuk modal. Data kartu diambil terpisah melalui Fetch API.
Halaman menyediakan status loading, error dengan tombol coba lagi, empty, dan
grid. Pencarian memakai debounce **300 ms**; Enter/tombol Cari langsung mencari
serta membatalkan timer. `AbortController` dan pemeriksaan request aktif mencegah
hasil pencarian lama menimpa hasil baru. Pencarian dan create AJAX tidak memuat
ulang dokumen halaman.

**Perubahan kontrak API dibanding Tutorial 04:** `/api/projects/` kini berisi
objek `pk` dan `fields` yang dirakit manual, dengan field berikut:

```json
{
  "pk": "<uuid-project>",
  "fields": {
    "title": "Nama proyek",
    "description": "Deskripsi",
    "tech_stack": "Django",
    "project_url": "https://example.com/",
    "star_count": 1,
    "is_starred": false,
    "starred_by_names": "nama-pengguna"
  }
}
```

Response berupa list objek tersebut. `is_starred` mengikuti pengguna pada request;
untuk pengunjung nilainya false. Query `?title=...` tetap didukung dan spasi di
tepi dibuang. `prefetch_related("starred_by")` menghindari query tambahan per
Project. Response tidak disimpan cache agar status pengguna tidak tertukar atau
menjadi stale. Tidak ada field gambar karena model Project di repository ini
memang tidak memilikinya. Password, email, session, dan ID internal User tidak
dimasukkan ke JSON.

Endpoint `/json/` sekarang menggunakan `get_projects_json_legacy` untuk menjaga
format serializer Django sebelumnya. `/json/<uuid>/`, `/xml/`, `/xml/<uuid>/`,
serta seluruh API Experience tetap tersedia dengan natural key pengguna.

Kartu AJAX mempertahankan title, description, tech stack, tautan Project, serta
form POST star/delete. CSRF token diklon dari template ke setiap form. URL aksi
dibentuk dari Django URL reversal dengan UUID placeholder. Star dapat digunakan
semua pengguna login, sedangkan delete hanya ditampilkan untuk superuser dan
memakai `confirm()` sebelum submit. View lama tetap memeriksa hak akses server.
Star/delete tetap memakai POST tradisional dan redirect, sesuai cakupan tutorial;
komponen template lama juga dipertahankan.

### Modal dan create AJAX

Tombol Tambah Proyek dan `components/project_form_modal.html` hanya dirender
untuk superuser. Modal memakai Popover API, label dialog, tombol backdrop/tutup/
Batal, focus trap, dan layout mobile. Form tetap mempunyai action tradisional
`/projects/add/`; route dan halaman form lama tetap berfungsi.

JavaScript mengirim `FormData` ke `/projects/add-ajax/` dengan header
`X-CSRFToken` dari cookie `csrftoken`. Submit dinonaktifkan selama request dan
submit ganda dicegah. Pada sukses, modal ditutup, form direset, toast muncul,
dan daftar di-fetch ulang dengan filter yang masih aktif. Proyek baru hanya
terlihat jika cocok dengan filter. Pada gagal, modal dan isi form tetap ada;
error validasi, respons non-JSON, dan gangguan jaringan ditampilkan melalui toast.
Listener form hanya dipasang jika modal ada, sehingga halaman pengunjung biasa
tidak memicu error karena elemen null.

| Request | Hasil |
| --- | --- |
| POST valid, superuser, CSRF sah | 201 JSON dengan message dan pk |
| POST form invalid oleh superuser | 400 JSON dengan errors per field |
| POST pengunjung/pengguna biasa/Editor, CSRF sah | 403 JSON |
| POST tanpa CSRF sah | 403 dari middleware Django |
| GET endpoint create AJAX | 405 Method Not Allowed |

Endpoint tidak memakai `login_required` agar penolakan otorisasi AJAX berupa JSON,
bukan redirect HTML login. `@require_POST`, pemeriksaan `is_superuser`, dan
`ProjectForm(request.POST)` tetap wajib; tidak ada `csrf_exempt`.

### Pertahanan XSS dan pembersihan input

Rendering aman diterapkan sejak milestone AJAX pertama, tanpa commit perantara
yang sengaja rentan. Title, description, dan tech stack di template literal
melewati `escapeHtml`; tooltip, label, dan hitungan star memakai DOM API/
`textContent`. Tautan hanya dibuat untuk URL HTTP/HTTPS yang dapat diparse, sehingga
nilai berbahaya dari data lama/Admin pun tidak menjadi tautan `javascript:`.

`ProjectForm.clean_title`, `clean_description`, dan `clean_tech_stack` menghapus
tag HTML serta whitespace tepi dan menolak hasil kosong. URLField tetap memvalidasi
URL. Form yang sama dipakai endpoint tradisional maupun AJAX. Pembersihan adalah
lapisan tambahan, **bukan pengganti escaping saat render**. Konsekuensinya, teks
seperti `List<String>` dapat menjadi `List`; field ini diperlakukan sebagai teks
biasa, bukan editor HTML.

Tes stored XSS menggunakan payload `<img src="x" onerror="alert('XSS!')">`
hanya pada database tes sementara. Payload yang sudah tersimpan tampil sebagai
teks literal tanpa alert; create baru dengan judul hanya tag ditolak server.
Database tes dibuang setelah pengujian, sehingga tidak ada payload uji tertinggal
di database portofolio lokal.

### Menjalankan dan menguji Tutorial 05

Setup environment tetap mengikuti bagian sebelumnya. Tutorial 05 tidak mengubah
model atau menambah migration. Gunakan browser modern dengan dukungan Fetch,
AbortController, dan Popover API.

```bash
source env/bin/activate
python manage.py check
python manage.py test
python manage.py showmigrations
python manage.py makemigrations --check --dry-run
python manage.py findstatic css/style.css js/toast.js
python manage.py runserver
```

Tes default menjalankan **35 tes Django** dan melewati **9 tes browser opt-in**.
Untuk menjalankan seluruh 44 tes, termasuk Chrome headless:

```bash
pip install selenium  # dependency tes browser opsional; Chrome juga diperlukan
RUN_BROWSER_TESTS=1 python manage.py test --noinput
# Atau hanya sembilan tes browser:
RUN_BROWSER_TESTS=1 python manage.py test main.test_browser --noinput
```

`main/test_browser.py` menjalankan server lokal dan database tes sendiri. Tidak
perlu menyalakan server lain, memasukkan password, atau mengubah role akun nyata.
Tes mencakup toast berulang, debounce, loading/empty/error/retry, respons stale,
XSS tersimpan, star/delete, modal keyboard/mobile, create tanpa reload, validasi,
submit ganda, respons HTML, jaringan offline simulasi, dan sesi kedaluwarsa.
QA akhir menjalankan seluruh **44 tes sekaligus dan semuanya lulus**.
Chrome performance log memverifikasi POST 201, GET API 200, respons invalid 400,
serta keberadaan header CSRF. Skenario kegagalan yang sengaja disimulasikan dapat
mencatat error tertangani; tidak ada exception JavaScript yang tidak tertangani.

Verifikasi juga dilakukan pada Django 5.2 sesuai `requirements.txt`, selain Django
6.1 yang terpasang di virtualenv lokal. Static finder menunjuk file aplikasi yang
benar. Smoke test `runserver` lokal memverifikasi halaman publik, auth, API,
Admin, CSS, dan toast.js tanpa respons 500; screenshot desktop/mobile juga
diperiksa. Jika browser masih memuat CSS/JS lama, lakukan hard reload/Disable Cache;
hasil collectstatic dan screenshot tidak dimasukkan ke Git.

### Progres dan AI disclosure Tutorial 05

OpenAI Codex membantu membaca spesifikasi, precheck Tutorial 04, implementasi
toast/AJAX/modal, desain penanganan error dan keamanan, tes Django/Selenium,
review screenshot, serta dokumentasi. Prompt meminta perubahan bertahap di
repository existing, mempertahankan fitur lama, menjalankan tes sebelum commit,
dan berhenti sebelum push. Hasil diadaptasi ke `projects.html`, path static milik
aplikasi, field Project yang benar-benar tersedia, dan palet warna existing.

Keputusan implementasi yang diperiksa: menjaga format endpoint legacy secara
terpisah, tidak menambah field gambar/migration, memasang escaping sejak awal,
dan menggunakan database tes untuk payload XSS. Tes otomatis serta pemeriksaan
screenshot desktop/mobile dilakukan; pemilik masih dapat meninjau langsung dengan
akun pilihannya. Tidak ada tautan chat eksternal atau klaim review manual pemilik
yang dibuat-buat. Log ringkas ini melengkapi disclosure sebelumnya.

Milestone lokal: toast teruji; daftar/pencarian AJAX aman; modal teruji;
create AJAX dengan pembersihan input bersama; dokumentasi dan QA akhir.
Tidak ada push, deployment, atau submisi SCELE otomatis untuk Tutorial 05.
Setelah puas meninjau hasil, pemilik dapat menjalankan `git push origin main`.

## Warm editorial makeover

The existing Django portfolio uses a cream, berry and terracotta editorial system,
with shared buttons/forms, a layered homepage portrait, narrative experience
cards, and a scrapbook gallery. Tutorial 5 AJAX handlers, permissions, CSRF,
authentication and toast behavior remain in place.

### Editing “Snapshots of My Life”

The gallery uses **11 original local photos**, as requested in the latest update.
Files remain `main/static/img/life/1.jpg` through `11.jpg`; no placeholders or
external images are used. Images retain their natural proportions, including EXIF
orientation. Click a photo to open the original. Images load lazily; the original
files are intentionally unchanged, so larger photos may take longer to load.

Edit **`main/life_snapshots.py`**. Every dictionary is identified by its `image`
path (for example `img/life/5.jpg`). Independently edit:

- `title`: heading below that photo.
- `caption`: descriptive sentence below the title.
- `category`: small label above the title.
- `year`: optional year; currently blank because dates were not supplied.
- `alt`: accessible description of the photograph.

These fields apply individually to all eleven entries. Changing text never
requires renaming a file. Generic initial captions are editable copy, not claims
about particular personal events. The template is
`main/templates/components/life_snapshots.html`; collage layout lives in the
“Scrapbook spreads” section of `main/static/css/style.css`.

### Local verification

```sh
python manage.py check
python manage.py test --noinput
RUN_BROWSER_TESTS=1 python manage.py test --noinput
git diff --check
```

The opt-in Selenium suite requires Chrome and Selenium. It uses a temporary test
database. It covers existing AJAX/auth/modal behavior plus all five public pages
at desktop, tablet and mobile widths, horizontal overflow, eleven loaded photos,
natural image ratios and JavaScript console errors. Set `BROWSER_SCREENSHOT_DIR`
to save review screenshots outside the repository.

In Chrome, review the hero, About/Education/Skills anchors and photo captions;
resize the page; try Login/Register and POST Logout; then check search, modal
keyboard focus, create, toast and star/unstar. Check normal-user, Editor and
superuser controls separately. No deployment or push is part of this makeover.

---

### Tugas 5

Tugas 5 menerapkan interaktivitas AJAX pada **Experience**, yaitu bagian yang sebelumnya sudah dikembangkan pada Tugas 3 dan Tugas 4. Implementasi Projects dari Tutorial 05, autentikasi, hak akses Editor, serta desain portofolio yang sudah ada tetap dipertahankan.

Pada Tugas 5, halaman Experience dikembangkan agar data dapat dimuat dan dicari secara asynchronous menggunakan Fetch API tanpa perlu melakukan reload seluruh halaman. Selain itu, proses penambahan Experience juga dapat dilakukan melalui modal menggunakan AJAX, disertai validasi, toast notification, perlindungan CSRF dan XSS, serta hak akses yang tetap mengikuti aturan dari Tugas 4.

#### Implementasi dan kesesuaian persyaratan

| Persyaratan | Implementasi | Status |
| --- | --- | --- |
| Daftar dimuat dengan AJAX | `show_experience` merender struktur halaman, sedangkan `experience.js` mengambil data menggunakan Fetch API | Selesai |
| JSON manual dan informasi star | `get_experiences_ajax` menggunakan `JsonResponse` serta menyertakan jumlah star dan status star pengguna saat ini | Selesai |
| Kondisi memuat, kosong, dan gagal | Tersedia pesan loading, empty state, error state, `aria-live`, `aria-busy`, dan tombol Coba lagi | Selesai |
| Pencarian tanpa reload halaman | Pencarian berdasarkan judul menggunakan debounce 300 ms dan pembatalan request sebelumnya | Selesai |
| Tambah melalui modal dan AJAX | Menggunakan `ExperienceForm`, Fetch API, respons 201/400/403, dan pembaruan daftar setelah data berhasil ditambahkan | Selesai |
| Toast berhasil dan gagal | Menggunakan kembali fungsi `showToast` dari Tutorial 05 | Selesai |
| CSRF dan pemeriksaan peran | Token CSRF dikirim bersama form dan hak akses tetap diperiksa di backend | Selesai |
| Perlindungan XSS | Menggunakan DOM API, `textContent`, validasi URL, serta `strip_tags` pada form | Selesai |
| Star, ubah, dan hapus | Endpoint dan aturan hak akses dari Tugas 4 tetap dipertahankan | Selesai |
| Tampilan dan aksesibilitas | Modal dapat digunakan dengan keyboard dan layout diuji pada beberapa ukuran layar | Selesai |
| Pengujian lokal | Django system check, automated test, browser test, dan pemeriksaan static file dijalankan | Selesai |
| Tiga pertanyaan reflektif | Jawaban tersedia dalam bahasa Indonesia pada bagian Pertanyaan Reflektif | Selesai |
| Pengungkapan penggunaan AI | Dokumentasi penggunaan ChatGPT dan OpenAI Codex tersedia pada bagian akhir | Selesai |

#### Daftar Experience dan struktur JSON

Endpoint baru **`GET /api/experience/list/`** digunakan untuk menyediakan data Experience yang akan ditampilkan melalui AJAX.

Endpoint lama `/api/experience/` dan `/api/experience/<uuid>/` tetap dipertahankan agar fitur dari tugas sebelumnya tidak rusak.

Contoh satu elemen dalam response endpoint AJAX:

```json
{
  "pk": "<uuid-experience>",
  "fields": {
    "title": "Judul pengalaman",
    "description": "Deskripsi pengalaman",
    "category": "volunteer",
    "category_label": "Relawan",
    "thumbnail": null,
    "started_at": "2026-10-01T10:00:00+00:00",
    "ended_at": null,
    "is_ongoing": true,
    "star_count": 2,
    "is_starred": false
  }
}
```

Response lengkap berupa list yang berisi objek Experience. Field `ended_at` yang bernilai `null` menandakan bahwa pengalaman tersebut masih berlangsung.

Field `started_at` pada model menggunakan `auto_now_add=True`, sehingga nilainya menunjukkan waktu data dicatat ke database. Karena itu, pada tampilan kartu digunakan keterangan **Dicatat**, bukan dianggap sebagai tanggal mulai kegiatan.

Informasi star juga disertakan pada response. `star_count` menunjukkan jumlah pengguna yang memberi bintang, sedangkan `is_starred` menunjukkan apakah pengguna yang sedang login sudah memberikan bintang pada Experience tersebut.

Untuk pengguna yang belum login, `is_starred` bernilai `false`, tetapi jumlah bintang tetap dapat dilihat.

Endpoint AJAX tidak mengirim informasi sensitif seperti password, email, session, maupun ID internal pengguna.

JavaScript juga memeriksa struktur data sebelum menampilkan kartu. Jika response gagal, bukan JSON, atau tidak memiliki format yang diharapkan, halaman akan menampilkan error state beserta tombol **Coba lagi**.

#### Pencarian dengan debouncing

Fitur pencarian menggunakan parameter:

```text
?title=...
```

Pencarian dilakukan terhadap judul Experience menggunakan `icontains`, sehingga pencarian tidak membedakan huruf besar dan kecil sesuai kemampuan pencocokan database.

Jika kolom pencarian kosong, seluruh Experience akan ditampilkan kembali.

Pencarian dilakukan menggunakan AJAX sehingga halaman tidak perlu dimuat ulang.

Untuk mengurangi jumlah request ke server, digunakan teknik **debouncing selama 300 ms**. Setiap kali pengguna mengetik, timer sebelumnya akan dibatalkan dan dibuat timer baru. Request baru hanya dikirim setelah pengguna berhenti mengetik selama kurang lebih 300 ms.

Jika pengguna menekan Enter atau tombol **Cari**, pencarian dapat langsung dijalankan tanpa harus menunggu timer.

Implementasi juga menggunakan `AbortController` untuk membatalkan request sebelumnya ketika pencarian baru dilakukan. Hal ini mencegah response dari pencarian lama yang datang terlambat menggantikan hasil pencarian terbaru.

#### Modal, validasi, dan toast

Untuk pengguna yang memiliki hak akses, penambahan Experience dapat dilakukan melalui modal tanpa berpindah ke halaman lain.

Tombol **Tambah Pengalaman** hanya ditampilkan untuk superuser.

Modal menggunakan komponen yang disesuaikan dengan pola modal pada Projects. Ketika modal dibuka, fokus berpindah ke input pertama. Navigasi menggunakan Tab dan Shift+Tab tetap berada di dalam modal, tombol Escape dapat digunakan untuk menutup modal, dan setelah modal ditutup fokus kembali ke tombol pembuka.

Form dikirim ke endpoint:

```text
POST /experience/add-ajax/
```

menggunakan `FormData` dan Fetch API.

Token `csrfmiddlewaretoken` ikut dikirim bersama form agar request POST tetap dilindungi oleh mekanisme CSRF Django.

Selama request berlangsung, tombol submit dan field form dinonaktifkan untuk mencegah submit ganda.

Response endpoint:

| Kondisi | Response |
| --- | --- |
| Superuser, data valid, CSRF valid | `201 Created` dengan JSON berisi `message` dan `pk` |
| Superuser, data tidak valid | `400 Bad Request` dengan error sesuai field |
| Pengunjung, pengguna biasa, atau Editor | `403 Forbidden` |
| Token CSRF tidak valid | `403 Forbidden` dari middleware Django |
| Request GET ke endpoint AJAX | `405 Method Not Allowed` |

Jika validasi gagal, modal tetap terbuka dan nilai input tidak langsung dihapus. Error ditampilkan di dalam modal pada field yang sesuai.

Atribut seperti `aria-invalid` dan `aria-describedby` digunakan agar error form tetap dapat dipahami oleh teknologi bantu.

Jika penambahan berhasil, form akan direset, modal ditutup, toast sukses ditampilkan, dan daftar Experience dimuat kembali menggunakan AJAX tanpa reload seluruh halaman.

Jika sedang terdapat filter pencarian, daftar tetap mengikuti kata kunci pencarian yang sedang aktif.

Untuk gangguan jaringan atau response yang tidak sesuai, pengguna mendapatkan toast error dan nilai input tetap dipertahankan agar dapat diperiksa kembali.

Toast menggunakan fungsi `showToast` yang sudah dibuat pada Tutorial 05 sehingga tidak perlu membuat sistem notifikasi baru.

#### Keamanan dan hak akses

Validasi server tetap dilakukan menggunakan `ExperienceForm`.

Pada `ExperienceForm`, `clean_title` dan `clean_description` menggunakan `strip_tags()` untuk membersihkan tag HTML serta menghapus whitespace pada bagian awal dan akhir input.

Validasi ini digunakan pada proses tambah melalui AJAX, tambah melalui halaman biasa, dan edit Experience.

Field lain seperti kategori, panjang judul, URL, dan tanggal tetap divalidasi melalui ModelForm Django.

Pembersihan menggunakan `strip_tags()` bukan pengganti escaping saat rendering. Data yang diterima dari server tetap diperlakukan sebagai data yang tidak dipercaya.

Pada frontend, judul, deskripsi, kategori, error, dan informasi lainnya dimasukkan ke halaman menggunakan DOM API dan `textContent`, sehingga nilai tersebut tidak diinterpretasikan sebagai HTML.

URL gambar juga diperiksa sebelum digunakan. URL dengan skema berbahaya seperti `javascript:` atau `data:` tidak digunakan sebagai sumber gambar.

Tidak terdapat penggunaan `csrf_exempt`, sehingga seluruh operasi yang mengubah data tetap dilindungi oleh middleware CSRF Django.

Hak akses Experience tetap mengikuti aturan dari Tugas 4:

| Peran | Baca/Cari | Beri/Batalkan Bintang | Tambah | Ubah | Hapus |
| --- | --- | --- | --- | --- | --- |
| Pengunjung | Ya | Login terlebih dahulu | Ditolak | Login terlebih dahulu | Login terlebih dahulu |
| Pengguna biasa | Ya | Ya | 403 | 403 | 403 |
| Editor | Ya | Ya | 403 | Ya | 403 |
| Superuser | Ya | Ya | Ya | Ya | Ya |

Editor ditentukan berdasarkan keanggotaan pada grup bernama `Editor`, bukan berdasarkan username atau status staff.

Tampilan tombol pada frontend hanya membantu user interface. Hak akses sebenarnya tetap diperiksa di backend sehingga pengguna tidak dapat memperoleh akses hanya dengan memodifikasi HTML atau URL.

Fitur star/unstar dan delete tetap menggunakan request POST dengan CSRF.

Edit Experience tetap menggunakan form edit yang sudah tersedia dari tugas sebelumnya.

#### Menjalankan dan memeriksa Tugas 5

Untuk menjalankan project secara lokal:

```bash
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test --noinput
python manage.py findstatic js/experience.js css/style.css
python manage.py runserver 127.0.0.1:8000
```

Tugas 5 tidak mengubah model sehingga tidak membutuhkan migration baru.

Untuk menjalankan browser test:

```bash
pip install selenium

RUN_BROWSER_TESTS=1 python manage.py test --noinput
```

Untuk hanya menjalankan test browser Experience:

```bash
RUN_BROWSER_TESTS=1 python manage.py test main.test_experience_browser --noinput
```

Jika driver yang kompatibel sudah tersedia pada cache lokal:

```bash
SE_OFFLINE=true RUN_BROWSER_TESTS=1 python manage.py test --noinput
```

#### Hasil pengujian

Hasil verifikasi lokal sebelum pengumpulan:

- `python manage.py check` berhasil dijalankan tanpa masalah.
- `python manage.py makemigrations --check --dry-run` menunjukkan bahwa tidak terdapat perubahan model yang membutuhkan migration baru.
- `python manage.py test --noinput` menjalankan **44 tes Django** dengan hasil lulus, sedangkan 19 browser test dilewati karena bersifat opsional.
- Dengan `RUN_BROWSER_TESTS=1`, seluruh **63 tes berhasil dijalankan**, terdiri dari 44 tes Django dan 19 browser test.
- Pengujian mencakup fitur Experience baru serta memastikan fitur Projects dan fungsi dari tugas sebelumnya tetap berjalan.
- `runserver` berhasil dijalankan secara lokal.
- Static finder berhasil menemukan `experience.js` dan stylesheet yang digunakan aplikasi.
- `git diff --check` telah diperiksa agar tidak terdapat masalah whitespace sebelum commit akhir.

Pengujian mencakup beberapa kondisi seperti:

- pemuatan daftar Experience melalui AJAX,
- pencarian dengan debouncing,
- pencarian tanpa hasil,
- pembatalan request lama,
- star dan unstar,
- validasi hak akses,
- penambahan Experience melalui modal,
- validasi form,
- toast notification,
- pencegahan submit ganda,
- CSRF,
- XSS,
- URL gambar tidak aman,
- kegagalan jaringan,
- sesi yang sudah tidak berlaku,
- serta pembaruan daftar tanpa reload halaman.

Pengujian XSS menggunakan payload:

```html
<img src="x" onerror="alert('XSS!')">
```

Payload tersebut hanya digunakan pada database test sementara. Input berbahaya tidak dieksekusi sebagai JavaScript pada halaman.

Browser test juga digunakan untuk memeriksa interaksi pada beberapa ukuran layar, navigasi keyboard, modal, dan kemungkinan error JavaScript.

Pengujian ini dilakukan pada environment lokal sehingga hasilnya tidak secara otomatis membuktikan kondisi deployment PWS.

---

#### Pertanyaan Reflektif

1. **Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!**

   Debouncing adalah teknik menunda pemanggilan suatu fungsi sampai tidak ada input baru selama selang waktu tertentu. Pada fitur pencarian Experience di portofolio saya, setiap ketikan akan membatalkan timer sebelumnya dan membuat timer baru selama 300 ms.

   Jika pengguna mengetik beberapa huruf dengan cepat, request tidak langsung dikirim untuk setiap huruf. Request baru dikirim setelah pengguna berhenti mengetik selama kurang lebih 300 ms.

   Tanpa debouncing, pencarian AJAX dapat mengirim banyak request ke server meskipun sebagian besar hasilnya sudah tidak dibutuhkan. Hal tersebut dapat menambah beban server dan penggunaan jaringan.

   Dengan debouncing, jumlah request dapat dikurangi sehingga proses pencarian menjadi lebih efisien dan tampilan hasil juga terasa lebih stabil.

   Pada implementasi ini, saya juga menggunakan `AbortController` untuk membatalkan request lama agar response sebelumnya tidak menggantikan hasil pencarian yang lebih baru.

2. **Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?**

   `fetch()` mengembalikan sebuah Promise, bukan langsung objek response yang sudah dapat digunakan.

   Ketika menggunakan:

   ```javascript
   const response = await fetch(url);
   ```

   `await` membuat eksekusi di dalam fungsi `async` menunggu sampai Promise dari `fetch()` selesai dan menghasilkan objek `Response`. Proses ini tidak memblokir seluruh halaman browser.

   Setelah mendapatkan response, saya juga menggunakan:

   ```javascript
   const data = await response.json();
   ```

   karena proses membaca body response dan mengubahnya menjadi data JavaScript juga bersifat asynchronous.

   Jika `await` tidak digunakan pada:

   ```javascript
   const response = fetch(url);
   ```

   maka variabel `response` masih berisi Promise. Jika kode langsung mencoba memanggil `response.json()`, maka akan terjadi error karena Promise bukan objek `Response`.

   Selain `await`, Promise sebenarnya juga dapat ditangani menggunakan `.then()`, tetapi urutan asynchronous-nya tetap harus diatur dengan benar.

   Pada implementasi Experience, `try/catch` juga digunakan untuk menangani gangguan jaringan atau kegagalan ketika membaca response. Selain itu, status HTTP tetap diperiksa karena response seperti 400 atau 403 tidak selalu menyebabkan `fetch()` langsung melempar error.

3. **Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!**

   XSS atau Cross-Site Scripting adalah serangan ketika input yang tidak dipercaya berhasil diperlakukan sebagai HTML atau JavaScript aktif di browser.

   Contohnya, input seperti:

   ```html
   <img src="x" onerror="alert('XSS!')">
   ```

   dapat menjalankan JavaScript apabila nilai tersebut langsung dimasukkan ke halaman menggunakan `innerHTML` tanpa perlindungan.

   Template Django secara default melakukan autoescaping terhadap variabel yang ditampilkan melalui template. Artinya, karakter HTML berbahaya biasanya akan ditampilkan sebagai teks biasa selama mekanisme autoescaping tidak dimatikan.

   Pada AJAX, data biasanya diterima dalam bentuk JSON kemudian dirender sendiri menggunakan JavaScript. Karena proses tersebut tidak melewati template Django, developer harus memastikan sendiri bagaimana data tersebut dimasukkan ke DOM.

   Jika data langsung dimasukkan menggunakan `innerHTML`, input berbahaya dapat diinterpretasikan sebagai markup aktif. Karena itu, pada Experience saya menggunakan DOM API dan `textContent` agar judul, deskripsi, kategori, maupun error selalu diperlakukan sebagai teks.

   URL gambar juga diperiksa secara terpisah karena escaping teks saja tidak cukup untuk mengamankan nilai yang digunakan sebagai URL.

   Selain itu, `strip_tags()` digunakan pada backend sebagai lapisan tambahan untuk membersihkan input. Namun, validasi server tetap tidak menggantikan kebutuhan untuk melakukan rendering secara aman di browser.

   CSRF dan XSS merupakan dua jenis serangan yang berbeda. CSRF melindungi request perubahan data agar berasal dari sumber yang valid, sedangkan perlindungan XSS berfokus pada mencegah data tidak dipercaya dijalankan sebagai kode pada browser.

---

#### Pengungkapan Penggunaan AI Tugas 5

Dalam pengerjaan Tugas 5, saya menggunakan **ChatGPT** dan **OpenAI Codex** sebagai alat bantu dalam proses pengembangan.

ChatGPT digunakan untuk membantu memahami requirement tugas, mendiskusikan konsep seperti AJAX, Fetch API, debouncing, CSRF, dan XSS, serta membantu meninjau dokumentasi dan jawaban reflektif.

OpenAI Codex digunakan untuk membantu implementasi beberapa bagian teknis, seperti pengembangan endpoint AJAX Experience, pencarian, modal penambahan Experience, validasi, pengujian, serta perbaikan kode berdasarkan hasil pengujian.

Dalam proses pengerjaan, saya memberikan konteks mengenai struktur project yang sudah ada, requirement resmi Tugas 5, serta ketentuan agar fitur dari Tutorial 05 dan Tugas sebelumnya tetap berjalan.

Hasil yang diberikan oleh AI tetap diperiksa melalui pengujian Django dan browser, serta disesuaikan kembali dengan struktur project, kebutuhan fitur, dan aturan hak akses yang sudah diterapkan sebelumnya.

AI digunakan sebagai alat bantu selama proses pengembangan dan debugging, bukan sebagai pengganti proses memahami requirement dan memeriksa hasil implementasi.

---

#### Progres Minggu 5 dan pemeriksaan sebelum pengumpulan

Pengerjaan Tugas 5 dilakukan secara bertahap, dimulai dari pengembangan backend dan endpoint AJAX Experience, implementasi daftar dan pencarian, pembuatan modal tambah Experience, validasi dan toast notification, penguatan keamanan CSRF/XSS, pengujian, hingga dokumentasi akhir.

Pemeriksaan manual sebelum pengumpulan:

1. Buka `http://127.0.0.1:8000/experience/` tanpa login. Coba mencari judul Experience yang tersedia dan yang tidak tersedia, kemudian kosongkan kembali pencarian. Daftar seharusnya berubah tanpa melakukan reload seluruh halaman.

2. Periksa request `/api/experience/list/?title=...` melalui DevTools ketika mengetik pada kolom pencarian. Request baru seharusnya dikirim setelah jeda kurang lebih 300 ms.

3. Login sebagai pengguna biasa. Coba fitur star dan unstar pada Experience. Pengguna biasa tidak memiliki tombol tambah, ubah, atau hapus.

4. Login sebagai anggota grup Editor. Editor dapat mengubah Experience, tetapi tidak dapat menambah atau menghapus Experience.

5. Login sebagai superuser. Buka modal Tambah Pengalaman dan coba submit form dengan data tidak valid. Error harus muncul pada modal dan nilai input tetap dipertahankan. Setelah data valid berhasil disimpan, modal akan tertutup, toast berhasil ditampilkan, dan daftar Experience diperbarui.

6. Uji penggunaan keyboard pada modal menggunakan Tab, Shift+Tab, Escape, dan tombol Batal. Setelah modal ditutup, fokus harus kembali ke tombol Tambah Pengalaman.

7. Periksa kembali halaman Projects untuk memastikan fitur dari Tutorial 05 masih berjalan setelah implementasi AJAX pada Experience.