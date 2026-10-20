"""L01 확률변수와 확률분포 — manim 애니메이션
렌더링: manim -qh l01_scenes.py <SceneName> --media_dir ../media
LaTeX 미설치 환경이므로 MathTex·DecimalNumber 대신 Text만 사용
"""
import numpy as np
from math import erf, sqrt, exp, pi
from manim import *

BG = "#FAFAF7"
INK = "#1F2A44"
BLUE_C = "#2E86AB"
ORANGE_C = "#E07A2E"
GREEN_C = "#3A9D5D"
GRAY_C = "#8A8F98"
FONT = "Malgun Gothic"

config.background_color = BG


def T(s, size=36, color=INK, weight=NORMAL):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def axes(x_range, y_range, x_len=10, y_len=5):
    return Axes(
        x_range=x_range, y_range=y_range, x_length=x_len, y_length=y_len,
        axis_config={"color": INK, "stroke_width": 3, "include_tip": True,
                     "tip_width": 0.2, "tip_height": 0.2},
    )


def coin(face):
    c = Circle(radius=0.28, color=INK, stroke_width=3,
               fill_color=ORANGE_C if face == "H" else BLUE_C, fill_opacity=1)
    return VGroup(c, T(face, 26, WHITE, BOLD).move_to(c))


class CoinMapping(Scene):
    """동전 두 번 → 앞면 개수 X 대응"""
    def construct(self):
        title = T("동전 2번 던지기 → 앞면의 개수", 40, weight=BOLD).to_edge(UP)
        self.play(Write(title))

        outcomes = ["HH", "HT", "TH", "TT"]
        values = {"HH": 2, "HT": 1, "TH": 1, "TT": 0}
        rows = VGroup(*[VGroup(coin(o[0]), coin(o[1])).arrange(RIGHT, buff=0.12)
                        for o in outcomes]).arrange(DOWN, buff=0.45).shift(LEFT * 3.2 + DOWN * 0.3)
        S = Ellipse(width=2.6, height=5.0, color=INK).move_to(rows)
        S_lab = T("표본공간 S", 30).next_to(S, UP, buff=0.15)

        nums = VGroup(*[T(str(v), 44, weight=BOLD) for v in (2, 1, 0)]
                      ).arrange(DOWN, buff=1.0).shift(RIGHT * 3.2 + DOWN * 0.3)
        Xe = Ellipse(width=2.0, height=5.0, color=ORANGE_C).move_to(nums)
        X_lab = T("X의 값 (실수)", 30, ORANGE_C).next_to(Xe, UP, buff=0.15)

        self.play(Create(S), FadeIn(S_lab))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.25))
        self.wait(0.5)
        self.play(Create(Xe), FadeIn(X_lab), FadeIn(nums))

        idx = {2: 0, 1: 1, 0: 2}
        for r, o in zip(rows, outcomes):
            a = Arrow(r.get_right(), nums[idx[values[o]]].get_left(), buff=0.25,
                      color=ORANGE_C, stroke_width=4, max_tip_length_to_length_ratio=0.08)
            self.play(GrowArrow(a), Indicate(r, color=ORANGE_C), run_time=0.9)
        self.wait(0.5)

        concl = T("확률변수 = 결과마다 실수 하나를 짝짓는 함수", 34, ORANGE_C, BOLD).to_edge(DOWN, buff=0.35)
        self.play(Write(concl))
        self.wait(2)


