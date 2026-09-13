# Portfolio Website - Tugas 1 & Tugas 2 PBP

Nama: Michelle Yuyun Margarethy Aritonang  

NPM: 2506656961  

Kelas: PBP C  

## Deskripsi Proyek

Website portofolio pribadi yang dibuat sebagai bagian dari mata kuliah Pemrograman Berbasis Platform. Website ini menampilkan informasi pribadi, profil singkat, pendidikan, pengalaman organisasi/kepanitiaan, skills, serta projects yang pernah dikerjakan.

Pada Tugas 1, website dibuat menggunakan HTML5 dan CSS3 dengan desain responsive. Pada Tugas 2, website dikembangkan menggunakan Django dengan menambahkan bagian Projects yang datanya disimpan di database dan ditampilkan secara dinamis.

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

1. **Penggunaan Elemen Semantik HTML5**

   Pada perancangan struktur HTML website portofolio ini, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>`. Elemen-elemen tersebut membantu saya mengorganisasi struktur halaman berdasarkan fungsi dan kontennya. Misalnya, `<header>` digunakan untuk bagian navigasi, `<main>` menjadi bagian utama website, `<section>` digunakan untuk mengelompokkan bagian seperti About Me, Education, dan Skills, sedangkan `<article>` digunakan untuk setiap informasi pendidikan dan pengalaman yang berdiri sebagai satu kesatuan.

   Penggunaan elemen semantik membuat struktur HTML lebih terorganisasi, mudah dibaca, dan lebih mudah dikembangkan ketika website bertambah kompleks. Selain itu, struktur tersebut membantu saya memahami hubungan antara struktur konten HTML dengan tampilan yang kemudian diatur menggunakan CSS.

2. **Tantangan Desain Responsive**

   Tantangan utama ketika membuat website responsive adalah memastikan tata letak dan ukuran elemen tetap nyaman digunakan pada berbagai ukuran layar. Pada tampilan desktop, informasi dapat ditampilkan dalam beberapa kolom, seperti bagian About Me dan foto profil yang diletakkan berdampingan serta Education dan Skills yang ditampilkan dalam dua kolom.

   Namun, pada ukuran layar yang lebih kecil, tata letak tersebut dapat menjadi terlalu sempit dan menyebabkan teks atau elemen visual terlihat kurang nyaman. Untuk mengatasi hal tersebut, saya menggunakan CSS Grid, Flexbox, dan media query untuk mengubah layout pada breakpoint tertentu.

   Saya mengevaluasi elemen berdasarkan prioritas informasi dan keterbacaan. Elemen yang penting seperti nama, About Me, foto, Skills, dan Education tetap dipertahankan, tetapi susunannya diubah menjadi satu kolom pada layar yang lebih kecil. Saya juga menyesuaikan ukuran font, jarak antar elemen, dan ukuran kartu agar website tetap mudah dibaca dan digunakan pada perangkat mobile.

3. **Rencana Pengembangan Fitur**

   Karena website pada awalnya masih berupa static web, informasi yang ditampilkan harus diperbarui secara manual melalui kode. Salah satu pengembangan yang kemudian dilakukan pada Tugas 2 adalah menambahkan halaman Projects yang datanya dapat disimpan dan dikelola melalui database, sehingga project baru dapat ditambahkan tanpa mengubah struktur HTML secara langsung.

   Selain itu, saya juga tertarik untuk mengembangkan fitur contact form agar pengunjung dapat mengirim pesan secara langsung.

---

## Tugas 2

### Pertanyaan Reflektif

1. **Alur Kerja MVT (Model-View-Template) pada Halaman Projects**

   Ketika pengguna membuka halaman `/projects/`, request dari browser pertama kali masuk ke `urls.py` tingkat proyek. Dari sana, request diteruskan ke `main/urls.py` menggunakan fungsi `include()`. Selanjutnya, `main/urls.py` menentukan bahwa URL `/projects/` akan menjalankan view `show_projects`.
   Di dalam `show_projects`, view mengambil data proyek dari model `Project` menggunakan `Project.objects.all()`. Data tersebut kemudian dimasukkan ke dalam `context` dan dikirim ke template `projects.html`. Template menggunakan data tersebut untuk menampilkan setiap proyek dengan looping DTL (`{% for %}`). Setelah proses rendering selesai, Django mengirimkan hasil HTML kembali ke browser.

2. **Pentingnya Penyimpanan Data pada Model**

   Menyimpan data di model membantu memisahkan antara data dan tampilan (*separation of concerns*). Jika data proyek ditulis langsung (*hard-coded*) di dalam template, setiap kali ada perubahan data kita harus mengubah kode HTML-nya. Dengan menyimpan data di model, informasi seperti nama proyek, deskripsi, dan tech stack dapat dikelola melalui database. Template cukup mengambil dan menampilkan data tersebut menggunakan looping. Hal ini membuat kode lebih rapi dan lebih mudah dipelihara (*maintainable*).

3. **Perbedaan `makemigrations` dan `migrate`**

   - `python manage.py makemigrations` digunakan untuk mendeteksi perubahan pada struktur model di `models.py` dan membuat berkas skrip migrasi baru sebagai cetak biru (*blueprint*).
   - `python manage.py migrate` digunakan untuk menerapkan skrip migrasi tersebut ke database.

   **Contoh Kasus:** Jika saya menambahkan field baru seperti `start_date` pada model `Project` di `models.py`, saya perlu menjalankan kedua perintah tersebut secara berurutan:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## AI Disclosure

Dalam pengerjaan Tugas 1 dan Tugas 2, saya menggunakan ChatGPT sebagai alat bantu, bukan sebagai pengganti proses pengerjaan dan pemahaman saya sendiri.

### Penggunaan AI

AI digunakan untuk:

- Memberikan saran mengenai layout CSS, Grid, Flexbox, dan responsive design.
- Memberikan masukan mengenai pemilihan warna, font, spacing, dan tampilan UI/UX.
- Memberikan ide untuk menyusun section seperti Education, Skills, Experience, dan Projects.
- Membantu memahami konsep Django seperti Model, View, Template, URL routing, migration, dan database.
- Membantu memahami konsep unit testing pada Django.
- Membantu mengecek kemungkinan penyebab masalah pada tampilan atau kode.
- Memberikan saran ketika terdapat kendala dalam proses pengembangan website.

### Strategi Prompting

Strategi prompting yang saya gunakan adalah dengan menyampaikan kebutuhan, tujuan desain, serta kendala yang saya temui kepada AI. Saya kemudian meminta pendapat, penjelasan, dan beberapa alternatif solusi yang dapat diterapkan pada website.

Pada Tugas 2, saya menggunakan AI untuk membantu memahami alur MVT, penggunaan model dan database, URL routing, proses migration, serta konsep testing. Saya memberikan konteks mengenai kode yang sedang saya kerjakan agar saran yang diberikan dapat disesuaikan dengan project.

Saya tetap melakukan pengecekan dan penyesuaian secara mandiri terhadap setiap saran yang diberikan, terutama pada struktur halaman, isi informasi, nama dan pemanggilan asset, link sosial media, warna, ukuran elemen, serta responsive layout. Tidak semua saran AI langsung saya terapkan karena saya perlu mempertimbangkan kesesuaiannya dengan project dan materi yang sedang dipelajari.

### Bagian yang Dibantu AI

Beberapa bagian yang mendapatkan bantuan AI antara lain:

- Pengembangan dan perbaikan layout portofolio.
- Responsive design menggunakan CSS.
- Pemahaman konsep Model, View, Template, dan URL pada Django.
- Pemahaman penggunaan database untuk menyimpan data Projects.
- Pemahaman mengenai `makemigrations` dan `migrate`.
- Pemahaman dan pengecekan unit test.
- Pengecekan struktur dan alur implementasi fitur Projects.

### Contoh Log Penggunaan AI

1. **Memahami konsep Django MVT**

   Prompt:
   
   > Jelaskan alur Model, View, Template pada Django untuk halaman Projects dengan bahasa yang mudah dipahami pemula.

   AI membantu saya memahami hubungan antara model, view, template, dan URL sebelum menerapkannya pada project.

2. **Memahami migration**

   Prompt:
   
   > Apa perbedaan `makemigrations` dan `migrate` di Django dan kapan masing-masing digunakan?

   AI membantu saya memahami fungsi kedua perintah tersebut sebelum menjalankannya pada project.

3. **Mengecek implementasi halaman Projects**

   Prompt:
   
   > Saya sudah membuat model Project, view, URL, dan template. Bantu cek apakah alur dari database sampai data ditampilkan di template sudah benar.

   AI digunakan untuk memberikan masukan mengenai alur implementasi. Saya tetap mengecek dan menjalankan kode tersebut secara mandiri.

4. **Memahami testing**

   Prompt:
   
   > Bantu saya memahami bagaimana membuat unit test untuk memastikan halaman Projects dapat diakses dan data Project tampil dengan benar.

   AI membantu saya memahami konsep testing dan contoh kondisi yang perlu diuji.

### Refleksi Penggunaan AI

Penggunaan AI membantu saya memahami konsep yang sebelumnya belum familiar, terutama hubungan antara Model, View, Template, URL, dan database pada Django. Saya tidak langsung menerapkan seluruh jawaban yang diberikan AI, tetapi menggunakan penjelasan dan alternatif yang diberikan sebagai referensi untuk memahami masalah dan menentukan implementasi yang sesuai.

Setelah menerapkan perubahan, saya melakukan pengecekan secara mandiri dengan menjalankan website, memeriksa hasil pada browser, menjalankan migration, serta menjalankan unit test. Dengan cara tersebut, AI saya gunakan sebagai alat bantu belajar dan debugging, sementara keputusan akhir mengenai implementasi tetap saya lakukan berdasarkan pemahaman dan kebutuhan project.

---

## Pengembangan Mingguan

### Minggu 1

- Membuat struktur dasar website menggunakan HTML5.
- Membuat halaman Profile/About Me.
- Menambahkan Education.
- Membuat styling menggunakan CSS3.
- Menerapkan Flexbox dan CSS Grid.
- Menambahkan responsive design menggunakan media query.
- Menambahkan Skills dan Experience.
- Menambahkan link GitHub, LinkedIn, dan Email.
- Melakukan perbaikan visual dan pengecekan tampilan website.

### Minggu 2

- Mengembangkan website menggunakan Django.
- Membuat model `Project` untuk menyimpan data project.
- Menambahkan migration untuk model `Project`.
- Menambahkan data project ke database.
- Membuat view `show_projects` untuk mengambil data dari database.
- Membuat template `projects.html` untuk menampilkan data project secara dinamis.
- Menggunakan looping DTL (`{% for %}`) untuk menampilkan setiap project.
- Menambahkan kondisi empty state ketika belum terdapat project.
- Menambahkan URL `/projects/` dan navigasi menuju halaman Projects.
- Membuat unit test untuk model dan halaman Projects.
- Melakukan pengecekan dan pengujian website setelah fitur Projects ditambahkan.