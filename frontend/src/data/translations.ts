export const UI_STRINGS = {
  appName: 'Nurtura',
  tagline: 'AI Co-Parenting & Early Development',
  competitionBadge: {
    event: 'Google Cloud AI Builder Cup 2026',
    category: 'Sustainability and Social Impact',
  },
  nav: {
    problem: { id: 'Masalah', en: 'Problem' },
    module1: { id: 'Modul 1', en: 'Module 1' },
    module2: { id: 'Modul 2', en: 'Module 2' },
    scanner: { id: 'AI Vision Scanner', en: 'AI Vision Scanner' },
  },
  hero: {
    title: 'Nurtura',
    lead: {
      id: 'Pendamping orang tua berbasis AI yang mengubah catatan tumbuh kembang menjadi tindakan kecil setiap hari: stimulasi bermain dan pengoptimal gizi MPASI anti-stunting.',
      en: 'An AI co-parenting companion that turns growth tracking into small daily actions: stimulation ideas from home goods and anti-stunting nutrition optimization for complementary feeding.',
    },
    ctaMod1: { id: 'Lihat Modul 1', en: 'See Module 1' },
    ctaMod2: { id: 'Lihat Modul 2', en: 'See Module 2' },
    facts: [
      { id: 'Usia 0–60 bulan', en: 'Ages 0–60 months' },
      { id: 'Rujukan WHO dan CDC', en: 'WHO and CDC guidance' },
      { id: 'Bahan dari dapur dan rak rumah', en: 'Materials from your kitchen and shelves' },
    ],
  },
  problem: {
    label: { id: 'Masalah', en: 'The problem' },
    lead: {
      id: 'Seribu hari pertama sampai usia lima tahun, <em>0–60 bulan</em>, menentukan arah kognitif dan fisik anak. Namun sebagian besar keluarga hanya memiliki dua titik pantau yang berjarak.',
      en: 'From the first 1,000 days through age five, <em>0–60 months</em>, a child’s cognitive and physical trajectory is set. Yet most families only get two distant check-ins.',
    },
    cards: [
      {
        type: 'a',
        title: { id: 'Mencatat tanpa arahan', en: 'Tracking without guidance' },
        desc: {
          id: 'Grafik pertumbuhan dan aplikasi parenting hanya mencatat berat dan tinggi badan. Ketika balita menunjukkan keterlambatan bicara ringan atau motorik halus yang lambat, orang tua dibiarkan bingung tanpa stimulasi harian terarah.',
          en: 'Growth charts and parenting apps only log weight and height. When a toddler shows a subtle delay in speech or fine motor skills, parents are left guessing without actionable daily stimulation.',
        },
      },
      {
        type: 'b',
        title: { id: 'MPASI dan risiko stunting', en: 'Complementary feeding and stunting' },
        desc: {
          id: 'Orang tua sulit menilai dengan mata apakah menu harian cukup protein hewani dan lemak sehat, atau justru teksturnya terlalu halus sehingga menghambat refleks mengunyah anak.',
          en: 'Parents struggle to judge by eye whether daily meals have enough animal protein and healthy fats, or whether pureeing too long delays chewing and speech readiness.',
        },
      },
    ],
    bridge: {
      text: {
        id: 'Nurtura menjembatani standar pediatrik klinis dan pengasuhan sehari-hari. Catatan pasif berubah menjadi kurikulum bermain tiga hari dan audit nutrisi visual secara instan.',
        en: 'Nurtura bridges clinical pediatric standards and everyday parenting, turning passive tracking into a 3-day play curriculum and instant visual nutrition audits.',
      },
      caption: {
        id: 'Jutaan orang tua di kawasan JAPAC menghadapi dua hambatan ini.',
        en: 'Millions of parents across JAPAC face these two hurdles.',
      },
    },
  },
  module1: {
    label: { id: 'Modul 1', en: 'Module 1' },
    title: 'Milestone & Daily Playbook Agent',
    sub: {
      id: 'Dari pengamatan orang tua ke rencana bermain tiga hari',
      en: 'From parent observations to a three-day play plan',
    },
    features: [
      {
        title: { id: 'Evaluasi sesuai konteks', en: 'Context-aware evaluation' },
        desc: {
          id: 'Mencocokkan pengamatan dan daftar milestone orang tua dengan panduan perkembangan WHO dan CDC, lengkap dengan batasan keamanan.',
          en: 'Matches parental observations and milestones against WHO and CDC developmental guidance, with clear safety thresholds.',
        },
      },
      {
        title: { id: 'Playbook stimulasi 3 hari', en: '3-day stimulation playbook' },
        desc: {
          id: 'Bukan teks medis umum. Nurtura menyusun kurikulum rumah mini selama tiga hari, hanya dari barang yang sudah ada di rumah: kardus, cangkir plastik, sendok, dan majalah bekas.',
          en: 'Not generic medical prose. Nurtura drafts a three-day home curriculum using everyday household objects: boxes, plastic cups, spoons, and food wrappers.',
        },
      },
    ],
    evalCard: {
      title: { id: 'Evaluasi hari ini', en: 'Today’s evaluation' },
      ageMonths: 18,
      ageLabel: { id: 'bulan', en: 'months' },
      noteLabel: { id: 'Catatan orang tua', en: 'Parent’s note' },
      note: {
        id: 'Baru bilang “mama”, “papa”, dan “num” untuk minum. Lebih sering menunjuk dan menarik tangan saya kalau mau sesuatu.',
        en: 'Only says “mama”, “papa”, and “num” for water. Mostly points and pulls my hand when wanting something.',
      },
      ref: {
        id: 'Rujukan: milestone CDC usia 18 bulan, mencoba mengucapkan tiga kata atau lebih selain mama/papa.',
        en: 'Reference: CDC 18-month milestone, tries to say three or more words besides mama/papa.',
      },
      statusTitle: { id: 'Perlu dipantau', en: 'Worth watching' },
      statusDesc: {
        id: 'Baru satu kata di luar mama dan papa, sedikit di bawah rujukan. Menunjuk sudah baik. Stimulasi artikulasi kata sederhana selama tiga hari.',
        en: 'One word beyond mama and papa, slightly below milestone reference. Pointing is strong. Stimulate simple word production over three days.',
      },
      safety: {
        id: 'Jika tiga hari ini tidak mengubah apa pun, atau anak berhenti mengucapkan kata yang pernah ia kuasai, konsultasikan ke dokter anak.',
        en: 'If these three days bring no change, or your child loses words they once had, check in with your pediatrician.',
      },
    },
    playCard: {
      title: { id: 'Playbook 3 hari: bicara', en: '3-day playbook: speech' },
      dayLabel: { id: 'Hari', en: 'Day' },
      progressSummary: {
        id: (done: number, total: number) => `${done} dari ${total} langkah selesai`,
        en: (done: number, total: number) => `${done} of ${total} steps completed`,
      },
      completedBanner: {
        id: 'Hebat! Semua langkah 3 hari ini telah selesai. Anak Anda mendapat stimulasi yang konsisten!',
        en: 'Awesome! All 3-day steps are completed. Your child received consistent, focused stimulation!',
      },
    },
  },
  module2: {
    label: { id: 'Modul 2', en: 'Module 2' },
    title: 'Smart Plate Vision',
    sub: {
      id: 'Pengoptimal gizi multimodal untuk piring bayi dan balita',
      en: 'Multimodal nutrition optimizer for baby and toddler plates',
    },
    features: [
      {
        title: { id: 'Audit piring instan', en: 'Instant plate audit' },
        desc: {
          id: 'Orang tua mengunggah foto makanan bayi atau balita.',
          en: 'Parents upload a photo of the baby or toddler meal.',
        },
      },
      {
        title: { id: 'Cek tekstur oral-motor', en: 'Oral-motor texture check' },
        desc: {
          id: 'Menilai apakah tekstur, dari saring sampai makanan keluarga, cocok dengan usia anak dalam bulan.',
          en: 'Evaluates whether the texture—puree to family food—fits the child’s age in months.',
        },
      },
      {
        title: { id: 'Meter makro anti-stunting', en: 'Anti-stunting macro meter' },
        desc: {
          id: 'Memeriksa protein hewani, lemak sehat, dan karbohidrat.',
          en: 'Audits animal protein, healthy fats, and carbohydrates.',
        },
      },
      {
        title: { id: 'Agen perbaikan makan berikutnya', en: 'Next-meal improvisation agent' },
        desc: {
          id: 'Peningkatan hemat dan resep penguat 5 menit untuk menutup kekurangan gizi.',
          en: 'Budget-friendly swaps and 5-minute booster recipes to cover nutritional gaps.',
        },
      },
    ],
    lab: {
      title: { id: 'Coba piring contoh', en: 'Try a sample plate' },
      tag: {
        id: 'Simulasi. Di Nurtura, isi piring dibaca dari foto.',
        en: 'Simulation. In Nurtura, plate contents are read from photos.',
      },
      plateLegend: { id: 'Isi piring', en: 'On the plate' },
      ageLegend: { id: 'Usia anak', en: 'Child’s age' },
      textureLegend: { id: 'Tekstur makanan', en: 'Food texture' },
      textureHead: { id: 'Tekstur', en: 'Texture' },
      macroHead: { id: 'Meter makro', en: 'Macro meter' },
      nextMealHead: { id: 'Makan berikutnya', en: 'Next meal booster' },
      aiScanBtn: { id: 'Coba Scan Foto MPASI (AI Vision)', en: 'Try AI Vision Photo Scanner' },
    },
  },
  footer: {
    wordmark: 'Nurtura',
    tagline: 'AI Co-Parenting & Early Development',
    competition: {
      id: 'Dibuat untuk Google Cloud AI Builder Cup 2026.',
      en: 'Built for Google Cloud AI Builder Cup 2026.',
    },
    disclaimer: {
      id: 'Contoh interaktif di halaman ini adalah simulasi dan bukan pengganti pemeriksaan oleh tenaga kesehatan profesional.',
      en: 'Interactive samples on this page are illustrative and do not replace personalized care from licensed healthcare professionals.',
    },
  },
};