class PMFBars(Scene):
    """확률분포 표 → 막대그래프 → 합 = 1"""
    def construct(self):
        title = T("확률분포: 표 → 그래프", 40, weight=BOLD).to_edge(UP)
        self.play(Write(title))

        xs, ps, plab = [0, 1, 2], [0.25, 0.5, 0.25], ["1/4", "1/2", "1/4"]
        table = Table([[str(x) for x in xs] + ["합계"], plab + ["1"]],
                      row_labels=[T("X", 30, weight=BOLD), T("P(X=x)", 30, weight=BOLD)],
                      element_to_mobject=lambda s: T(s, 30),
                      line_config={"color": INK, "stroke_width": 2},
                      v_buff=0.35, h_buff=0.7).scale(0.75).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
        self.play(Create(table), run_time=1.5)
        self.wait(0.5)

        ax = axes([-0.5, 2.8, 1], [0, 1.05, 0.25], x_len=6, y_len=4.6).to_edge(DOWN, buff=0.6).shift(LEFT * 2.2)
        xl = VGroup(*[T(str(x), 28).next_to(ax.c2p(x, 0), DOWN, buff=0.2) for x in xs])
        yl = VGroup(*[T(s, 24).next_to(ax.c2p(-0.5, v), LEFT, buff=0.15)
                      for s, v in (("1/4", 0.25), ("1/2", 0.5), ("1", 1.0))])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl))

        colors = [BLUE_C, ORANGE_C, GREEN_C]
        bars = VGroup()
        for i, (x, p) in enumerate(zip(xs, ps)):
            b = Rectangle(width=0.9, height=ax.c2p(0, p)[1] - ax.c2p(0, 0)[1],
                          fill_color=colors[i], fill_opacity=0.85, stroke_color=INK, stroke_width=2)
            b.move_to(ax.c2p(x, 0), aligned_edge=DOWN)
            cell = table.get_entries((2, i + 2))
            self.play(Indicate(cell, color=colors[i]), GrowFromEdge(b, DOWN), run_time=0.9)
            bars.add(b)
        self.wait(1)

        # 막대를 쌓아 합 = 1 보여주기
        base = np.array([ax.c2p(0, 0)[0] + 5.6, ax.c2p(0, 0)[1], 0])
        targets, y = VGroup(), 0
        for b in bars:
            t = b.copy().move_to(base + UP * y, aligned_edge=DOWN)
            y += b.height
            targets.add(t)
        self.play(*[TransformFromCopy(b, t) for b, t in zip(bars, targets)], run_time=1.6)
        brace = Brace(targets, RIGHT, color=INK)
        one = T("합 = 1", 34, ORANGE_C, BOLD).next_to(brace, RIGHT)
        self.play(GrowFromCenter(brace), Write(one))
        self.wait(2)


class DiceSum(Scene):
    """주사위 2개 합: 시행 횟수 ↑ → 상대도수가 확률분포에 접근"""
    def construct(self):
        title = T("주사위 2개의 합 — 많이 던질수록?", 40, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        ax = axes([1, 13, 1], [0, 0.25, 0.05], x_len=10.5, y_len=4.6).shift(DOWN * 0.5)
        xl = VGroup(*[T(str(k), 24).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k in range(2, 13)])
        yl = VGroup(*[T(f"{v:.2f}", 20).next_to(ax.c2p(1, v), LEFT, buff=0.1) for v in (0.05, 0.1, 0.15, 0.2)])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl))

        theo = np.array([min(k - 1, 13 - k) / 36 for k in range(2, 13)])
        rng = np.random.default_rng(7)
        rolls = rng.integers(1, 7, (10000, 2)).sum(axis=1)

        def bars_for(freq):
            g = VGroup()
            for k, f in zip(range(2, 13), freq):
                h = max(ax.c2p(0, f)[1] - ax.c2p(0, 0)[1], 0.001)
                g.add(Rectangle(width=0.7, height=h, fill_color=BLUE_C, fill_opacity=0.8,
                                stroke_color=INK, stroke_width=1.5).move_to(ax.c2p(k, 0), aligned_edge=DOWN))
            return g

        bars = counter = None
        for n in (10, 50, 200, 1000, 10000):
            freq = np.array([(rolls[:n] == k).mean() for k in range(2, 13)])
            nb = bars_for(freq)
            nc = T(f"던진 횟수 n = {n:,}", 34, ORANGE_C, BOLD).to_corner(UR).shift(DOWN * 1.0)
            if bars is None:
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in nb], lag_ratio=0.05), FadeIn(nc))
                bars, counter = nb, nc
            else:
                self.play(Transform(bars, nb), Transform(counter, nc), run_time=1.2)
            self.wait(0.8)

        dots = VGroup(*[Dot(ax.c2p(k, p), color=ORANGE_C, radius=0.09) for k, p in zip(range(2, 13), theo)])
        line = VMobject(color=ORANGE_C, stroke_width=4).set_points_as_corners([d.get_center() for d in dots])
        lab = T("이론 확률 P(X=x)", 30, ORANGE_C, BOLD).next_to(ax.c2p(10.5, 0.2), UP)
        self.play(Create(line), FadeIn(dots), Write(lab))
        self.wait(2.5)


