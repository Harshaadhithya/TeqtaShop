!(function (a) {
    "use strict";
    function b(a) {
      return "[data-value" + (a ? "=" + a : "") + "]";
    }
    function c(a, b, c) {
      var d = c.activeIcon,
        e = c.inactiveIcon;
      a.removeClass(b ? e : d).addClass(b ? d : e);
    }
    function d(b, c) {
      var d = a.extend({}, i, b.data(), c);
      return (
        (d.inline = "" === d.inline || d.inline),
        (d.readonly = "" === d.readonly || d.readonly),
        d.clearable === !1
          ? (d.clearableLabel = "")
          : (d.clearableLabel = d.clearable),
        (d.clearable = "" === d.clearable || d.clearable),
        d
      );
    }
    function e(b, c) {
      if (c.inline) var d = a('<span class="rating-input"></span>');
      else var d = a('<div class="rating-input"></div>');
      c.copyClasses && (d.addClass(b.attr("class")), d.removeClass("rating"));
      for (var e = c.min; e <= c.max; e++)
        d.append('<i class="' + c.iconLib + '" data-value="' + e + '"></i>');
      return (
        c.clearable &&
          !c.readonly &&
          d
            .append("&nbsp;")
            .append(
              '<a class="' +
                f +
                '"><i class="' +
                c.iconLib +
                " " +
                c.clearableIcon +
                '"/>' +
                c.clearableLabel +
                "</a>"
            ),
        d
      );
    }
    var f = "rating-clear",
      g = "." + f,
      h = "hidden",
      i = {
        min: 1,
        max: 5,
        "empty-value": 0,
        iconLib: "glyphicon",
        activeIcon: "glyphicon-star",
        inactiveIcon: "glyphicon-star-empty",
        clearable: !1,
        clearableIcon: "glyphicon-remove",
        clearableRemain: !1,
        inline: !1,
        readonly: !1,
        copyClasses: !0,
      },
      j = function (a, b) {
        var c = (this.$input = a);
        this.options = d(c, b);
        var f = (this.$el = e(c, this.options));
        c.addClass(h).before(f),
          c.attr("type", "hidden"),
          this.highlight(c.val());
      };
    (j.VERSION = "0.4.0"),
      (j.DEFAULTS = i),
      (j.prototype = {
        clear: function () {
          this.setValue(this.options["empty-value"]);
        },
        setValue: function (a) {
          this.highlight(a), this.updateInput(a);
        },
        highlight: function (a, d) {
          var e = this.options,
            f = this.$el;
          if (a >= this.options.min && a <= this.options.max) {
            var i = f.find(b(a));
            c(i.prevAll("i").addBack(), !0, e), c(i.nextAll("i"), !1, e);
          } else c(f.find(b()), !1, e);
          d ||
            (this.options.clearableRemain
              ? f.find(g).removeClass(h)
              : a && a != this.options["empty-value"]
              ? f.find(g).removeClass(h)
              : f.find(g).addClass(h));
        },
        updateInput: function (a) {
          var b = this.$input;
          b.val() != a && b.val(a).change();
        },
      });
    var k = (a.fn.rating = function (c) {
      return this.filter("input[type=number]").each(function () {
        var d = a(this),
          e = ("object" == typeof c && c) || {},
          f = new j(d, e);
        f.options.readonly ||
          f.$el
            .on("mouseenter", b(), function () {
              f.highlight(a(this).data("value"), !0);
            })
            .on("mouseleave", b(), function () {
              f.highlight(d.val(), !0);
            })
            .on("click", b(), function () {
              f.setValue(a(this).data("value"));
            })
            .on("click", g, function () {
              f.clear();
            });
      });
    });
    (k.Constructor = j),
      a(function () {
        a("input.rating[type=number]").each(function () {
          a(this).rating();
        });
      });
  })(jQuery);
  