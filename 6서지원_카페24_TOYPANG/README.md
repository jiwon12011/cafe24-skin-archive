# 토이팡 (TOYPANG) — 카페24 스킨

키즈/토이 전문몰 콘셉트의 **카페24 쇼핑몰 스킨(디자인)** 입니다.
구매·결제·로그인 등 실제 기능은 카페24가 처리하며, 이 저장소는 **모양(HTML/CSS/최소 바닐라 JS)** 만 담고 있습니다.

## 페이지 구성

| 파일 | 설명 |
|------|------|
| `index.html` | 메인 — 헤더 + 히어로(Swiper 3장) + 이달의 추천(카테고리) + NEW 신제품 + 띠배너① + BEST + EVENT + MD추천 + 특가/패키지 + 띠배너② + 푸터 |
| `products.html` | 상품목록 — 정렬바 + 상품카드 그리드(16개) + 페이지네이션 |
| `product-detail.html` | 상품상세 — 큰 이미지 + 옵션/수량/구매 + 상세설명(800×3000 이미지) + 상세/리뷰/문의/배송 탭 |
| `cart.html` | 장바구니 — 상품표(체크박스·썸네일·수량·합계·삭제) + 합계 + 주문 |
| `login.html` / `signup.html` | 로그인 / 회원가입 |
| `board-notice.html` / `board-qna.html` / `board-review.html` | 게시판(공지/Q&A/리뷰) |

## 디자인 규칙

- **헤더·푸터는 모든 페이지 완전 동일**, 서브페이지 콘텐츠 폭 `max 1550px`.
- 메인 각 영역은 **독립 `<section>`** (운영자가 켜고끄고 순서변경 용이).
- **CSS는 각 HTML `<head>`에 인라인** (`<style>`), 외부 CSS 없음.
- 상품카드는 **HTML에 직접 작성한 `<li>`** (JS 생성 X), 모바일 2열, `border-radius:8px`.
- 아이콘은 **Font Awesome CDN**, 슬라이드는 **Swiper JS**, 스크롤 등장 효과는 **순수 바닐라 JS(IntersectionObserver)**. (AOS/GSAP/jQuery 미사용)
- 모든 이미지는 `<img>` 로 노출 (히어로/카테고리/배너/상품썸네일/상세설명).

## 커스터마이즈 (CSS 변수)

각 페이지 `<head>` 상단 `:root` 에서 한 곳만 고치면 전체에 반영됩니다.

```css
:root{
  --main:#15b5a8;      /* 메인 컬러 */
  --sub:#ff8fb1;       /* 서브 컬러 */
  --point:#ff5b5b;     /* 포인트 컬러 (버튼·가격·배지·강조) */
  --bg:#ffffff;        /* 배경색 */
  --section-gap:70px;  /* 섹션별 간격 */
  --pad:20px;          /* 여백 */
  --container:1550px;  /* 콘텐츠 폭 */
  --fs-hero:42px; --fs-h2:26px; --fs-h3:17px; --fs-body:15px;  /* 계층별 글자크기 */
  --fw-reg:400; --fw-med:500; --fw-bold:700; --fw-black:800;    /* 글자 두께 */
  --radius:8px; --radius-lg:16px; --radius-pill:999px;          /* 둥글기 */
}
```

## 이미지 에셋 (`assets/images/toyland/`)

- 히어로 3종, 띠배너 2종, 이벤트 배너 3종, 카테고리 아이콘 시트 1종(`cat/` 에 8개로 분할)
- 상품 이미지 16종 + 부가/패키지 이미지, 상품별 상세설명 이미지(`detail/` · 800×3000)
- 모두 실사 톤의 생성 이미지이며 SVG/온라인 임시이미지는 사용하지 않았습니다.
- 전체 인벤토리는 `assets/images/toyland/manifest.md` 참고.
