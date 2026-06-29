# 01_ROUGEN_skin — 카페24 스킨 (HTML/CSS)

ROUGEN · 다크 럭셔리 핸드백 쇼핑몰 스킨. 메인 레퍼런스 레이아웃을 그대로 재현했습니다.
디자인(모양)만 구현 — 구매·결제·로그인 기능은 카페24가 처리합니다.

## 페이지
- index.html — 메인(스크롤 없는 풀스크린 히어로, Swiper, 하단 미니 푸터)
- products.html — 상품목록 27개(연출이미지 → 호버 시 제품이미지)
- product-detail.html — 상품상세(원본비율 이미지·옵션·상세/리뷰/문의/배송 탭)
- cart.html / login.html / signup.html
- notice.html / review.html / qna.html — 게시판

## 색·간격·글자 = CSS 변수
각 HTML <head> <style> 상단 :root{} 의 값만 바꾸면 전체 톤이 바뀝니다.
포인트색은 --point 한 줄로 버튼·가격·배지·링크호버 전부 제어.

## 로컬 미리보기
저장소 루트에서 `python3 -m http.server` 실행 후
http://localhost:8000/01_ROUGEN_skin/index.html
(이미지가 ../assets/ 경로라 폴더 안이 아닌 루트에서 서버를 띄워야 보입니다)
