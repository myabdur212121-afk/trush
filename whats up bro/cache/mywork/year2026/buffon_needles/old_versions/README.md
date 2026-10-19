# পুরোনো Buffon's Needle সংস্করণ (castom_manimlib repo থেকে)

`paper_lib.py`-এর থেকে **আলাদা** implementation (মাত্র ৫% মিল), তাই রাখা হলো:
- `neddle.py`: `BuffonsNeedleAnimationOnly` (ThreeDScene, silver needle, টেবিল)
- `buffons_neddle_info.py`: `BuffonsNeedleFullIntro` (পূর্ণ intro scene)

⚠️ `neddle.py` `buffons_needle_intro` import করে। ওই helper-গুলো `buffons_neddle_info.py`-তে আছে, তাই চালাতে হলে import-এর নাম বদলাতে হবে।
