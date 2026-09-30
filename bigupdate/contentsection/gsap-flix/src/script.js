class HeroCarousel {
  constructor() {
    gsap.registerPlugin(Draggable, window.InertiaPlugin ?? []);

    this.slides = gsap.utils.toArray(".slide");
    if (!this.slides.length) return;

    this.el = {
      track: document.getElementById("carouselTrack"),
      current: document.getElementById("currentCounter"),
      total: document.getElementById("totalCounter"),
      progress: document.getElementById("progressBar"),
      prev: document.getElementById("prevBtn"),
      next: document.getElementById("nextBtn")
    };

    this.activeContentTimeline = null;
    this.init();
  }

  init() {
    if (this.el.total) {
      this.el.total.textContent = String(this.slides.length).padStart(2, "0");
    }

    this.alignTrackToCenter();

    this.loop = this.createHorizontalLoop(this.slides, {
      paused: true,
      draggable: true,
      speed: 1,
      onChange: (slide, i) => this.handleSlideChange(slide, i),
      onUpdate: () => this.handleParallaxUpdate()
    });

    this.loop.toIndex(0, { duration: 0 });
    this.handleParallaxUpdate();
    this.bindEvents();
  }

  alignTrackToCenter() {
    const slide = this.slides[0];
    const marginLeft =
      parseFloat(window.getComputedStyle(slide).marginLeft) || 0;
    const centerOffset =
      window.innerWidth / 2 - (marginLeft + slide.offsetWidth / 2);
    gsap.set(this.el.track, { left: `${centerOffset}px` });
  }

  handleParallaxUpdate() {
    const halfViewport = window.innerWidth / 2;

    this.slides.forEach((slide) => {
      const img = slide.querySelector(".slide__img");
      if (!img) return;

      const { left, width } = slide.getBoundingClientRect();
      const progress = (left + width / 2 - halfViewport) / halfViewport;
      const clamped = gsap.utils.clamp(-1.5, 1.5, progress);

      gsap.set(img, { xPercent: clamped * -16 });
    });
  }

  handleSlideChange(activeSlide, index) {
    if (this.el.current) {
      this.el.current.textContent = String(index + 1).padStart(2, "0");
    }

    if (this.el.progress) {
      const fillPercent = ((index + 1) / this.slides.length) * 100;
      gsap.to(this.el.progress, {
        width: `${fillPercent}%`,
        duration: 0.6,
        ease: "power2.out"
      });
    }

    this.slides.forEach((slide, i) => {
      const isCurrent = i === index;
      slide.setAttribute("aria-selected", isCurrent);

      gsap.to(slide, {
        scale: isCurrent ? 1 : 0.86,
        opacity: isCurrent ? 1 : 0.32,
        filter: isCurrent
          ? "brightness(1) blur(0px)"
          : "brightness(0.4) blur(1px)",
        duration: 0.8,
        ease: "expo.out"
      });

      if (!isCurrent) {
        gsap.set(
          slide.querySelectorAll(
            ".slide__badge, .slide__title, .slide__meta, .slide__synopsis, .btn"
          ),
          {
            y: 40,
            opacity: 0
          }
        );
      }
    });

    this.activeContentTimeline?.kill();
    const content = activeSlide.querySelectorAll(
      ".slide__badge, .slide__title, .slide__meta, .slide__synopsis, .btn"
    );

    this.activeContentTimeline = gsap
      .timeline()
      .fromTo(
        content,
        { y: 45, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.9,
          ease: "expo.out",
          stagger: 0.08,
          delay: 0.1
        }
      );
  }

  bindEvents() {
    const nav = (dir) => this.loop[dir]({ duration: 1.2, ease: "expo.out" });

    this.el.prev?.addEventListener("click", () => nav("previous"));
    this.el.next?.addEventListener("click", () => nav("next"));

    this.slides.forEach((slide, i) => {
      slide.addEventListener("click", (e) => {
        if (i !== this.loop.tl.current()) {
          e.preventDefault();
          this.loop.toIndex(i, { duration: 1.2, ease: "expo.out" });
        }
      });
    });

    window.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") nav("previous");
      if (e.key === "ArrowRight") nav("next");
    });

    window.addEventListener("resize", () => {
      this.alignTrackToCenter();
      this.handleParallaxUpdate();
    });
  }

  createHorizontalLoop(items, config = {}) {
    items = gsap.utils.toArray(items);
    const {
      onChange,
      onUpdate,
      repeat,
      paused,
      snap: snapVal = 1,
      speed = 1,
      paddingRight = 0,
      draggable = false
    } = config;
    const len = items.length;
    const startX = items[0].offsetLeft;
    const times = [];
    const widths = [];
    const xPercents = [];
    let curIndex = 0;
    const pixelsPerSecond = speed * 100;
    const snap = snapVal === false ? (v) => v : gsap.utils.snap(snapVal);

    const tl = gsap.timeline({
      repeat,
      onUpdate,
      paused,
      defaults: { ease: "none" },
      onReverseComplete: () => tl.totalTime(tl.rawTime() + tl.duration() * 100)
    });

    const style = window.getComputedStyle(items[0]);
    const totalMargin =
      (parseFloat(style.marginRight) || 0) +
      (parseFloat(style.marginLeft) || 0);

    gsap.set(items, {
      xPercent: (i, el) => {
        const w = (widths[i] = parseFloat(gsap.getProperty(el, "width", "px")));
        return (xPercents[i] = snap(
          (parseFloat(gsap.getProperty(el, "x", "px")) / w) * 100 +
            gsap.getProperty(el, "xPercent")
        ));
      },
      x: 0
    });

    const last = items[len - 1];
    const totalWidth =
      last.offsetLeft +
      (xPercents[len - 1] / 100) * widths[len - 1] -
      startX +
      last.offsetWidth * gsap.getProperty(last, "scaleX") +
      (parseFloat(paddingRight) || 0) +
      totalMargin;

    items.forEach((item, i) => {
      const curX = (xPercents[i] / 100) * widths[i];
      const distStart = item.offsetLeft + curX - startX;
      const distLoop = distStart + widths[i] * gsap.getProperty(item, "scaleX");

      tl.to(
        item,
        {
          xPercent: snap(((curX - distLoop) / widths[i]) * 100),
          duration: distLoop / pixelsPerSecond
        },
        0
      )
        .fromTo(
          item,
          {
            xPercent: snap(((curX - distLoop + totalWidth) / widths[i]) * 100)
          },
          {
            xPercent: xPercents[i],
            duration: (totalWidth - distLoop) / pixelsPerSecond,
            immediateRender: false
          },
          distLoop / pixelsPerSecond
        )
        .add(`label${i}`, distStart / pixelsPerSecond);

      times[i] = distStart / pixelsPerSecond;
    });

    const toIndex = (index, vars = {}) => {
      if (Math.abs(index - curIndex) > len / 2)
        index += index > curIndex ? -len : len;
      const newIndex = gsap.utils.wrap(0, len, index);
      let time = times[newIndex];

      if (time > tl.time() !== index > curIndex) {
        vars.modifiers = { time: gsap.utils.wrap(0, tl.duration()) };
        time += tl.duration() * (index > curIndex ? 1 : -1);
      }
      if (time < 0) time += tl.duration();

      curIndex = newIndex;
      vars.overwrite = true;
      onChange?.(items[curIndex], curIndex);
      return tl.tweenTo(time, vars);
    };

    tl.next = (vars) => toIndex(curIndex + 1, vars);
    tl.previous = (vars) => toIndex(curIndex - 1, vars);
    tl.toIndex = (index, vars) => toIndex(index, vars);
    tl.current = () => curIndex;
    tl.progress(1, true).progress(0, true);

    if (draggable && typeof Draggable === "function") {
      const proxy = document.createElement("div");
      proxy.style.cssText =
        "position:absolute;top:0;left:0;width:1px;height:1px;visibility:hidden;";
      document.body.appendChild(proxy);

      const wrap = gsap.utils.wrap(0, 1);
      let ratio = 1 / totalWidth;
      let startProgress = 0;

      const align = () => {
        const p = wrap(startProgress + (drag.startX - drag.x) * ratio);
        tl.progress(p);

        const normP = p * tl.duration();
        let closestIdx = 0;
        let minDist = Infinity;

        times.forEach((t, idx) => {
          const dist = Math.abs(t - normP);
          if (dist < minDist) {
            minDist = dist;
            closestIdx = idx;
          }
        });

        if (closestIdx !== curIndex) {
          curIndex = closestIdx;
          onChange?.(items[curIndex], curIndex);
        }
      };

      const drag = Draggable.create(proxy, {
        trigger: items[0].parentNode,
        type: "x",
        inertia: typeof InertiaPlugin !== "undefined",
        allowNativeTouchScrolling: false,
        onPress() {
          startProgress = tl.progress();
          tl.progress(0);
          ratio = 1 / totalWidth;
          tl.progress(startProgress);
          gsap.killTweensOf(tl);
        },
        onDrag: align,
        onThrowUpdate: align,
        onRelease: () => toIndex(curIndex, { duration: 1.0, ease: "expo.out" })
      })[0];
    }

    return { tl, toIndex, next: tl.next, previous: tl.previous };
  }
}

document.addEventListener("DOMContentLoaded", () => new HeroCarousel());
