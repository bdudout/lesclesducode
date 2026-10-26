"""Génère les 91 illustrations SVG des mots-référents (style commun : traits épais, aplats)."""
import json, math, os, sys

ROOT = sys.argv[1]
C = dict(D="#2b2118", R="#e63946", O="#f77f00", Y="#ffd166", G="#52b788", DG="#2d6a4f",
         B="#3a86ff", LB="#a2d2ff", P="#8338ec", BR="#a0522d", LBR="#d4a373", SK="#f6c9a0",
         GR="#9aa0a6", PK="#ffafcc", W="#ffffff", GO="#e9b949")

def svg(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            '<g fill="none" stroke="#2b2118" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
            + body.format(**C) + '</g></svg>\n')

def crayon(col, fonce):
    """Une couleur : le trait d'un crayon de couleur, et le crayon qui l'a tracé."""
    return (trait("M10 74 Q20 50 32 66 Q44 84 56 62", col, 11)
            + '<g transform="translate(58 60) rotate(-40)">'
              '<path d="M0 0 L16 -8 L16 8Z" fill="#f2d4a7"/>'
              f'<path d="M0 0 L6 -3 L6 3Z" fill="{col}" stroke-width="2"/>'
              f'<rect x="16" y="-8" width="40" height="16" rx="2" fill="{col}"/>'
              f'<path d="M24 -8 L24 8 M48 -8 L48 8" stroke="{fonce}" stroke-width="2"/>'
              f'<rect x="56" y="-8" width="6" height="16" rx="2" fill="{fonce}"/></g>')

def trait(d, col, w=9):
    # chiffre ou trait épais : contour sombre puis couleur
    return f'<path d="{d}" stroke="#2b2118" stroke-width="{w + 6}"/><path d="{d}" stroke="{col}" stroke-width="{w}"/>'

def coeur(x, y, s, col):
    return (f'<path d="M{x} {y + s * .9} C{x - s * 1.6} {y - s * .2} {x - s * .6} {y - s * 1.3} {x} {y - s * .3} '
            f'C{x + s * .6} {y - s * 1.3} {x + s * 1.6} {y - s * .2} {x} {y + s * .9}Z" fill="{col}" stroke-width="2"/>')

def goutte(x, y, col):
    return f'<path d="M{x} {y} Q{x - 7} {y + 11} {x} {y + 15} Q{x + 7} {y + 11} {x} {y}Z" fill="{col}" stroke-width="2"/>'

def etoile(cx, cy, r, col):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * .45
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{col}" stroke-width="2"/>'