class UniformSubway(Scene):
    """지하철 대기 시간 X ~ 0~10분: 확률 = 넓이"""
    def construct(self):
        title = T("지하철 대기 시간 X (10분 간격)", 40, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        ax = axes([0, 11, 1], [0, 0.15, 0.05], x_len=10, y_len=4).shift(DOWN * 0.6)
        xl = VGroup(*[T(str(k), 24).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k in (0, 2, 4, 6, 8, 10)])
        xn = T("x (분)", 26).next_to(ax.x_axis, RIGHT, buff=0.1).shift(DOWN * 0.4)
        self.play(Create(ax), FadeIn(xl), FadeIn(xn))

        f = ax.plot(lambda x: 0.1, x_range=[0, 10], color=BLUE_C, stroke_width=6)
        flab = T("f(x) = 1/10", 30, BLUE_C, BOLD).next_to(ax.c2p(10, 0.1), UR, buff=0.15)
        y10 = T("1/10", 24).next_to(ax.c2p(0, 0.1), LEFT, buff=0.15)
        edge = DashedLine(ax.c2p(10, 0), ax.c2p(10, 0.1), color=BLUE_C)
        self.play(Create(f), Write(flab), FadeIn(y10), Create(edge))

        full = ax.get_area(f, x_range=[0, 10], color=BLUE_C, opacity=0.25)
        tot = T("전체 넓이 = 10 × 1/10 = 1", 32, INK, BOLD).next_to(ax.c2p(5, 0.1), UP, buff=0.5)
        self.play(FadeIn(full), Write(tot))
        self.wait(1.2)
        self.play(FadeOut(full), FadeOut(tot))

        a, b = ValueTracker(2), ValueTracker(4)
        area = always_redraw(lambda: ax.get_area(f, x_range=[a.get_value(), b.get_value()],
                                                 color=ORANGE_C, opacity=0.6))
        la = always_redraw(lambda: T("a", 28, ORANGE_C, BOLD).next_to(ax.c2p(a.get_value(), 0), DOWN, buff=0.55))
        lb = always_redraw(lambda: T("b", 28, ORANGE_C, BOLD).next_to(ax.c2p(b.get_value(), 0), DOWN, buff=0.55))
        prob = always_redraw(lambda: VGroup(
            T("P(a ≤ X ≤ b) = (b − a)/10 =", 32, INK, BOLD),
            T(f"{(b.get_value() - a.get_value()) / 10:.2f}", 44, ORANGE_C, BOLD)).arrange(RIGHT).next_to(ax.c2p(5, 0.1), UP, buff=0.5))
        self.play(FadeIn(area), FadeIn(la), FadeIn(lb), FadeIn(prob))
        self.play(b.animate.set_value(7), run_time=2)
        self.play(a.animate.set_value(5), run_time=1.5)
        self.play(a.animate.set_value(0), b.animate.set_value(5), run_time=2)
        q = T("5분 이하로 기다릴 확률 = 1/2", 32, ORANGE_C, BOLD).next_to(title, DOWN, buff=0.3)
        self.play(Write(q))
        self.wait(2)


class PointZero(Scene):
    """연속확률변수: 한 점의 확률 = 0"""
    def construct(self):
        title = T("정확히 5분일 확률은?", 40, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        ax = axes([0, 11, 1], [0, 0.15, 0.05], x_len=10, y_len=4).shift(DOWN * 0.6)
        xl = VGroup(*[T(str(k), 24).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k in (0, 5, 10)])
        f = ax.plot(lambda x: 0.1, x_range=[0, 10], color=BLUE_C, stroke_width=6)
        self.play(Create(ax), FadeIn(xl), Create(f))

        w = ValueTracker(2.0)
        area = always_redraw(lambda: ax.get_area(f, x_range=[5 - w.get_value() / 2, 5 + w.get_value() / 2],
                                                 color=ORANGE_C, opacity=0.7))
        info = always_redraw(lambda: VGroup(
            T("폭", 30), T(f"{w.get_value():.3f}", 38, INK, BOLD),
            T("→ 넓이", 30), T(f"{w.get_value() / 10:.4f}", 44, ORANGE_C, BOLD)
        ).arrange(RIGHT, buff=0.25).next_to(ax.c2p(5, 0.1), UP, buff=0.6))
        self.play(FadeIn(area), FadeIn(info))
        self.play(w.animate.set_value(0.5), run_time=2)
        self.play(w.animate.set_value(0.05), run_time=2)
        self.play(w.animate.set_value(0.001), run_time=2)
        res = T("P(X = 5) = 0  →  끝점 포함 여부는 확률에 영향 없음", 32, ORANGE_C, BOLD).to_edge(DOWN, buff=0.25)
        self.play(Write(res))
        self.wait(2)


class HistToCurve(Scene):
    """히스토그램 계급 폭 ↓ → 확률밀도함수 곡선"""
    def construct(self):
        title = T("저항값 측정 데이터: 계급을 잘게 나누면?", 40, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        mu, sd = 100.0, 2.0
        ax = axes([92, 108.5, 2], [0, 0.24, 0.05], x_len=11, y_len=4.6).shift(DOWN * 0.5)
        xl = VGroup(*[T(str(k), 22).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k in range(92, 109, 4)])
        xn = T("저항 (Ω)", 24).next_to(ax.c2p(108, 0), DOWN, buff=0.5)
        self.play(Create(ax), FadeIn(xl), FadeIn(xn))

        cdf = lambda x: 0.5 * (1 + erf((x - mu) / (sd * sqrt(2))))
        pdf = lambda x: exp(-((x - mu) / sd) ** 2 / 2) / (sd * sqrt(2 * pi))

        def hist(width):
            g = VGroup()
            edges = np.arange(92, 108 + 1e-9, width)
            for lo in edges[:-1]:
                dens = (cdf(lo + width) - cdf(lo)) / width   # 높이 = 상대도수/폭 → 넓이 = 확률
                p0, p1 = ax.c2p(lo, 0), ax.c2p(lo + width, dens)
                g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.001),
                                fill_color=BLUE_C, fill_opacity=0.75, stroke_color=INK,
                                stroke_width=1.5 if width > 0.3 else 0.5).move_to(p0, aligned_edge=DL))
            return g

        h = hist(4)
        lab = T("계급 폭 4Ω", 32, ORANGE_C, BOLD).to_corner(UR).shift(DOWN * 1.1)
        self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in h], lag_ratio=0.1), FadeIn(lab))
        self.wait(0.8)
        for wdt in (2, 1, 0.5, 0.2):
            nl = T(f"계급 폭 {wdt:g}Ω", 32, ORANGE_C, BOLD).to_corner(UR).shift(DOWN * 1.1)
            self.play(Transform(h, hist(wdt)), Transform(lab, nl), run_time=1.3)
            self.wait(0.5)

        curve = ax.plot(pdf, x_range=[92, 108], color=ORANGE_C, stroke_width=6)
        self.play(Create(curve), run_time=1.5)
        self.play(h.animate.set_fill(opacity=0.15).set_stroke(opacity=0.2))
        name = T("확률밀도함수 y = f(x)", 34, ORANGE_C, BOLD).next_to(ax.c2p(103, 0.16), RIGHT, buff=0)
        self.play(Write(name))
        self.wait(2)


