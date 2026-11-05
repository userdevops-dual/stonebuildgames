#!/usr/bin/env python3
"""Generates the low-poly rock SVGs used behind page sections (site/assets/rock-*.svg)."""
import math, os, random
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'assets')
GREY = ['#ececee', '#e4e4e7', '#d9d9de', '#cfcfd5', '#c4c4cb']
ORANGE = ['#ffc4a8', '#ffb08c', '#ff9a6c', '#ff8650', '#f2703a']
def rock(seed, pal, wire=False):
    r = random.Random(seed); n = r.randint(7, 9); C = 100
    outer = []
    for i in range(n):
        a = 2 * math.pi * i / n + r.uniform(-.16, .16); R = r.uniform(70, 94)
        outer.append((C + R * math.cos(a), C + R * math.sin(a) * .86))
    inner = []
    for i in range(n // 2 + 1):
        a = 2 * math.pi * i / (n // 2 + 1) + r.uniform(-.2, .2); R = r.uniform(26, 44)
        inner.append((C - 10 + R * math.cos(a), C - 14 + R * math.sin(a) * .86))
    pts = lambda *p: ' '.join(f'{x:.1f},{y:.1f}' for x, y in p)
    def shade(*p):
        cx = sum(q[0] for q in p) / len(p); cy = sum(q[1] for q in p) / len(p)
        t = max(0, min(.999, ((cx - C) + (cy - C)) / 150 + .5))   # lit from the top left
        return pal[int(t * len(pal))]
    tris = []
    near = lambda o: min(range(len(inner)), key=lambda k: (inner[k][0]-o[0])**2 + (inner[k][1]-o[1])**2)
    for i in range(n):
        a, b = outer[i], outer[(i + 1) % n]; ia, ib = near(a), near(b)
        tris.append((a, b, inner[ib]))
        if ia != ib: tris.append((a, inner[ib], inner[ia]))
    for i in range(1, len(inner) - 1): tris.append((inner[0], inner[i], inner[i + 1]))
    if wire:
        body = ''.join(f'<polygon points="{pts(*t)}"/>' for t in tris)
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><g fill="none" stroke="#ff6a2b" stroke-width="1.6" stroke-linejoin="round" opacity=".55">{body}</g></svg>\n'
    body = ''.join(f'<polygon points="{pts(*t)}" fill="{shade(*t)}" stroke="{shade(*t)}" stroke-width=".6"/>' for t in tris)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><g stroke-linejoin="round">{body}</g></svg>\n'
for name, seed, pal, wire in [('rock-1', 3, GREY, False), ('rock-2', 11, GREY, False), ('rock-3', 23, GREY, False), ('rock-4', 7, ORANGE, False), ('rock-5', 31, GREY, True)]:
    open(os.path.join(OUT, name + '.svg'), 'w').write(rock(seed, pal, wire))
print('rocks ok')
