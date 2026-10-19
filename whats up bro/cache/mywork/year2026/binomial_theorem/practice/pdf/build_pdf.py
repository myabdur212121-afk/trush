"""Printable PDF of the EXACT narration text used for the TTS voice.
XeLaTeX · Noto Serif Bengali (Bangla) + CMU Serif (English).
Run:  python3 build_pdf.py   ->  Narration_Script.pdf"""
import pathlib, re, subprocess

HERE = pathlib.Path(__file__).parent
NAR = pathlib.Path('/home/user/project/narration')
BN = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')
PARTS = [
    ("p1", ["s1a", "s1b", "s2", "s3", "s4"], "ভূমিকা", "Intro"),
    ("p2", [f"{i:02d}" for i in range(1, 18)], "Combination", "অধ্যায় ১"),
    ("p3", [f"{i:02d}" for i in range(1, 18)], "Binomial Theorem", "অধ্যায় ২"),
    ("p4", [f"{i:02d}" for i in range(1, 20)], "Pascal's Triangle ও Summary", "অধ্যায় ৩ · সারাংশ"),
]
LATIN = re.compile(r"[A-Za-z][A-Za-z']*(?:[ ]+[A-Za-z][A-Za-z']*)*")


def esc(s):
    for a, b in (('\\', r'\textbackslash{}'), ('&', r'\&'), ('%', r'\%'), ('$', r'\$'),
                 ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}')):
        s = s.replace(a, b)
    return s


def tex(s):
    """escape + put English words in CMU Serif"""
    return LATIN.sub(lambda m: r'\en{' + m.group(0) + '}', esc(s))


out = []
for pi, (pre, ids, title, sub) in enumerate(PARTS, 1):
    out.append(rf"\npart{{{pi}}}{{{tex(sub)}}}{{{tex(title)}}}{{{str(len(ids)).translate(BN)}}}")
    for ci, i in enumerate(ids, 1):
        cid = f"{pre}_{i}"
        lines = [l.strip() for l in (NAR / f"{cid}.txt").read_text(encoding='utf-8').splitlines() if l.strip()]
        out.append(rf"\clip{{{f'{ci:02d}'.translate(BN)}}}{{{esc(cid)}}}")
        out += [rf"\sline{{{tex(l)}}}" for l in lines]
        out.append(r"\clipend")

doc = r"""\documentclass[paper=a4,fontsize=12pt,parskip=false]{scrartcl}
\usepackage[top=14mm,bottom=16mm,left=16mm,right=16mm,headheight=14pt,headsep=4mm,footskip=8mm]{geometry}
\usepackage{fontspec,xcolor,fancyhdr,needspace}
\setmainfont{NotoSerifBengali}[Path=fonts/,Extension=.ttf,UprightFont=*-Regular,BoldFont=*-Bold,Script=Bengali]
\newfontfamily\cmu{cmun}[Path=fonts/,Extension=.ttf,UprightFont=*rm,BoldFont=*bx,ItalicFont=*ti,Scale=1.12]
\newfontfamily\bnsemi{NotoSerifBengali-SemiBold}[Path=fonts/,Extension=.ttf,Script=Bengali]
\newcommand\en[1]{{\cmu #1}}
\definecolor{ink}{HTML}{111111}\definecolor{mute}{HTML}{6E6A62}\definecolor{rule}{HTML}{D5CFC3}
\color{ink}
\linespread{1.32}\selectfont
\setlength\parindent{0pt}\setlength\parskip{0pt}
\raggedright
\pagestyle{fancy}\fancyhf{}
\renewcommand\headrulewidth{0pt}
\fancyhead[L]{\scriptsize\color{mute}\cmu Binomial Theorem \,·\, Narration Script}
\fancyhead[R]{\scriptsize\color{mute}\leftmark}
\fancyfoot[C]{\scriptsize\color{mute}\cmu\thepage}
\newcommand\npart[4]{\vspace{5mm}
  \markboth{\cmu Part #1}{}
  {\large\bfseries #3}\hspace{.8em}{\small\color{mute}\cmu Part #1\normalfont\,·\,#2\,·\,#4টি ক্লিপ}\par
  \vspace{.6mm}{\color{ink}\rule{\linewidth}{1pt}}\par\nobreak\vspace{1mm}\nobreak}
\newcommand\clip[2]{\vspace{1.6mm}
  \noindent{\color{mute}\raisebox{.1ex}{\framebox(7,7){}}}\hspace{.5em}{\bnsemi\small ক্লিপ #1}\hspace{.6em}{\scriptsize\color{mute}\cmu #2}\par\nobreak
  \vspace{.3mm}\nobreak}
\newcommand\sline[1]{\clubpenalty=0\hangindent=1.2em\hspace*{1.2em}\ignorespaces #1\par\vspace{.6mm}}
\newcommand\clipend{\vspace{.8mm}{\color{rule}\rule{\linewidth}{.4pt}}\par}
\begin{document}
\thispagestyle{fancy}
{\small\color{mute}\cmu\addfontfeatures{LetterSpace=10}NARRATION SCRIPT}\par
{\fontsize{20}{26}\selectfont\cmu\bfseries Binomial Theorem}\hspace{.6em}{\large — সংখ্যাগুলো আসলে কোথা থেকে আসে?}\par
{\scriptsize\color{mute} প্রতিটি লাইন একটি বাক্য \,·\, ``—'' চিহ্নে একটু থামুন \,·\, কোড (যেমন \cmu p2\_05\normalfont) = অডিও ফাইলের নাম\par}
\vspace{-2mm}
""" + "\n".join(out) + r"""
\end{document}
"""
(HERE / 'Narration_Script.tex').write_text(doc, encoding='utf-8')
for _ in range(2):
    r = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'Narration_Script.tex'],
                       cwd=HERE, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-3000:]); raise SystemExit(1)
for ext in ('aux', 'log', 'out'):
    (HERE / f'Narration_Script.{ext}').unlink(missing_ok=True)
print('OK', (HERE / 'Narration_Script.pdf').stat().st_size // 1024, 'KB')
