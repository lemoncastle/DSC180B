console.log('you semll'); // sry

// Change document title when details is opened/closed
(() => {
    const originalTitle = document.title;
    const titleText = "chicken";
    document.querySelectorAll('details.chicken').forEach(details => {
        details.addEventListener('toggle', () => {
            document.title = details.open ? `${titleText}` : originalTitle;
        });

        // Update title when switching tabs and closing details
        window.addEventListener('visibilitychange', () => {
            if (details.open && document.visibilityState === 'visible') {
                document.title = `${titleText}`;
            }
            else { document.title = originalTitle; }
        });
  });
})();

// Get the button:
let mybutton = document.getElementById("topButton");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}