def criniere():
    pts = []
    for i in range(24):
        a = i * math.pi / 12
        rr = 40 if i % 2 == 0 else 33
        pts.append(f"{50 + rr * math.cos(a):.1f},{52 + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="#bc6c25"/>'

def petales():
    s = ""
    for i in range(6):
        a = i * math.pi / 3
        s += f'<circle cx="{50 + 15 * math.cos(a):.1f}" cy="{38 + 15 * math.sin(a):.1f}" r="11" fill="{{PK}}"/>'
    return s

def graduations():
    s = ""
    for i, x in enumerate(range(16, 86, 6)):
        h = 10 if i % 2 == 0 else 6
        s += f'<path d="M{x} 37 L{x} {37 + h}" stroke-width="2"/>'
    return s

def dents_peigne():
    return "".join(f'<rect x="{x}" y="40" width="4" height="34" rx="2" fill="#ff8fab" stroke-width="2"/>' for x in range(14, 86, 7))

def perforations():
    s = ""
    for t in range(14, 87, 8):
        for (x, y) in [(t, 14), (t, 86), (14, t), (86, t)]:
            s += f'<circle cx="{x}" cy="{y}" r="3" fill="#fff" stroke="none"/>'
    return s

def ballon_foot():
    """Ballon de football : pentagone noir au centre, pentagones partiels au bord."""
    def penta(cx, cy, r, rot):
        return " ".join(f"{cx + r * math.cos(rot + i * 2 * math.pi / 5):.1f},{cy + r * math.sin(rot + i * 2 * math.pi / 5):.1f}" for i in range(5))
    s = '<clipPath id="c"><circle cx="50" cy="52" r="38"/></clipPath><circle cx="50" cy="52" r="38" fill="#fff"/>'
    s += f'<polygon points="{penta(50, 52, 13, -math.pi / 2)}" fill="{{D}}"/><g clip-path="url(#c)">'
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        x1, y1 = 50 + 13 * math.cos(a), 52 + 13 * math.sin(a)
        x2, y2 = 50 + 30 * math.cos(a), 52 + 30 * math.sin(a)
        s += f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke-width="2.5"/>'
        cx, cy = 50 + 40 * math.cos(a), 52 + 40 * math.sin(a)
        s += f'<polygon points="{penta(cx, cy, 12, a + math.pi)}" fill="{{D}}"/>'
    return s + '</g><circle cx="50" cy="52" r="38"/><path d="M26 36 Q30 28 38 25" stroke="#fff" stroke-width="4" opacity=".8"/>'

def spirale(cx, cy, tours, r_max):
    """Spirale d'Archimède (coquille d'escargot)."""
    pts = []
    for i in range(0, int(tours * 60) + 1):
        t = i / 60 * 2 * math.pi
        r = r_max * i / (tours * 60)
        pts.append(f"{cx + r * math.cos(t):.1f} {cy + r * math.sin(t):.1f}")
    return "M" + " L".join(pts)

def feston(cx, cy, rx, ry, n, creux, debut=0.0, fin=2 * math.pi):
    """Contour ondulé (feuilles de salade frisées) le long d'une ellipse."""
    pts = []
    pas = 120
    for i in range(pas + 1):
        t = debut + (fin - debut) * i / pas
        k = 1 - creux * (0.5 + 0.5 * math.cos(n * t))
        pts.append(f"{cx + rx * k * math.cos(t):.1f} {cy + ry * k * math.sin(t):.1f}")
    return "M" + " L".join(pts) + "Z"

def bord_dentele(x0, y0, x1, y1, r=2.6, pas=6.4):
    """Contour d'un timbre : rectangle aux bords dentelés (demi-cercles creusés)."""
    def cote(xa, ya, xb, yb):
        longueur = math.hypot(xb - xa, yb - ya)
        n = max(1, round(longueur / pas))
        dx, dy = (xb - xa) / n, (yb - ya) / n
        d = ""
        for i in range(n):
            mx, my = xa + dx * (i + .5), ya + dy * (i + .5)
            ux, uy = dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
            d += (f" L{mx - ux * r:.1f} {my - uy * r:.1f}"
                  f" A{r} {r} 0 0 0 {mx + ux * r:.1f} {my + uy * r:.1f}"
                  f" L{xa + dx * (i + 1):.1f} {ya + dy * (i + 1):.1f}")
        return d
    return (f"M{x0} {y0}" + cote(x0, y0, x1, y0) + cote(x1, y0, x1, y1)
            + cote(x1, y1, x0, y1) + cote(x0, y1, x0, y0) + "Z")

ALPHABET = {
 "a": '<clipPath id="c"><ellipse cx="50" cy="64" rx="24" ry="28"/></clipPath>'
      '<path d="M50 38 L36 10 L47 22 L50 4 L54 22 L66 10 L58 38Z" fill="{G}"/>'
      '<ellipse cx="50" cy="64" rx="24" ry="28" fill="{Y}"/>'
      '<g clip-path="url(#c)" stroke="#b5651d" stroke-width="2"><path d="M20 40 L80 100 M20 60 L70 110 M30 30 L90 90 M80 40 L20 100 M80 60 L30 110 M70 30 L10 90"/></g>'
      '<ellipse cx="50" cy="64" rx="24" ry="28"/>',
 "b": ballon_foot(),
 "c": '<path d="M40 24 Q30 8 18 12 M46 22 Q46 4 56 4 M50 26 Q64 12 74 18" stroke="{DG}" stroke-width="6"/>'
      '<path d="M26 34 Q42 14 60 30 L80 90 Z" fill="{O}"/>'
      '<path d="M38 44 L48 42 M46 60 L56 58 M56 74 L64 73" stroke-width="2"/>',
 "d": trait("M30 34 Q30 14 50 14 Q70 14 70 34 Q70 50 32 86 L72 86", "{B}"),
 "e": '<path d="M18 12 L40 36 L18 52Z" fill="{O}"/><path d="M82 12 L60 36 L82 52Z" fill="{O}"/>'
      '<path d="M12 40 Q50 22 88 40 Q80 70 50 88 Q20 70 12 40Z" fill="{O}"/>'
      '<path d="M26 56 Q40 52 50 62 Q60 52 74 56 Q66 76 50 88 Q34 76 26 56Z" fill="#fff"/>'
      '<circle cx="36" cy="48" r="4" fill="{D}"/><circle cx="64" cy="48" r="4" fill="{D}"/>'
      '<ellipse cx="50" cy="84" rx="6" ry="4" fill="{D}"/>',
 "f": '<path d="M24 88 L24 44 Q24 14 50 14 Q76 14 76 44 L76 88 L67 80 L58 88 L50 80 L42 88 L33 80 Z" fill="#fff"/>'
      '<ellipse cx="40" cy="42" rx="5" ry="7" fill="{D}"/><ellipse cx="60" cy="42" rx="5" ry="7" fill="{D}"/>'
      '<ellipse cx="50" cy="60" rx="6" ry="8" fill="{D}"/>',
 "g": '<ellipse cx="50" cy="86" rx="42" ry="6" fill="#e5e5e5"/>'
      '<rect x="16" y="56" width="68" height="28" rx="4" fill="{BR}"/>'
      '<path d="M16 60 Q16 52 24 52 L76 52 Q84 52 84 60 Q78 68 72 60 Q66 70 60 60 Q54 70 48 60 Q42 70 36 60 Q30 70 24 60 Q20 66 16 60Z" fill="{PK}"/>'
      '<rect x="28" y="34" width="44" height="20" rx="4" fill="{BR}"/>'
      '<path d="M28 40 Q28 32 34 32 L66 32 Q72 32 72 40 Q66 46 60 40 Q55 46 50 40 Q45 46 40 40 Q34 46 28 40Z" fill="{PK}"/>'
      '<rect x="46" y="14" width="8" height="18" rx="2" fill="{B}"/><path d="M50 3 Q57 10 50 14 Q43 10 50 3Z" fill="{Y}" stroke-width="2"/>',
 "h": # « on ne l'entend pas » : une oreille, avec un badge rouge barré
      '<g transform="translate(-8 0)">'
      '<path d="M34 30 Q36 8 60 8 Q86 10 84 40 Q82 58 68 66 Q60 72 60 82 Q60 94 48 94 Q38 94 38 84 Q38 74 32 64 Q26 50 34 30Z" fill="{SK}"/>'
      '<path d="M46 32 Q50 20 62 22 Q74 25 72 40 Q70 52 60 56" stroke-width="3.5"/>'
      '<path d="M52 44 Q56 37 62 41 Q64 49 56 53 Q50 57 52 67" stroke-width="3"/></g>'
      '<circle cx="76" cy="76" r="19" fill="{R}"/>'
      '<path d="M67 67 L85 85 M85 67 L67 85" stroke="#fff" stroke-width="6"/>',
 "i": crayon("#9aa0a6", "#6c757d"),
 "j": '<rect x="30" y="16" width="40" height="11" rx="3" fill="{P}"/>'
      '<path d="M30 27 L70 27 L88 82 Q50 92 12 82Z" fill="#c77dff"/>'
      '<path d="M42 27 L34 88 M58 27 L66 88 M50 27 L50 90" stroke-width="2"/>',
 "k": '<path d="M36 68 Q14 76 4 94 Q22 86 40 78Z" fill="{LBR}"/>'
      '<ellipse cx="44" cy="62" rx="18" ry="25" fill="{LBR}" transform="rotate(20 44 62)"/>'
      '<path d="M38 80 L26 93 L60 93 L56 82Z" fill="{LBR}"/>'
      '<ellipse cx="55" cy="16" rx="4" ry="10" fill="{LBR}" transform="rotate(-15 55 16)"/>'
      '<ellipse cx="62" cy="30" rx="12" ry="10" fill="{LBR}"/><ellipse cx="74" cy="34" rx="9" ry="6" fill="{LBR}"/>'
      '<circle cx="64" cy="27" r="2.5" fill="{D}"/><circle cx="82" cy="33" r="2" fill="{D}"/>'
      '<path d="M58 52 L70 60 M56 58 L66 66" stroke-width="4"/><path d="M40 66 Q48 76 56 66" stroke-width="2"/>',
 "l": '<rect x="10" y="28" width="12" height="58" rx="3" fill="{BR}"/><rect x="80" y="48" width="10" height="38" rx="3" fill="{BR}"/>'
      '<rect x="20" y="52" width="62" height="16" fill="#fff"/><rect x="40" y="50" width="42" height="20" rx="2" fill="{B}"/>'
      '<rect x="22" y="42" width="20" height="12" rx="5" fill="#fff"/><rect x="18" y="68" width="64" height="8" fill="{BR}"/>',
 "m": '<circle cx="22" cy="70" r="15" fill="{D}"/><circle cx="22" cy="70" r="6" fill="#ccc"/>'
      '<circle cx="78" cy="70" r="15" fill="{D}"/><circle cx="78" cy="70" r="6" fill="#ccc"/>'
      '<path d="M22 70 L40 52 L64 52 L78 70" stroke-width="5"/>'
      '<path d="M36 50 Q50 34 66 46 L62 58 L40 58Z" fill="{R}"/><rect x="22" y="42" width="22" height="8" rx="4" fill="{D}"/>'
      '<path d="M66 46 L70 28 L80 26" stroke-width="5"/><circle cx="76" cy="40" r="4" fill="{Y}"/>',
 "n": '<path d="M24 74 Q6 74 8 56 Q10 40 28 42 Q30 22 50 24 Q68 20 74 38 Q92 38 92 56 Q92 74 74 74Z" fill="#fff"/>'
      '<path d="M30 56 Q36 50 44 52" stroke="{LB}" stroke-width="3"/>',
 "o": '<path d="M50 32 Q30 20 18 40 Q10 64 30 84 Q40 92 50 86 Q60 92 70 84 Q90 64 82 40 Q70 20 50 32Z" fill="{R}"/>'
      '<path d="M50 32 Q50 20 56 10" stroke-width="4"/><path d="M54 22 Q66 6 80 12 Q70 26 54 22Z" fill="{G}"/>'
      '<ellipse cx="32" cy="50" rx="4" ry="9" fill="#fff" stroke="none" opacity=".7"/>',
 "p": '<path d="M36 34 Q28 60 36 80 Q44 94 58 88 Q68 80 64 60 Q66 40 62 30 Q50 22 36 34Z" fill="{SK}"/>'
      '<circle cx="35" cy="22" r="7" fill="{SK}"/><circle cx="47" cy="15" r="6" fill="{SK}"/><circle cx="57" cy="15" r="5" fill="{SK}"/>'
      '<circle cx="65" cy="20" r="4.5" fill="{SK}"/><circle cx="71" cy="28" r="4" fill="{SK}"/>',
 "q": trait("M68 14 L36 14 L32 46 Q44 38 56 40 Q72 44 72 62 Q72 86 50 86 Q36 86 30 76", "{O}"),
 "r": '<path d="M50 20 L50 10"/><circle cx="50" cy="8" r="4" fill="{R}"/>'
      '<rect x="30" y="20" width="40" height="28" rx="6" fill="#ced4da"/>'
      '<circle cx="42" cy="32" r="5" fill="{Y}"/><circle cx="58" cy="32" r="5" fill="{Y}"/><rect x="40" y="40" width="20" height="4" fill="{D}"/>'
      '<path d="M26 60 L12 76 M74 60 L88 76" stroke-width="6"/><path d="M38 84 L38 95 M62 84 L62 95" stroke-width="6"/>'
      '<rect x="26" y="52" width="48" height="32" rx="6" fill="#8d99ae"/><rect x="40" y="60" width="20" height="12" rx="2" fill="{B}"/>',
 "s": # salade : feuilles frisées vert tendre autour d'un cœur clair, nervures
      f'<path d="{feston(50, 58, 40, 32, 9, .12)}" fill="#6a994e"/>'
      f'<path d="{feston(50, 56, 31, 25, 8, .13)}" fill="#a7c957"/>'
      f'<path d="{feston(50, 54, 19, 15, 7, .15)}" fill="#dde5b6"/>'
      '<path d="M50 54 L28 70 M50 54 L72 70 M50 54 L50 84 M50 54 L22 52 M50 54 L78 52" stroke="#386641" stroke-width="2"/>',
 "t": '<rect x="16" y="44" width="8" height="42" rx="2" fill="{BR}"/><rect x="76" y="44" width="8" height="42" rx="2" fill="{BR}"/>'
      '<rect x="22" y="44" width="56" height="8" fill="#8b4513"/><rect x="8" y="34" width="84" height="11" rx="3" fill="{BR}"/>',
 "u": '<rect x="4" y="30" width="22" height="24" fill="{PK}"/><path d="M1 32 L15 16 L29 32Z" fill="{R}"/>'
      '<rect x="74" y="26" width="22" height="28" fill="{LB}"/><path d="M71 28 L85 12 L99 28Z" fill="{R}"/>'
      '<path d="M38 30 L62 30 L94 92 L6 92Z" fill="#6c757d"/>'
      '<path d="M50 36 L50 42 M50 52 L50 62 M50 72 L50 86" stroke="#fff" stroke-width="4"/>',
 "v": '<circle cx="24" cy="66" r="18" stroke-width="5"/><circle cx="76" cy="66" r="18" stroke-width="5"/>'
      '<path d="M24 66 L42 40 L66 40 L76 66 M42 40 L50 66 L66 40 M50 66 L24 66" stroke="{R}" stroke-width="5"/>'
      '<path d="M42 40 L40 32 M34 31 L48 31" stroke-width="5"/><path d="M66 40 L64 28 L74 26" stroke-width="5"/>',
 "w": '<path d="M2 92 L98 92" stroke-width="4"/>'
      '<rect x="10" y="30" width="80" height="46" rx="6" fill="#2a9d8f"/><rect x="6" y="24" width="88" height="9" rx="3" fill="#264653"/>'
      '<rect x="18" y="40" width="16" height="16" rx="2" fill="{LB}"/><rect x="42" y="40" width="16" height="16" rx="2" fill="{LB}"/>'
      '<rect x="66" y="40" width="16" height="16" rx="2" fill="{LB}"/>'
      '<circle cx="28" cy="82" r="8" fill="{D}"/><circle cx="72" cy="82" r="8" fill="{D}"/>',
 "x": '<path d="M8 44 L90 48 M8 70 L90 66" stroke="{BR}" stroke-width="6"/>'
      + "".join(f'<rect x="{12 + i * 13}" y="{56 - (56 - 5 * i) / 2:.0f}" width="10" height="{56 - 5 * i}" rx="2" fill="{c}"/>'
                for i, c in enumerate(["{R}", "{O}", "{Y}", "{G}", "{B}", "{P}"]))
      + '<path d="M58 94 L84 72" stroke-width="4"/><circle cx="87" cy="69" r="6" fill="{R}"/>',
 "y": '<path d="M30 14 L42 18 Q50 24 58 18 L70 14 L92 34 L80 46 L72 40 L72 88 L28 88 L28 40 L20 46 L8 34Z" fill="{LB}"/>'
      '<path d="M42 18 L50 30 L58 18" stroke-width="2.5"/>'
      '<circle cx="50" cy="42" r="3" fill="#fff"/><circle cx="50" cy="56" r="3" fill="#fff"/><circle cx="50" cy="70" r="3" fill="#fff"/>'
      + etoile(36, 54, 6, "{Y}") + etoile(62, 72, 6, "{Y}") + etoile(64, 40, 5, "{Y}"),
 "z": '<path d="M32 26 L26 6 L42 20Z" fill="#fff"/><path d="M68 26 L74 6 L58 20Z" fill="#fff"/>'
      '<path d="M30 20 Q50 10 70 20 Q78 50 66 74 L34 74 Q22 50 30 20Z" fill="#fff"/>'
      '<path d="M33 30 L43 33 M30 50 L42 52 M33 64 L42 63 M67 30 L57 33 M70 50 L58 52 M67 64 L58 63 M50 14 L50 26" stroke-width="5"/>'
      '<ellipse cx="50" cy="80" rx="18" ry="14" fill="#555"/><circle cx="44" cy="80" r="2.5" fill="{D}"/><circle cx="56" cy="80" r="2.5" fill="{D}"/>'
      '<circle cx="39" cy="41" r="3" fill="{D}"/><circle cx="61" cy="41" r="3" fill="{D}"/>'
      '<path d="M42 12 L46 4 L50 12 L54 4 L58 12" stroke-width="4"/>',
}

COMPLEXES = {
 "ou": crayon("{R}", "#9d0208"),
 "on": '<path d="M28 50 L8 32 L12 50 L8 68Z" fill="#ff8fab"/><path d="M72 50 L92 32 L88 50 L92 68Z" fill="#ff8fab"/>'
       '<ellipse cx="50" cy="50" rx="25" ry="19" fill="#ff4d6d"/><path d="M36 44 Q50 36 64 44 M36 56 Q50 64 64 56" stroke="#fff" stroke-width="3"/>',
 "eacute": '<path d="M36 60 L80 12 L92 8 L88 20 L40 64Z" fill="#dfe4ea"/><path d="M44 56 L84 14" stroke="#adb5bd" stroke-width="2"/>'
           '<rect x="20" y="58" width="34" height="9" rx="3" fill="{Y}" transform="rotate(45 37 62)"/>'
           '<path d="M33 67 L17 83" stroke="{D}" stroke-width="12"/><path d="M33 67 L17 83" stroke="{BR}" stroke-width="7"/><circle cx="14" cy="86" r="5" fill="{Y}"/>',
 "an": '<rect x="10" y="28" width="80" height="9" rx="2" fill="{BR}"/><rect x="10" y="41" width="80" height="9" rx="2" fill="{BR}"/>'
       '<path d="M22 50 L22 58 M78 50 L78 58 M16 68 L16 90 M84 68 L84 90" stroke-width="5"/>'
       '<rect x="6" y="57" width="88" height="11" rx="2" fill="{BR}"/>',
 "au": crayon("{Y}", "#e09f3e"),
 "in": '<ellipse cx="38" cy="26" rx="8" ry="22" fill="#fff"/><ellipse cx="62" cy="26" rx="8" ry="22" fill="#fff"/>'
       '<ellipse cx="38" cy="28" rx="3.5" ry="14" fill="{PK}" stroke="none"/><ellipse cx="62" cy="28" rx="3.5" ry="14" fill="{PK}" stroke="none"/>'
       '<circle cx="50" cy="64" r="27" fill="#fff"/><circle cx="40" cy="58" r="3.5" fill="{D}"/><circle cx="60" cy="58" r="3.5" fill="{D}"/>'
       '<path d="M46 66 L54 66 L50 71Z" fill="{PK}" stroke-width="2"/><path d="M50 71 L50 76 M44 78 Q50 82 56 78" stroke-width="2"/>'
       '<path d="M34 70 L16 66 M34 74 L16 78 M66 70 L84 66 M66 74 L84 78" stroke-width="1.5"/>',
 "ai": '<path d="M28 14 L72 14 L66 90 L34 90Z" fill="#e8f4ff"/><path d="M30 34 L70 34 L66 90 L34 90Z" fill="#fff"/>'
       '<path d="M30 34 Q40 40 50 34 Q60 40 70 34" stroke-width="2"/><path d="M38 48 L36 80" stroke="#cfe3ff" stroke-width="4"/>',
 "oi": '<path d="M22 52 L4 44 L8 62Z" fill="{B}"/><ellipse cx="46" cy="56" rx="28" ry="20" fill="{B}"/>'
       '<circle cx="70" cy="40" r="14" fill="{B}"/><path d="M30 52 Q46 40 60 56 Q44 68 30 52Z" fill="#1d4ed8"/>'
       '<path d="M82 37 L95 42 L82 47Z" fill="{O}"/><circle cx="72" cy="37" r="3" fill="{D}"/>'
       '<path d="M42 76 L40 90 M54 76 L56 90" stroke="{O}" stroke-width="4"/>',
 "ch": '<path d="M22 40 L24 10 L44 30Z" fill="#f4a261"/><path d="M78 40 L76 10 L56 30Z" fill="#f4a261"/>'
       '<ellipse cx="50" cy="56" rx="32" ry="28" fill="#f4a261"/>'
       '<ellipse cx="38" cy="50" rx="5" ry="7" fill="#8ac926"/><ellipse cx="62" cy="50" rx="5" ry="7" fill="#8ac926"/>'
       '<ellipse cx="38" cy="50" rx="1.5" ry="5" fill="{D}" stroke="none"/><ellipse cx="62" cy="50" rx="1.5" ry="5" fill="{D}" stroke="none"/>'
       '<path d="M46 62 L54 62 L50 67Z" fill="{PK}" stroke-width="2"/><path d="M50 67 Q44 74 40 70 M50 67 Q56 74 60 70" stroke-width="2"/>'
       '<path d="M30 64 L8 60 M30 68 L8 72 M70 64 L92 60 M70 68 L92 72" stroke-width="1.5"/>',
 "ion": criniere() + '<circle cx="31" cy="33" r="7" fill="{Y}"/><circle cx="69" cy="33" r="7" fill="{Y}"/>'
       '<circle cx="50" cy="54" r="26" fill="{Y}"/><circle cx="41" cy="48" r="3.5" fill="{D}"/><circle cx="59" cy="48" r="3.5" fill="{D}"/>'
       '<path d="M44 58 L56 58 L50 65Z" fill="#6b3e26"/><path d="M50 65 L50 70 M42 72 Q50 78 58 72" stroke-width="2"/>',
 "er1": '<rect x="24" y="10" width="58" height="80" rx="4" fill="{B}"/><rect x="36" y="26" width="36" height="18" rx="2" fill="#fff"/>'
        '<path d="M40 32 L68 32 M40 38 L60 38" stroke-width="2"/>'
        '<path d="M18 20 L30 20 M18 32 L30 32 M18 44 L30 44 M18 56 L30 56 M18 68 L30 68 M18 80 L30 80" stroke-width="4"/>',
 "en": trait("M14 30 L24 20 L24 80", "{P}", 7) + trait("M50 20 Q62 20 62 50 Q62 80 50 80 Q38 80 38 50 Q38 20 50 20Z", "{P}", 7)
       + trait("M80 20 Q92 20 92 50 Q92 80 80 80 Q68 80 68 50 Q68 20 80 20Z", "{P}", 7),
 "eau": '<ellipse cx="50" cy="72" rx="44" ry="11" fill="#6b4226"/><path d="M28 72 L30 28 Q50 20 70 28 L72 72Z" fill="#6b4226"/>'
        '<rect x="29" y="58" width="42" height="9" fill="{R}"/>',
 "ain": # main ouverte : les doigts prolongent exactement les bords de la paume
      trait("M35 50 L35 22", "{SK}", 10) + trait("M45 50 L45 12", "{SK}", 10)
      + trait("M55 50 L55 14", "{SK}", 10) + trait("M65 50 L65 24", "{SK}", 10)
      + trait("M31 72 L15 52", "{SK}", 11)
      + '<path d="M28.5 46 L71.5 46 L71.5 74 Q71.5 92 52 92 L48 92 Q28.5 92 28.5 74Z" fill="{SK}" stroke="none"/>'
      '<path d="M71.5 44 L71.5 74 Q71.5 92 52 92 L48 92 Q28.5 92 28.5 74 L28.5 66" fill="none"/>'
      '<path d="M40 72 Q50 78 60 72" stroke-width="2"/>',
 "egrave": '<g transform="rotate(-15 50 50)"><rect x="8" y="36" width="84" height="26" rx="3" fill="{Y}"/>' + graduations() + '</g>',
 "oin": # un point, simplement : gros et centré
      '<circle cx="50" cy="50" r="20" fill="{D}"/>',
 "ph": # phoque allongé, tête relevée, ballon sur le nez
      '<path d="M16 74 L2 66 Q4 78 2 90 L16 80Z" fill="#6c7a89"/>'
      '<path d="M14 76 Q12 62 32 60 Q50 58 60 46 Q66 30 76 28 Q90 28 88 42 Q86 54 78 62 Q70 78 52 84 Q32 90 14 76Z" fill="#8d99ae"/>'
      '<path d="M30 80 Q48 82 64 72" stroke="#c9d1db" stroke-width="5"/>'
      '<path d="M52 74 Q46 88 56 94 Q62 86 60 74Z" fill="#6c7a89"/>'
      '<circle cx="78" cy="38" r="3" fill="{D}"/><ellipse cx="88" cy="44" rx="3.5" ry="2.5" fill="{D}"/>'
      '<path d="M84 48 L96 46 M84 50 L96 52" stroke-width="1.5"/>'
      '<circle cx="86" cy="15" r="11" fill="{R}"/><path d="M75 15 Q86 9 97 15" stroke="#fff" stroke-width="3"/>',
 "or": '<path d="M18 64 L6 70 L18 72Z" fill="#a7c957"/>'
       '<rect x="22" y="60" width="13" height="18" rx="5" fill="#a7c957"/><rect x="64" y="60" width="13" height="18" rx="5" fill="#a7c957"/>'
       '<ellipse cx="88" cy="58" rx="10" ry="9" fill="#a7c957"/><circle cx="91" cy="55" r="2" fill="{D}"/>'
       '<path d="M14 66 Q18 24 50 24 Q82 24 86 66Z" fill="#6a994e"/>'
       '<path d="M40 38 L60 38 L66 52 L60 64 L40 64 L34 52Z" fill="#a7c957" stroke-width="2"/>'
       '<path d="M40 38 L32 28 M60 38 L68 28 M34 52 L18 52 M66 52 L82 52" stroke-width="2"/>',
 "ez": '<path d="M58 10 Q88 12 88 48 Q88 82 62 90 L44 90 L44 78 Q34 78 34 70 L34 64 Q28 64 30 58 L32 56 Q16 56 14 50 L34 32 Q38 14 58 10Z" fill="{SK}"/>'
       '<path d="M35 31 L13 49 Q12 56 22 57 L33 57" fill="#f08a8f" stroke-width="3"/>'
       '<path d="M58 10 Q88 12 88 48 Q80 30 64 30 Q50 26 40 30 Q44 14 58 10Z" fill="{BR}"/>'
       '<ellipse cx="68" cy="52" rx="6" ry="8" fill="{SK}"/><circle cx="46" cy="40" r="3" fill="{D}"/>'
       '<path d="M36 70 L44 69" stroke-width="2.5"/>',
 "eu": crayon("{B}", "#1d4ed8"),
 "ette": '<path d="M12 48 L4 38 M88 48 L96 38" stroke-width="4"/>'
         '<circle cx="29" cy="54" r="17" fill="{LB}" stroke-width="5"/><circle cx="71" cy="54" r="17" fill="{LB}" stroke-width="5"/>'
         '<path d="M46 50 Q50 44 54 50" stroke-width="4"/><path d="M20 48 Q24 42 30 42 M62 48 Q66 42 72 42" stroke="#fff" stroke-width="3"/>',
 "ein": '<rect x="4" y="40" width="92" height="20" rx="4" fill="{BR}"/>'
        '<circle cx="70" cy="50" r="2.2" fill="{D}"/><circle cx="78" cy="50" r="2.2" fill="{D}"/><circle cx="86" cy="50" r="2.2" fill="{D}"/>'
        '<rect x="28" y="32" width="26" height="36" rx="4" stroke="{D}" stroke-width="10"/><rect x="28" y="32" width="26" height="36" rx="4" stroke="{GO}" stroke-width="5"/>'
        '<path d="M28 50 L50 50" stroke-width="4"/>',
 "ecirc": # la tête : un gros plan du visage seul (le garçon, lui, est en pied)
      '<circle cx="14" cy="54" r="8" fill="{SK}"/><circle cx="86" cy="54" r="8" fill="{SK}"/>'
      '<circle cx="50" cy="52" r="38" fill="{SK}"/>'
      '<path d="M12 46 Q10 8 50 8 Q90 8 88 46 Q80 22 64 24 Q56 14 46 22 Q30 18 12 46Z" fill="#e9b949"/>'
      '<circle cx="36" cy="50" r="4.5" fill="{D}"/><circle cx="64" cy="50" r="4.5" fill="{D}"/>'
      '<path d="M50 54 L46 66 L53 66" stroke-width="2.5"/><path d="M36 76 Q50 86 64 76" stroke-width="3"/>'
      '<circle cx="28" cy="66" r="5" fill="{PK}" stroke="none" opacity=".7"/><circle cx="72" cy="66" r="5" fill="{PK}" stroke="none" opacity=".7"/>',
 "ui": trait("M50 46 Q34 46 34 31 Q34 16 50 16 Q66 16 66 31 Q66 46 50 46 Q30 46 30 66 Q30 86 50 86 Q70 86 70 66 Q70 46 50 46Z", "{G}"),
 "qu": trait("M62 86 L62 14 L26 64 L76 64", "{R}"),
 "eur": '<path d="M50 52 Q46 74 50 96" stroke="{DG}" stroke-width="5"/><path d="M50 80 Q64 64 76 70 Q66 84 50 80Z" fill="{G}"/>'
        + petales() + '<circle cx="50" cy="38" r="10" fill="{Y}"/>',
 "et": '<path d="M18 70 Q18 24 50 24 Q82 24 82 70Z" fill="{R}"/><path d="M36 30 Q30 46 30 66 M50 26 L50 66 M64 30 Q70 46 70 66" stroke="#c1121f" stroke-width="2"/>'
       '<rect x="14" y="64" width="72" height="18" rx="4" fill="#c1121f"/>'
       '<path d="M22 66 L22 80 M30 66 L30 80 M38 66 L38 80 M46 66 L46 80 M54 66 L54 80 M62 66 L62 80 M70 66 L70 80 M78 66 L78 80" stroke-width="1.5"/>'
       '<circle cx="50" cy="20" r="10" fill="#fff"/>',
 "euille": '<path d="M22 78 L10 90" stroke-width="4"/><path d="M22 78 Q16 28 82 16 Q88 72 22 78Z" fill="{G}"/>'
           '<path d="M22 78 L72 28 M38 62 L36 44 M48 52 L48 34 M58 42 L58 26 M38 62 L56 62 M48 52 L66 52 M58 42 L74 42" stroke-width="2"/>',
 "elle": '<path d="M50 8 L50 56" stroke="{D}" stroke-width="12"/><path d="M50 8 L50 56" stroke="{LBR}" stroke-width="7"/>'
         '<rect x="38" y="4" width="24" height="9" rx="4" fill="{LBR}"/>'
         '<path d="M32 52 L68 52 L68 76 Q50 100 32 76Z" fill="{B}"/>',
 "ien": '<ellipse cx="22" cy="50" rx="11" ry="24" fill="#6b3e26" transform="rotate(15 22 50)"/>'
        '<ellipse cx="78" cy="50" rx="11" ry="24" fill="#6b3e26" transform="rotate(-15 78 50)"/>'
        '<ellipse cx="50" cy="50" rx="28" ry="31" fill="{LBR}"/><ellipse cx="62" cy="42" rx="9" ry="8" fill="#6b3e26" stroke="none"/>'
        '<circle cx="39" cy="42" r="3.5" fill="{D}"/><circle cx="62" cy="42" r="3.5" fill="#fff" stroke="none"/><circle cx="62" cy="42" r="3" fill="{D}"/>'
        '<ellipse cx="50" cy="66" rx="17" ry="13" fill="#fff"/><path d="M46 76 Q50 90 54 76Z" fill="{PK}" stroke-width="2"/>'
        '<ellipse cx="50" cy="59" rx="6" ry="4.5" fill="{D}"/><path d="M50 63 L50 70 M42 70 Q50 76 58 70" stroke-width="2"/>',
 "ei": # reine : femme couronnée, cape rouge bordée d'hermine
      '<path d="M14 98 Q18 62 50 60 Q82 62 86 98Z" fill="{R}"/>'
      '<path d="M26 72 Q50 82 74 72 L74 80 Q50 90 26 80Z" fill="#fff"/>'
      '<circle cx="34" cy="78" r="1.6" fill="{D}" stroke="none"/><circle cx="46" cy="82" r="1.6" fill="{D}" stroke="none"/><circle cx="58" cy="81" r="1.6" fill="{D}" stroke="none"/><circle cx="68" cy="77" r="1.6" fill="{D}" stroke="none"/>'
      '<path d="M28 66 Q24 40 50 38 Q76 40 72 66Z" fill="#8b4513"/>'
      '<circle cx="50" cy="54" r="18" fill="{SK}"/><circle cx="44" cy="53" r="2.5" fill="{D}"/><circle cx="56" cy="53" r="2.5" fill="{D}"/>'
      '<path d="M44 62 Q50 66 56 62" stroke="{R}" stroke-width="2"/>'
      '<path d="M30 38 L30 12 L40 24 L50 6 L60 24 L70 12 L70 38Z" fill="{Y}"/>'
      '<circle cx="50" cy="28" r="4" fill="{R}" stroke-width="2"/><circle cx="37" cy="32" r="3" fill="{B}" stroke-width="2"/><circle cx="63" cy="32" r="3" fill="{B}" stroke-width="2"/>',
 "ill": '<ellipse cx="17" cy="54" rx="8" ry="15" fill="#6b3e26"/><ellipse cx="83" cy="54" rx="8" ry="15" fill="#6b3e26"/>'
        + coeur(20, 38, 6, "{PK}") + coeur(80, 38, 6, "{PK}")
        + '<path d="M30 94 L36 78 L64 78 L70 94Z" fill="{PK}"/>'
          '<circle cx="50" cy="52" r="25" fill="{SK}"/>'
          '<path d="M25 52 Q23 24 50 24 Q77 24 75 52 Q66 36 50 38 Q34 36 25 52Z" fill="#6b3e26"/>'
          '<circle cx="41" cy="54" r="3" fill="{D}"/><circle cx="59" cy="54" r="3" fill="{D}"/><path d="M42 64 Q50 70 58 64" stroke-width="2.5"/>',
 "gu": '<rect x="45" y="10" width="10" height="38" fill="#6b3e26"/><rect x="41" y="2" width="18" height="11" rx="2" fill="#6b3e26"/>'
       '<path d="M50 38 Q66 38 66 54 Q66 58 62 62 Q72 66 72 78 Q72 96 50 96 Q28 96 28 78 Q28 66 38 62 Q34 58 34 54 Q34 38 50 38Z" fill="{O}"/>'
       '<circle cx="50" cy="66" r="6" fill="#6b3e26"/><rect x="42" y="82" width="16" height="4" fill="#6b3e26" stroke-width="1.5"/>'
       '<path d="M48 10 L48 84 M52 10 L52 84" stroke-width="1"/>',
 "es": # escargot : coquille ronde à spirale, corps et cornes
      '<path d="M6 86 L80 86 Q94 86 92 72 L88 52 Q84 46 80 52 L78 74 L18 74 Q6 76 6 86Z" fill="#e9c46a"/>'
      '<path d="M84 50 L80 34 M88 50 L96 36" stroke-width="2.5"/><circle cx="80" cy="32" r="3.5" fill="{D}"/><circle cx="96" cy="34" r="3.5" fill="{D}"/>'
      '<circle cx="44" cy="48" r="28" fill="#bc6c25"/>'
      f'<path d="{spirale(44, 48, 2.6, 25)}" stroke="#7f4f24" stroke-width="3.5"/>'
      '<circle cx="44" cy="48" r="28"/>',
 "gn": dents_peigne() + '<rect x="10" y="26" width="80" height="18" rx="5" fill="#ff8fab"/>',
 "aille": '<path d="M28 4 L44 4 L58 46 L42 46Z" fill="{B}"/><path d="M72 4 L56 4 L42 46 L58 46Z" fill="{R}"/>'
          '<circle cx="50" cy="66" r="24" fill="{Y}"/><circle cx="50" cy="66" r="17" stroke="{GO}" stroke-width="3"/>' + etoile(50, 66, 12, "{GO}"),
 "erre": '<circle cx="50" cy="50" r="38" fill="{B}"/>'
         '<path d="M30 24 Q46 18 48 32 Q42 46 30 42 Q20 36 30 24Z" fill="{G}"/>'
         '<path d="M56 46 Q74 40 80 54 Q76 74 60 78 Q50 64 56 46Z" fill="{G}"/>'
         '<path d="M18 58 Q28 54 32 66 Q26 74 18 68Z" fill="{G}"/>',
 "ouille": '<path d="M50 28 Q50 14 60 8" stroke="{DG}" stroke-width="7"/>'
           '<ellipse cx="31" cy="60" rx="21" ry="30" fill="{O}"/><ellipse cx="69" cy="60" rx="21" ry="30" fill="{O}"/>'
           '<ellipse cx="50" cy="60" rx="20" ry="32" fill="#f8961e"/><path d="M56 22 Q70 12 80 22 Q68 30 56 22Z" fill="{G}"/>',
 "er2": crayon("{G}", "{DG}"),
 "eille": '<ellipse cx="40" cy="30" rx="12" ry="17" fill="#e0f2ff" transform="rotate(-20 40 30)"/>'
          '<ellipse cx="60" cy="30" rx="12" ry="17" fill="#e0f2ff" transform="rotate(20 60 30)"/>'
          '<path d="M20 58 L8 60 L20 62Z" fill="{D}"/>'
          '<ellipse cx="50" cy="58" rx="30" ry="20" fill="{Y}"/><path d="M38 41 L38 75 M54 38 L54 78" stroke-width="7"/>'
          '<path d="M86 46 L92 34 M80 46 L78 34" stroke-width="2"/><circle cx="83" cy="56" r="12" fill="{D}"/><circle cx="87" cy="53" r="2.5" fill="#fff" stroke="none"/>',
}

DOUBLES = {
 "cr": '<rect x="24" y="62" width="10" height="16" rx="3" fill="{G}"/><rect x="50" y="62" width="10" height="16" rx="3" fill="{G}"/>'
       '<path d="M2 62 Q20 44 50 46 L70 46 Q84 40 97 48 L97 58 L70 60 Q50 74 20 70 Q8 68 2 62Z" fill="{G}"/>'
       '<path d="M18 50 L22 43 L26 49 L30 42 L34 48 L38 41 L42 47" fill="{DG}" stroke-width="2"/>'
       '<circle cx="64" cy="40" r="7" fill="{G}"/><circle cx="65" cy="39" r="2.5" fill="{D}"/>'
       '<path d="M66 59 L69 64 L72 59 L75 64 L78 58 L81 63 L84 58 L87 62 L90 58" fill="#fff" stroke-width="1.5"/>'
       '<path d="M70 52 L96 52" stroke-width="2"/>',
 "br": # bras plié qui montre ses muscles
      '<rect x="2" y="56" width="20" height="30" rx="4" fill="{B}"/>'
      + trait("M20 72 L54 72 L62 30", "{SK}", 20)
      + '<ellipse cx="37" cy="59" rx="15" ry="12" fill="{SK}" stroke="none"/><path d="M21 63 Q36 40 52 61" fill="none"/>'
      '<circle cx="63" cy="22" r="13" fill="{SK}"/><path d="M56 18 L66 20 M56 25 L66 27" stroke-width="2"/>',
 "dr": '<path d="M30 50 L8 18 L20 26 L22 14 L32 28 L36 20 L42 44Z" fill="{DG}"/>'
       '<path d="M24 74 Q4 80 8 94 L14 86 Q20 84 32 80Z" fill="{G}"/>'
       '<ellipse cx="46" cy="64" rx="24" ry="22" fill="{G}"/><ellipse cx="50" cy="68" rx="12" ry="14" fill="{Y}"/>'
       '<path d="M42 62 L58 62 M42 70 L58 70" stroke-width="1.5"/>'
       '<path d="M57 24 L54 9 L64 20Z M68 22 L71 7 L75 23Z" fill="{Y}" stroke-width="2"/>'
       '<ellipse cx="65" cy="34" rx="16" ry="13" fill="{G}"/><ellipse cx="80" cy="38" rx="10" ry="8" fill="{G}"/>'
       '<circle cx="64" cy="31" r="3" fill="{D}"/><circle cx="86" cy="35" r="1.5" fill="{D}"/>'
       '<path d="M90 38 Q97 30 99 38 Q95 42 99 48 Q93 46 90 41Z" fill="{O}" stroke-width="2"/>',
 "fr": '<path d="M8 56 L72 26 L94 42Z" fill="#ffe8a3"/><path d="M8 56 L94 42 L94 74 L8 84Z" fill="{Y}"/>'
       '<ellipse cx="38" cy="68" rx="7" ry="6" fill="{GO}" stroke-width="2"/><ellipse cx="68" cy="58" rx="5" ry="4" fill="{GO}" stroke-width="2"/>'
       '<ellipse cx="78" cy="68" rx="3.5" ry="3" fill="{GO}" stroke-width="2"/><ellipse cx="66" cy="36" rx="4" ry="2.5" fill="{GO}" stroke-width="2"/>',
 "gr": '<circle cx="31" cy="34" r="14" fill="#80b918"/><circle cx="69" cy="34" r="14" fill="#80b918"/>'
       '<ellipse cx="50" cy="62" rx="40" ry="27" fill="#80b918"/>'
       '<circle cx="31" cy="33" r="8" fill="#fff"/><circle cx="69" cy="33" r="8" fill="#fff"/><circle cx="32" cy="34" r="4" fill="{D}"/><circle cx="68" cy="34" r="4" fill="{D}"/>'
       '<path d="M24 64 Q50 84 76 64" stroke-width="3"/><circle cx="20" cy="62" r="5" fill="{PK}" stroke="none"/><circle cx="80" cy="62" r="5" fill="{PK}" stroke="none"/>',
 "pr": '<path d="M50 28 Q50 16 56 10" stroke-width="4"/><path d="M54 18 Q66 4 80 10 Q70 24 54 18Z" fill="{G}"/>'
       '<ellipse cx="50" cy="60" rx="28" ry="32" fill="#7b2cbf"/><path d="M50 30 Q40 60 50 92" stroke="#5a189a" stroke-width="2"/>'
       '<ellipse cx="36" cy="52" rx="4" ry="9" fill="#fff" stroke="none" opacity=".4"/>',
 "tr": '<circle cx="70" cy="14" r="7" fill="#e5e5e5" stroke-width="2"/><circle cx="84" cy="6" r="5" fill="#e5e5e5" stroke-width="2"/>'
       '<path d="M62 44 L59 24 L75 24 L72 44Z" fill="{D}"/>'
       '<rect x="12" y="26" width="30" height="46" rx="3" fill="{R}"/><rect x="18" y="32" width="18" height="14" fill="{LB}"/>'
       '<rect x="8" y="20" width="38" height="8" rx="2" fill="{D}"/>'
       '<rect x="40" y="44" width="46" height="28" rx="6" fill="{B}"/><path d="M86 62 L97 80 L86 80Z" fill="#6c757d"/>'
       '<circle cx="26" cy="78" r="11" fill="{D}"/><circle cx="56" cy="80" r="9" fill="{D}"/><circle cx="76" cy="80" r="9" fill="{D}"/>'
       '<circle cx="26" cy="78" r="3" fill="#ccc"/><circle cx="56" cy="80" r="3" fill="#ccc"/><circle cx="76" cy="80" r="3" fill="#ccc"/>',
 "vr": '<path d="M4 28 L4 86 Q30 80 50 92 Q70 80 96 86 L96 28" fill="{R}"/>'
       '<path d="M50 30 Q30 18 8 24 L8 80 Q30 74 50 86Z" fill="#fff"/><path d="M50 30 Q70 18 92 24 L92 80 Q70 74 50 86Z" fill="#fff"/>'
       '<path d="M16 36 Q30 32 42 38 M16 46 Q30 42 42 48 M16 56 Q30 52 42 58 M16 66 Q30 62 42 68 M58 38 Q70 32 84 36 M58 48 Q70 42 84 46 M58 58 Q70 52 84 56 M58 68 Q70 62 84 66" stroke="#adb5bd" stroke-width="2"/>',
 "cl": '<path d="M44 45 L92 45 L92 55 L88 55 L88 66 L79 66 L79 55 L73 55 L73 63 L64 63 L64 55 L44 55Z" fill="{Y}"/>'
       '<path d="M8 50 a19 19 0 1 0 38 0 a19 19 0 1 0 -38 0 M20 50 a7 7 0 1 1 14 0 a7 7 0 1 1 -14 0" fill="{Y}" fill-rule="evenodd"/>',
 "bl": crayon("#ffffff", "#ced4da"),
 "fl": '<path d="M44 8 L56 8 L58 78 L64 92 L36 92 L42 78Z" fill="#f2e8cf"/><path d="M44 8 L56 8 L55 20 L45 20Z" fill="{LBR}"/>'
       '<rect x="46" y="24" width="8" height="4" fill="{D}"/>'
       '<circle cx="50" cy="38" r="3" fill="{D}"/><circle cx="50" cy="48" r="3" fill="{D}"/><circle cx="50" cy="58" r="3" fill="{D}"/>'
       '<circle cx="50" cy="68" r="3" fill="{D}"/><circle cx="50" cy="78" r="2.5" fill="{D}"/><path d="M40 82 L60 82" stroke-width="2"/>',
 "gl": '<clipPath id="c"><path d="M30 52 L70 52 L50 94Z"/></clipPath>'
       '<path d="M30 52 L70 52 L50 94Z" fill="#e9c46a"/>'
       '<g clip-path="url(#c)" stroke-width="1.5"><path d="M20 50 L70 100 M30 50 L80 100 M80 50 L30 100 M70 50 L20 100 M60 50 L10 100 M40 50 L90 100"/></g>'
       '<path d="M30 52 L70 52 L50 94Z"/>'
       '<circle cx="38" cy="45" r="14" fill="{PK}"/><circle cx="62" cy="45" r="14" fill="#a7c957"/><circle cx="50" cy="29" r="14" fill="#fff3b0"/>'
       '<circle cx="50" cy="12" r="5" fill="{R}"/>',
 "pl": '<path d="M22 50 Q8 50 10 38 Q12 26 26 28 Q30 12 50 14 Q66 10 72 26 Q88 26 88 40 Q88 50 76 50Z" fill="#cfd8e3"/>'
       + goutte(28, 58, "{B}") + goutte(50, 62, "{B}") + goutte(72, 58, "{B}") + goutte(38, 78, "{B}") + goutte(62, 80, "{B}"),
}

AUTRES = {
 "am": '<path d="M32 8 L68 8 L64 42 Q60 56 62 70 L64 80 L38 82 L40 70 Q34 56 34 42Z" fill="{SK}"/>'
       '<path d="M40 46 Q50 52 60 46" stroke-width="2.5"/><rect x="26" y="4" width="48" height="20" rx="4" fill="{B}"/>'
       '<path d="M36 78 L64 76 Q88 78 92 92 L36 94Z" fill="{R}"/><path d="M36 89 L92 89" stroke-width="2"/>',
 "ccedille": # garçon en pied, en marinière (pour ne pas le confondre avec « tête »)
      '<clipPath id="c"><path d="M38 46 Q50 41 62 46 L61 76 L39 76Z"/></clipPath>'
      '<path d="M44 74 L43 94 M56 74 L57 94" stroke-width="7"/><path d="M44 74 L43 94 M56 74 L57 94" stroke="#264653" stroke-width="3"/>'
      '<path d="M38 94 L47 94 M53 94 L62 94" stroke="{D}" stroke-width="5"/>'
      '<path d="M39 49 L30 66 M61 49 L70 66" stroke-width="7"/><path d="M39 49 L30 66 M61 49 L70 66" stroke="{SK}" stroke-width="3"/>'
      '<path d="M38 46 Q50 41 62 46 L61 76 L39 76Z" fill="#fff" stroke="none"/>'
      '<g clip-path="url(#c)" stroke="#1d3557" stroke-width="3.2"><path d="M30 51 L70 51 M30 57 L70 57 M30 63 L70 63 M30 69 L70 69 M30 75 L70 75"/></g>'
      '<path d="M38 46 Q50 41 62 46 L61 76 L39 76Z" fill="none"/>'
      '<circle cx="50" cy="26" r="16" fill="{SK}"/>'
      '<path d="M34 24 Q33 9 50 9 Q67 9 66 24 L61 17 L55 21 L50 14 L45 21 L39 17Z" fill="#6b3e26"/>'
      '<circle cx="44" cy="27" r="2.2" fill="{D}"/><circle cx="56" cy="27" r="2.2" fill="{D}"/><path d="M44 33 Q50 37 56 33" stroke-width="2"/>',
 "em": '<path d="M18 52 Q34 34 50 45 Q66 34 82 52 Q66 72 50 72 Q34 72 18 52Z" fill="{R}"/>'
       '<path d="M20 52 Q50 60 80 52" stroke-width="2"/>' + coeur(78, 22, 8, "{R}") + coeur(90, 40, 5, "{PK}"),
 "esse": # princesse : jeune fille au chapeau pointu à voile, robe rose
      '<path d="M50 6 L34 40 L66 40Z" fill="{PK}"/><path d="M50 6 Q70 20 82 56" stroke="#c77dff" stroke-width="3" opacity=".8"/>'
      '<path d="M28 94 Q24 58 50 56 Q76 58 72 94Z" fill="{PK}"/>'
      '<path d="M32 46 Q30 72 36 78 L64 78 Q70 72 68 46Z" fill="{Y}"/>'
      '<circle cx="50" cy="54" r="17" fill="{SK}"/><circle cx="44" cy="53" r="2.5" fill="{D}"/><circle cx="56" cy="53" r="2.5" fill="{D}"/>'
      '<path d="M45 61 Q50 65 55 61" stroke="{R}" stroke-width="2"/>'
      '<path d="M34 40 L66 40" stroke-width="4"/>',
 "ge": '<path d="M76 58 L96 50 L94 68Z" fill="#8d8d8d"/>'
       '<path d="M44 78 L42 90 M56 78 L58 90" stroke="#ff8fab" stroke-width="4"/>'
       '<ellipse cx="52" cy="58" rx="30" ry="22" fill="#b0b0b0"/><circle cx="25" cy="38" r="13" fill="#b0b0b0"/>'
       '<path d="M26 48 Q36 56 42 44 Q34 36 26 48Z" fill="#7bc8a4" stroke-width="2"/>'
       '<path d="M46 52 Q64 42 80 58 Q62 72 46 52Z" fill="#8d8d8d"/><path d="M58 56 L66 50 M62 60 L70 54" stroke-width="2"/>'
       '<path d="M13 36 L3 40 L13 43Z" fill="#555"/><circle cx="22" cy="35" r="3" fill="{O}" stroke-width="1.5"/>',
 "im": # timbre : bords dentelés, profil de femme au bonnet phrygien, aux couleurs du drapeau
      f'<path d="{bord_dentele(20, 12, 80, 88)}" fill="#fff"/>'
      '<rect x="27" y="19" width="46" height="62" fill="{R}" stroke-width="2"/>'
      '<path d="M58 30 Q44 28 40 40 Q39 44 41 47 L36 53 Q35 55 38 56 L40 57 Q38 60 41 61 Q39 64 42 65 '
      'Q43 70 50 70 L51 78 L68 78 L66 66 Q72 58 70 46 Q70 32 58 30Z" fill="#fff" stroke-width="2"/>'
      '<path d="M64 40 Q80 48 77 62 Q75 72 66 78 Q70 68 68 60 Q66 52 60 48Z" fill="#fff" stroke-width="2"/>'
      '<path d="M68 52 Q72 58 70 66" stroke-width="1.5"/>'
      '<path d="M41 39 Q42 22 58 22 Q70 23 72 34 Q73 42 68 46 Q66 38 58 36 Q48 34 41 39Z" fill="{B}" stroke-width="2"/>'
      '<circle cx="47" cy="47" r="1.6" fill="{D}" stroke="none"/>',
 "oeu_oeuf": '<path d="M50 10 Q76 10 80 56 Q80 90 50 90 Q20 90 20 56 Q24 10 50 10Z" fill="#fff8e1"/>'
             '<path d="M34 34 Q38 24 46 20" stroke="#fff" stroke-width="5"/>',
 "oeu_noeud": '<path d="M46 54 L32 88 L41 83 L46 90Z M54 54 L68 88 L59 83 L54 90Z" fill="#ff8fab"/>'
              '<path d="M50 50 L16 28 Q6 50 16 72Z" fill="{PK}"/><path d="M50 50 L84 28 Q94 50 84 72Z" fill="{PK}"/>'
              '<path d="M22 40 Q28 50 22 60 M78 40 Q72 50 78 60" stroke-width="2"/>'
              '<rect x="41" y="41" width="18" height="18" rx="5" fill="#ff8fab"/>',
 "om": '<path d="M22 96 Q26 78 50 78 Q74 78 78 96Z" fill="#264653"/><path d="M26 89 L74 89" stroke="{Y}" stroke-width="4"/>'
       '<circle cx="50" cy="58" r="22" fill="{SK}"/><circle cx="42" cy="60" r="3" fill="{D}"/><circle cx="58" cy="60" r="3" fill="{D}"/>'
       '<path d="M43 69 Q50 74 57 69" stroke-width="2.5"/>'
       '<path d="M24 46 Q24 16 50 16 Q76 16 76 46Z" fill="{R}"/><path d="M50 18 L50 46" stroke="#c1121f" stroke-width="3"/>'
       '<path d="M14 46 L86 46 Q88 53 81 53 L19 53 Q12 53 14 46Z" fill="#c1121f"/><circle cx="50" cy="32" r="6" fill="{Y}"/>',
 "ss": '<path d="M38 30 Q33 22 40 14 M52 30 Q47 22 54 14" stroke="#adb5bd" stroke-width="3"/>'
       '<ellipse cx="46" cy="84" rx="40" ry="8" fill="#fff"/>'
       '<path d="M70 48 Q88 48 86 60 Q84 72 68 66" stroke-width="6"/>'
       '<path d="M20 40 L72 40 L66 74 Q46 86 26 74Z" fill="#fff"/><path d="M23 54 L69 54" stroke="{B}" stroke-width="5"/>'
       '<ellipse cx="46" cy="40" rx="26" ry="5" fill="#6f4e37"/>',
 "t_addition": trait("M10 36 L22 26 L22 76", "{B}", 7) + trait("M38 51 L62 51 M50 39 L50 63", "{R}", 7) + trait("M78 36 L90 26 L90 76", "{B}", 7),
 "y_yaourt": '<path d="M22 30 L78 30 L70 90 L30 90Z" fill="#fff"/><path d="M27 46 L73 46 L70 70 L30 70Z" fill="{PK}"/>'
             '<circle cx="44" cy="58" r="5" fill="{R}" stroke-width="2"/><circle cx="56" cy="58" r="5" fill="{R}" stroke-width="2"/>'
             '<rect x="16" y="20" width="68" height="11" rx="3" fill="{LB}"/><path d="M76 14 L92 2" stroke-width="5"/>',
}

CERISE = ('<path d="M60 12 Q50 30 36 56 M60 12 Q66 34 66 58" stroke="{DG}" stroke-width="4"/>'
          '<path d="M60 12 Q74 4 86 12 Q74 22 60 12Z" fill="{G}"/>'
          '<circle cx="34" cy="68" r="17" fill="{R}"/><circle cx="68" cy="70" r="17" fill="{R}"/>'
          '<ellipse cx="28" cy="62" rx="3" ry="6" fill="#fff" stroke="none" opacity=".6"/>'
          '<ellipse cx="62" cy="64" rx="3" ry="6" fill="#fff" stroke="none" opacity=".6"/>')
POT = ('<rect x="22" y="34" width="56" height="58" rx="12" fill="#c1121f"/>'
       '<rect x="16" y="18" width="68" height="18" rx="5" fill="#e9c46a"/>'
       '<path d="M22 36 L30 46 L38 36 L46 46 L54 36 L62 46 L70 36 L78 46" stroke-width="2"/>'
       '<rect x="32" y="56" width="36" height="22" rx="3" fill="#fff"/><path d="M38 64 L62 64 M38 70 L56 70" stroke-width="2"/>')
ROSE = ('<path d="M50 50 Q47 74 50 96" stroke="{DG}" stroke-width="5"/>'
        '<path d="M49 66 L43 63 M50 80 L56 77" stroke="{DG}" stroke-width="2.5"/>'
        '<path d="M50 74 Q66 62 78 70 Q66 82 50 74Z" fill="{G}"/><path d="M49 84 Q34 76 24 82 Q36 92 49 84Z" fill="{G}"/>'
        '<path d="M26 30 Q24 54 50 56 Q76 54 74 30 Q66 40 50 38 Q34 40 26 30Z" fill="#c9184a"/>'
        '<path d="M32 30 Q34 12 50 14 Q66 12 68 30 Q60 40 50 38 Q40 40 32 30Z" fill="#ff4d6d"/>'
        '<path d="M42 28 Q44 20 52 22 Q58 26 54 32 Q48 34 46 28" stroke="#9d0b4b" stroke-width="2.5"/>'
        '<path d="M26 30 Q36 44 50 38 Q64 44 74 30" stroke="#9d0b4b" stroke-width="2"/>')
GIRAFE = ('<path d="M38 98 L46 44 L62 44 L66 98Z" fill="{Y}"/>'
          '<ellipse cx="50" cy="62" rx="5" ry="4" fill="{BR}" stroke="none"/><ellipse cx="58" cy="78" rx="5" ry="4" fill="{BR}" stroke="none"/>'
          '<ellipse cx="47" cy="88" rx="4" ry="3" fill="{BR}" stroke="none"/>'
          '<path d="M48 22 L46 8 M60 20 L62 6" stroke-width="4"/><circle cx="46" cy="7" r="4" fill="{BR}"/><circle cx="62" cy="5" r="4" fill="{BR}"/>'
          '<ellipse cx="36" cy="28" rx="9" ry="4" fill="{Y}" transform="rotate(-25 36 28)"/>'
          '<ellipse cx="56" cy="34" rx="22" ry="15" fill="{Y}"/><ellipse cx="74" cy="39" rx="12" ry="9" fill="#f2c57c"/>'
          '<circle cx="54" cy="30" r="3" fill="{D}"/><circle cx="80" cy="37" r="1.8" fill="{D}"/>')

def duo(gauche, droite):
    """Deux mots-référents pour une même lettre (« c de carotte ou de cerise »)."""
    return ('<g transform="translate(-6 18) scale(.64)" stroke-width="4.7">' + gauche + '</g>'
            '<g transform="translate(42 18) scale(.64)" stroke-width="4.7">' + droite + '</g>')

ALPHABET["c"] = duo(ALPHABET["c"], CERISE)
ALPHABET["o"] = duo(POT, ALPHABET["o"])
ALPHABET["s"] = duo(ALPHABET["s"], ROSE)
ALPHABET["g"] = duo(ALPHABET["g"], GIRAFE)

FAMILLES = {"alphabet": ALPHABET, "complexes": COMPLEXES, "doubles": DOUBLES, "autres": AUTRES}
ref = json.load(open(os.path.join(ROOT, "data/referentiel.json")))["familles"]
liste = []
for fam, dessins in FAMILLES.items():
    ids = [i["id"] for i in ref[fam]]
    manquants = set(ids) - set(dessins)
    assert not manquants, (fam, manquants)
    os.makedirs(os.path.join(ROOT, "img/referents", fam), exist_ok=True)
    for i in ids:
        with open(os.path.join(ROOT, "img/referents", fam, i + ".svg"), "w") as f:
            f.write(svg(dessins[i]))
        liste.append(f"{fam}/{i}.svg")
json.dump(liste, open(os.path.join(ROOT, "img/images.json"), "w"), indent=0)
print(len(liste), "dessins")
