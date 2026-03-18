UI_HTML = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="SchoolSystem">
<title>SchoolSystem</title>
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;margin:0;padding:0}
:root{
  --bg:#f2f2f7;--bg2:rgba(255,255,255,0.92);--bg3:#fff;--bg4:#f2f2f7;
  --text:#1c1c1e;--text2:#6e6e73;--text3:#aeaeb2;
  --blue:#007aff;--accent:#5856d6;--ok:#34c759;--warn:#ff9f0a;--danger:#ff3b30;
  --border:rgba(0,0,0,0.08);--shadow:0 1px 10px rgba(0,0,0,0.06);
  --r:16px;--rsm:12px;
}
body.dark{
  --bg:#000;--bg2:rgba(28,28,30,0.95);--bg3:#1c1c1e;--bg4:#2c2c2e;
  --text:#fff;--text2:#98989d;--text3:#48484a;
  --border:rgba(255,255,255,0.1);--shadow:0 2px 14px rgba(0,0,0,0.5);
}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding-bottom:80px;transition:background .25s,color .25s}
.nav{position:fixed;top:0;left:0;right:0;z-index:200;padding-top:env(safe-area-inset-top,0);background:var(--bg2);-webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);border-bottom:.5px solid var(--border)}
.nav-in{padding:10px 16px 0}
.nav-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.nav-logo{font-size:17px;font-weight:600;letter-spacing:-.3px}
.nav-right{display:flex;gap:6px}
.icon-btn{width:30px;height:30px;border-radius:50%;border:none;background:var(--bg4);color:var(--text2);font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .15s}
.icon-btn:active{transform:scale(.9)}
.nav-tabs{display:flex;gap:2px;overflow-x:auto;padding-bottom:10px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.nav-tabs::-webkit-scrollbar{display:none}
.tab{padding:7px 14px;border-radius:20px;border:none;background:none;color:var(--text2);font-size:13px;font-weight:500;cursor:pointer;white-space:nowrap;font-family:inherit;flex-shrink:0;transition:all .2s}
.tab.on{background:var(--accent);color:#fff}
.page{max-width:760px;margin:0 auto;padding:16px;padding-top:calc(env(safe-area-inset-top,0px) + 96px)}
.ptitle{font-size:34px;font-weight:700;letter-spacing:-1.5px;margin-bottom:4px}
.psub{font-size:15px;color:var(--text2);margin-bottom:20px}
.slabel{font-size:12px;font-weight:600;color:var(--text2);text-transform:uppercase;letter-spacing:.8px;margin:18px 0 8px 4px}
.card{background:var(--bg3);border-radius:var(--r);padding:18px;margin-bottom:12px;box-shadow:var(--shadow)}
.kgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:4px}
@media(max-width:440px){.kgrid{grid-template-columns:repeat(2,1fr)}}
.kpi{background:var(--bg3);border-radius:var(--rsm);padding:14px 8px;text-align:center;box-shadow:var(--shadow)}
.knum{font-size:28px;font-weight:700;letter-spacing:-1px;line-height:1}
.klbl{font-size:11px;color:var(--text2);margin-top:5px;font-weight:500}
.hwg{background:var(--bg3);border-radius:var(--r);overflow:hidden;box-shadow:var(--shadow);margin-bottom:12px}
.hwr{display:flex;align-items:center;gap:10px;padding:13px 14px;border-bottom:.5px solid var(--border);transition:opacity .2s}
.hwr:last-child{border-bottom:none}
.dc{width:24px;height:24px;border-radius:50%;border:2px solid var(--border);background:none;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:transparent;font-size:11px;transition:all .2s}
.dc:hover,.dc:active{border-color:var(--ok);color:var(--ok)}
.hwb{flex:1;min-width:0}
.hwn{font-size:15px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hwt{display:flex;flex-wrap:wrap;gap:4px;margin-top:4px;align-items:center}
.xb{width:26px;height:26px;border-radius:8px;border:none;background:rgba(255,59,48,.1);color:var(--danger);cursor:pointer;font-size:12px;flex-shrink:0}
.bd{display:inline-flex;align-items:center;padding:2px 7px;border-radius:5px;font-size:11px;font-weight:600;white-space:nowrap}
.sCHEM{background:rgba(0,122,255,.12);color:#0a84ff}
.sMATH,.sM2{background:rgba(88,86,214,.12);color:#5856d6}
.sENG{background:rgba(52,199,89,.12);color:#248a3d}
body.dark .sENG{color:#34c759}
.sICT{background:rgba(255,159,10,.12);color:#c07800}
body.dark .sICT{color:#ff9f0a}
.sCHI{background:rgba(255,59,48,.12);color:#cf2a1f}
body.dark .sCHI{color:#ff453a}
.sLS,.sLIFEED{background:rgba(48,209,88,.12);color:#1a7f37}
body.dark .sLS,body.dark .sLIFEED{color:#30d158}
.sx{background:var(--bg4);color:var(--text2)}
.pH{background:rgba(255,59,48,.12);color:#ff3b30}
.pM{background:rgba(255,159,10,.12);color:#ff9f0a}
.pL{background:rgba(52,199,89,.12);color:#34c759}
.do{color:var(--danger);font-size:12px;font-weight:600}
.dt{color:var(--warn);font-size:12px;font-weight:600}
.ds{color:var(--warn);font-size:12px}
.dn{color:var(--text3);font-size:12px}
.ttbadge{display:inline-flex;align-items:center;gap:8px;background:rgba(88,86,214,.12);color:var(--accent);padding:8px 16px;border-radius:20px;font-size:15px;font-weight:600;margin-bottom:14px}
.ttr{display:flex;align-items:center;gap:10px;padding:12px 14px;border-bottom:.5px solid var(--border)}
.ttr:last-child{border-bottom:none}
.ttr.now{background:rgba(88,86,214,.06)}
.tttime{font-size:12px;color:var(--text2);width:96px;flex-shrink:0;font-variant-numeric:tabular-nums}
.ttsubj{flex:1}
.ttroom{font-size:12px;color:var(--text3)}
.ttdot{width:6px;height:6px;border-radius:50%;background:var(--accent);flex-shrink:0}
/* Exam/Test unified card */
.exr{display:flex;align-items:center;gap:12px;background:var(--bg3);border-radius:var(--rsm);padding:14px;margin-bottom:8px;box-shadow:var(--shadow)}
.exdays{font-size:24px;font-weight:700;letter-spacing:-1px;line-height:1}
.exdl{font-size:11px;color:var(--text2);margin-top:2px}
.seg{display:flex;background:var(--bg4);border-radius:10px;padding:2px;margin-bottom:16px}
.seg-btn{flex:1;padding:7px 4px;border:none;background:none;border-radius:8px;font-size:13px;font-weight:500;cursor:pointer;color:var(--text2);font-family:inherit;transition:all .2s}
.seg-btn.on{background:var(--bg3);color:var(--text);box-shadow:0 1px 4px rgba(0,0,0,.1)}
.fgrp{background:var(--bg3);border-radius:var(--r);overflow:hidden;box-shadow:var(--shadow);margin-bottom:12px}
.frow{display:flex;align-items:center;padding:13px 14px;border-bottom:.5px solid var(--border)}
.frow:last-child{border-bottom:none}
.flbl{font-size:15px;font-weight:500;min-width:68px;flex-shrink:0}
.fctl{flex:1;background:none;border:none;color:var(--text);font-size:15px;text-align:right;font-family:inherit;outline:none;min-width:0}
.fctl::placeholder{color:var(--text3)}
select.fctl option{background:var(--bg3)}
.fta{width:100%;background:none;border:none;color:var(--text);font-size:15px;font-family:inherit;outline:none;resize:none;padding:13px 14px;min-height:76px;display:block}
.fta::placeholder{color:var(--text3)}
.abtn{width:100%;padding:16px;border-radius:var(--rsm);border:none;background:var(--blue);color:#fff;font-size:17px;font-weight:600;cursor:pointer;font-family:inherit;letter-spacing:-.3px;margin-top:4px;transition:opacity .15s}
.abtn:active{opacity:.8}
.gbtn{width:100%;padding:15px;border-radius:var(--rsm);border:1px solid var(--border);background:var(--bg3);color:var(--text2);font-size:17px;font-weight:500;cursor:pointer;font-family:inherit;margin-top:4px;transition:opacity .15s}
.gbtn:active{opacity:.7}
.btn-row{display:flex;gap:8px}
.btn-row .abtn,.btn-row .gbtn{margin-top:0}
.aibox{min-height:120px;margin-bottom:10px}
.aimsg{padding:12px 14px;border-radius:var(--rsm);margin-bottom:8px;font-size:14px;line-height:1.6;word-break:break-word}
.aimsg.user{background:var(--accent);color:#fff;margin-left:48px}
.aimsg.bot{background:var(--bg4);margin-right:48px;white-space:pre-wrap}
.aimsg.bot.loading{color:var(--text2)}
.airow{display:flex;gap:8px;margin-top:10px;align-items:flex-end}
.aiinput{flex:1;background:var(--bg3);border:1px solid var(--border);color:var(--text);padding:11px 13px;border-radius:var(--rsm);font-size:15px;font-family:inherit;outline:none;box-shadow:var(--shadow)}
.aisend{padding:11px 16px;border-radius:var(--rsm);border:none;background:var(--blue);color:#fff;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;flex-shrink:0}
.aichip{padding:7px 13px;border-radius:20px;border:1px solid var(--border);background:var(--bg3);color:var(--text2);font-size:13px;cursor:pointer;font-family:inherit;box-shadow:var(--shadow);white-space:nowrap;flex-shrink:0}
.recitem{display:flex;align-items:center;gap:10px;background:var(--bg3);border-radius:var(--rsm);padding:13px;margin-bottom:8px;box-shadow:var(--shadow)}
.recplay{width:34px;height:34px;border-radius:50%;border:none;background:var(--blue);color:#fff;font-size:13px;cursor:pointer;flex-shrink:0}
.recinfo{flex:1;min-width:0}
.recname{font-size:14px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.recmeta{font-size:12px;color:var(--text2);margin-top:3px}
.pbar{height:4px;background:var(--bg4);border-radius:2px;overflow:hidden;margin-top:6px}
.pf{height:100%;border-radius:2px;background:var(--accent);transition:width .4s}
.upload-zone{border:2px dashed var(--border);border-radius:var(--r);padding:32px 20px;text-align:center;cursor:pointer;transition:border-color .2s;margin-bottom:12px}
.upload-zone:hover,.upload-zone.drag{border-color:var(--blue)}
.upload-zone-i{font-size:40px;margin-bottom:10px}
.upload-zone-t{font-size:15px;font-weight:500;color:var(--text2)}
.upload-zone-s{font-size:13px;color:var(--text3);margin-top:4px}
.wb-item{background:var(--bg3);border-radius:var(--rsm);padding:14px;margin-bottom:8px;box-shadow:var(--shadow)}
.wb-img{width:100%;border-radius:8px;margin-bottom:10px;max-height:200px;object-fit:cover}
.wb-hw{padding:8px 10px;background:var(--bg4);border-radius:8px;margin-bottom:6px;cursor:pointer;transition:background .15s}
.wb-hw:hover{background:var(--bg5,#e5e5ea)}
.wb-hw-title{font-size:14px;font-weight:500}
.wb-hw-meta{font-size:12px;color:var(--text2);margin-top:2px}
.empty{text-align:center;padding:36px 20px;color:var(--text2)}
.empi{font-size:34px;margin-bottom:10px}
.empt{font-size:15px;font-weight:500}
.emps{font-size:13px;color:var(--text3);margin-top:4px}
.section{display:none}.section.on{display:block}
#toast{position:fixed;bottom:calc(env(safe-area-inset-bottom,0px) + 90px);left:50%;transform:translateX(-50%) translateY(10px);background:rgba(28,28,30,.92);color:#fff;padding:10px 16px;border-radius:20px;font-size:14px;font-weight:500;opacity:0;transition:all .25s;z-index:500;pointer-events:none;-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);white-space:nowrap;max-width:calc(100vw - 40px);display:flex;align-items:center;gap:8px}
#toast.on{opacity:1;transform:translateX(-50%) translateY(0);pointer-events:auto}
.bbar{display:none;position:fixed;bottom:0;left:0;right:0;background:var(--bg2);-webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);border-top:.5px solid var(--border);padding:6px 0 env(safe-area-inset-bottom,10px);z-index:100}
.bt{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;border:none;background:none;cursor:pointer;font-family:inherit;padding:4px 0;-webkit-tap-highlight-color:transparent}
.bti{font-size:22px;line-height:1.2}
.btl{font-size:10px;font-weight:500;color:var(--text3)}
.bt.on .btl{color:var(--blue)}
@media(max-width:680px){
  .bbar{display:flex}
  .nav-tabs{display:none}
  .page{padding-top:calc(env(safe-area-inset-top,0px) + 72px)}
  body{padding-bottom:calc(env(safe-area-inset-bottom,0px) + 70px)}
}
</style>
</head>
<body>
<div class="nav">
  <div class="nav-in">
    <div class="nav-top">
      <div class="nav-logo">📚 SchoolSystem</div>
      <div class="nav-right">
        <button class="icon-btn" onclick="toggleDark()">◑</button>
        <button class="icon-btn" onclick="location.href='/admin'">⚙️</button>
        <button class="icon-btn" onclick="location.href='/logout'">⏏</button>
      </div>
    </div>
    <div class="nav-tabs">
      <button class="tab on" onclick="go('dash',this)">主頁</button>
      <button class="tab" onclick="go('tt',this)">時間表</button>
      <button class="tab" onclick="go('hw',this)">功課</button>
      <button class="tab" onclick="go('add',this)">＋ 加功課</button>
      <button class="tab" onclick="go('exam',this)">考試 &amp; 小測</button>
      <button class="tab" onclick="go('rec',this)">🎙️ 錄音</button>
      <button class="tab" onclick="go('ai',this)">🤖 AI</button>
      <button class="tab" onclick="go('stats',this)">統計</button>
    </div>
  </div>
</div>
<div class="bbar">
  <button class="bt on" id="bb-dash" onclick="goB('dash',this)"><div class="bti">🏠</div><div class="btl">主頁</div></button>
  <button class="bt" id="bb-tt" onclick="goB('tt',this)"><div class="bti">📋</div><div class="btl">時間表</div></button>
  <button class="bt" id="bb-hw" onclick="goB('hw',this)"><div class="bti">📝</div><div class="btl">功課</div></button>
  <button class="bt" id="bb-add" onclick="goB('add',this)"><div class="bti">➕</div><div class="btl">加功課</div></button>
  <button class="bt" id="bb-exam" onclick="goB('exam',this)"><div class="bti">📅</div><div class="btl">考試</div></button>
  <button class="bt" id="bb-ai" onclick="goB('ai',this)"><div class="bti">🤖</div><div class="btl">AI</div></button>
</div>
<div class="page">

  <!-- DASHBOARD -->
  <div class="section on" id="s-dash">
    <div class="ptitle" id="d-date"></div>
    <div class="psub" id="d-day"></div>
    <div class="kgrid" id="d-kpi"></div>
    <div id="d-cycle" style="margin:12px 0"></div>
    <div class="slabel">今日待做</div>
    <div id="d-hw"></div>
    <div class="slabel">即將考試 &amp; 小測</div>
    <div id="d-ex"></div>
  </div>

  <!-- TIMETABLE -->
  <div class="section" id="s-tt">
    <div class="ptitle">時間表</div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px">
      <button onclick="loadTT(0)" class="abtn" style="width:auto;padding:8px 16px;font-size:14px;border-radius:20px;margin:0">今日</button>
      <button onclick="loadTT(1)" class="gbtn" style="width:auto;padding:7px 12px;font-size:13px;border-radius:20px;margin:0">Day1</button>
      <button onclick="loadTT(2)" class="gbtn" style="width:auto;padding:7px 12px;font-size:13px;border-radius:20px;margin:0">Day2</button>
      <button onclick="loadTT(3)" class="gbtn" style="width:auto;padding:7px 12px;font-size:13px;border-radius:20px;margin:0">Day3</button>
      <button onclick="loadTT(4)" class="gbtn" style="width:auto;padding:7px 12px;font-size:13px;border-radius:20px;margin:0">Day4</button>
      <button onclick="loadTT(5)" class="gbtn" style="width:auto;padding:7px 12px;font-size:13px;border-radius:20px;margin:0">Day5</button>
      <button onclick="loadTT(6)" class="gbtn" style="width:auto;padding:7px 12px;font-size:13px;border-radius:20px;margin:0">Day6</button>
      <button onclick="loadTT(7)" class="gbtn" style="width:auto;padding:7px 12px;font-size:13px;border-radius:20px;margin:0">Day7</button>
    </div>
    <div id="tt-content"></div>
  </div>

  <!-- HOMEWORK LIST -->
  <div class="section" id="s-hw">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
      <div class="ptitle" style="margin:0">功課</div>
      <select id="f-filter" onchange="loadHW()" style="background:var(--bg3);border:none;color:var(--text);font-size:13px;padding:7px 12px;border-radius:20px;font-family:inherit;box-shadow:var(--shadow);outline:none">
        <option value="">全部</option>
        <option>CHEM</option><option>MATH</option><option>M2</option>
        <option>ENG</option><option>CHI</option><option>ICT</option><option>LS</option>
      </select>
    </div>
    <div id="hw-list"></div>
  </div>

  <!-- ADD HOMEWORK -->
  <div class="section" id="s-add">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0">
      <div><div class="ptitle" style="margin-bottom:4px">加功課</div><div class="psub" style="margin-bottom:16px">記錄新嘅功課或小測</div></div>
      <button onclick="go('wb',null);document.getElementById('bb-add')&&document.getElementById('bb-add').classList.remove('on')" style="display:flex;flex-direction:column;align-items:center;gap:3px;background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:10px 14px;cursor:pointer;font-family:inherit;box-shadow:var(--shadow)">
        <span style="font-size:22px">📷</span>
        <span style="font-size:11px;color:var(--text2);font-weight:500">白板掃描</span>
      </button>
    </div>
    <div class="fgrp">
      <div class="frow"><div class="flbl">標題</div><input class="fctl" id="a-title" placeholder="功課標題"></div>
      <div class="frow"><div class="flbl">科目</div>
        <select class="fctl" id="a-subj"><option>CHEM</option><option>MATH</option><option>M2</option><option>ENG</option><option>CHI</option><option>ICT</option><option>LS</option><option>LIFE-ED</option><option>CSD</option><option>PE</option></select>
      </div>
      <div class="frow"><div class="flbl">類型</div>
        <select class="fctl" id="a-type"><option>功課</option><option>小測</option><option>考試</option><option>報告</option><option>Project</option><option>默書</option><option>實驗</option></select>
      </div>
      <div class="frow"><div class="flbl">截止</div><input class="fctl" id="a-due" type="date"></div>
      <div class="frow"><div class="flbl">優先</div>
        <select class="fctl" id="a-pri"><option>高</option><option selected>中</option><option>低</option></select>
      </div>
    </div>
    <div class="fgrp"><textarea class="fta" id="a-notes" placeholder="備註（可選）"></textarea></div>
    <div class="btn-row">
      <button class="gbtn" style="flex:1" onclick="clearAddForm()">清除</button>
      <button class="abtn" style="flex:2" onclick="addHW()">加入功課表</button>
    </div>
  </div>

  <!-- EXAM & TEST (unified) -->
  <div class="section" id="s-exam">
    <div class="ptitle">考試 &amp; 小測</div>
    <div class="psub">統一管理所有測試</div>
    <!-- Segment control -->
    <div class="seg">
      <button class="seg-btn on" id="seg-list" onclick="examSeg('list')">📋 列表</button>
      <button class="seg-btn" id="seg-add" onclick="examSeg('add')">➕ 新增</button>
    </div>
    <!-- List view -->
    <div id="exam-list-panel">
      <div class="slabel">即將考試 &amp; 小測</div>
      <div id="ex-list"></div>
    </div>
    <!-- Add view -->
    <div id="exam-add-panel" style="display:none">
      <div class="slabel">新增考試 / 小測</div>
      <div class="fgrp">
        <div class="frow"><div class="flbl">科目</div>
          <select class="fctl" id="e-subj"><option>CHEM</option><option>MATH</option><option>M2</option><option>ENG</option><option>CHI</option><option>ICT</option><option>LS</option></select>
        </div>
        <div class="frow"><div class="flbl">類型</div>
          <select class="fctl" id="e-etype"><option>考試</option><option>小測</option><option>默書</option><option>統測</option></select>
        </div>
        <div class="frow"><div class="flbl">名稱</div><input class="fctl" id="e-title" placeholder="例：第二學期統測"></div>
        <div class="frow"><div class="flbl">日期</div><input class="fctl" id="e-date" type="date"></div>
        <div class="frow"><div class="flbl">範圍</div><input class="fctl" id="e-scope" placeholder="例：第9–12節"></div>
      </div>
      <div class="btn-row">
        <button class="gbtn" style="flex:1" onclick="clearExamForm()">清除</button>
        <button class="abtn" style="flex:2" onclick="addExam()">加入</button>
      </div>
    </div>
  </div>

  <!-- WHITEBOARD -->
  <div class="section" id="s-wb">
    <div class="ptitle">白板拍照</div>
    <div class="psub">AI 自動識別功課內容</div>
    <input type="file" id="wb-input" accept="image/*" capture="environment" style="display:none" onchange="handleWB(this)">
    <input type="file" id="wb-browse" accept="image/*" style="display:none" onchange="handleWB(this)">
    <div class="upload-zone" id="wb-zone" onclick="document.getElementById('wb-input').click()">
      <div class="upload-zone-i">📷</div>
      <div class="upload-zone-t">拍攝白板</div>
      <div class="upload-zone-s">撳此處開啟相機</div>
    </div>
    <button onclick="document.getElementById('wb-browse').click()" class="gbtn" style="margin-bottom:16px">🖼️ 從相簿選擇</button>
    <div id="wb-preview" style="display:none">
      <img id="wb-img" class="wb-img" alt="whiteboard">
      <div id="wb-status" style="font-size:13px;color:var(--text2);margin-bottom:10px;text-align:center"></div>
      <div id="wb-results"></div>
    </div>
  </div>

  <!-- RECORDING -->
  <div class="section" id="s-rec">
    <div class="ptitle">錄音</div>
    <div class="psub">錄製課堂筆記</div>
    <div class="card">
      <div style="font-size:13px;color:var(--text2);margin-bottom:16px;line-height:1.6">撳「開始錄音」→ iOS/Android 原生錄音 → 選好後上載</div>
      <div style="display:flex;gap:10px;margin-bottom:16px">
        <div style="flex:1">
          <div style="font-size:12px;color:var(--text2);margin-bottom:5px">科目</div>
          <select id="rec-subj" style="width:100%;background:var(--bg4);border:none;color:var(--text);padding:9px 10px;border-radius:10px;font-family:inherit;font-size:14px;outline:none">
            <option>CHEM</option><option>MATH</option><option>M2</option><option>ENG</option><option>CHI</option><option>ICT</option><option>LS</option><option>LIFE-ED</option>
          </select>
        </div>
        <div style="flex:1">
          <div style="font-size:12px;color:var(--text2);margin-bottom:5px">堂次</div>
          <input id="rec-period" placeholder="例：第1堂" style="width:100%;background:var(--bg4);border:none;color:var(--text);padding:9px 10px;border-radius:10px;font-family:inherit;font-size:14px;outline:none">
        </div>
      </div>
      <input type="file" id="rec-input-capture" accept="audio/*" capture="microphone" style="display:none" onchange="handleRecFile(this)">
      <input type="file" id="rec-input-browse" accept="audio/*,.m4a,.mp3,.wav" style="display:none" onchange="handleRecFile(this)">
      <button style="width:100%;padding:17px;border-radius:var(--rsm);border:none;background:var(--blue);color:#fff;font-size:17px;font-weight:600;cursor:pointer;font-family:inherit" onclick="document.getElementById('rec-input-capture').click()">🎙️ 開始錄音</button>
      <button onclick="document.getElementById('rec-input-browse').click()" style="width:100%;margin-top:10px;padding:14px;border-radius:var(--rsm);border:1px solid var(--border);background:var(--bg3);color:var(--text2);font-size:15px;font-weight:500;cursor:pointer;font-family:inherit">📁 上載現有音頻</button>
      <div id="rec-status" style="font-size:13px;color:var(--text2);margin-top:12px;min-height:18px"></div>
      <div id="rec-preview" style="display:none;margin-top:16px">
        <audio id="rec-preview-audio" controls style="width:100%;border-radius:10px;margin-bottom:12px"></audio>
        <div class="btn-row">
          <button class="gbtn" style="flex:1" onclick="cancelRecPreview()">取消</button>
          <button class="abtn" style="flex:2;margin-top:0" onclick="confirmUpload()">確認上載</button>
        </div>
      </div>
    </div>
    <div class="slabel">錄音記錄</div>
    <div id="rec-list"></div>
  </div>

  <!-- AI -->
  <div class="section" id="s-ai">
    <div class="ptitle">AI 助手</div>
    <div class="psub">DeepSeek Reasoner 驅動</div>

    <!-- Today priorities card (no AI key needed) -->
    <div class="card" id="ai-priorities-card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
        <div style="font-size:15px;font-weight:600">⚡ 今日優先事項</div>
        <button onclick="loadPriorities()" style="background:var(--bg4);border:none;color:var(--text2);padding:5px 12px;border-radius:10px;cursor:pointer;font-size:12px;font-family:inherit">刷新</button>
      </div>
      <div id="ai-priorities"><div class="empty"><div class="empt">載入中...</div></div></div>
    </div>

    <!-- Study plan generator -->
    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">📅 AI 溫書計劃</div>
      <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap">
        <button class="aichip" onclick="aiStudyPlan(1)">今晚</button>
        <button class="aichip" onclick="aiStudyPlan(3)">3日計劃</button>
        <button class="aichip" onclick="aiStudyPlan(7)">1週計劃</button>
      </div>
      <div id="study-plan-result" style="display:none">
        <div style="background:var(--bg4);border-radius:var(--rsm);padding:14px;font-size:14px;line-height:1.7;white-space:pre-wrap;color:var(--text)" id="study-plan-text"></div>
      </div>
      <div id="study-plan-loading" style="display:none;text-align:center;color:var(--text2);font-size:13px;padding:20px">⏳ AI 思考中，請稍等...</div>
    </div>

    <!-- Quick chips -->
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px">
      <button class="aichip" onclick="aiQ('今日有咩功課？')">📋 今日功課</button>
      <button class="aichip" onclick="aiQ('哪科功課最緊急？')">⚡ 最緊急</button>
      <button class="aichip" onclick="aiQ('考試前溫書建議')">🎯 考試建議</button>
      <button class="aichip" onclick="aiQ('有咩空堂可以做功課？')">🕐 空堂</button>
    </div>

    <!-- Chat -->
    <div class="aibox" id="ai-chat"></div>
    <div class="airow">
      <input class="aiinput" id="ai-input" placeholder="問 AI 任何問題..." onkeydown="if(event.key==='Enter')sendAI()">
      <button class="aisend" onclick="sendAI()">送出</button>
    </div>
    <div id="ai-status" style="font-size:12px;color:var(--text3);text-align:center;margin-top:6px"></div>
  </div>

  <!-- STATS -->
  <div class="section" id="s-stats">
    <div class="ptitle">統計</div>
    <div class="psub">學習表現一覽</div>
    <div class="kgrid" id="st-kpi"></div>
    <div class="slabel">各科功課量</div>
    <div class="card"><div id="st-subj"></div></div>
  </div>

</div>
<div id="toast"></div>
<script>
const KEY="KEY_PLACEHOLDER";
const $=id=>document.getElementById(id);
const api=(p,o={})=>fetch(p+(p.includes('?')?'&':'?')+'key='+KEY,o).then(r=>r.json());
let dark=window.matchMedia&&window.matchMedia('(prefers-color-scheme:dark)').matches;
if(dark)document.body.classList.add('dark');
function toggleDark(){dark=!dark;document.body.classList.toggle('dark',dark);}

function go(t,el){
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('on'));
  document.querySelectorAll('.tab').forEach(b=>b.classList.remove('on'));
  $('s-'+t).classList.add('on');
  if(el)el.classList.add('on');
  if(t==='dash')loadDash();
  else if(t==='tt')loadTT(0);
  else if(t==='hw')loadHW();
  else if(t==='exam'){loadExams();examSeg('list');}
  else if(t==='stats')loadStats();
  else if(t==='rec')loadRecList();
  else if(t==='ai'){loadPriorities();}
}
function goB(t,el){
  document.querySelectorAll('.bt').forEach(b=>b.classList.remove('on'));
  el.classList.add('on');
  go(t,null);
}
function examSeg(v){
  $('seg-list').classList.toggle('on',v==='list');
  $('seg-add').classList.toggle('on',v==='add');
  $('exam-list-panel').style.display=v==='list'?'':'none';
  $('exam-add-panel').style.display=v==='add'?'':'none';
  if(v==='list')loadExams();
}

function sb(s){const m={CHEM:'CHEM',MATH:'MATH',M2:'M2',ENG:'ENG',ICT:'ICT',CHI:'CHI',LS:'LS','LIFE-ED':'LIFEED'};return'<span class="bd s'+(m[s]||'x')+'">'+s+'</span>';}
function pb(p){return'<span class="bd p'+(p==='高'?'H':p==='低'?'L':'M')+'">'+p+'</span>';}
function due(d){
  if(!d)return'';
  const df=Math.ceil((new Date(d)-new Date())/86400000);
  if(df<0)return'<span class="do">逾期'+Math.abs(df)+'天</span>';
  if(df===0)return'<span class="dt">今日截止</span>';
  if(df<=2)return'<span class="ds">'+df+'天後</span>';
  return'<span class="dn">'+d+'</span>';
}

let _tt;
function toast(msg,ms=2500,undoId){
  clearTimeout(_tt);
  const el=$('toast');
  if(undoId){
    el.innerHTML=msg+' <button onclick="undoHW('+undoId+')" style="background:rgba(255,255,255,.22);border:none;color:#fff;padding:3px 10px;border-radius:10px;cursor:pointer;font-size:13px;font-family:inherit;margin-left:4px">撤銷</button>';
  }else{el.textContent=msg;}
  el.classList.add('on');
  _tt=setTimeout(()=>{el.classList.remove('on');setTimeout(()=>el.textContent='',300);},ms);
}

function hwRow(h,del=true){
  return'<div class="hwr" id="hw-'+h.id+'">'+
    '<button class="dc" onclick="markDone('+h.id+')" title="完成">✓</button>'+
    '<div class="hwb"><div class="hwn">'+h.title+'</div>'+
    '<div class="hwt">'+sb(h.subject)+'<span class="bd sx">'+h.hw_type+'</span>'+pb(h.priority)+due(h.due_date)+'</div></div>'+
    (del?'<button class="xb" onclick="delHW('+h.id+')">✕</button>':'')+
    '</div>';
}

function exCard(e){
  const dl=Math.ceil((new Date(e.exam_date)-new Date())/86400000);
  const c=dl<=3?'var(--danger)':dl<=7?'var(--warn)':'var(--ok)';
  const typeBadge=e.title&&e.title.includes('小測')?'<span class="bd sx">小測</span>':e.title&&e.title.includes('默書')?'<span class="bd sx">默書</span>':'';
  return'<div class="exr">'+sb(e.subject)+
    '<div style="flex:1;margin-left:10px">'+
    (typeBadge?typeBadge+'<br>':'')+
    '<div style="font-size:15px;font-weight:600;margin-top:2px">'+(e.title||e.subject+' 考試')+'</div>'+
    (e.scope?'<div style="font-size:12px;color:var(--text2);margin-top:2px">'+e.scope+'</div>':'')+
    '</div>'+
    '<div style="text-align:right;flex-shrink:0"><div class="exdays" style="color:'+c+'">'+(dl<0?'已過':dl)+'</div><div class="exdl">'+(dl<0?'':'天後')+'</div></div>'+
    '<button class="xb" style="margin-left:10px" onclick="delExam('+e.id+')">✕</button></div>';
}

async function loadDash(){
  const now=new Date();
  const ms=['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'];
  const ds=['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
  $('d-date').textContent=now.getDate()+' '+ms[now.getMonth()]+' '+now.getFullYear();
  $('d-day').textContent=ds[now.getDay()];
  const[d,s]=await Promise.all([api('/api/today'),api('/api/stats')]);
  $('d-kpi').innerHTML=
    '<div class="kpi"><div class="knum" style="color:var(--warn)">'+s.pending+'</div><div class="klbl">待做</div></div>'+
    '<div class="kpi"><div class="knum" style="color:var(--ok)">'+s.done+'</div><div class="klbl">完成</div></div>'+
    '<div class="kpi"><div class="knum" style="color:var(--danger)">'+s.overdue+'</div><div class="klbl">逾期</div></div>'+
    '<div class="kpi"><div class="knum" style="color:var(--accent)">'+s.total+'</div><div class="klbl">總計</div></div>';
  $('d-cycle').innerHTML=d.cycle_day
    ?'<span class="ttbadge">📅 今日 Day '+d.cycle_day+(d.is_school_day?'':' · 假期')+'</span>'
    :'<span class="ttbadge">🏠 假期 / 非上學日</span>';
  const hw=d.overdue_and_today||[];
  $('d-hw').innerHTML=hw.length?'<div class="hwg">'+hw.map(h=>hwRow(h,false)).join('')+'</div>':
    '<div class="empty"><div class="empi">🎉</div><div class="empt">今日無待做功課</div></div>';
  const ex=d.upcoming_exams||[];
  $('d-ex').innerHTML=ex.length?ex.map(e=>exCard(e)).join(''):
    '<div class="empty"><div class="empi">📅</div><div class="empt">暫無即將考試</div></div>';
}

function nowHHMM(){const n=new Date();return String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');}
async function loadTT(override){
  let dayNum=override,label='';
  if(override===0){
    const c=await api('/api/cycle');
    if(!c.is_school_day){$('tt-content').innerHTML='<div class="empty"><div class="empi">🏠</div><div class="empt">今日非上學日</div><div class="emps">下一個上學日：'+c.next_school_date+' (Day '+c.next_cycle_day+')</div></div>';return;}
    dayNum=c.cycle_day;label='今日 · ';
  }
  if(!dayNum){$('tt-content').innerHTML='<div class="empty"><div class="empt">無法獲取 Cycle Day</div></div>';return;}
  const data=await api('/api/timetable?day='+dayNum);
  const slots=data.slots||[],nt=nowHHMM();
  $('tt-content').innerHTML='<div class="ttbadge">📋 '+label+'Day '+dayNum+'</div>'+
    '<div class="hwg">'+slots.map(s=>{
      const now=nt>=s.start&&nt<s.end;
      return'<div class="ttr'+(now?' now':'')+'">'+
        (now?'<div class="ttdot"></div>':'<div style="width:6px"></div>')+
        '<div class="tttime">'+s.start+'–'+s.end+'</div>'+
        '<div class="ttsubj">'+sb(s.subject)+'</div>'+
        '<div class="ttroom">'+s.room+'</div></div>';
    }).join('')+'</div>';
}

async function loadHW(){
  const subj=$('f-filter')?.value||'';
  const rows=await api('/api/hw?done=0'+(subj?'&subject='+subj:''));
  $('hw-list').innerHTML=rows.length?'<div class="hwg">'+rows.map(h=>hwRow(h,true)).join('')+'</div>':
    '<div class="empty"><div class="empi">✅</div><div class="empt">暫無待做功課</div></div>';
}

async function markDone(id){
  await api('/api/hw/'+id+'/done',{method:'POST'});
  const el=$('hw-'+id);
  if(el){el.style.opacity='0';el.style.transition='opacity .2s';setTimeout(()=>el.remove(),200);}
  toast('✅ 已完成',4000,id);setTimeout(()=>loadDash(),300);
}
async function undoHW(id){
  clearTimeout(_tt);$('toast').classList.remove('on');
  await api('/api/hw/'+id+'/undone',{method:'POST'});
  toast('↩️ 已撤銷');loadDash();loadHW();
}
async function delHW(id){
  if(!confirm('確定刪除？'))return;
  await api('/api/hw/'+id,{method:'DELETE'});
  const el=$('hw-'+id);if(el){el.style.opacity='0';setTimeout(()=>el.remove(),200);}
  toast('🗑️ 已刪除');
}
function clearAddForm(){
  ['a-title','a-notes','a-due'].forEach(id=>{if($(id))$(id).value='';});
  $('a-subj').selectedIndex=0;$('a-type').selectedIndex=0;$('a-pri').selectedIndex=1;
  toast('🗑️ 已清除');
}
async function addHW(){
  const t=$('a-title').value.trim();
  if(!t){toast('⚠️ 請輸入標題');return;}
  await api('/api/hw',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({title:t,subject:$('a-subj').value,hw_type:$('a-type').value,due_date:$('a-due').value,priority:$('a-pri').value,notes:$('a-notes').value})});
  toast('📥 已加入功課表！');$('a-title').value='';$('a-notes').value='';$('a-due').value='';
}

function clearExamForm(){
  ['e-title','e-date','e-scope'].forEach(id=>{if($(id))$(id).value='';});
  $('e-subj').selectedIndex=0;$('e-etype').selectedIndex=0;toast('🗑️ 已清除');
}
async function addExam(){
  const d=$('e-date').value;if(!d){toast('⚠️ 請選擇日期');return;}
  const etype=$('e-etype').value;
  const title=$('e-title').value||($('e-subj').value+' '+etype);
  await api('/api/exams',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({subject:$('e-subj').value,title:title,exam_date:d,scope:$('e-scope').value})});
  toast('📅 '+etype+'已加入！');clearExamForm();examSeg('list');
}
async function loadExams(){
  const rows=await api('/api/exams');
  $('ex-list').innerHTML=rows.length?rows.map(e=>exCard(e)).join(''):
    '<div class="empty"><div class="empi">📅</div><div class="empt">暫無記錄</div><div class="emps">撳「新增」加入考試或小測</div></div>';
}
async function delExam(id){
  if(!confirm('確定刪除？'))return;
  await api('/api/exams/'+id,{method:'DELETE'});toast('🗑️ 已刪除');loadExams();
}

// ── Whiteboard ────────────────────────────────────────────────────────────────
async function handleWB(input){
  const file=input.files[0];if(!file)return;
  // Show image preview immediately
  const url=URL.createObjectURL(file);
  $('wb-img').src=url;$('wb-preview').style.display='block';
  $('wb-results').innerHTML='';
  $('wb-status').textContent='上載中...';
  const fd=new FormData();fd.append('file',file,file.name||'whiteboard.jpg');
  try{
    const r=await fetch('/api/whiteboard/upload?key='+KEY,{method:'POST',body:fd}).then(x=>x.json());
    if(!r.ok){$('wb-status').textContent='❌ 上載失敗：'+(r.error||'');return;}

    let html='';

    // AI results
    if(r.homeworks&&r.homeworks.length>0){
      $('wb-status').textContent='✅ AI 識別到 '+r.homeworks.length+' 項功課，撳加入：';
      html+=r.homeworks.map((h,i)=>{
        const hj=encodeURIComponent(JSON.stringify(h));
        return'<div class="wb-hw" onclick="addWBHWOne(''+hj+'')">'+
          '<div style="display:flex;align-items:center;gap:8px">'+sb(h.subject||'CHI')+
          '<div><div class="wb-hw-title">'+(h.title||'未識別標題')+'</div>'+
          (h.due_date?'<div class="wb-hw-meta">截止：'+h.due_date+'</div>':'')+
          '</div></div></div>';
      }).join('');
    }else if(r.ai_note){
      $('wb-status').textContent='📷 圖片已儲存 · '+r.ai_note;
    }else if(r.ai_errors){
      $('wb-status').textContent='⚠️ AI 識別失敗，請手動輸入';
    }else{
      $('wb-status').textContent='📷 圖片已儲存';
    }

    // Always show manual entry form
    html+='<div style="margin-top:14px;padding:14px;background:var(--bg4);border-radius:var(--rsm)">'+
      '<div style="font-size:13px;font-weight:600;color:var(--text2);margin-bottom:10px">✏️ 手動加入功課</div>'+
      '<div style="display:flex;gap:8px;margin-bottom:8px">'+
        '<select id="wb-subj" style="flex:1;background:var(--bg3);border:none;color:var(--text);padding:9px;border-radius:8px;font-family:inherit;font-size:14px;outline:none">'+
          '<option>CHEM</option><option>MATH</option><option>M2</option><option>ENG</option>'+
          '<option>CHI</option><option>ICT</option><option>LS</option><option>LIFE-ED</option>'+
        '</select>'+
        '<input id="wb-due" type="date" style="flex:1;background:var(--bg3);border:none;color:var(--text);padding:9px;border-radius:8px;font-family:inherit;font-size:14px;outline:none">'+
      '</div>'+
      '<input id="wb-title" placeholder="功課描述" style="width:100%;background:var(--bg3);border:none;color:var(--text);padding:10px;border-radius:8px;font-family:inherit;font-size:14px;outline:none;margin-bottom:8px">'+
      '<button onclick="addWBManual()" style="width:100%;padding:12px;border-radius:8px;border:none;background:var(--blue);color:#fff;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit">加入功課表</button>'+
    '</div>';

    $('wb-results').innerHTML=html;
  }catch(e){$('wb-status').textContent='❌ '+e.message;}
  input.value='';
}

async function addWBHWOne(hj){
  const h=JSON.parse(decodeURIComponent(hj));
  await api('/api/hw',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({title:h.title||'白板功課',subject:h.subject||'CHI',
      due_date:h.due_date||'',source:'白板拍照',priority:'中'})});
  toast('📥 已加入：'+(h.title||'白板功課'));
}

async function addWBManual(){
  const title=$('wb-title')?.value.trim();
  if(!title){toast('⚠️ 請輸入功課描述');return;}
  const subj=$('wb-subj')?.value||'CHI';
  const due=$('wb-due')?.value||'';
  await api('/api/hw',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({title,subject:subj,due_date:due,source:'白板拍照',priority:'中'})});
  toast('📥 已加入：'+title);
  if($('wb-title'))$('wb-title').value='';
  if($('wb-due'))$('wb-due').value='';
}

// ── Recording ─────────────────────────────────────────────────────────────────
let pendingBlob=null;
function handleRecFile(input){
  const file=input.files[0];if(!file)return;
  pendingBlob=file;
  $('rec-preview-audio').src=URL.createObjectURL(file);
  $('rec-preview').style.display='block';
  $('rec-status').textContent='已選擇：'+file.name;
  input.value='';
}
function cancelRecPreview(){
  pendingBlob=null;$('rec-preview').style.display='none';
  $('rec-status').textContent='';$('rec-preview-audio').pause();$('rec-preview-audio').src='';
}
async function confirmUpload(){
  if(!pendingBlob){toast('⚠️ 未選擇檔案');return;}
  $('rec-status').textContent='上載中...';
  const fd=new FormData();
  fd.append('file',pendingBlob,pendingBlob.name||'recording.m4a');
  fd.append('subject',$('rec-subj').value);fd.append('period',$('rec-period').value);
  try{
    const r=await fetch('/api/recordings/upload?key='+KEY,{method:'POST',body:fd}).then(x=>x.json());
    if(r.ok){toast('🎙️ 錄音已儲存！');cancelRecPreview();$('rec-period').value='';loadRecList();}
    else{$('rec-status').textContent='❌ '+(r.error||'');}
  }catch(e){$('rec-status').textContent='❌ '+e.message;}
}
async function loadRecList(){
  const rows=await api('/api/recordings');
  $('rec-list').innerHTML=rows.length?rows.map(r=>
    '<div class="recitem" id="rec-'+r.id+'">'+
    '<button class="recplay" onclick="playRec('+r.id+',this)">▶</button>'+
    '<div class="recinfo"><div class="recname">'+(r.subject?'['+r.subject+'] ':'')+( r.period||r.rec_date)+'</div>'+
    '<div class="recmeta">'+r.rec_date+'</div></div>'+
    '<button class="xb" onclick="delRec('+r.id+')">✕</button></div>'
  ).join(''):'<div class="empty"><div class="empi">🎙️</div><div class="empt">暫無錄音</div></div>';
}
let curAudio=null,curPlayBtn=null;
function playRec(id,btn){
  if(curAudio){curAudio.pause();curAudio=null;if(curPlayBtn)curPlayBtn.textContent='▶';if(curPlayBtn===btn){curPlayBtn=null;return;}}
  curAudio=new Audio('/api/recordings/'+id+'?key='+KEY);curAudio.play();
  btn.textContent='⏸';curPlayBtn=btn;curAudio.onended=()=>{btn.textContent='▶';curAudio=null;curPlayBtn=null;};
}
async function delRec(id){
  if(!confirm('確定刪除？'))return;
  await api('/api/recordings/'+id,{method:'DELETE'});
  const el=$('rec-'+id);if(el){el.style.opacity='0';setTimeout(()=>el.remove(),200);}toast('🗑️ 已刪除');
}

// ── AI ─────────────────────────────────────────────────────────────────────────
function aiQ(q){$('ai-input').value=q;sendAI();}

async function loadPriorities(){
  const el=$('ai-priorities');
  try{
    const r=await api('/api/study/priorities');
    if(r.error){el.innerHTML='<div class="empty"><div class="empt">載入失敗</div></div>';return;}
    let html='';
    if(r.urgent&&r.urgent.length){
      html+='<div style="margin-bottom:10px"><div style="font-size:12px;font-weight:600;color:var(--danger);margin-bottom:6px">🔴 今日截止</div>';
      html+=r.urgent.map(h=>'<div class="hwr" style="border-radius:8px;margin-bottom:4px">'+sb(h.subject)+'<div class="hwb"><div class="hwn">'+h.title+'</div></div></div>').join('');
      html+='</div>';
    }
    if(r.due_tomorrow&&r.due_tomorrow.length){
      html+='<div style="margin-bottom:10px"><div style="font-size:12px;font-weight:600;color:var(--warn);margin-bottom:6px">🟡 明日截止</div>';
      html+=r.due_tomorrow.map(h=>'<div class="hwr" style="border-radius:8px;margin-bottom:4px">'+sb(h.subject)+'<div class="hwb"><div class="hwn">'+h.title+'</div></div></div>').join('');
      html+='</div>';
    }
    if(r.exams_soon&&r.exams_soon.length){
      html+='<div style="margin-bottom:10px"><div style="font-size:12px;font-weight:600;color:var(--danger);margin-bottom:6px">📅 7日內考試</div>';
      html+=r.exams_soon.map(e=>'<div style="display:flex;align-items:center;gap:8px;padding:8px;background:var(--bg4);border-radius:8px;margin-bottom:4px">'+sb(e.subject)+'<span style="font-size:13px;flex:1">'+(e.title||e.subject+'考試')+'</span><span style="font-size:12px;color:var(--danger)">'+Math.round(e.days_left||0)+'天後</span></div>').join('');
      html+='</div>';
    }
    if(r.free_periods&&r.free_periods.length){
      html+='<div style="font-size:12px;color:var(--text2)">🕐 今日空堂：'+r.free_periods.map(p=>p.type+' '+p.start+'-'+p.end).join('、')+'</div>';
    }
    if(!r.urgent?.length&&!r.due_tomorrow?.length&&!r.exams_soon?.length){
      html='<div class="empty"><div class="empi">🎉</div><div class="empt">近期無緊急功課</div></div>';
    }
    el.innerHTML=html;
  }catch(e){el.innerHTML='<div class="empty"><div class="empt">載入失敗</div></div>';}
}

async function aiStudyPlan(days=3){
  const result=$('study-plan-result');
  const loading=$('study-plan-loading');
  const text=$('study-plan-text');
  result.style.display='none';
  loading.style.display='block';
  try{
    const r=await api('/api/ai/study_plan',{method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({days})});
    loading.style.display='none';
    if(r.error==='no_key'){
      text.textContent='⚠️ 請先在管理員介面設定 DEEPSEEK_API_KEY';
    }else if(r.ok){
      text.textContent=r.plan;
    }else{
      text.textContent='❌ '+(r.error||'未知錯誤');
    }
    result.style.display='block';
  }catch(e){
    loading.style.display='none';
    text.textContent='❌ '+e.message;
    result.style.display='block';
  }
}
async function aiStudyPlan(){
  const chat=$('ai-chat');
  const msg=document.createElement('div');msg.className='aimsg bot loading';msg.textContent='⏳ 生成中...';
  chat.appendChild(msg);chat.scrollTop=chat.scrollHeight;
  try{
    const r=await api('/api/ai/study_plan',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
    if(r.error==='no_key'){msg.textContent='⚠️ 請先在管理員介面設定 DEEPSEEK_API_KEY';}
    else if(r.ok){msg.className='aimsg bot';msg.textContent='📅 今晚溫書計劃：' + r.plan;}
    else{msg.textContent='❌ '+(r.error||'');}
  }catch(e){msg.textContent='❌ '+e.message;}
  chat.scrollTop=chat.scrollHeight;
}
async function sendAI(){
  const q=$('ai-input').value.trim();if(!q)return;
  const chat=$('ai-chat');
  chat.innerHTML+='<div class="aimsg user">'+q.replace(/</g,'&lt;')+'</div>';
  $('ai-input').value='';
  const loading=document.createElement('div');loading.className='aimsg bot loading';loading.textContent='💭 思考中...';
  chat.appendChild(loading);chat.scrollTop=chat.scrollHeight;
  try{
    const r=await api('/api/ai/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
    if(r.error==='no_key'){loading.textContent='⚠️ 請先在管理員介面設定 DEEPSEEK_API_KEY';}
    else if(r.ok){loading.className='aimsg bot';loading.textContent=r.answer;}
    else{loading.textContent='❌ '+(r.error||'');}
  }catch(e){loading.textContent='❌ '+e.message;}
  chat.scrollTop=chat.scrollHeight;
}

// ── Stats ─────────────────────────────────────────────────────────────────────
async function loadStats(){
  const s=await api('/api/stats');
  const rate=s.total?Math.round(s.done/s.total*100):0;
  $('st-kpi').innerHTML=
    '<div class="kpi"><div class="knum" style="color:var(--blue)">'+s.total+'</div><div class="klbl">總功課</div></div>'+
    '<div class="kpi"><div class="knum" style="color:var(--ok)">'+s.done+'</div><div class="klbl">已完成</div></div>'+
    '<div class="kpi"><div class="knum" style="color:var(--warn)">'+s.pending+'</div><div class="klbl">待做</div></div>'+
    '<div class="kpi"><div class="knum" style="color:var(--accent)">'+rate+'%</div><div class="klbl">完成率</div></div>';
  const subj=s.by_subject||[];const mx=subj.length?subj[0].cnt:1;
  $('st-subj').innerHTML=subj.length?subj.map(r=>
    '<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">'+sb(r.subject)+
    '<div style="flex:1"><div class="pbar"><div class="pf" style="width:'+Math.round(r.cnt/mx*100)+'%"></div></div></div>'+
    '<span style="font-size:13px;color:var(--text2);min-width:34px;text-align:right">'+r.cnt+' 項</span></div>'
  ).join(''):'<div class="empty"><div class="empt">暫無數據</div></div>';
}

// ── Global error handler ───────────────────────────────────────────────────
window.onerror = function(msg, src, line, col, err){
  showErrBanner(msg + (src?' ('+src+':'+line+')':''));
  return false;
};
window.onunhandledrejection = function(e){
  showErrBanner('Unhandled promise: '+(e.reason?.message||e.reason||'unknown'));
};
function showErrBanner(msg){
  let el=document.getElementById('err-banner');
  if(!el){
    el=document.createElement('div');el.id='err-banner';
    el.style.cssText='position:fixed;bottom:0;left:0;right:0;background:#1c1414;border-top:1px solid #ff453a;padding:12px 16px;z-index:999;font-size:13px;color:#ff453a;display:flex;align-items:center;gap:10px;-webkit-backdrop-filter:blur(10px)';
    el.innerHTML='<span style="flex:1" id="err-txt"></span>'+
      '<button onclick="copyErr()" style="background:rgba(255,69,58,.2);border:none;color:#ff453a;padding:5px 12px;border-radius:8px;cursor:pointer;font-family:inherit;font-size:12px;flex-shrink:0">複製</button>'+
      '<button onclick="this.parentElement.remove()" style="background:none;border:none;color:#636366;cursor:pointer;font-size:18px;flex-shrink:0">×</button>';
    document.body.appendChild(el);
  }
  document.getElementById('err-txt').textContent='⚠️ '+msg;
  el.style.display='flex';
  window._lastErr=msg;
}
function copyErr(){
  if(navigator.clipboard)navigator.clipboard.writeText(window._lastErr||'');
  else{const t=document.createElement('textarea');t.value=window._lastErr||'';document.body.appendChild(t);t.select();document.execCommand('copy');t.remove();}
  toast('✅ 已複製錯誤訊息');
}

loadDash();
</script>
</body>
</html>"""
