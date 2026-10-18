# Music assets

সব music-ই এই package-এর `tools/make_music.py` দিয়ে code থেকে তৈরি।
কোনোটি অন্য কারও বিদ্যমান track-এর copy নয়।

## এখন যা আছে

| ফাইল | দৈর্ঘ্য | অবস্থা / ব্যবহার |
|---|---:|---|
| `background/background_factorial_full_03m41s.mp3` | প্রায় 03:41.7 | Factorial final video-তে সত্যিই ব্যবহৃত পুরো background track (MP3 রূপ) |
| `intro/intro_soft_piano_08s.mp3` | প্রায় 8.0s | ভবিষ্যতের জন্য একই generator-এর `--preset intro` দিয়ে তৈরি; Factorial-এ আলাদা করে ব্যবহৃত হয়নি |
| `outro/outro_soft_piano_12s.mp3` | প্রায় 12.0s | ভবিষ্যতের জন্য `--preset outro` দিয়ে তৈরি; শেষ bar-এ Cmaj7-তে resolve করে; Factorial-এ আলাদা করে ব্যবহৃত হয়নি |

> Factorial-এর মাঝখান ও শেষের logo অংশে আলাদা intro/outro ফাইল বাজানো
> হয়নি। পুরো ভিডিও জুড়ে একটানা background track-ই ছিল; voice না থাকায়
> ducking ছেড়ে দিলে সেটাই সেখানে একটু সামনে শোনা গেছে।

## নতুন music বানানো

```bash
# যেকোনো দৈর্ঘ্যের background (WAV)
python tools/make_music.py 660 background_11min.wav

# Intro / outro
python tools/make_music.py 8  intro.wav  --preset intro
python tools/make_music.py 12 outro.wav  --preset outro

# WAV থেকে MP3
ffmpeg -i background_11min.wav -codec:a libmp3lame -b:a 256k background_11min.mp3
```

একই `--seed` (default 7) ব্যবহার করলে প্রতিবার একই music পাওয়া যাবে।
আলাদা layer (stem) লাগলে একই duration/seed/preset রেখে তিনবার চালাও;
mix-এর ভারসাম্য রাখতে `--peak 0` ব্যবহার করো:

```bash
python tools/make_music.py 60 piano.wav --only piano --peak 0
python tools/make_music.py 60 pad.wav   --only pad   --peak 0
python tools/make_music.py 60 bass.wav  --only bass  --peak 0
```

বিস্তারিত: [`../docs/bn/01-music-system.md`](../docs/bn/01-music-system.md)
