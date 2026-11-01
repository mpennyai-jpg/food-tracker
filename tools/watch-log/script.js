(function(){
  "use strict";
  var BAKED = window.__POSTERS__ || {};      // posters embedded at build time
  var CACHE_KEY = "wl.posters.v2";
  var cache = {};
  try { cache = JSON.parse(localStorage.getItem(CACHE_KEY) || "{}") || {}; } catch (e) { cache = {}; }
  var saveTimer = null;
  function saveCache(){
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function(){
      try { localStorage.setItem(CACHE_KEY, JSON.stringify(cache)); } catch (e) {}
    }, 800);
  }

  function tier(r){
    if (r === null) return "t-none";
    if (r >= 4) return "t-top";
    if (r >= 3) return "t-mid";
    if (r >= 2) return "t-low";
    return "t-bad";
  }
  function fmt(r){
    if (r === null) return "Unrated";
    return (r % 1 === 0) ? String(r) : String(r).replace(/^0\./, ".");
  }
  function initials(t){
    var words = t.replace(/[^\w\s:]/g, " ").split(/\s+/).filter(function(w){
      return w && !/^(the|a|an|of|and|in|to|on|for|with)$/i.test(w);
    });
    if (!words.length) words = t.split(/\s+/);
    return words.slice(0, 2).map(function(w){ return w[0]; }).join("");
  }

  function pips(r){
    var out = "";
    for (var i = 1; i <= 5; i++){
      var cls = "pip";
      if (r !== null){
        if (r >= i) cls += " on";
        else if (r > i - 1) cls += " half";
      }
      out += '<span class="' + cls + '"></span>';
    }
    return out;
  }

  var rows = [];

  function rowEl(it){
    var li = document.createElement("li");
    li.className = "row";
    var t = tier(it.r);
    li.innerHTML =
      '<div class="art" data-q="' + encodeURIComponent(it.q) +
           '" data-q2="' + encodeURIComponent(it.q2 || "") + '">' +
        '<span class="fb">' + initials(it.t) + '</span>' +
      '</div>' +
      '<p class="name">' + esc(it.t) +
        (it.y && it.y !== "-" ? '<span class="yr">' + esc(it.y) + '</span>' : '') +
      '</p>' +
      '<div class="score ' + t + '">' +
        '<span class="num ' + t + '">' + fmt(it.r) + '</span>' +
        '<span class="pips">' + pips(it.r) + '</span>' +
      '</div>' +
      '<p class="blurb">' + esc(it.d) + '</p>';
    rows.push({ el: li, hay: (it.t + " " + it.g + " " + it.d + " " + (it.y || "")).toLowerCase() });
    return li;
  }

  function esc(s){
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function slug(s){
    return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  }

  function renderGroups(groups, mount, prefix){
    var frag = document.createDocumentFragment();
    groups.forEach(function(grp){
      var sec = document.createElement("section");
      sec.className = "genre";
      sec.id = prefix + "-" + slug(grp.g);
      var head = document.createElement("div");
      head.className = "genre-head";
      head.innerHTML = '<h3>' + esc(grp.g) + '</h3><span class="bar"></span>' +
                       '<span class="c">' + grp.items.length + '</span>';
      var ol = document.createElement("ol");
      ol.className = "rows";
      grp.items.forEach(function(it){ ol.appendChild(rowEl(it)); });
      sec.appendChild(head);
      sec.appendChild(ol);
      frag.appendChild(sec);
    });
    mount.appendChild(frag);
  }

  var D = window.__WATCHLOG__;

  renderGroups(D.movies, document.getElementById("list-mov"), "m");
  renderGroups(D.tv, document.getElementById("list-tv"), "t");

  var qGroups = [
    { g: "Series", items: D.queue.filter(function(i){ return i.kind === "TV"; }) },
    { g: "Films", items: D.queue.filter(function(i){ return i.kind === "MOVIE"; }) }
  ].filter(function(g){ return g.items.length; });
  renderGroups(qGroups, document.getElementById("list-queue"), "q");

  // ---- genre jump chips ----
  var chipIndex = {};
  (function buildNav(){
    var nav = document.getElementById("genrenav");
    if (!nav) return;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function row(label, groups, prefix){
      if (!groups.length) return;
      var wrap = document.createElement("div");
      wrap.className = "chiprow";
      var lab = document.createElement("span");
      lab.className = "chiplabel";
      lab.textContent = label;
      var box = document.createElement("div");
      box.className = "chips";
      groups.forEach(function(grp){
        var id = prefix + "-" + slug(grp.g);
        var a = document.createElement("a");
        a.className = "chip";
        a.href = "#" + id;
        a.innerHTML = esc(grp.g) + '<span class="k">' + grp.items.length + '</span>';
        a.addEventListener("click", function(ev){
          var target = document.getElementById(id);
          if (!target) return;
          ev.preventDefault();
          // a long page: glide for a near jump, cut straight there for a far one
          var dist = Math.abs(target.getBoundingClientRect().top);
          var smooth = !reduce && dist < window.innerHeight * 2.5;
          target.scrollIntoView({ behavior: smooth ? "smooth" : "auto", block: "start" });
          target.setAttribute("tabindex", "-1");
          target.focus({ preventScroll: true });
        });
        chipIndex[id] = a;
        box.appendChild(a);
      });
      wrap.appendChild(lab);
      wrap.appendChild(box);
      nav.appendChild(wrap);
    }

    row("Movies", D.movies, "m");
    row("Television", D.tv, "t");
  })();

  // tallies
  var rated = [];
  D.movies.concat(D.tv).forEach(function(g){ rated = rated.concat(g.items); });
  var avg = rated.reduce(function(a, i){ return a + i.r; }, 0) / rated.length;
  document.getElementById("t-mov").textContent = D.counts.movies;
  document.getElementById("t-tv").textContent = D.counts.tv;
  document.getElementById("t-avg").textContent = avg.toFixed(2);
  document.getElementById("t-queue").textContent = D.counts.queue;
  document.getElementById("n-mov").textContent = D.counts.movies + " titles / " + D.movies.length + " genres";
  document.getElementById("n-tv").textContent = D.counts.tv + " titles / " + D.tv.length + " genres";
  document.getElementById("n-queue").textContent = D.counts.queue + " titles";

  // ---- poster lookup, in the viewer's browser ----
  var queue = [], active = 0, MAX = 4, found = 0, tried = 0;
  var pcount = document.getElementById("pcount");
  var tally = function(hit){
    tried++;
    if (hit) found++;
    if (pcount && found) {
      pcount.hidden = false;
      pcount.textContent = found + " posters";
    }
  };

  function pump(){
    while (active < MAX && queue.length){
      var box = queue.shift();
      active++;
      fill(box).then(done, done);
    }
  }
  function done(){ active--; pump(); }

  function paint(box, src){
    var img = document.createElement("img");
    img.alt = "";
    img.loading = "lazy";
    img.decoding = "async";
    img.onload = function(){ var fb = box.querySelector(".fb"); if (fb) fb.remove(); };
    img.onerror = function(){ img.remove(); };
    img.src = src;
    box.appendChild(img);
  }

  function ask(q){
    var url = "https://en.wikipedia.org/w/api.php?action=query&format=json&origin=*" +
              "&generator=search&gsrsearch=" + encodeURIComponent(q) +
              "&gsrlimit=1&prop=pageimages&piprop=thumbnail&pithumbsize=300";
    return fetch(url).then(function(r){
      if (!r.ok) throw new Error("http " + r.status);
      return r.json();
    }).then(function(j){
      var pages = j && j.query && j.query.pages;
      if (!pages) return null;
      var keys = Object.keys(pages);
      if (!keys.length) return null;
      var p = pages[keys[0]];
      return (p && p.thumbnail && p.thumbnail.source) || null;
    });
  }

  function fill(box){
    var q = decodeURIComponent(box.dataset.q || "");
    if (BAKED[q]){ paint(box, BAKED[q]); return Promise.resolve(); }
    var q2 = decodeURIComponent(box.dataset.q2 || "");
    if (!q) return Promise.resolve();
    if (Object.prototype.hasOwnProperty.call(cache, q)){
      if (cache[q]) { paint(box, cache[q]); tally(true); } else { tally(false); }
      return Promise.resolve();
    }
    return ask(q).then(function(src){
      if (src || !q2 || q2 === q) return src;
      return ask(q2).catch(function(){ return null; });
    }).then(function(src){
      cache[q] = src || "";
      saveCache();
      if (src) paint(box, src);
      tally(!!src);
    }).catch(function(){ tally(false); });
  }

  // when posters ship with the page, say so once instead of counting them in
  var bakedCount = Object.keys(BAKED).length;
  if (bakedCount && pcount){
    pcount.hidden = false;
    pcount.textContent = bakedCount + " posters";
    tally = function(){};
  }

  var boxes = document.querySelectorAll(".art");
  if ("IntersectionObserver" in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (en.isIntersecting){
          io.unobserve(en.target);
          queue.push(en.target);
        }
      });
      pump();
    }, { rootMargin: "600px 0px" });
    Array.prototype.forEach.call(boxes, function(b){ io.observe(b); });
  } else {
    Array.prototype.forEach.call(boxes, function(b){ queue.push(b); });
    pump();
  }

  // ---- filter ----
  var q = document.getElementById("q");
  var hits = document.getElementById("hits");
  var debounce = null;

  function apply(){
    var term = q.value.trim().toLowerCase();
    var shown = 0;
    rows.forEach(function(r){
      var on = !term || r.hay.indexOf(term) !== -1;
      r.el.hidden = !on;
      if (on) shown++;
    });
    document.querySelectorAll("section.genre").forEach(function(sec){
      var vis = sec.querySelectorAll("li.row:not([hidden])").length;
      sec.hidden = !vis;
      var chip = chipIndex[sec.id];
      if (vis){
        sec.querySelector(".c").textContent = vis;
        if (chip){
          chip.classList.remove("off");
          chip.querySelector(".k").textContent = vis;
        }
      } else if (chip){
        chip.classList.add("off");
        chip.querySelector(".k").textContent = 0;
      }
    });
    document.querySelectorAll("section.medium").forEach(function(sec){
      var old = sec.querySelector(".empty");
      if (old) old.remove();
      if (term && !sec.querySelector("section.genre:not([hidden])")){
        var p = document.createElement("p");
        p.className = "empty";
        p.textContent = "Nothing here matches “" + q.value.trim() + "”.";
        sec.appendChild(p);
      }
    });
    hits.textContent = term ? shown + " of " + rows.length : "";
    try { term ? sessionStorage.setItem("wl.q", q.value) : sessionStorage.removeItem("wl.q"); } catch (e) {}
  }

  try {
    var saved = sessionStorage.getItem("wl.q");
    if (saved) { q.value = saved; apply(); }
  } catch (e) {}

  q.addEventListener("input", function(){
    clearTimeout(debounce);
    debounce = setTimeout(apply, 120);
  });
})();
