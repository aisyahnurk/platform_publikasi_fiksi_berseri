import { useState, useEffect } from 'react';
import api from './api';
import './App.css';

function App() {
  // Data dummy sementara sebelum endpoint FastAPI dihubungkan
  const [stories, setStories] = useState([
    {
      id: 1,
      title: 'Senja di Stasiun Purwosari',
      author: 'Aisyah',
      genre: 'Romance / AU',
      chapters: 12,
      synopsis: 'Pertemuan singkat di peron kereta yang mengubah rutinitas harian.',
    },
    {
      id: 2,
      title: 'Kode Rahasia Tengah Malam',
      author: 'Amanda Nadhi',
      genre: 'Mystery / Thriller',
      chapters: 8,
      synopsis: 'Sebuah catatan misterius ditemukan di server kampus.',
    },
  ]);

  // Nanti tinggal buka komentar di bawah ini saat endpoint FastAPI sudah siap
  /*
  useEffect(() => {
    api.get('/stories')
      .then((res) => setStories(res.data))
      .catch((err) => console.error('Gagal mengambil data cerita:', err));
  }, []);
  */

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '24px', fontFamily: 'sans-serif' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #ddd', paddingBottom: '16px' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '24px' }}>📖 AksaraSeri</h1>
          <p style={{ margin: '4px 0 0', color: '#666', fontSize: '14px' }}>Platform Publikasi Fiksi Berseri & AU</p>
        </div>
        <button style={{ padding: '8px 16px', backgroundColor: '#2563eb', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
          + Tulis Cerita
        </button>
      </header>

      <main style={{ marginTop: '24px' }}>
        <h2 style={{ fontSize: '18px', marginBottom: '16px' }}>Daftar Fiksi Berseri Terbaru</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '16px' }}>
          {stories.map((story) => (
            <div key={story.id} style={{ border: '1px solid #e5e7eb', borderRadius: '8px', padding: '16px', backgroundColor: '#fff' }}>
              <span style={{ fontSize: '12px', backgroundColor: '#eff6ff', color: '#1d4ed8', padding: '4px 8px', borderRadius: '4px' }}>
                {story.genre}
              </span>
              <h3 style={{ margin: '12px 0 6px', fontSize: '17px' }}>{story.title}</h3>
              <p style={{ margin: '0 0 12px', fontSize: '13px', color: '#555' }}>Oleh: <strong>{story.author}</strong> • {story.chapters} Bab</p>
              <p style={{ margin: '0 0 16px', fontSize: '14px', color: '#333', lineHeight: '1.4' }}>{story.synopsis}</p>
              <button style={{ width: '100%', padding: '8px', backgroundColor: '#f3f4f6', border: '1px solid #d1d5db', borderRadius: '6px', cursor: 'pointer' }}>
                Baca Sekarang
              </button>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;