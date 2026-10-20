"""L01 슬라이드 빌드 (테스트판) — python build_l01.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from deck import Deck, BLUE, GREEN, ORANGE

V = os.path.join(HERE, "media", "videos", "l01_scenes", "1080p60")
P = os.path.join(HERE, "media", "posters")
vid = lambda n: (os.path.join(V, n + ".mp4"), os.path.join(P, n + ".png"))

d = Deck("확률과 통계 · L01 확률변수와 확률분포", os.path.join(HERE, "images"))
d.title("확률변수와 확률분포", "불확실한 결과를 숫자로 다루는 방법", "확률과 통계 · L01 · 대학교 1학년 공학 기초")
d.bullets("학습목표", ["확률변수의 뜻과 표기 이해", "이산확률변수의 확률분포·확률질량함수 이해",
                     "연속확률변수의 확률밀도함수와 **넓이 = 확률** 이해"])
d.analogy("확률변수란?", "barcode_scanner.jpg", "확률변수 = 결과를 숫자로 바꾸는 바코드 스캐너",
          ["물건(결과) → 스캔 → 가격(숫자)", "결과마다 숫자 하나씩 대응", "같은 숫자에 여러 결과 가능"],
          notes="바코드 스캐너 비유로 확률변수가 '함수'임을 강조.")
d.video("동전 2번 던지기", *vid("CoinMapping"), side=["표본공간 S = {HH, HT, TH, TT}", "X = 앞면의 개수", "X의 값: 0, 1, 2"])
d.two_images("이산 vs 연속", ("marbles.jpg", "이산: 셀 수 있음", ["구슬 개수처럼 띄엄띄엄한 값"]),
             ("water.jpg", "연속: 잴 수 있음", ["물의 양처럼 구간의 모든 실수"]))
d.video("확률분포: 표와 그래프", *vid("PMFBars"), side=["막대 높이 = 확률", "모든 확률의 합 = 1"])
d.video("많이 던질수록?", *vid("DiceSum"), side=["상대도수 → 이론 확률분포에 근접"])
d.video("연속확률변수: 확률 = 넓이", *vid("UniformSubway"), side=["X: 0~10 사이 모든 실수", "f(x) = 1/10", "확률 = 직사각형 넓이"])
d.analogy("한 점의 확률", "dartboard.jpg", "다트가 정확히 한 점에 꽂힐 확률 = 0",
          ["점은 넓이 0", "구간에 꽂힐 확률만 의미"])
d.video("정확히 5분일 확률", *vid("PointZero"), side=["폭 → 0이면 넓이 → 0", "P(a≤X≤b) = P(a<X<b)"])
d.video("히스토그램 → 확률밀도함수", *vid("HistToCurve"), side=["계급 폭 → 0", "매끄러운 곡선 = 확률밀도함수"])
d.video("확률밀도함수의 성질", *vid("AreaProb"), side=["f(x) 값 자체는 확률 아님", "넓이만 확률"])
d.video("문제: f(x) = kx", *vid("TriangleK"), side=["전체 넓이 = 1로 k 결정", "구하는 확률 = 부분 넓이"])
d.cards("요약", [("확률변수", ["결과 → 실수 대응 함수"], BLUE),
                ("이산", ["확률질량함수 P(X=x)", "확률의 합 = 1"], GREEN),
                ("연속", ["확률밀도함수 f(x)", "넓이 = 확률, 한 점 확률 = 0"], ORANGE)])
print(d.save(os.path.join(HERE, "output", "L01_확률변수와_확률분포.pptx")))
