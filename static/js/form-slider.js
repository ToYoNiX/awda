const foundBtn = document.getElementById("foundBtn");
const lookingBtn = document.getElementById("lookingBtn");
const foundSection = document.getElementById("foundSection");
const lookingSection = document.getElementById("lookingSection");

foundBtn.addEventListener("click", () => {
    foundSection.classList.remove("d-none");
    lookingSection.classList.add("d-none");
    foundBtn.classList.add("btn-dark");
    foundBtn.classList.remove("btn-outline-dark");
    lookingBtn.classList.add("btn-outline-dark");
    lookingBtn.classList.remove("btn-dark");
});

lookingBtn.addEventListener("click", () => {
    lookingSection.classList.remove("d-none");
    foundSection.classList.add("d-none");
    lookingBtn.classList.add("btn-dark");
    lookingBtn.classList.remove("btn-outline-dark");
    foundBtn.classList.add("btn-outline-dark");
    foundBtn.classList.remove("btn-dark");
});