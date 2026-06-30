# 01_ROAMER_skin — 카페24 스킨 (HTML/CSS)

ROAMER · 고프코어 아웃도어 핸드기어 쇼핑몰 스킨. 메인 레퍼런스 레이아웃을 그대로 재현했습니다.
디자인(모양)만 구현 — 구매·결제·로그인 기능은 카페24가 처리합니다.

## 페이지
- index.html — 메인(히어로 3분할, Field Notes, Weekly Best 탭, Best Seller, Trail Journal)
- products.html — 상품목록 16개(정렬바·뱃지·위시·페이지네이션)
- product-detail.html — 상품상세(갤러리·색상/사이즈 옵션·수량·상세/스펙/배송/리뷰 탭·관련상품)
- cart.html / login.html / signup.html
- notice.html / review.html / qna.html — 게시판(공지·후기·문의)

## 색·간격·글자 = CSS 변수
각 HTML `<head>` `<style>` 상단 `:root{}` 의 값만 바꾸면 전체 톤이 바뀝니다.
포인트색은 `--lime` 한 줄로 버튼·뱃지·강조·링크호버 전부 제어.

```
--lime:#c2d500;   /* ★ 포인트 칼라 */
--ink:#15171a;    /* 기본 글자/버튼 */
--bg:#ffffff;     /* 배경 */
--bg-soft:#f4f5f3;/* 카드/표면 */
```

## 로컬 미리보기
저장소 루트에서 `python3 -m http.server` 실행 후
http://localhost:8000/01_ROAMER_skin/index.html

(이미지는 `01_ROAMER_skin/assets/roamer/` 에 함께 들어 있어 폴더째 업로드해도 그대로 보입니다.)

## 카페24 업로드
관리자 → 디자인(웹) → 디자인 보관함 → HTML/CSS 편집에서
이 폴더의 HTML과 `assets/` 를 같은 구조로 올리면 됩니다. 상품·게시판 영역은
카페24 모듈로 교체해 실제 데이터와 연결하세요.