class AreaProb(Scene):
    """확률밀도함수의 성질: f ≥ 0, 전체 넓이 1, 확률 = 넓이"""
    def construct(self):
        title = T("확률밀도함수의 세 가지 성질", 40, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        ax = axes([0, 10.5, 1], [0, 0.32, 0.1], x_len=8, y_len=4).shift(DOWN * 0.4 + LEFT * 2.3)
        f = lambda x: 0.6 * np.exp(-((x - 3.5) ** 2) / 2) / np.sqrt(2 * np.pi) + \
            0.4 * np.exp(-((x - 6.8) ** 2) / (2 * 0.8 ** 2)) / (0.8 * np.sqrt(2 * np.pi))
        g = ax.plot(f, x_range=[0, 10.3], color=BLUE_C, stroke_width=6)
        self.play(Create(ax), Create(g))

        items = VGroup(T("① f(x) ≥ 0", 30), T("② 전체 넓이 = 1", 30), T("③ 확률 = 색칠한 넓이", 30)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)

        self.play(Write(items[0]), g.animate.set_stroke(color=GREEN_C), run_time=1.2)
        self.play(g.animate.set_stroke(color=BLUE_C))
        full = ax.get_area(g, x_range=[0, 10.3], color=BLUE_C, opacity=0.35)
        self.play(Write(items[1]), FadeIn(full))
        one = T("1", 60, BLUE_C, BOLD).move_to(ax.c2p(4.2, 0.08))
        self.play(FadeIn(one, scale=1.5))
        self.wait(0.8)
        self.play(FadeOut(full), FadeOut(one))

        a, b = ValueTracker(2.5), ValueTracker(4.5)
        area = always_redraw(lambda: ax.get_area(g, x_range=[a.get_value(), b.get_value()],
                                                 color=ORANGE_C, opacity=0.65))
        la = always_redraw(lambda: T("a", 28, ORANGE_C, BOLD).next_to(ax.c2p(a.get_value(), 0), DOWN, buff=0.2))
        lb = always_redraw(lambda: T("b", 28, ORANGE_C, BOLD).next_to(ax.c2p(b.get_value(), 0), DOWN, buff=0.2))
        self.play(Write(items[2]), FadeIn(area), FadeIn(la), FadeIn(lb))
        self.play(a.animate.set_value(5.5), b.animate.set_value(8), run_time=2.5)
        self.play(a.animate.set_value(1), b.animate.set_value(3), run_time=2)
        self.wait(2)


class TriangleK(Scene):
    """문제 3: f(x) = kx (0 ≤ x ≤ 4) — k와 P(0≤X≤2)"""
    def construct(self):
        title = T("f(x) = kx  (0 ≤ x ≤ 4)", 40, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        ax = axes([0, 5, 1], [0, 0.6, 0.25], x_len=6, y_len=4.2).shift(LEFT * 3 + DOWN * 0.5)
        xl = VGroup(*[T(str(k), 24).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k in (2, 4)])
        self.play(Create(ax), FadeIn(xl))
        k = 1 / 8
        g = ax.plot(lambda x: k * x, x_range=[0, 4], color=BLUE_C, stroke_width=6)
        v = DashedLine(ax.c2p(4, 0), ax.c2p(4, 0.5), color=BLUE_C)
        hk = T("4k", 26, BLUE_C, BOLD).next_to(ax.c2p(0, 0.5), LEFT, buff=0.15)
        hl = DashedLine(ax.c2p(0, 0.5), ax.c2p(4, 0.5), color=GRAY_C, stroke_width=2)
        self.play(Create(g), Create(v), FadeIn(hk), Create(hl))

        tri = ax.get_area(g, x_range=[0, 4], color=BLUE_C, opacity=0.3)
        steps = VGroup(
            T("전체 넓이 = 1", 32, weight=BOLD),
            T("½ × 4 × 4k = 8k = 1", 32),
            T("k = 1/8", 38, ORANGE_C, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.8).shift(UP * 0.8)
        self.play(FadeIn(tri), Write(steps[0]))
        self.play(Write(steps[1]))
        self.play(Write(steps[2]))
        self.wait(1)

        small = ax.get_area(g, x_range=[0, 2], color=ORANGE_C, opacity=0.75)
        s2 = VGroup(
            T("P(0 ≤ X ≤ 2)", 32, weight=BOLD),
            T("= ½ × 2 × 2/8", 32),
            T("= 1/4", 38, ORANGE_C, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(steps, DOWN, buff=0.7, aligned_edge=LEFT)
        self.play(FadeIn(small), Write(s2[0]))
        self.play(Write(s2[1]))
        self.play(Write(s2[2]))
        self.wait(2)
