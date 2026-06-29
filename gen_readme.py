# -*- coding: utf-8 -*-
"""README.md 자동 생성 스크립트.
저장소 안의 각 프로젝트 폴더를 훑어서 htmlpreview 링크가 달린 README.md를 만든다.
새 폴더/페이지를 추가한 뒤 `python gen_readme.py` 만 실행하면 README가 갱신된다.
"""
import os
import urllib.parse

REPO = "jiwon12011/cafe24-skin-archive"
BRANCH = "main"
ROOT = os.path.dirname(os.path.abspath(__file__))

# 페이지 정렬 우선순위 (index/홈을 맨 앞으로)
ORDER = ["index.html", "products.html", "product-detail.html", "cart.html",
         "wishlist.html", "login.html", "signup.html", "mypage.html"]

# 보기 좋은 한글 라벨
LABELS = {
    "index.html": "메인", "products.html": "상품목록",
    "product-detail.html": "상품상세", "cart.html": "장바구니",
    "wishlist.html": "위시리스트", "login.html": "로그인",
    "signup.html": "회원가입", "mypage.html": "마이페이지",
    "board.html": "게시판", "board-list.html": "게시판",
    "board-view.html": "게시글", "board-write.html": "글쓰기",
    "board-notice.html": "공지", "board-qna.html": "Q&A",
    "board-review.html": "리뷰", "notice.html": "공지",
    "qna.html": "Q&A", "review.html": "리뷰",
}


def preview_url(folder, fname):
    raw = "https://github.com/%s/blob/%s/%s/%s" % (
        REPO, BRANCH,
        urllib.parse.quote(folder), urllib.parse.quote(fname))
    return "https://htmlpreview.github.io/?" + raw


def sort_pages(files):
    def key(f):
        return (ORDER.index(f) if f in ORDER else len(ORDER), f)
    return sorted(files, key=key)


def main():
    folders = sorted(
        d for d in os.listdir(ROOT)
        if os.path.isdir(os.path.join(ROOT, d)) and not d.startswith("."))

    lines = ["# cafe24-skin-archive", "",
             "서지원 — 카페24 쇼핑몰 스킨 제작 아카이브.",
             "아래 **[메인]** 링크를 누르면 실제 화면이 바로 열립니다. (GitHub 원본은 폴더명 링크)",
             ""]

    for folder in folders:
        fpath = os.path.join(ROOT, folder)
        htmls = sort_pages([f for f in os.listdir(fpath) if f.endswith(".html")])
        if not htmls:
            continue
        folder_url = "https://github.com/%s/tree/%s/%s" % (
            REPO, BRANCH, urllib.parse.quote(folder))
        lines.append("## [%s](%s)" % (folder, folder_url))
        links = []
        for h in htmls:
            label = LABELS.get(h, h.replace(".html", ""))
            links.append("[%s](%s)" % (label, preview_url(folder, h)))
        lines.append(" · ".join(links))
        lines.append("")

    lines.append("---")
    lines.append("> README는 `python gen_readme.py` 로 자동 생성됩니다.")
    lines.append("")

    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("README.md 생성 완료 (%d개 프로젝트)" % len(folders))


if __name__ == "__main__":
    main()
