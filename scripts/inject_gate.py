import hashlib, os, pathlib

ROOT = pathlib.Path(__file__).parent.parent
SRC  = ROOT / "output" / "영아부_예배안내_생성기.html"
DEST = ROOT / "docs" / "index.html"

PW_HASH = os.environ.get(
    "PW_HASH",
    "b85c65c827d834bb6e24fad6dde064ca12f2134f7334bdec269500619dd5ab08",
)

GATE = f"""<script>
(function(){{
  var DEFAULT_HASH='{PW_HASH}';
  var OVERRIDE_KEY='yab26pwHash';
  var AUTH_KEY='yab26auth';
  var HASH=localStorage.getItem(OVERRIDE_KEY)||DEFAULT_HASH;
  if(sessionStorage.getItem(AUTH_KEY)===HASH)return;
  var overlay=document.createElement('div');
  overlay.id='pwOverlay';
  overlay.style.cssText='position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:#fafaf9;font-family:"Apple SD Gothic Neo","Malgun Gothic",sans-serif';
  overlay.innerHTML='<div style="background:#fff;border-radius:16px;box-shadow:0 0 0 1px rgba(0,0,0,.07),0 8px 32px rgba(0,0,0,.12);padding:36px 32px;width:100%;max-width:360px;display:flex;flex-direction:column;gap:18px;text-align:center">'
    +'<div style="font-size:28px">🐒</div>'
    +'<div><div style="font-size:18px;font-weight:700;color:#1c1917;letter-spacing:-.02em">영아부 예배 안내 생성기</div>'
    +'<div style="font-size:13px;color:#a8a29e;margin-top:4px">접근 비밀번호를 입력하세요</div></div>'
    +'<input id="pwInput" type="password" placeholder="비밀번호" autocomplete="current-password" style="width:100%;padding:10px 13px;border:1px solid rgba(0,0,0,.13);border-radius:8px;font-size:15px;font-family:inherit;text-align:center;outline:none;box-sizing:border-box">'
    +'<div id="pwErr" style="font-size:12px;color:#dc2626;min-height:16px"></div>'
    +'<button id="pwBtn" style="background:#b45309;color:#fff;border:none;border-radius:8px;padding:11px;font-size:14px;font-weight:600;font-family:inherit;cursor:pointer">확인</button>'
    +'</div>';
  document.body.appendChild(overlay);
  function check(){{
    var pw=document.getElementById('pwInput').value;
    crypto.subtle.digest('SHA-256',new TextEncoder().encode(pw)).then(function(buf){{
      var hex=Array.from(new Uint8Array(buf)).map(function(b){{return b.toString(16).padStart(2,'0');}}).join('');
      if(hex===HASH){{sessionStorage.setItem(AUTH_KEY,HASH);document.getElementById('pwOverlay').remove();}}
      else{{document.getElementById('pwErr').textContent='비밀번호가 올바르지 않습니다.';document.getElementById('pwInput').value='';}}
    }});
  }}
  document.getElementById('pwBtn').addEventListener('click',check);
  document.getElementById('pwInput').addEventListener('keydown',function(e){{if(e.key==='Enter')check();}});
}})();
</script>
"""

src = SRC.read_text(encoding="utf-8")
out = src.replace("<body>\n", "<body>\n" + GATE, 1)
DEST.parent.mkdir(parents=True, exist_ok=True)
DEST.write_text(out, encoding="utf-8")
print(f"✅  {DEST} ({len(out):,} chars)")

