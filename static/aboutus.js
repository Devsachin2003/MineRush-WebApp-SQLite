function ws_book(e, t, i) {
  var s,
    a = jQuery,
    n = a(this),
    o = a(".ws_list", i),
    r = a("<div>")
      .addClass("ws_effect ws_book")
      .css({
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
      })
      .appendTo(i),
    d = e.duration,
    l = e.perspective || 0.4,
    c = e.shadow || 0.35,
    h = e.noCanvas || !1,
    p = e.no3d || !1,
    u = {
      domPrefixes: " Webkit Moz ms O Khtml".split(" "),
      testDom: function (e) {
        for (var t = this.domPrefixes.length; t--; )
          if (void 0 !== document.body.style[this.domPrefixes[t] + e])
            return !0;
        return !1;
      },
      cssTransitions: function () {
        return this.testDom("Transition");
      },
      cssTransforms3d: function () {
        var e =
          void 0 !== document.body.style.perspectiveProperty ||
          this.testDom("Perspective");
        if (e && /AppleWebKit/.test(navigator.userAgent)) {
          var t = document.createElement("div"),
            i = document.createElement("style"),
            s = "Test3d" + Math.round(99999 * Math.random());
          (i.textContent =
            "@media (-webkit-transform-3d){#" + s + "{height:3px}}"),
            document.getElementsByTagName("head")[0].appendChild(i),
            (t.id = s),
            document.body.appendChild(t),
            (e = 3 === t.offsetHeight),
            i.parentNode.removeChild(i),
            t.parentNode.removeChild(t);
        }
        return e;
      },
      canvas: function () {
        if (void 0 !== document.createElement("canvas").getContext) return !0;
      },
    };
  function f(t, i, s, a, n, o, r, u, f, m, g, v) {
    if (p) {
      if (!t) {
        i *= -1;
        var w = a;
        (a = s), (s = w), (w = o), (o = n), (n = w);
      }
      setTimeout(function () {
        s
          .children("img")
          .css("opacity", c)
          .animate({ opacity: 1 }, d / 2),
          n
            .css("transform", "rotateY(" + i + "deg)")
            .children("img")
            .css("opacity", 1)
            .animate({ opacity: c }, d / 2, function () {
              n.hide(),
                o
                  .show()
                  .css("transform", "rotateX(0deg) rotateY(0deg)")
                  .children("img")
                  .css("opacity", c)
                  .animate({ opacity: 1 }, d / 2),
                a
                  .children("img")
                  .css("opacity", 1)
                  .animate({ opacity: c }, d / 2);
            });
      }, 0),
        setTimeout(v, d);
    } else if (h) {
      r.show();
      new Date();
      var b = !0;
      wowAnimate(
        function (i) {
          var d = jQuery.easing.easeInOutQuint(1, i, 0, 1, 1),
            h = jQuery.easing.easeInOutCubic(1, i, 0, 1, 1),
            p = !t;
          if (i < 0.5) {
            (d *= 2), (h *= 2);
            var g = n;
          } else {
            (p = t), (d = 2 * (1 - d)), (h = 2 * (1 - h));
            g = o;
          }
          var v = (r.height() * l) / 2,
            w = ((1 - d) * r.width()) / 2,
            C = 1 + h * l,
            y = r.width() / 2;
          !(function (t, i, s, a, n, o, r, d, l, c, h) {
            (numSlices = n / 2),
              (widthScale = n / l),
              (heightScale = (1 - o) / numSlices),
              t.clearRect(0, 0, h.width(), h.height());
            for (var p = 0; p < numSlices + widthScale; p++) {
              var u = r
                  ? (p * e.width) / n + e.width / 2
                  : ((numSlices - p) * e.width) / n,
                f = s + (r ? 2 : -2) * p,
                m = a + (c * heightScale * p) / 2;
              u < 0 && (u = 0),
                f < 0 && (f = 0),
                m < 0 && (m = 0),
                t.drawImage(
                  i,
                  u,
                  0,
                  2.5,
                  e.height,
                  f,
                  m,
                  2,
                  c * (1 - heightScale * p)
                );
            }
            t.save(),
              t.beginPath(),
              t.moveTo(s, a),
              t.lineTo(
                s + (r ? 2 : -2) * (numSlices + widthScale),
                a + (c * heightScale * (numSlices + widthScale)) / 2
              ),
              t.lineTo(
                s + (r ? 2 : -2) * (numSlices + widthScale),
                c * (1 - heightScale * (numSlices + widthScale)) +
                  a +
                  (c * heightScale * (numSlices + widthScale)) / 2
              ),
              t.lineTo(s, a + c),
              t.closePath(),
              t.clip(),
              (t.fillStyle = "rgba(0,0,0," + Math.round(100 * d) / 100 + ")"),
              t.fillRect(0, 0, h.width(), h.height()),
              t.restore();
          })(s, g, y, v, w, C, p, h * c, y, r.height(), u),
            b && (m.show(), (b = !1)),
            a.clearRect(0, 0, f.width(), f.height()),
            (a.fillStyle = "rgba(0,0,0," + (c - h * c) + ")"),
            a.fillRect(p ? y : 0, 0, f.width() / 2, f.height());
        },
        0,
        1,
        d,
        v
      );
    }
  }
  p || (p = u.cssTransitions() && u.cssTransforms3d()),
    h || (h = u.canvas()),
    (this.go = function (e, c, u) {
      if (s) return -1;
      var m = t.get(e),
        g = t.get(c);
      u = null == u ? (0 == c && e != c + 1) || e == c - 1 : !u;
      var v = a("<div>").appendTo(r),
        w = a(m);
      if (
        ((w = {
          width: w.width(),
          height: w.height(),
          marginLeft: parseFloat(w.css("marginLeft")),
          marginTop: parseFloat(w.css("marginTop")),
        }),
        p)
      ) {
        var b = {
          background: "#000",
          position: "absolute",
          left: 0,
          top: 0,
          width: "100%",
          height: "100%",
          transformStyle: "preserve-3d",
          zIndex: 3,
          outline: "1px solid transparent",
        };
        (perspect = i.width() * (3 - 2 * l)),
          v
            .css(b)
            .css({ perspective: perspect, transform: "translate3d(0,0,0)" });
        var C = 90,
          y = a("<div>")
            .css(b)
            .css({
              position: "relative",
              float: "left",
              width: "50%",
              overflow: "hidden",
            })
            .append(
              a("<img>")
                .attr("src", (u ? m : g).src)
                .css(w)
            )
            .appendTo(v),
          T = a("<div>")
            .css(b)
            .css({
              position: "relative",
              float: "left",
              width: "50%",
              overflow: "hidden",
            })
            .append(
              a("<img>")
                .attr("src", (u ? g : m).src)
                .css(w)
                .css({ marginLeft: -w.width / 2 })
            )
            .appendTo(v),
          S = a("<div>")
            .css(b)
            .css({
              display: u ? "block" : "none",
              width: "50%",
              transform: "rotateY(" + (u ? 0.1 : C) + "deg)",
              transition: (u ? "ease-in " : "ease-out ") + d / 2e3 + "s",
              transformOrigin: "right",
              overflow: "hidden",
            })
            .append(
              a("<img>")
                .attr("src", (u ? g : m).src)
                .css(w)
            )
            .appendTo(v),
          x = a("<div>")
            .css(b)
            .css({
              display: u ? "none" : "block",
              left: "50%",
              width: "50%",
              transform: "rotateY(-" + (u ? C : 0.1) + "deg)",
              transition: (u ? "ease-out " : "ease-in ") + d / 2e3 + "s",
              transformOrigin: "left",
              overflow: "hidden",
            })
            .append(
              a("<img>")
                .attr("src", (u ? m : g).src)
                .css(w)
                .css({ marginLeft: -w.width / 2 })
            )
            .appendTo(v);
      } else if (h)
        var j = a("<div>")
            .css({
              position: "absolute",
              top: 0,
              left: u ? 0 : "50%",
              width: "50%",
              height: "100%",
              overflow: "hidden",
              zIndex: 6,
            })
            .append(
              a(t.get(e))
                .clone()
                .css({
                  position: "absolute",
                  height: "100%",
                  right: u ? "auto" : 0,
                  left: u ? 0 : "auto",
                })
            )
            .appendTo(v)
            .hide(),
          I = a("<div>")
            .css({
              position: "absolute",
              width: "100%",
              height: "100%",
              left: 0,
              top: 0,
              zIndex: 8,
            })
            .appendTo(v)
            .hide(),
          O = a("<canvas>")
            .css({
              position: "absolute",
              zIndex: 2,
              left: 0,
              top: (-I.height() * l) / 2,
            })
            .attr({ width: I.width(), height: I.height() * (l + 1) })
            .appendTo(I),
          P = O.clone()
            .css({ top: 0, zIndex: 1 })
            .attr({ width: I.width(), height: I.height() })
            .appendTo(I),
          A = O.get(0).getContext("2d"),
          E = P.get(0).getContext("2d");
      else
        o.stop(!0).animate(
          {
            left: e
              ? -e + "00%"
              : /Safari/.test(navigator.userAgent)
              ? "0%"
              : 0,
          },
          d,
          "easeInOutExpo"
        );
      if (!p && h) (y = A), (T = E), (S = g), (x = m);
      s = new f(u, C, y, T, S, x, I, O, P, j, w, function () {
        n.trigger("effectEnd"), v.remove(), (s = 0);
      });
    });
}
window.innerWidth < 768 &&
  [].slice
    .call(document.querySelectorAll("[data-bss-disabled-mobile]"))
    .forEach(function (e) {
      e.classList.remove("animated"),
        e.removeAttribute("data-bss-hover-animate"),
        e.removeAttribute("data-aos"),
        e.removeAttribute("data-bss-parallax-bg"),
        e.removeAttribute("data-bss-scroll-zoom");
    }),
  document.addEventListener("DOMContentLoaded", function () {}, !1),
  jQuery(document).ready(function (e) {
    var t,
      s,
      a = 2e3,
      n = 3800;
    function o(e) {
      var t = c(e);
      if (e.parents(".cd-headline").hasClass("type")) {
        var i = e.parent(".cd-words-wrapper");
        i.addClass("selected").removeClass("waiting"),
          setTimeout(function () {
            i.removeClass("selected"),
              e
                .removeClass("is-visible")
                .addClass("is-hidden")
                .children("i")
                .removeClass("in")
                .addClass("out");
          }, 500),
          setTimeout(function () {
            r(t, 150);
          }, 1300);
      } else if (e.parents(".cd-headline").hasClass("letters")) {
        var s = e.children("i").length >= t.children("i").length;
        d(e.find("i").eq(0), e, s, 50), l(t.find("i").eq(0), t, s, 50);
      } else
        e.parents(".cd-headline").hasClass("clip")
          ? e
              .parents(".cd-words-wrapper")
              .animate({ width: "2px" }, 600, function () {
                h(e, t), r(t);
              })
          : e.parents(".cd-headline").hasClass("loading-bar")
          ? (e.parents(".cd-words-wrapper").removeClass("is-loading"),
            h(e, t),
            setTimeout(function () {
              o(t);
            }, n),
            setTimeout(function () {
              e.parents(".cd-words-wrapper").addClass("is-loading");
            }, 800))
          : (h(e, t),
            setTimeout(function () {
              o(t);
            }, a));
    }
    function r(e, t) {
      e.parents(".cd-headline").hasClass("type")
        ? (l(e.find("i").eq(0), e, !1, t),
          e.addClass("is-visible").removeClass("is-hidden"))
        : e.parents(".cd-headline").hasClass("clip") &&
          e
            .parents(".cd-words-wrapper")
            .animate({ width: e.width() + 10 }, 600, function () {
              setTimeout(function () {
                o(e);
              }, 1500);
            });
    }
    function d(t, i, s, n) {
      if (
        (t.removeClass("in").addClass("out"),
        t.is(":last-child")
          ? s &&
            setTimeout(function () {
              o(c(i));
            }, a)
          : setTimeout(function () {
              d(t.next(), i, s, n);
            }, n),
        t.is(":last-child") && e("html").hasClass("no-csstransitions"))
      ) {
        var r = c(i);
        h(i, r);
      }
    }
    function l(e, t, i, s) {
      e.addClass("in").removeClass("out"),
        e.is(":last-child")
          ? (t.parents(".cd-headline").hasClass("type") &&
              setTimeout(function () {
                t.parents(".cd-words-wrapper").addClass("waiting");
              }, 200),
            i ||
              setTimeout(function () {
                o(t);
              }, a))
          : setTimeout(function () {
              l(e.next(), t, i, s);
            }, s);
    }
    function c(e) {
      return e.is(":last-child") ? e.parent().children().eq(0) : e.next();
    }
    function h(e, t) {
      e.removeClass("is-visible").addClass("is-hidden"),
        t.removeClass("is-hidden").addClass("is-visible");
    }
    e(".cd-headline.letters")
      .find("b")
      .each(function () {
        var t = e(this),
          s = t.text().split(""),
          a = t.hasClass("is-visible");
        for (i in s)
          t.parents(".rotate-2").length > 0 && (s[i] = "<em>" + s[i] + "</em>"),
            (s[i] = a
              ? '<i class="in">' + s[i] + "</i>"
              : "<i>" + s[i] + "</i>");
        var n = s.join("");
        t.html(n).css("opacity", 1);
      }),
      (t = e(".cd-headline")),
      (s = a),
      t.each(function () {
        var t = e(this);
        if (t.hasClass("loading-bar"))
          (s = n),
            setTimeout(function () {
              t.find(".cd-words-wrapper").addClass("is-loading");
            }, 800);
        else if (t.hasClass("clip")) {
          var i = t.find(".cd-words-wrapper"),
            a = i.width() + 10;
          i.css("width", a);
        } else if (!t.hasClass("type")) {
          var r = t.find(".cd-words-wrapper b"),
            d = 0;
          r.each(function () {
            var t = e(this).width();
            t > d && (d = t);
          }),
            t.find(".cd-words-wrapper").css("width", d);
        }
        setTimeout(function () {
          o(t.find(".is-visible").eq(0));
        }, s);
      });
  }),
  jQuery.extend(jQuery.easing, {
    easeInOutCubic: function (e, t, i, s, a) {
      return (t /= a / 2) < 1
        ? (s / 2) * t * t * t + i
        : (s / 2) * ((t -= 2) * t * t + 2) + i;
    },
    easeInOutQuint: function (e, t, i, s, a) {
      return (t /= a / 2) < 1
        ? (s / 2) * t * t * t * t * t + i
        : (s / 2) * ((t -= 2) * t * t * t * t + 2) + i;
    },
  }),
  jQuery("#wowslider-container1").wowSlider({
    effect: "book",
    prev: "",
    next: "",
    duration: 2e3,
    delay: 2e3,
    width: 400,
    height: 360,
    autoPlay: !0,
    autoPlayVideo: !1,
    playPause: !1,
    stopOnHover: !1,
    loop: !1,
    bullets: 0,
    caption: !1,
    captionEffect: "parallax",
    controls: !1,
    controlsThumb: [
      "data1/tooltips/021s96x48.jpg",
      "data1/tooltips/023s96x48.jpg",
      "data1/tooltips/024.jpg",
      "data1/tooltips/026.jpg",
      "data1/tooltips/027s96x48.jpg",
    ],
    responsive: 1,
    fullScreen: !1,
    gestures: 2,
    onBeforeStep: 0,
    images: 0,
  });
