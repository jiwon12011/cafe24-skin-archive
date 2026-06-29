# -*- coding: utf-8 -*-
"""새 카페24 스킨 작업 폴더를 규칙대로 자동 생성한다.

사용법:
    python new_skin.py <브랜드명> [포인트색HEX]
    예: python new_skin.py LUMINE #c8a24b

- 폴더명 규칙: "<번호>서지원_카페24_<브랜드명>"  (번호 = 기존 최대 + 1, 자동)
- 생성 페이지: index / products / product-detail / cart / login / signup /
  board / board-view / board-write
- CLAUDE.md 의 모든 절대 규칙을 만족하는 뼈대를 만든다:
  * 각 HTML <head> 에 <style> 인라인, :root{--point:...}
  * 헤더/푸터 모든 페이지 동일, 서브페이지 중앙영역 max 1550px + 페이지 제목
  * 메인은 독립 <section> (히어로/카테고리/추천/신상품/베스트/프로모)
  * 상품카드 8개 HTML 직접 하드코딩 (JS 생성 X)
  * 아이콘 Font Awesome CDN, 외부 CSS/번들러/프레임워크 X
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FA = ('<link rel="stylesheet" '
      'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">')


def next_number():
    nums = []
    for d in os.listdir(ROOT):
        if os.path.isdir(os.path.join(ROOT, d)):
            m = re.match(r"^(\d+)서지원_카페24_", d)
            if m:
                nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1


# ---- 공통 스타일 (모든 페이지 head 에 인라인) ----
def base_css(point):
    return """:root{ --point:%s; }
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',sans-serif;color:#222;line-height:1.5}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%%;height:auto}
.container{max-width:1550px;margin:0 auto;padding:0 20px}
.btn{display:inline-block;padding:12px 24px;border:none;border-radius:4px;
  background:var(--point);color:#fff;font-size:15px;cursor:pointer}
.btn-line{background:#fff;color:var(--point);border:1px solid var(--point)}
.price{color:var(--point);font-weight:700}
.badge{display:inline-block;padding:2px 8px;font-size:12px;border-radius:3px;
  background:var(--point);color:#fff}
a:hover{color:var(--point)}
/* header */
.site-header{border-bottom:1px solid #eee}
.site-header .inner{display:flex;align-items:center;justify-content:space-between;
  height:72px}
.site-header .logo{font-size:24px;font-weight:800;letter-spacing:1px}
.gnb{display:flex;gap:28px;font-size:15px}
.gnb a:hover{color:var(--point)}
.utils{display:flex;gap:18px;font-size:18px}
/* footer */
.site-footer{margin-top:60px;background:#f7f7f7;padding:40px 0;font-size:13px;color:#666}
.site-footer .cols{display:flex;gap:60px;flex-wrap:wrap}
/* subpage title */
.page-title{text-align:center;font-size:28px;font-weight:700;margin:48px 0 32px}
/* product grid */
.prod-grid{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.prod-grid .name{margin:10px 0 4px;font-size:15px}
@media(max-width:900px){.prod-grid{grid-template-columns:repeat(2,1fr)}}
""" % point


# 헤더 (모든 페이지 동일)
HEADER = """<header class="site-header">
  <div class="inner container">
    <a href="index.html" class="logo">{brand}</a>
    <nav class="gnb">
      <a href="products.html">NEW</a>
      <a href="products.html">BEST</a>
      <a href="products.html">상품</a>
      <a href="board.html">게시판</a>
    </nav>
    <div class="utils">
      <a href="login.html"><i class="fa-regular fa-user"></i></a>
      <a href="cart.html"><i class="fa-solid fa-cart-shopping"></i></a>
    </div>
  </div>
</header>"""

# 푸터 (모든 페이지 동일)
FOOTER = """<footer class="site-footer">
  <div class="container cols">
    <div>
      <strong>{brand}</strong><br>
      대표 서지원 · 사업자등록번호 000-00-00000<br>
      주소 · 고객센터 1234-5678
    </div>
    <div>
      <a href="board.html">공지사항</a> · <a href="board.html">FAQ</a><br>
      이용약관 · 개인정보처리방침
    </div>
  </div>
</footer>"""


def doc(title, css, body, brand):
    return ("""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
%s
<style>
%s
</style>
</head>
<body>
%s
</body>
</html>""" % (FA, css, body)).format(title=title, brand=brand)


def product_cards(n=8):
    li = []
    for i in range(1, n + 1):
        li.append("""    <li>
      <a href="product-detail.html">
        <img src="images/product-{i}.jpg" alt="상품{i}">
        <p class="name">상품명 {i}</p>
        <p class="price">39,000원</p>
      </a>
    </li>""".format(i=i))
    return "\n".join(li)


def subpage(title, inner, brand):
    body = (HEADER + "\n<main class=\"container\">\n  <h1 class=\"page-title\">"
            + title + "</h1>\n" + inner + "\n</main>\n" + FOOTER)
    return body.format(brand=brand)


def build(brand, point):
    css = base_css(point)
    pages = {}

    # index.html — 독립 section 들 + <img> 자리
    idx_body = (HEADER + """
<!-- 히어로 -->
<section class="hero">
  <a href="products.html"><img src="images/hero.jpg" alt="히어로 배너"></a>
</section>
<!-- 카테고리 -->
<section class="cat container">
  <h2>CATEGORY</h2>
  <ul class="prod-grid">
    <li><a href="products.html"><img src="images/cat-1.jpg" alt="카테고리1"><p class="name">신상품</p></a></li>
    <li><a href="products.html"><img src="images/cat-2.jpg" alt="카테고리2"><p class="name">베스트</p></a></li>
    <li><a href="products.html"><img src="images/cat-3.jpg" alt="카테고리3"><p class="name">아우터</p></a></li>
    <li><a href="products.html"><img src="images/cat-4.jpg" alt="카테고리4"><p class="name">악세서리</p></a></li>
  </ul>
</section>
<!-- 추천상품 -->
<section class="recommend container">
  <h2>RECOMMEND</h2>
  <ul class="prod-grid">
""" + product_cards(8) + """
  </ul>
</section>
<!-- 신상품 -->
<section class="new container">
  <h2>NEW ARRIVALS</h2>
  <ul class="prod-grid">
""" + product_cards(8) + """
  </ul>
</section>
<!-- 베스트 -->
<section class="best container">
  <h2>BEST</h2>
  <ul class="prod-grid">
""" + product_cards(8) + """
  </ul>
</section>
<!-- 기획전 / 룩북 띠배너 -->
<section class="promo">
  <a href="products.html"><img src="images/promo.jpg" alt="기획전 배너"></a>
</section>
""" + FOOTER).format(brand=brand)
    pages["index.html"] = doc(brand, css, idx_body, brand)

    # products.html
    prod_inner = """  <div class="sortbar" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
    <span>전체상품 (전체 32개)</span>
    <select><option>신상품순</option><option>낮은가격순</option><option>높은가격순</option></select>
  </div>
  <ul class="prod-grid">
""" + product_cards(8) + """
  </ul>
  <nav class="pagination" style="text-align:center;margin:40px 0">
    <a href="#">&laquo;</a> <a href="#" class="badge">1</a> <a href="#">2</a> <a href="#">3</a> <a href="#">&raquo;</a>
  </nav>"""
    pages["products.html"] = doc(brand + " - 상품목록", css,
                                 subpage("상품목록", prod_inner, brand), brand)

    # product-detail.html
    detail_inner = """  <div class="detail" style="display:flex;gap:40px;flex-wrap:wrap">
    <div style="flex:1;min-width:300px"><img src="images/product-1.jpg" alt="상품 대표이미지"></div>
    <div style="flex:1;min-width:300px">
      <h2>상품명 1</h2>
      <p class="price" style="font-size:24px;margin:16px 0">39,000원</p>
      <div class="opt"><label>옵션
        <select><option>옵션 선택</option><option>옵션 A</option><option>옵션 B</option></select>
      </label></div>
      <div class="qty" style="margin:16px 0">수량 <input type="number" value="1" min="1" style="width:60px"></div>
      <button class="btn">바로구매</button>
      <button class="btn btn-line">장바구니</button>
    </div>
  </div>
  <div class="tabs" style="margin-top:48px">
    <nav style="display:flex;gap:24px;border-bottom:2px solid var(--point);padding-bottom:8px">
      <a href="#desc">상세정보</a><a href="#review">리뷰</a><a href="#qna">문의</a>
    </nav>
    <section id="desc" style="padding:24px 0"><img src="images/detail.jpg" alt="상세설명 이미지"></section>
    <section id="review" style="padding:24px 0">리뷰 영역</section>
    <section id="qna" style="padding:24px 0">상품문의 영역</section>
  </div>"""
    pages["product-detail.html"] = doc(brand + " - 상품상세", css,
                                       subpage("상품상세", detail_inner, brand), brand)

    # cart.html
    cart_inner = """  <table style="width:100%;border-collapse:collapse;text-align:center">
    <thead><tr style="border-bottom:2px solid #222">
      <th><input type="checkbox"></th><th>이미지</th><th>상품명</th><th>수량</th><th>합계</th><th>삭제</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #eee">
        <td><input type="checkbox"></td>
        <td><img src="images/product-1.jpg" alt="상품1" style="width:80px;margin:0 auto"></td>
        <td>상품명 1</td>
        <td><input type="number" value="1" min="1" style="width:50px"></td>
        <td class="price">39,000원</td>
        <td><button class="btn-line btn">X</button></td>
      </tr>
    </tbody>
  </table>
  <div style="text-align:right;margin:24px 0;font-size:20px">총 합계 <span class="price">39,000원</span></div>
  <div style="text-align:center"><button class="btn">주문하기</button></div>"""
    pages["cart.html"] = doc(brand + " - 장바구니", css,
                             subpage("장바구니", cart_inner, brand), brand)

    # login.html
    login_inner = """  <form style="max-width:400px;margin:0 auto;display:flex;flex-direction:column;gap:12px">
    <input type="text" placeholder="아이디">
    <input type="password" placeholder="비밀번호">
    <button class="btn" type="submit">로그인</button>
    <a href="signup.html" style="text-align:center">회원가입</a>
  </form>"""
    pages["login.html"] = doc(brand + " - 로그인", css,
                              subpage("로그인", login_inner, brand), brand)

    # signup.html
    signup_inner = """  <form style="max-width:400px;margin:0 auto;display:flex;flex-direction:column;gap:12px">
    <input type="text" placeholder="아이디">
    <input type="password" placeholder="비밀번호">
    <input type="password" placeholder="비밀번호 확인">
    <input type="text" placeholder="이름">
    <input type="email" placeholder="이메일">
    <button class="btn" type="submit">가입하기</button>
  </form>"""
    pages["signup.html"] = doc(brand + " - 회원가입", css,
                               subpage("회원가입", signup_inner, brand), brand)

    # board.html (목록)
    board_inner = """  <table style="width:100%;border-collapse:collapse;text-align:center">
    <thead><tr style="border-bottom:2px solid #222"><th>번호</th><th>제목</th><th>작성자</th><th>날짜</th></tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #eee"><td>1</td><td><a href="board-view.html">공지사항입니다</a></td><td>관리자</td><td>2026-01-01</td></tr>
      <tr style="border-bottom:1px solid #eee"><td>2</td><td><a href="board-view.html">배송 안내</a></td><td>관리자</td><td>2026-01-02</td></tr>
    </tbody>
  </table>
  <div style="text-align:right;margin-top:20px"><a href="board-write.html" class="btn">글쓰기</a></div>"""
    pages["board.html"] = doc(brand + " - 게시판", css,
                              subpage("게시판", board_inner, brand), brand)

    # board-view.html
    view_inner = """  <article>
    <h2 style="border-bottom:2px solid var(--point);padding-bottom:12px">공지사항입니다</h2>
    <p style="color:#888;margin:8px 0">관리자 · 2026-01-01</p>
    <div style="padding:24px 0;min-height:200px">본문 내용 영역</div>
    <a href="board.html" class="btn btn-line">목록</a>
  </article>"""
    pages["board-view.html"] = doc(brand + " - 게시글", css,
                                   subpage("게시글", view_inner, brand), brand)

    # board-write.html
    write_inner = """  <form style="display:flex;flex-direction:column;gap:12px">
    <input type="text" placeholder="제목">
    <textarea rows="12" placeholder="내용"></textarea>
    <div style="text-align:right"><button class="btn" type="submit">등록</button></div>
  </form>"""
    pages["board-write.html"] = doc(brand + " - 글쓰기", css,
                                    subpage("글쓰기", write_inner, brand), brand)

    return pages


def main():
    if len(sys.argv) < 2:
        print("사용법: python new_skin.py <브랜드명> [포인트색HEX]")
        print("예:    python new_skin.py LUMINE #c8a24b")
        sys.exit(1)
    brand = sys.argv[1]
    point = sys.argv[2] if len(sys.argv) > 2 else "#000000"
    if not point.startswith("#"):
        point = "#" + point

    n = next_number()
    folder = "%d서지원_카페24_%s" % (n, brand)
    fpath = os.path.join(ROOT, folder)
    if os.path.exists(fpath):
        print("이미 존재함:", folder)
        sys.exit(1)
    os.makedirs(os.path.join(fpath, "images"))

    for name, html in build(brand, point).items():
        with open(os.path.join(fpath, name), "w", encoding="utf-8") as f:
            f.write(html)

    # 이미지 폴더 안내 파일
    with open(os.path.join(fpath, "images", "README.txt"), "w", encoding="utf-8") as f:
        f.write("여기에 hero.jpg, cat-1~4.jpg, product-1~8.jpg, promo.jpg, detail.jpg 를 넣으세요.\n")

    print("생성 완료: %s  (포인트색 %s)" % (folder, point))
    print("다음: 작업 후  python gen_readme.py  → commit & push")


if __name__ == "__main__":
    main()
