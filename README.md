# Portfolio Website - Tugas 1, Tugas 2 & Tugas 3 PBP

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