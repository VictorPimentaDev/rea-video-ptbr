"""pt-BR locale (added by Victor Pimenta): catalog keyed by the English string."""
import re
import string

from rea_video.i18n import T, join, lang, set_lang
from rea_video.i18n_pt_br import PT_BR


def _fields(s):
    return {f for _, f, _, _ in string.Formatter().parse(s) if f}


def test_pt_br_follows_language():
    from rea_video.classify import LABEL_ZH
    from rea_video.visual import LABEL_SHORT

    try:
        assert set_lang("pt-br") == "pt-BR" and lang() == "pt-BR"
        assert T("实拍", "live action") == PT_BR["live action"]
        assert T("{k}（{v} 个镜头）", "{k} ({v} shots)", k="A", v=3) == "A (3 planos)"
        assert T("只有中文") == "只有中文"
        assert T("中文", "not in the catalog") == "not in the catalog"  # falls back to English
        assert LABEL_ZH["ai_video"] == "vídeo gerado por IA"
        assert not any(re.search(r"[㐀-鿿]", v) for v in LABEL_SHORT.values())
        assert join(["a", "b"]) == "a, b"
    finally:
        set_lang("zh")


def test_catalog_keeps_placeholders_and_has_no_em_dash():
    for en, pt in PT_BR.items():
        assert _fields(pt) <= _fields(en), en
        assert "—" not in pt or pt == "—", en
