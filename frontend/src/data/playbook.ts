import type { PlaybookDay } from '../types';

export const PLAYBOOK_DAYS: PlaybookDay[] = [
  {
    day: 1,
    item: {
      id: 'Kardus bekas',
      en: 'An old cardboard box',
    },
    title: {
      id: 'Kotak kejutan',
      en: 'Surprise box',
    },
    steps: [
      {
        id: 'Masukkan tiga benda yang dikenal anak ke dalam kardus: sendok plastik, cangkir, bola kecil.',
        en: 'Put three things your child knows into the box: a plastic spoon, a cup, a small ball.',
      },
      {
        id: 'Keluarkan satu per satu dan sebutkan namanya dengan jelas dua kali: “sendok, sendok”.',
        en: 'Take them out one at a time and say each name clearly twice: “spoon, spoon.”',
      },
      {
        id: 'Diam lima detik dan beri anak kesempatan menirukan bunyi apa pun.',
        en: 'Pause for five seconds and let your child copy any sound.',
      },
    ],
  },
  {
    day: 2,
    item: {
      id: 'Dua cangkir dan sendok plastik',
      en: 'Two cups and a plastic spoon',
    },
    title: {
      id: 'Tuang dan “lagi”',
      en: 'Pour and “more”',
    },
    steps: [
      {
        id: 'Duduk berhadapan, lalu tuang air atau beras dari cangkir ke cangkir.',
        en: 'Sit face to face and pour water or rice from cup to cup.',
      },
      {
        id: 'Ucapkan satu kata kunci untuk tiap gerakan: “tuang”, “habis”, “lagi”.',
        en: 'Say one key word for each move: “pour,” “all gone,” “more.”',
      },
      {
        id: 'Berhenti sebelum menuang lagi, supaya anak memintanya dengan suara atau isyarat.',
        en: 'Stop before pouring again so your child asks with a sound or a gesture.',
      },
    ],
  },
  {
    day: 3,
    item: {
      id: 'Bungkus makanan bergambar dan kardus',
      en: 'Picture food wrappers and a box',
    },
    title: {
      id: 'Mana yang…?',
      en: 'Which one…?',
    },
    steps: [
      {
        id: 'Gunting tiga gambar benda sehari-hari dari bungkus makanan dan tempel di kardus.',
        en: 'Cut three everyday pictures from food wrappers and stick them on the box.',
      },
      {
        id: 'Tanya “Mana kucing?” dan biarkan anak menunjuk. Puji setiap tunjukannya.',
        en: 'Ask “Where is the cat?” and let your child point. Praise every point.',
      },
      {
        id: 'Tunjuk gambar dan tanya “Ini apa?”, lalu tunggu. Terima tebakan apa adanya dan ulangi kata yang benar.',
        en: 'Point to a picture and ask “What is this?” then wait. Accept any attempt and repeat the right word.',
      },
    ],
  },
];
