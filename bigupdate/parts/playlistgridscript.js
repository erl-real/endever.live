console.clear();

const bentoContainer = document.querySelector(".bento-container");
const bentoItems = bentoContainer.querySelectorAll("[data-row]");

const artImages = [
  "basstestside.png", "aciddrop.jpg", "backseat66side.png", "closeingtime.png",
  "dither.png", "exe obj by themighty808.png", "fullcds.png", "homesick.png",
  "hustlenationside.png", "knockoutside.png", "LSDTV.jpg", "nevr.jpg",
  "postpop.jpg", "redplaylist1.png", "reloaded.png", "top100beta.jpg", "unsigned.jpg"
];

const shuffle = (arr) => {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
};

const pool = shuffle([...artImages]).slice(0, bentoItems.length);
const artBase = new URL("../../../../", new URL(document.currentScript.src)).href;
bentoItems.forEach((item, i) => {
  const file = pool[i % pool.length];
  item.querySelector("img").src = artBase + encodeURI(file);
  const label = document.createElement("span");
  label.className = "bento-label";
  label.textContent = decodeURI(file).replace(/\.[^.]+$/, "");
  item.appendChild(label);
});

gsap.registerPlugin(Flip);

const rowClasses = ["rows-3-1-1", "rows-1-3-1", "rows-1-1-3"];
const colClasses = ["cols-3-1-1", "cols-1-3-1", "cols-1-1-3"];
// Remember 0 index for the classes array, same for the data attribute on the HTML elements
let activeColumn = 1,
  activeRow = 1,
  doFlip = false;

bentoItems.forEach((e, i) => {
  const colNumber = e.dataset.column;
  const rowNumber = e.dataset.row;
  e.addEventListener("mouseenter", () => {
    // console.log("Item", i, "column", colNumber, "row", rowNumber);
    const state = Flip.getState(bentoItems);
    if (colNumber !== activeColumn) {
      bentoContainer.classList.remove(colClasses[activeColumn]);
      bentoContainer.classList.add(colClasses[colNumber]);
      activeColumn = colNumber;
      doFlip = true;
    }
    if (rowNumber !== activeRow) {
      bentoContainer.classList.remove(rowClasses[activeRow]);
      bentoContainer.classList.add(rowClasses[rowNumber]);
      activeRow = rowNumber;
      doFlip = true;
    }
    doFlip &&
      Flip.from(state, {
        duration: 0.4,
        ease: "power2.out",
        onStart: () => (doFlip = false),
        absolute: true
      });
  });
});

bentoContainer.addEventListener("mouseleave", () => {
  // Toggle the boolean just in case
  doFlip = true;
  // Get the state
  const state = Flip.getState(bentoItems);

  // Update the classes in the container
  bentoContainer.classList.remove(colClasses[activeColumn]);
  bentoContainer.classList.remove(rowClasses[activeRow]);
  bentoContainer.classList.add(colClasses[1]);
  bentoContainer.classList.add(rowClasses[1]);

  // Update the index values
  activeColumn = 1;
  activeRow = 1;

  // Run the Flip Animation
  Flip.from(state, {
    duration: 0.4,
    ease: "power2.out",
    onStart: () => (doFlip = false),
    absolute: true
  });
});

document.querySelectorAll(".exclusive").forEach((section) => {
  const row = section.querySelector(".exclusive__row");
  const more = section.querySelector(".exclusive__more");

  if (row) {
    for (let i = 0; i < 12; i++) {
      const t = document.createElement("div");
      t.className = "thumb";
      row.appendChild(t);
    }
  }

  if (row && more) {
    more.addEventListener("click", () => {
      const first = row.querySelector(".thumb");
      if (!first) return;
      const gap = 18;
      const step = first.offsetWidth + gap;
      const visible = Math.max(1, Math.round(row.clientWidth / step));
      const next = row.scrollLeft + step * visible;
      if (next >= row.scrollWidth - 1) {
        row.scrollTo({ left: 0, behavior: "smooth" });
      } else {
        row.scrollTo({ left: next, behavior: "smooth" });
      }
    });
  }
});

const siteLogo = document.querySelector(".site-logo");
if (siteLogo) {
  window.addEventListener("scroll", () => {
    siteLogo.classList.toggle("scrolled", window.scrollY > 50);
  });
}
