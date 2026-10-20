---
name: lecture-slides
description: 이 폴더의 교과서·outline을 바탕으로 manim 애니메이션과 인터넷 비유 그림이 들어간 강의 PPT(.pptx)를 만든다. "L03 슬라이드 만들어줘", "강의자료 만들어줘" 같은 요청에 사용.
---

# 강의 슬라이드 제작

대상 강의: 인자로 받은 `LXX` (없으면 사용자에게 확인). 모든 규칙은 `CLAUDE.md`를 따른다 (명사형 종결, 그림 중심, 60분 ≈ 25~30장).

## 절차
1. **내용 파악**: `lectures/LXX_*/outline.md`, `notes.md` 읽기 → 교과서 해당 쪽을 PyMuPDF로 이미지 렌더링해서 확인 (텍스트 추출은 수식이 깨짐).
2. **슬라이드 계획**: 섹션별로 비유 → 정의 → 애니메이션 → 예제/문제 순서. 마지막은 요약 + 확인 퀴즈 + 정답.
3. **manim 애니메이션**: `lectures/LXX_*/manim/lXX_scenes.py` 작성 (L01 파일의 색·`T()`·`axes()` 도우미 그대로 복사).
   - LaTeX 미설치 → `MathTex`, `Tex`, `DecimalNumber` 금지. 숫자는 `always_redraw(lambda: T(f"{v:.2f}"))`.
   - 먼저 `-ql`로 렌더링 → 중간·마지막 프레임을 이미지로 뽑아 겹침 확인 → 수정 후 `-qh --media_dir ../media` (백그라운드).
4. **비유 그림**: Wikimedia Commons API(`generator=search`, `filetype:bitmap`)로 검색, 라이선스 CC0/PD/CC BY만.
   - 요청 사이 3~4초 간격 (429 방지), URL의 `?` 뒤를 떼고 확장자 판별, 0바이트 파일 제외.
   - 후보를 콘택트 시트로 모아 눈으로 고른 뒤 `images/`에 복사, `sources.md`·`credits.json` 작성.
5. **PPT 빌드**: `lectures/LXX_*/build_lXX.py`에서 `tools/deck.py`의 `Deck` 사용
   (`title, section, bullets, analogy, two_images, video, definition, table, cards, problem`).
   CC BY 그림은 출처가 자동 표기됨. 슬라이드 노트에 강의 멘트 작성.
6. **결과**: `output/LXX_*.pptx` 경로와 장수, 영상 개수를 보고. 영상은 슬라이드에서 클릭하면 재생.

## 참고 구현
- `lectures/L01_확률변수와_확률분포/` (manim 장면 8개, build 스크립트, 이미지 출처)
