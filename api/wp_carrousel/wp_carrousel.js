let slideIndex = 0;

const images = [
  // List of image URLs
];

// Open the Modal
function openModal() {
  document.getElementById("myModal").style.display = "block";
}

// Close the Modal
function closeModal() {
  document.getElementById("myModal").style.display = "none";
}

// Show slides in the lightbox
function showLightboxSlide(n) {
  let modalImage = document.querySelector('.modal-image');
  if (n >= images.length) slideIndex = 0;
  if (n < 0) slideIndex = images.length - 1;
  modalImage.src = images[slideIndex];
}

// Move to the next/previous slide in the lightbox
function moveLightboxSlide(n) {
  showLightboxSlide(slideIndex += n);
}

window.onload = function() {
  const container = document.querySelector('.carousel-slides');
  images.forEach(url => {
    let img = document.createElement('img');
    img.src = url;
    container.appendChild(img);
  });

  showSlides(slideIndex);

  // Attach click event to open the modal
  let slides = document.querySelectorAll('.carousel-slides img');
  slides.forEach((slide, index) => {
    slide.onclick = function() {
      openModal();
      slideIndex = index;
      showLightboxSlide(slideIndex);
    };
  });
};

function moveSlide(n) {
  showSlides(slideIndex += n);
}

function showSlides(n) {
  let slides = document.querySelectorAll('.carousel-slides img');
  if (n >= slides.length) slideIndex = 0;
  if (n < 0) slideIndex = slides.length - 1;

  slides.forEach(slide => slide.style.display = "none");
  slides[slideIndex].style.display = "block";
}
