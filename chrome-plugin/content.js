chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'overlayImage') {
    const imageUrl = request.imageUrl;

    // Your logic to overlay the image on the page goes here
    // You can use DOM manipulation to achieve this

    // Inform the popup that the overlay is complete
    chrome.runtime.sendMessage({ action: 'closeOverlay' });
  }
});
